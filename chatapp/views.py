from django.shortcuts import render
from .models import ChatRoom, messages


def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, "chatapp/index.html", {"rooms":rooms})

def chatroom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    message = messages.objects.filter(room=chatroom)[0:30]
    return render(request, "chatapp/room.html", {"chatroom":chatroom, "messages":message})