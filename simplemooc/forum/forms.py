from django import forms
from .models import Comment

class ReplyForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("text",)
