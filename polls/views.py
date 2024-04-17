from django.shortcuts import render, redirect
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

def editar_nome(request):
    return render(request, 'nome.html')


def update_user(request):
    if request.method == 'POST':
        novo_nome = request.POST['new_name']
        # Supondo que você tenha um modelo de usuário chamado 'Usuario'
        usuario = Estoque.objects.get(id=1)  # Use o ID correto do usuário que deseja modificar
        usuario.nome = novo_nome
        usuario.save()
        return redirect('index')  # Redirecionar para uma página de sucesso após a atualização

    return render(request, 'formulario.html')