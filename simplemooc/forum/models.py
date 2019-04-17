from django.db import models
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from ..courses.models import Course

class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        null=False, on_delete=models.CASCADE
    )
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    # limit = models.Q(thread_type.model_class()) | models.Q(comment_type.model_class())
    #limit = models.Q(app_label='forum', model='Thread') | models.Q(app_label='forum', model='Comment') limit_choices_to = limit, 

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

class Thread(models.Model):

    title = models.CharField('Título', max_length=200)
    text = models.TextField('Texto', blank=True)
    slug = models.SlugField('Atalho', max_length=100, unique=True)

    course = models.ForeignKey(
        Course, verbose_name='Curso',
        null=True, blank=True, default=None,
        related_name='discussoes',
        on_delete=models.CASCADE
    )
    answers = models.IntegerField('Respostas', blank=True, default=0)
    
    activities = GenericRelation(Activity)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='discussão', null=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    tags = TaggableManager()

    class Meta:
        verbose_name = "Discussão"
        verbose_name_plural = "Discussões"
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):        
        return reverse(
            'forum:thread',
            kwargs={'slug': str(self.slug)}
            )

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    text = models.TextField('Texto')
    activities = GenericRelation(Activity)
    correct = models.BooleanField('Correta?', blank=True, default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='replies', null=False,
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        Thread, verbose_name='thread', default=None,
        related_name='comentarios',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

#métodos a seguir só são ativados com método .save()
#se for update, não vai ativar
def post_save_reply(created, instance, **kwargs):
    # Esse kwargs é porque os signals do django passam vários atributos
    # só iremos usar os dois primeiros
    instance.thread.answers = instance.thread.comentarios.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.comentarios.exclude(pk=instance.pk).update(
            correct=False
        )

def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.comentarios.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply,
    sender=Comment,
    dispatch_uid='post_save_reply'
)

models.signals.post_delete.connect(
    post_delete_reply,
    sender=Comment,
    dispatch_uid='post_delete_reply'
)