from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentAnnouncement
from .decorators import enrollment_required

from simplemooc.core.enums import Status_Course

def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request,'courses/index.html', context) #presume a pasta 'templates' como raiz

def details(request, slug):
    # course = Course.objects.get(pk=id)
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST) #contato
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            # print(form.cleaned_data['name'])
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form
    return render(request,'courses/details.html', context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created or (enrollment.status == Status_Course.CAN.value):
        enrollment.active()
        messages.add_message(request, messages.INFO, 'Inscrição realizada com sucesso')
    else:
        messages.add_message(request, messages.ERROR, 'Inscrição não pôde ser concluida. Por favor, verifique se você já está inscrito, e caso não, tente mais tarde.')

    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment,
        user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.status = Status_Course.CAN.value
        enrollment.save()
        messages.add_message(request, messages.INFO, 'Inscrição cancelada')
        return redirect('accounts:dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template_name = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)

@login_required
@enrollment_required
def announcement_detail(request, slug, pk):
    course = request.course
    form = CommentAnnouncement(request.POST or None) #se veio por get, o request.POST vem QueryDic vazio
    announcement = get_object_or_404(course.announcements.all(), pk=pk)

    context = {}
    if form.is_valid(): #vai dar false, mas não vai validar os dados se estiver vazio
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()

        messages.add_message(request, messages.INFO, 'Comentário enviado')
        form = CommentAnnouncement()
    context['form'] = form

    template_name = 'courses/show_announcement.html'

    context['course'] = course
    context['announcement'] = announcement

    return render(request, template_name, context)

    
@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template_name = 'courses/lessons.html'
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template_name, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    # restringindo para o curso, o usuario pode manipular a url e colocar de outro curso
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and lesson.is_available():
        messages.add_message(request, messages.ERROR, 'Essa aula não está mais disponível')
        return redirect('courses:lessons', slug=course.slug)
    template_name = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template_name, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    # duplo underline __ acessa a propriedado do outro objeto
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and lesson.is_available():
        messages.add_message(request, messages.ERROR, 'Esse material não está mais disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk )
    if not material.is_embedded:
        return redirect(material.file.url)
        
    template_name = 'courses/material.html'
    context = {
        'course': request.course,
        'lesson': lesson,
        'material': material
    }
    return render(request, template_name, context)