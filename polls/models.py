from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords #pip install django-simple-history

# id (primary key - automático)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)

# Depois
# category (foreign key), show (boolean), owner (foreign key)
# picture (imagem)

SALA_CHOICES = [
    ('SALA 1.1.03', 'SALA 1.1.03'),
        ('SALA 1.1.04', 'SALA 1.1.04'),
        ('SALA 1.1.05' ,'SALA 1.1.05'),
        ('Laboratório de H&P', 'Laboratório de H&P'  ),
        ('Laboratório Telecomunicações', 'Laboratório Telecomunicações'),
        ('Laboratório de Robótica', 'Laboratório de Robótica'),
        ('Laboratório de Sistemas Digitais', 'Laboratório de Sistemas Digitais'),
        ('Laboratório BIM', 'Laboratório BIM'),
        ('Laboratório CAX', 'Laboratório CAX'),
        ('Laboratório de Eletrônica', 'Laboratório de Eletrônica'),
        ('Laboratório de Informática 1', 'Laboratório de Informática 1'),
        ('Laboratório de Informática 2', 'Laboratório de Informática 2'),
        ('Laboratório de Informática 3', 'Laboratório de Informática 3'),
        ('Laboratório de Programação Avançada', 'Laboratório de Programação Avançada'),
        ('Laboratório Cyber', 'Laboratório Cyber'),
        ('SALA 2.1.01', 'SALA 2.1.01'),
        ('SALA 2.1.02', 'SALA 2.1.02'),
        ('SALA 2.1.03', 'SALA 2.1.03'),
        ('SALA 2.1.04', 'SALA 2.1.04'),
        ('SALA 2.1.06', 'SALA 2.1.06'),
        ('SALA 2.1.07', 'SALA 2.1.07'),
        ('SALA 2.1.08', 'SALA 2.1.08'),
        ('SALA 2.1.09', 'SALA 2.1.09'),
        ('SALA 2.2.01', 'SALA 2.2.01'),
        ('SALA 2.2.02', 'SALA 2.2.02'),
        ('SALA 2.2.03', 'SALA 2.2.03'),
        ('SALA 2.2.04', 'SALA 2.2.04'),
        ('SALA 2.2.05', 'SALA 2.2.05'),
        ('SALA 2.2.06', 'SALA 2.2.06'),
        ('SALA 2.2.08', 'SALA 2.2.08'),
        ('SALA 2.2.09', 'SALA 2.2.09'),
        ('SALA 2.2.10', 'SALA 2.2.10'),
        ('SALA 2.3.01 (AUDITÓRIO)', 'SALA 2.3.01 (AUDITÓRIO)'),
        ('SALA 2.3.03', 'SALA 2.3.03'),
        ('SALA 2.3.09 (AUDITÓRIO)', 'SALA 2.3.09 (AUDITÓRIO)'),
        ('SALA 2.3.05', 'SALA 2.3.05'),
        ('SALA 2.3.06', 'SALA 2.3.06'),
        ('Laboratório de Simulação Numérica', 'Laboratório de Simulação Numérica'),
        ('Laboratório de Redes', 'Laboratório de Redes'),
        ('Laboratório de Software', 'Laboratório de Software'),
        ('Laboratório de Equipamentos Industriais', 'Laboratório de Equipamentos Industriais'),
        ('Laboratório de Gestão Empresarial', 'Laboratório de Gestão Empresarial'),
        ('Laboratório de Transporte e Distribuição', 'Laboratório de Transporte e Distribuição'),
        ('SALA 4.1.1','SALA 4.1.1'),
        ('SALA 4.1.2', 'SALA 4.1.2'),
        ('SALA 4.1.3','SALA 4.1.3'),
        ('SALA 4.1.4', 'SALA 4.1.4'),
        ('SALA 4.1.5', 'SALA 4.1.5'),
        ('SALA 4.1.6', 'SALA 4.1.6'),
        ('SALA 4.1.7', 'SALA 4.1.7'),
        ('SALA 4.1.8', 'SALA 4.1.8'),
        ('SALA 5.4.1','SALA 5.4.1'),
        ('SALA 5.4.2','SALA 5.4.2'),
        ('SALA 5.4.3','SALA 5.4.3'),
        ('SALA 5.4.4','SALA 5.4.4'),
        ('SALA 5.4.5','SALA 5.4.5'),
        ('SALA 5.4.6','SALA 5.4.6'),
        ('SALA 5.4.7','SALA 5.4.7'),
        ('SALA 5.4.8','SALA 5.4.8'),
        ('SALA 5.4.9','SALA 5.4.9'),
        ('SALA 5.4.10','SALA 5.4.10'),
        ('SALA 5.4.11','SALA 5.4.11'),
        ('SALA 5.4.12','SALA 5.4.12'),
        ('SALA 5.4.13','SALA 5.4.12'),
        ('SALA 5.4.14','SALA 5.4.14'),
        ('SALA 5.4.15','SALA 5.4.15'),
        ('ASSISTÊNCIA TÉCNICA','ASSISTÊNCIA TÉCNICA'),
        ('DEMANDA CORPORATIVA','DEMANDA CORPORATIVA'),
]



from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords



class Estoque(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    retirada = models.IntegerField(default=0)
    estoque = models.IntegerField()
    data_estoque = models.DateTimeField(default=timezone.now)
    sala_laboratorio = models.CharField(max_length=50, choices=SALA_CHOICES,blank=True)
    foto = models.ImageField(upload_to='fotos/', default='caminho_para_a_imagem.jpg')
    history = HistoricalRecords()
    adicao = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.nome}'

    def save(self, *args, **kwargs):
         # Subtrai o valor de retirada do estoque
         self.estoque -= self.retirada
         super().save(*args, **kwargs)

    def realizar_retirada(self):
        if self.retirada > 0:
            self.estoque -= self.retirada
            self.save()  # Salva o objeto após subtrair a retirada do estoque
            self.retirada = 0  # Reseta o valor de retirada após a operação
            super().save()  # Salva novamente para refletir o valor de retirada zerado   

class EstoqueAT(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    retirada = models.IntegerField(default=0)
    estoque = models.IntegerField()
    data_estoque = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(upload_to='fotos/', default='caminho_para_a_imagem.jpg')
    history = HistoricalRecords()
    adicao = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.nome}'

    def save(self, *args, **kwargs):
         # Subtrai o valor de retirada do estoque
         self.estoque -= self.retirada
         super().save(*args, **kwargs)

    def realizar_retirada(self):
        if self.retirada > 0:
            self.estoque -= self.retirada
            self.save()  # Salva o objeto após subtrair a retirada do estoque
            self.retirada = 0  # Reseta o valor de retirada após a operação
            super().save()  # Salva novamente para refletir o valor de retirada zerado
    class Meta:
        permissions = [
            ("change_estoque_at", "Pode editar Estoque AT"),
        ]

class EstoqueAlmo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    retirada = models.IntegerField(default=0)
    estoque = models.IntegerField()
    endereco = models.CharField(max_length=255, default="Sem registro de localização")
    data_estoque = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(upload_to='fotos/', default='caminho_para_a_imagem.jpg')
    history = HistoricalRecords()
    adicao = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.nome}'

    def save(self, *args, **kwargs):
         # Subtrai o valor de retirada do estoque
         self.estoque -= self.retirada
         super().save(*args, **kwargs)

    def realizar_retirada(self):
        if self.retirada > 0:
            self.estoque -= self.retirada
            self.save()  # Salva o objeto após subtrair a retirada do estoque
            self.retirada = 0  # Reseta o valor de retirada após a operação
            super().save()  # Salva novamente para refletir o valor de retirada zerado

    class Meta:
        permissions = [
            ("change_estoque_almo", "Pode editar Estoque Almo"),
        ]


class Demanda(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=253)
    data = models.DateTimeField(default=timezone.now)
    sala_laboratorio = models.CharField(max_length=50, choices=SALA_CHOICES,blank=True)
    foto = models.ImageField(upload_to='fotos/', default='caminho_para_a_imagem.jpg')
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.titulo}'

class EstoqueHistorico(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    quantidade_adicionada = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    @property
    def nome(self):
        return self.estoque.nome  # Adiciona um método para pegar o nome do estoque
class EstoqueHistoricoAT(models.Model):
    estoque = models.ForeignKey(EstoqueAT, on_delete=models.CASCADE)
    quantidade_adicionada = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    @property
    def nome(self):
        return self.estoque.nome  # Adiciona um método para pegar o nome do estoque
class EstoqueHistoricoAlmo(models.Model):
    estoque = models.ForeignKey(EstoqueAlmo, on_delete=models.CASCADE)
    quantidade_adicionada = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    @property
    def nome(self):
        return self.estoque.nome  # Adiciona um método para pegar o nome do estoque