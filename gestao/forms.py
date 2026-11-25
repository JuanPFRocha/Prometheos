from django import forms
from .models import *
from evento_fogo.models import EventoFogo

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
        if self.instance and self.instance.pk:
            self.fields['id'].disabled = True

class NoticiaForm(forms.ModelForm):
    class Meta:
          model = NoticiaFogo
          fields = '__all__'
    def __init__(self, *args, **kwargs):
            super(NoticiaForm, self).__init__(*args, **kwargs)
            self.fields['id'].widget.attrs['placeholder'] = 'Número de segurança'
            self.fields['titulo'].widget.attrs['placeholder'] = 'Digite o título da notícia'
            self.fields['descricao'].widget.attrs['placeholder'] = 'Digite o conteúdo da notícia'

            campoEventoFogo = self.fields['id_evento_fogo']
            campoEventoFogo.empty_label = 'Escolha o evento de fogo'
            campoEventoFogo.label_from_instance = lambda ef: (
                 f"{ef.codigo}"
            )
            campoEventoFogo.queryset = (
                 EventoFogo.objects.order_by("-id")
            )
            if self.instance and self.instance.pk:
                self.fields['id'].disabled = True

