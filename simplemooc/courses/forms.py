from django import forms
from django.core.mail import send_mail
from django.conf import settings #carrega o arquivo settings e todas as confs django padrão

from simplemooc.core.mail import send_email_template

from .models import Comment

# import settings traz somente o arquivo settings.py

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome',max_length=60)
    email  = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def send_mail(self, course):
        subject = '[%s] Contato ' % course
        context = {
            'name':self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'
        send_email_template(
            subject, template_name,
            context, [settings.CONTACT_EMAIL]
        )

class CommentAnnouncement(forms.ModelForm):
    
    #comment = forms.CharField(label='Mensagem', widget=forms.Textarea)
    class Meta:
        model = Comment 
        fields = ["comment"]
