from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import login, home

urlpatterns = [
    path('', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', home, name='home')
]
