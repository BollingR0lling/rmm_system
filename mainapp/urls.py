from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    auth,
    HomeView,
    MachinesView,
    AddMachineView,
    DeleteMachineView,
    WSview,
)

urlpatterns = [
    path('', auth, name='auth'),
    path('', include('django_prometheus.urls')),
    path('cli/<str:ip_addr>&port=<int:port>', WSview.as_view(), name='cli'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', HomeView.as_view(), name='home'),
    path('machines', MachinesView.as_view(), name='machines'),
    path('delete_machine/<str:ip_addr>/<int:port>', DeleteMachineView.as_view(), name='delete_machine'),
    path('add_machine', AddMachineView.as_view(), name='add_machine'),
]
