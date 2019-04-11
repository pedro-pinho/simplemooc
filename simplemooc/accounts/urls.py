from django.contrib import admin, auth
from django.urls import path
from simplemooc import courses
from django.contrib.auth.views import LoginView, LogoutView

from simplemooc import accounts
from simplemooc.accounts import views 

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    # urls provided
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
    path('resetar-senha/', accounts.views.password_reset, name="password_reset"),
    path('confirmar-senha/<key>', accounts.views.password_reset_confirm, name="password_reset_confirm"),
    path('cadastrar/', accounts.views.register, name="register"),
    path('sair/', LogoutView.as_view(), name="logout"),
    path('painel/', accounts.views.dashboard, name="dashboard"),
    path('editar/', accounts.views.edit, name="edit"),
    path('editar-senha/', accounts.views.edit_password, name="edit_password"),
]
