from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    auth,
    sys_info,
    HomeView,
    MachinesView,
    AddMachineView,
    CLIView,
)

urlpatterns = [
    path('', auth, name='auth'),
    path('', include('django_prometheus.urls')),
    path('sys_info', sys_info, name='sys_info'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', HomeView.as_view(), name='home'),
    path('machines', MachinesView.as_view(), name='machines'),
    path('cli/<str:ip_addr>', CLIView.as_view(), name='cli'),
    path('add_machine', AddMachineView.as_view(), name='add_machine'),
]
