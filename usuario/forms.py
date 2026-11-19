from django import forms
from django.db.models import Q
from .models import *


class BombeiroForm(forms.ModelForm):
    class Meta:
        model = Bombeiro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        campoUser = self.fields['id_usuario']
        campoUser.widget = forms.Select(attrs={"class": "form-select"})
        campoUser.empty_label = "Selecione um Usuário do sistema"
        campoUser.label_from_instance = lambda e: e.nome
        userDisponivel = Q(bombeiro__isnull=True)
        if self.instance.pk:
            userDisponivel |= Q(pk=self.instance.id_usuario_id)
        campoUser.queryset = Usuario.objects.filter(userDisponivel).order_by("nome")

        campoEscala = self.fields['id_escala']
        campoEscala.widget = forms.SelectMultiple(attrs={"class": "form-select", "size": 5})
        campoEscala.label_from_instance = (
            lambda e: f"{e.id_guarnicao} · {e.data_inicio:%d/%m/%Y} a {e.data_fim:%d/%m/%Y}"
        )
        campoEscala.queryset = Escala.objects.select_related("id_guarnicao").order_by("-data_inicio")

class BombeiroEdicaoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome do bombeiro'
        self.fields['email'].widget.attrs['placeholder'] = 'bombeiro@email.com'