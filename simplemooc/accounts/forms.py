from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import PasswordReset
from simplemooc.core.tokens import TokenGenerator
from simplemooc.core.mail import send_email_template

User = get_user_model()
TokenGenerator = TokenGenerator()

# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('custom_field',)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1:
            raise forms.ValidationError("Digite uma senha")
        if not password2:
            raise forms.ValidationError("Confirme sua senha")
        if password1 != password2:
            raise forms.ValidationError("Sua senha e confirmação de senha não são iguais")
        return password2

    def save(self, commit=True): #overwrite
        user = super(RegisterForm,self).save(commit=False) #chama save do model form, não salva
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save() #agora sim salva
        return user
    class Meta:
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username","email","name"]

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Email não existe no sistema')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        import time
        key = TokenGenerator._make_token_with_timestamp(user, int(time.time()))
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = '[Simple MOOC] Redefinição de senha'
        context = {
            'reset': reset
        }
        send_email_template(subject, template_name, context, [user.email] )

#usado para forçar email unico, mas depreciado pois nosso custom user ja tem isso
# def clean_email(self):
#     #django, por padrão, além de verificar o tipo
#     # procura um clean_nomedocampo e usa se houver
#     email = self.cleaned_data['email']
#     if User.objects.filter(email=email).exists():
#         raise forms.ValidationError('Email já cadastrado no sistema')
#     return email