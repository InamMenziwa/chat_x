from django.contrib import admin
from .models import ChatRoom, messages

admin.site.register(ChatRoom)
admin.site.register(messages)