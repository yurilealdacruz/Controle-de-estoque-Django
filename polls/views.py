from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
import logging
from django.contrib.auth.decorators import login_required
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


logger = logging.getLogger(__name__)

def cadastro_login(request):
    logger.info('Acessou a view cadastro_login')
    if request.method == 'POST':
        logger.info('Método POST recebido')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            logger.info('Formulário válido')
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        logger.info('Método GET recebido')
        form = UserCreationForm()
    return render(request, 'cadastro_login.html', {'form': form})

def profile(request):
    # Lógica para recuperar e exibir o perfil do usuário
    return render(request,  'accounts/profile/profile.html')


@login_required
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
         