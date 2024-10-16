from django.shortcuts import render, redirect
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseBadRequest
from .forms import AdicionarEstoqueForm
from .models import Estoque, SALA_CHOICES, EstoqueAT, EstoqueAlmo, EstoqueHistorico, EstoqueHistoricoAT, EstoqueHistoricoAlmo
import matplotlib.pyplot as plt
import io
import numpy as np
import base64
import matplotlib
matplotlib.use('Agg')  # Use o backend Agg para gerar imagens
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from .forms import EstoqueAlmoForm, EstoqueATForm, EstoqueForm



# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    dados = Estoque.objects.all().order_by('id')
    return render(request, 'index.html', {'dados':dados, "salas": SALA_CHOICES})

def estoqueat(request):
    dadosat = EstoqueAT.objects.all()
    dadosat = EstoqueAT.objects.all().order_by('id')
    return render(request, 'templatesat/index.html', {"dadosat":dadosat})

def estoquealmo(request):
    dadosalmo = EstoqueAlmo.objects.all()
    dadosalmo = EstoqueAlmo.objects.all().order_by('id')
    return render(request, 'templatesalmo/index.html', {"dadosalmo":dadosalmo})


def buscar_item(request):
    query = request.GET.get('q')  # Obtenha o termo de busca
    if query:
        # Busque por itens que contenham o termo no nome
        items = Estoque.objects.filter(nome__icontains=query)
    else:
        # Se nenhum termo for buscado, mostre todos os itens
        items = Estoque.objects.all()
    
    return render(request, 'index.html', {'dados': items, 'query': query, 'salas': SALA_CHOICES})


def buscar_itemAT(request):
    query = request.GET.get('q')  # Obtenha o termo de busca
    if query:
        # Busque por itens que contenham o termo no nome
        items = EstoqueAT.objects.filter(nome__icontains=query)
    else:
        # Se nenhum termo for buscado, mostre todos os itens
        items = EstoqueAT.objects.all()

    # Renderize o template e passe os itens e salas
    return render(request, 'templatesat/index.html', {'dadosat': items, 'query': query})

def buscar_itemAlmo(request):
    query = request.GET.get('q')  # Obtenha o termo de busca
    if query:
        # Busque por itens que contenham o termo no nome
        items = EstoqueAlmo.objects.filter(nome__icontains=query)
    else:
        # Se nenhum termo for buscado, mostre todos os itens
        items = EstoqueAlmo.objects.all()

    # Renderize o template e passe os itens e salas
    return render(request, 'templatesalmo/index.html', {'dadosalmo': items, 'query': query})
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
    return render(request, 'accounts/profile/profile.html')

def profileat(request):
    # Lógica para recuperar e exibir o perfil do usuário
    return render(request, 'templatesat/accounts/profile/profile.html')

@login_required
def editar_estoque(request, item_id):
    try:
        item = Estoque.objects.get(id=item_id)  # Obter o item primeiro
    except Estoque.DoesNotExist:
        messages.error(request, "Item não encontrado.")
        return redirect('index')

    if not request.user.has_perm('polls.change_estoque'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('index')  # Redireciona para o índice ou a página desejada

    if request.method == 'POST':
        try:
            retirada = int(request.POST['retirada'])
            sala_laboratorio = request.POST['sala_laboratorio']  # Obtém o valor do campo sala_laboratorio
        except (ValueError, KeyError):
            messages.error(request, "Por favor, forneça um valor válido para retirada e sala.")
            return redirect('index')  # Redireciona se houver erro

        # Verifica se a quantidade retirada não excede o estoque disponível
        if retirada >= 0 and retirada <= item.estoque:
            item.retirada = retirada
            item.sala_laboratorio = sala_laboratorio  # Atualiza o valor do campo sala_laboratorio
            item.adicao = 0
            item.save()
            messages.success(request, "Estoque atualizado com sucesso.")
            return redirect('index')
        else:
            messages.error(request, "Quantidade de retirada inválida. Você não pode retirar mais do que o disponível em estoque.")
            return redirect('index')

    salas_laboratorio = Estoque.objects.values_list('sala_laboratorio', flat=True).distinct()
    return render(request, 'nome.html', {'item': item, 'salas_laboratorio': salas_laboratorio})

@login_required
def editar_estoqueat(request, item_id):
    item = EstoqueAT.objects.get(id=item_id)  # Obter o item primeiro
    
    if not request.user.has_perm('polls.change_estoque_at'):
        messages.error(request, "Você não tem permissão para alterar o item.")
        return redirect('estoqueat')  # Redirecionar para a lista de estoque
    
    if request.method == 'POST':
        try:
            quantidade_retirada = int(request.POST['retirada'])
        except (ValueError, KeyError):
            messages.error(request, "Por favor, forneça um valor válido para retirada.")
            return redirect('estoqueat')  # Redirecionar para a lista de estoque
        
        if quantidade_retirada >= 0 and quantidade_retirada <= item.estoque:
            item.retirada = quantidade_retirada
            item.adicao = 0
            item.save()
            messages.success(request, "Estoque alterado com sucesso.")
            return redirect('estoqueat')
        else:
            messages.error(request, "Quantidade de retirada inválida. Verifique o estoque disponível.")
            return redirect('estoqueat')  # Redirecionar para a lista de estoque
    
    return render(request, 'nome.html', {'item': item})

@login_required
def editar_estoquealmo(request, item_id):
    try:
        item = EstoqueAlmo.objects.get(id=item_id)  # Obter o item primeiro
    except EstoqueAlmo.DoesNotExist:
        messages.error(request, "Item não encontrado.")
        return redirect('estoquealmo')

    if not request.user.has_perm('polls.change_estoque_almo'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('estoquealmo')

    if request.method == 'POST':
        try:
            retirada = int(request.POST['retirada'])
        except (ValueError, KeyError):
            messages.error(request, "Por favor, forneça um valor válido para retirada.")
            return redirect('estoquealmo')

        # Verifica se a quantidade retirada não excede o estoque disponível
        if retirada >= 0 and retirada <= item.estoque:
            item.retirada = retirada
            item.adicao = 0
            item.save()
            messages.success(request, "Estoque atualizado com sucesso.")
            return redirect('estoquealmo')
        else:
            messages.error(request, "Quantidade de retirada inválida. Você não pode retirar mais do que o disponível em estoque.")
            return redirect('estoquealmo')

    return render(request, 'nome.html', {'item': item})

def adicionar_estoque(request, dado_id):
    if not request.user.has_perm('polls.change_estoque'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('index')
    else:
        if request.method == 'POST':
            dado = Estoque.objects.get(id=dado_id)
            form = AdicionarEstoqueForm(request.POST)
            if form.is_valid():
                quantidade = form.cleaned_data['quantidade']
                adicao = quantidade
                dado.estoque += adicao
                dado.adicao = adicao # Atualiza o estoque
                dado.sala_laboratorio = ''
                dado.retirada = 0
                dado.save()

                # Adicionando um registro no histórico personalizado
                EstoqueHistorico.objects.create(estoque=dado, quantidade_adicionada=adicao)

                return redirect('index')
        else:
            return HttpResponseBadRequest("Método inválido")


def adicionar_estoqueat(request, dado_id):
    if not request.user.has_perm('polls.change_estoque_at'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('estoqueat')
    else:
        if request.method == 'POST':
            dado = EstoqueAT.objects.get(id=dado_id)
            form = AdicionarEstoqueForm(request.POST)
            if form.is_valid():
                quantidade = form.cleaned_data['quantidade']
                adicao = quantidade
                dado.estoque += adicao
                dado.adicao = adicao # Atualiza o estoque
                dado.retirada = 0
                dado.save()

                # Adicionando um registro no histórico personalizado
                EstoqueHistoricoAT.objects.create(estoque=dado, quantidade_adicionada=adicao)

                return redirect('estoqueat')
        else:
            return HttpResponseBadRequest("Método inválido")
    

def adicionar_estoquealmo(request, dado_id):
    if not request.user.has_perm('polls.change_estoque_almo'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('estoquealmo')
    else:
        if request.method == 'POST':
            dado = EstoqueAlmo.objects.get(id=dado_id)
            form = AdicionarEstoqueForm(request.POST)
            if form.is_valid():
                quantidade = form.cleaned_data['quantidade']
                adicao = quantidade
                dado.estoque += adicao
                dado.adicao = adicao # Atualiza o estoque
                dado.retirada = 0
                dado.save()

                # Adicionando um registro no histórico personalizado
                EstoqueHistoricoAlmo.objects.create(estoque=dado, quantidade_adicionada=adicao)

                return redirect('estoquealmo')
        else:
            return HttpResponseBadRequest("Método inválido")

def historico_retiradas(request):
    # Obtendo o histórico de retiradas de Estoque
    historico_estoque = Estoque.history.all()

    context = {
        'historico_estoque': historico_estoque,
    }

    return render(request, 'historico_retiradas.html', context)





def historico_retiradasAT(request):
    # Obtendo o histórico de retiradas de Estoque
    historico_estoqueat = EstoqueAT.history.all()

    context = {
        'historico_estoqueat': historico_estoqueat,
    }

    return render(request, 'templatesat/historico_retiradasat.html', context)

def historico_retiradasAlmo(request):
    # Obtendo o histórico de retiradas de Estoque
    historico_estoquealmo = EstoqueAlmo.history.all()

    context = {
        'historico_estoquealmo': historico_estoquealmo,
    }

    return render(request, 'templatesalmo/historico_retiradasalmo.html', context)




def historico_retiradas_grafico_at(request):
    # Agrupar os dados históricos por nome e somar as retiradas
    estoques = EstoqueAT.history.values('nome').annotate(total_retiradas=Sum('retirada'))

    # Prepara os dados para o gráfico
    labels = [estoque['nome'] for estoque in estoques]
    sizes = [estoque['total_retiradas'] for estoque in estoques]
    colors = plt.cm.Paired.colors[:len(labels)]

    # Verifica se há dados para plotar
    if not sizes:
        sizes = [1]  # Para evitar erro no gráfico se não houver dados

    # Criar gráfico de pizza sem porcentagens internas
    fig, ax = plt.subplots(figsize=(15, 10))
    wedges, texts = ax.pie(sizes, colors=colors, shadow=True, startangle=140)

    # Calcula a porcentagem de cada item
    porcentagens = [f"{size / sum(sizes) * 100:.1f}%" for size in sizes]

    # Cria uma lista de rótulos com nome e porcentagem
    legend_labels = [f"{label} ({porcentagem})" for label, porcentagem in zip(labels, porcentagens)]

    # Adiciona a legenda fora do gráfico
    ax.legend(wedges, legend_labels, title="Itens", loc="center left", bbox_to_anchor=(0.85, 0, 0.5, 1))

    # Configura o gráfico para ser "igual"
    ax.axis('equal')

    # Salvar a imagem em um objeto BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Converter a imagem em base64
    grafico_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Retornar o template com o gráfico
    return render(request, 'historico_retiradas_grafico_at.html', {'grafico_base64': grafico_base64})

def historico_retiradas_grafico_almo(request):
    # Agrupar os dados históricos por nome e somar as retiradas
    estoques = EstoqueAlmo.history.values('nome').annotate(total_retiradas=Sum('retirada'))

    # Ordenar todos os itens do maior para o menor
    estoques = sorted(estoques, key=lambda x: x['total_retiradas'], reverse=True)

    # Prepara os dados para o gráfico
    labels = [estoque['nome'] for estoque in estoques]
    sizes = [estoque['total_retiradas'] for estoque in estoques]
    
    # Criar gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 9))  # Aumentar o tamanho do gráfico
    ax.barh(labels, sizes, color='skyblue', height=0.5)  # Ajustar a altura das barras

    # Adicionar rótulos e título
    ax.set_xlabel('Total de Retiradas', fontsize=14)  # Aumentar o tamanho do rótulo do eixo x
    ax.set_title('Gráfico de Retiradas de Insumos', fontsize=16)  # Aumentar o tamanho do título

    # Adicionar os valores ao lado de cada barra
    for index, value in enumerate(sizes):
        ax.text(value, index, str(value), fontsize=12)  # Aumentar o tamanho da fonte dos valores

    # Aumentar o tamanho da fonte dos rótulos das barras
    ax.tick_params(axis='y', labelsize=12)  # Altera o tamanho da fonte dos nomes dos itens

    # Inverter a ordem dos itens para que o maior fique no topo
    ax.invert_yaxis()

    # Ajustar o layout para centralizar e melhorar a apresentação
    plt.subplots_adjust(left=0.3, right=0.9, top=3.0, bottom=0.2, hspace=1.0)  # Aumentar o espaçamento vertical

    # Salvar a imagem em um objeto BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # Usar bbox_inches='tight' para ajustar a imagem
    buf.seek(0)
    plt.close()

    # Converter a imagem em base64
    grafico_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Retornar o template com o gráfico
    return render(request, 'historico_retiradas_grafico_almo.html', {'grafico_base64': grafico_base64})

def historico_retiradas_grafico(request):
    # Agrupar os dados históricos por nome e somar as retiradas
    estoques = Estoque.history.values('nome').annotate(total_retiradas=Sum('retirada'))

    # Prepara os dados para o gráfico de itens
    labels = [estoque['nome'] for estoque in estoques]
    sizes = [estoque['total_retiradas'] for estoque in estoques]
    colors = plt.cm.Paired.colors[:len(labels)]

    # Verifica se há dados para plotar
    if not sizes:
        sizes = [1]  # Para evitar erro no gráfico se não houver dados

    # Prepara os dados para o gráfico de laboratórios, limitando a 6 resultados
    laboratorios = (Estoque.history
                    .values('sala_laboratorio')
                    .annotate(total_retiradas=Sum('retirada'))
                    .order_by('-total_retiradas')[:6])  # Limitando a 6 laboratórios

    lab_labels = [lab['sala_laboratorio'] for lab in laboratorios]
    lab_sizes = [lab['total_retiradas'] for lab in laboratorios]

    # Verifica se há dados para plotar
    if not lab_sizes:
        lab_sizes = [1]  # Para evitar erro no gráfico se não houver dados

    # Gráficos lado a lado
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))  # Uma linha, duas colunas

    # Gráfico de pizza para itens
    wedges, texts = ax1.pie(sizes, colors=colors, shadow=True, startangle=140)

    porcentagens = [f"{size / sum(sizes) * 100:.1f}%" for size in sizes]
    # Adiciona a quantidade junto à porcentagem na legenda
    legend_labels = [f"{label} ({porcentagem}) - {quantidade} retiradas"
                     for label, porcentagem, quantidade in zip(labels, porcentagens, sizes)]
    ax1.legend(wedges, legend_labels, title="Itens", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax1.set_title("Distribuição de Retiradas por Item")
    ax1.axis('equal')

    # Gráfico de barras para laboratórios
    bar_width = 0.5  # Largura das barras
    x_positions = range(len(lab_labels))  # Posições das barras
    ax2.bar(x_positions, lab_sizes, color=colors[:len(lab_labels)], width=bar_width)

    # Configurar os rótulos das barras
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(lab_labels, rotation=45, ha='right')  # Alinhamento à direita

    ax2.set_xlabel('Laboratórios')
    ax2.set_ylabel('Total de Retiradas')
    ax2.set_title("Total de Retiradas por Laboratório (Top 6)")

    # Ajustar layout para evitar sobreposição
    plt.tight_layout()

    # Salvar a imagem em um objeto BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Converter a imagem em base64
    grafico_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Retornar o template com o gráfico
    return render(request, 'historico_retiradas_grafico.html', {'grafico_base64': grafico_base64})

# Adicione uma nova view para renderizar o template

def mostrar_grafico(request):
    return render(request, 'seu_template.html')

def realizar_logout(request):
    logout(request)  # Realiza o logout
    return redirect('login')  # Redireciona para a página inicial ou qualquer outra página

def adicionar_item_almo(request):
    if not request.user.has_perm('polls.change_estoque_almo'):
        raise PermissionDenied("Você não tem permissão para editar o estoque.")
    else:
        if request.method == 'POST':
            form = EstoqueAlmoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('estoquealmo')  # Redirecione para a página inicial ou para onde você quiser
        else:
            form = EstoqueAlmoForm()
        return render(request, 'adicionar_item_almo.html', {'form': form})
    

def adicionar_item(request):
    if not request.user.has_perm('polls.change_estoque'):
        messages.error(request, "Você não tem permissão para editar o estoque.")
        return redirect('index')  # Redireciona para o índice ou a página desejada
    else:
        if request.method == 'POST':
            form = EstoqueForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')  # Redirecione para a página inicial ou para onde você quiser
        else:
            form = EstoqueForm()
        return render(request, 'adicionar_item.html', {'form': form})
    

def adicionar_item_at(request):
    if not request.user.has_perm('polls.change_estoque_at'):
        raise PermissionDenied("Você não tem permissão para editar o estoque.")
    else:
        if request.method == 'POST':
            form = EstoqueATForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('estoqueat')  # Redirecione para a página inicial ou para onde você quiser
        else:
            form = EstoqueATForm()
        return render(request, 'adicionar_item_at.html', {'form': form})