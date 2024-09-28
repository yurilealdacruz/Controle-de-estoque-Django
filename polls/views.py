from django.shortcuts import render, redirect
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseBadRequest
from .forms import AdicionarEstoqueForm
from .models import Estoque, SALA_CHOICES, EstoqueAT, EstoqueAlmo
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use o backend Agg para gerar imagens
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth import logout



# Create your views here.


def index(request):
    dados = Estoque.objects.all()
    dados = Estoque.objects.all().order_by('id')
    return render(request, 'index.html', {'dados':dados, "salas": SALA_CHOICES})

def estoqueat(request):
    dadosat = EstoqueAT.objects.all()
    dadosat = EstoqueAT.objects.all().order_by('id')
    return render(request, 'templatesat/index.html', {"dadosat":dadosat, "salas":SALA_CHOICES})

def estoquealmo(request):
    dadosalmo = EstoqueAlmo.objects.all()
    dadosalmo = EstoqueAlmo.objects.all().order_by('id')
    return render(request, 'templatesalmo/index.html', {"dadosalmo":dadosalmo, "salas":SALA_CHOICES})


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
    return render(request, 'accounts/profile/profile.html')

def profileat(request):
    # Lógica para recuperar e exibir o perfil do usuário
    return render(request, 'templatesat/accounts/profile/profile.html')

@login_required
def editar_estoque(request, item_id):

        if request.method == 'POST':
                try:
                    retirada = int(request.POST['retirada'])
                    sala_laboratorio = request.POST['sala_laboratorio']  # Obtém o valor do campo sala_laboratorio
                except (ValueError, KeyError):
                    retirada = 0
                    sala_laboratorio = ''
                if retirada >= 0:
                    item = Estoque.objects.get(id=item_id)
                    item.retirada = retirada
                    item.sala_laboratorio = sala_laboratorio  # Atualiza o valor do campo sala_laboratorio no objeto Estoque
                    item.save()
                    return redirect('index')
                else:
                    return HttpResponseBadRequest("Método inválido")

        item = Estoque.objects.get(id=item_id)
        salas_laboratorio = Estoque.objects.values_list('sala_laboratorio', flat=True).distinct()
        return render(request, 'nome.html', {'item': item, 'salas_laboratorio': salas_laboratorio})

@login_required
def editar_estoqueat(request, item_id):

        if request.method == 'POST':
                try:
                    retirada = int(request.POST['retirada'])
                except (ValueError, KeyError):
                    retirada = 0
                if retirada >= 0:
                    item = EstoqueAT.objects.get(id=item_id)
                    item.retirada = retirada
                    item.save()
                    return redirect('estoqueat')
                else:
                    return HttpResponseBadRequest("Método inválido")

        item = EstoqueAT.objects.get(id=item_id)
        return render(request, 'nome.html', {'item': item})

@login_required
def editar_estoquealmo(request, item_id):

        if request.method == 'POST':
                try:
                    retirada = int(request.POST['retirada'])
                except (ValueError, KeyError):
                    retirada = 0
                if retirada >= 0:
                    item = EstoqueAlmo.objects.get(id=item_id)
                    item.retirada = retirada
                    item.save()
                    return redirect('estoquealmo')
                else:
                    return HttpResponseBadRequest("Método inválido")

        item = EstoqueAlmo.objects.get(id=item_id)
        return render(request, 'nome.html', {'item': item})


def adicionar_estoque(request, dado_id):
    if request.method == 'POST':
        # Obtenha o objeto de dado com base no ID
        dado = Estoque.objects.get(id=dado_id)
        # Crie um formulário com os dados enviados pelo usuário
        form = AdicionarEstoqueForm(request.POST)
        if form.is_valid():
            # Obtenha a quantidade a ser adicionada do formulário
            quantidade = form.cleaned_data['quantidade']
            # Adicione a quantidade ao estoque do objeto dado
            dado.estoque += quantidade + 1
            # Salve o objeto atualizado
            dado.save()
            # Redirecione para a página de detalhes do objeto ou para onde desejar
            return redirect('index')  # Substitua 'nome_da_url' pela URL desejada
    else:
        # Se o método da solicitação não for POST, retorne um erro ou redirecione
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
    legend_labels = [f"{label} ({porcentagem})" for label, porcentagem in zip(labels, porcentagens)]
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
