from django.contrib import admin
from django.urls import path
from simplemooc import courses
from simplemooc.courses import views

app_name = 'courses'
urlpatterns = [
    path('', courses.views.index , name='index'),
    # path('<int:id>/', courses.views.details, name='details')
    path('<slug:slug>/', courses.views.details, name='details'),
    path('<slug:slug>/inscricao/', courses.views.enrollment, name='enrollment'),
    path('<slug:slug>/cancelar-inscricao/', courses.views.undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/anuncios/', courses.views.announcements, name='announcements'),
    path('<slug:slug>/anuncios/<pk>/', courses.views.announcement_detail, name='announcement_detail'),
    path('<slug:slug>/aulas/', courses.views.lessons, name='lessons'),
    path('<slug:slug>/aula/<pk>', courses.views.lesson, name='lesson'),
    path('<slug:slug>/material/<pk>', courses.views.material, name='material'),
]
