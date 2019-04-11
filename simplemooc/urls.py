"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# barra não é obrigatoria em "contato/"" por exemplo
# O django tenta achar a url que o usuario solicitou e, se não encontrar, coloca com "/"
app_name = 'main'
urlpatterns = [
    path('', include('simplemooc.core.urls', namespace='core')),
    path('conta/', include('simplemooc.accounts.urls', namespace='accounts')),
    path('cursos/', include('simplemooc.courses.urls', namespace='courses')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #em Produção, se coloca em um servidor a parte