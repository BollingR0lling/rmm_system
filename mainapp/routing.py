from django.urls import path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('cli/<str:ip_addr>&port=<int:port>', WSConsumer.as_asgi())
]
