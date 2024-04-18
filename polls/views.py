from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Estoque, SALA_CHOICES

# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    return render(request, 'index.html', {'dados':dados, "salas": SALA_CHOICES})


def buscar_item(request):
    query = request.GET.get('q')  # Obtenha o parâmetro 'q' da query string (nome do item a ser buscado)
    if query:
        # Faça a busca no banco de dados pelos itens com o nome semelhante ao que foi buscado
        items = Estoque.objects.filter(nome__icontains=query)
    else:
        items = Estoque.objects.all()  # Se nenhum termo de busca foi fornecido, retorne todos os itens

    return render(request, 'index.html', {'dados': items, 'query': query})

# def editar_nome(request):
#     return render(request, 'nome.html')

def editar_nome(request, item_id):
    if request.method == 'POST':
        novo_nome = request.POST['new_name']
        item = Estoque.objects.get(id=item_id)
        item.nome = novo_nome
        item.save()
        return redirect('index')
    
    item = Estoque.objects.get(id=item_id)
    return render(request, 'nome.html', {'item': item, 'salas_laboratorio': SALA_CHOICES})