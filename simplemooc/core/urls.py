from django.contrib import admin
from django.urls import path
from simplemooc import core
from simplemooc.core import views 

app_name = 'core'
urlpatterns = [
    path('', core.views.home , name='home'),
    path('contato/', core.views.contact , name='contact')
]
