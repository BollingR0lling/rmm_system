from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    auth,
    home,
    machines,
    sys_info,
    cli,
)

urlpatterns = [
    path('', auth, name='auth'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', home, name='home'),
    path('machines', machines, name='machines'),
    path('sys_info', sys_info, name='sys_info'),
    path('cli', cli, name='cli')
]
