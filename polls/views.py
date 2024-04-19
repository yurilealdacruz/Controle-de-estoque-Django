from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Estoque, SALA_CHOICES

# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    dados = Estoque.objects.all().order_by('id')
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

def editar_estoque(request, item_id):
    if request.method == 'POST':
        try:
            retirada = int(request.POST['retirada'])
            sala_laboratorio = request.POST['sala_laboratorio']  # Obtém o valor do campo sala_laboratorio
        except (ValueError, KeyError):
            retirada = 0
            sala_laboratorio = ''
        item = Estoque.objects.get(id=item_id)
        item.retirada = retirada
        item.sala_laboratorio = sala_laboratorio  # Atualiza o valor do campo sala_laboratorio no objeto Estoque
        item.save()
        return redirect('index')
    
    item = Estoque.objects.get(id=item_id)
    salas_laboratorio = Estoque.objects.values_list('sala_laboratorio', flat=True).distinct()
    return render(request, 'nome.html', {'item': item, 'salas_laboratorio': salas_laboratorio})