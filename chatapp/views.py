from django.shortcuts import render
from .models import ChatRoom

def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, "chatapp/index.html", {"rooms":rooms})
