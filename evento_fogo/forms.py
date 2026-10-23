from django import forms
from .models import *

class EventoFogoForm(forms.ModelForm):
    class Meta:
        model = EventoFogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventoFogoForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['placeholder'] = 'Número de segurança'
        self.fields['data_registro'].widget.attrs['placeholder'] = 'Ex: 26/10/2005 12:00'
        self.fields['descricao'].widget.attrs['placeholder'] = 'Preencha com detalhes do evento'
        self.fields['latitude'].widget.attrs['placeholder'] = 'Ex: 12.12312'
        self.fields['longitude'].widget.attrs['placeholder'] = 'Ex: 32.13232'
        self.fields['codigo'].widget.attrs['placeholder'] = 'Código de identificação'