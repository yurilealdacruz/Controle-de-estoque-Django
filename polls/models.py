from django.db import models
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from simple_history.models import HistoricalRecords

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
]


class Estoque(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    retirada = models.IntegerField(default=0)
    estoque = models.IntegerField()
    data_estoque = models.DateTimeField(default=timezone.now)
    sala_laboratorio = models.CharField(max_length=50, choices=SALA_CHOICES,blank=True)
    foto = models.ImageField(blank=True)
    history = HistoricalRecords()

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

