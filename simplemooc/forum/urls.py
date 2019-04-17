from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from simplemooc import forum
from simplemooc.forum import views

app_name = 'forum'
urlpatterns = [
    path('', forum.views.index , name='index'),
    path('tag/<slug:tag>/', forum.views.index, name='index_tagged'),
    path('comentarios/<slug:slug>/', forum.views.thread, name='thread'),
    path('resposta/correta/<int:pk>/', forum.views.reply_correct, name='reply_correct'),
    path('resposta/errada/<int:pk>/', forum.views.reply_incorrect, name='reply_incorrect'),
]
