from django.db import models

class User(models.Model):
    """Пользователь Telegram"""
    chat_id = models.IntegerField()
    username = models.CharField(max_length=64)
    is_bot = models.BooleanField()
    date = models.DateTimeField(auto_now=True)

class Files(models.Model):
    """Файлы пользователя"""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    file_id = models.CharField(max_length=96)
    file_unique_id = models.CharField(max_length=32)
    mime_type = models.CharField(max_length=32)
    file_size = models.IntegerField()
    date = models.DateTimeField(auto_now=True)


