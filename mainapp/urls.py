from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import auth, home

urlpatterns = [
    path('', auth, name='auth'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', home, name='home')
]
