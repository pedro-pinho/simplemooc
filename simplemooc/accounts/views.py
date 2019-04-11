from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from simplemooc.courses.models import Enrollment
from simplemooc.core.enums import Status_Course

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    context['enrollments'] = Enrollment.objects.filter(user=request.user).exclude(status=Status_Course.CAN.value)
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        # precisa desses instance=request.user se não, não leva em consideração o usuario atual
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso')
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Senha alterada com sucesso')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #todo form associado ao model tem um .save()
            user = form.save()
            # a senha do user.password está criptografada
            # password1 e 2 são as mesmas (senha e confirmação de senha)
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

def password_reset(request):
    template_name='accounts/password_reset.html'
    form = PasswordResetForm(request.POST or None) #se veio por get, o request.POST vem QueryDic vazio
    context = {}

    if form.is_valid(): #vai dar false, mas não vai validar os dados se estiver vazio
        form.save()
        messages.add_message(request, messages.INFO, 'Um e-mail foi enviando para você com mais detalhes de como criar uma nova senha')
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key) 
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, 'Sucesso')
        reset.delete()
    context['form'] = form
    return render(request, template_name, context)