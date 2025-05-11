from django import forms
from .models import EstoqueAlmo, EstoqueAT, Estoque



class AdicionarEstoqueForm(forms.Form):
    quantidade = forms.IntegerField(label='Quantidade a adicionar')

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['nome', 'estoque', 'sala_laboratorio', 'foto']



class EstoqueAlmoForm(forms.ModelForm):
    class Meta:
        model = EstoqueAlmo
        fields = ['nome', 'estoque', 'modelo','tipo','endereco', 'categoria', 'foto']
        labels = {
            'tipo': 'Categoria',
        }

class EstoqueATForm(forms.ModelForm):
    class Meta:
        model = EstoqueAT
        fields = ['nome', 'estoque', 'foto']