from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

def enrollment_required(view_func):
    def _wrapper(request,*args, **kwargs):
        slug = kwargs['slug'] #pra usar o decorator, deve ter slug como parametro nomeado
        course = get_object_or_404(Course, slug=slug)
        has_permission = request.user.is_staff
        if not has_permission:
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except Enrollment.DoesNotExist:
                message = 'Você não tem permissão para acessar essa página'
            else:
                if enrollment.is_registered():
                    has_permission = True
                else:
                    message = 'A sua inscrição está pendente ou cancelada'
        if not has_permission:
            messages.add_message(request, messages.ERROR, message)
            return redirect('accounts:dashboard')
        request.course = course
        return view_func(request, *args, **kwargs)
    return _wrapper