from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.enums import Status_Course
from simplemooc.core.mail import send_email_template

class CourseManager(models.Manager):
    #Django já tem um manager padrão que faz queries basicas, ex: Courses.object.all()
    
    def search(self, query):
        #return self.get_queryset().filter(name__icontains=query, description__icontains=query) #AND
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query))#OR 
        #Course.objects.search('python') 

class Course(models.Model):

    # importa models.Model para funcionalidades de acessar/manipular tabelas
    name = models.CharField('Nome', max_length=100) #1º param: texto a nivel de usuário
    slug = models.SlugField('Atalho') #Valor único, atalho,de url, não é id
    description = models.TextField('Descrição', blank=True) #charfiels sem tamanho maximo, não obrigatório (em branco, no mínimo)
    about = models.TextField('Sobre o curso', blank=True) #charfiels sem tamanho maximo, não obrigatório (em branco, no mínimo)
    start_date = models.DateField('Data de ínício', null=True, blank=True) #não obrigatório e nullable à nivel de banco
    image = models.ImageField(upload_to='courses/images',verbose_name='Imagem', null=True, blank=True) #upload_to é após o MEDIA_ROOT em settings.py
    created_at = models.DateTimeField('Criado em', auto_now_add=True) #preenchido automaticamente na adição
    updated_at = models.DateTimeField('Atualizado em', auto_now=True) #toda vez que for salvo, atualize pra data atual

    objects = CourseManager() #criar um novo custom

    def __str__(self):
        return self.name #para representar o nome como o nome, e não 'Courses object'
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(
            'courses:details', 
            #args=(), 
            kwargs={'slug': str(self.slug)}
            )
    
    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

    class Meta: #pra ficar bonito no painel do admin
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name'] #para decrescente, -name

class Lesson(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0) #ordenar aulas (backend)
    
    release_date = models.DateField('Disponível em', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='lessons',
        on_delete=models.CASCADE    
    )

    def __str__(self):
        return self.name

    # timezone leva em consideração a timezone configurada
    # se usar datetime.now() vai pegar a data do computador do usuario
    # que pode estar em qualquer timezone
    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Video', blank=True) #link
    file = models.FileField(
        upload_to='lessons/materials/',
        verbose_name='Material',
        null=True, blank=True)

    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Lição',
        related_name='materials',
        on_delete=models.CASCADE    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        ordering = ['created_at']

class Enrollment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='enrollments', #related_name serve para fazer buscas, a partir do usuário, nesse model
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso',
        related_name='enrollments', #related_name serve para fazer buscas, a partir do usuário, nesse model
        on_delete=models.CASCADE
    )
    status = models.CharField(
        'Situação',
        max_length = 2,
        choices=[(tag, tag.value) for tag in Status_Course],
        default=Status_Course.PEN.value, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = Status_Course.INS
        self.save()

    def is_registered(self):
        return bool(self.status == Status_Course.INS.value or self.status == Status_Course.APR.value)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user','course'),) #evitar repetição

class Announcement(models.Model):

    course = models.ForeignKey(
        Course, verbose_name='Curso',
        related_name='announcements', #related_name serve para fazer buscas, a partir do usuário, nesse model
        on_delete=models.CASCADE
    )

    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio',
        related_name='comments', #related_name serve para fazer buscas, a partir do usuário, nesse model
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuario',
        related_name='comments', #related_name serve para fazer buscas, a partir do usuário, nesse model
        on_delete=models.CASCADE
    )
    comment = models.TextField('Comentário', blank=False)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs):
    # Esse kwargs é porque os signals do django passam vários atributos
    # só iremos usar os dois primeiros
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course,
            status=Status_Course.INS
        )
        #envia um por vez pra evitar bloqueio por spam
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_email_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
    post_save_announcement,
    sender=Announcement,
    dispatch_uid='post_save_announcement' #evita cadastro do mesmo sinal, multiplas vezes
)