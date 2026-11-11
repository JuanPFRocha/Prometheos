from django import forms
from .models import *

class GuarnicaoForm(forms.ModelForm):
    class Meta:
        model = Guarnicao
        fields = '__all__'

def __init__(self, *args, **kwargs):
        super(GuarnicaoForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['placeholder'] = 'Número de segurança'
        self.fields['codigo'].widget.attrs['placeholder'] = 'Código de identificação'
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome da Guarnição'
        self.fields['cep'].widget.attrs['placeholder'] = 'Ex: 12345678'