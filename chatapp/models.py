from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    