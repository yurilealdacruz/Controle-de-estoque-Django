from django.shortcuts import render
from django.http import HttpResponse
from .models import Estoque

# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    return render(request, 'index.html', {'dados':dados})


def buscar_item(request):
    query = request.GET.get('q')  # Obtenha o parâmetro 'q' da query string (nome do item a ser buscado)
    if query:
        # Faça a busca no banco de dados pelos itens com o nome semelhante ao que foi buscado
        items = Estoque.objects.filter(nome__icontains=query)
    else:
        items = Estoque.objects.all()  # Se nenhum termo de busca foi fornecido, retorne todos os itens

    return render(request, 'index.html', {'dados': items, 'query': query})