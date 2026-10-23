from django import forms
from django.db.models import Q
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

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['placeholder'] = 'Número de segurança'
        self.fields['data_emissao'].widget.attrs['placeholder'] = 'Ex: 26/10/2005 12:00'
        campo = self.fields['id_evento_fogo']

        campo.widget = forms.Select(attrs={"class" : "form-select"})
        campo.empty_label = "Selecione um evento de fogo disponível"
        campo.label_from_instance = (
            lambda e: f"{e.codigo}"
        )

        disponivel = Q(ordemservico__isnull=True)
        if self.instance.pk: 
            disponivel |= Q(pk=self.instance.id_evento_fogo_id)

        campo.queryset = EventoFogo.objects.filter(disponivel).order_by("-data_registro")