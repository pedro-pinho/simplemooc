from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    
    # username = models.CharField('Nome de usuário', unique=True, max_length=30)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Nome de usuário',
        max_length=30,
        unique=True,
        help_text='Obrigatório. 50 caracteres ou menos. Letras, números e and @/./+/-/_ apenas.',
        validators=[username_validator],
        error_messages={
            'unique': 'Já existe um usuário com esse nome',
        },
    )

    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nome completo', blank=True, max_length=100)
    is_active = models.BooleanField('Esta ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É admin?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    #as seguintes classes não são obrigatorias, mas recomendadas pra integração 100% com as funcionalidades do django
    def get_short_name(self):
        return self.username
    
    def def_full_name(self):
        return str(self)
    
    class Meta:
        verbose_name='Usuário'
        verbose_name_plural='Usuários'

class PasswordReset(models.Model): #criação da chave verificadora que foi enviada por email
    #usuario pode ter 1 ou mais password resets

    # no django, uma relação "um para muitos"
    # a relação fica no "muitos", no "filho"
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', #pra poder acessar com user.resets.all()
        on_delete=models.CASCADE
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    # para evitar que o mesmo usuário receba no email a mesma chave
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)
    
    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name = 'Novas Senha2'
        ordering = ['-created_at'] #decrescente
