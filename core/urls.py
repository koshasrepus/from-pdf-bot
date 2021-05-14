from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core import views


urlpatterns = [
    path('', views.index),
    path('telegram_bot_path', csrf_exempt(views.TelegramBotWebhookView.as_view()))
]

