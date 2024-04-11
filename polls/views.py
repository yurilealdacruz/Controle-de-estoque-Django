from django.shortcuts import render
from django.http import HttpResponse
from .models import Estoque

# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    return render(request, 'index.html', {'dados':dados})


