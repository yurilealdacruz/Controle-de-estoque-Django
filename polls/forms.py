from django import forms

class AdicionarEstoqueForm(forms.Form):
    quantidade = forms.IntegerField(label='Quantidade a adicionar')
