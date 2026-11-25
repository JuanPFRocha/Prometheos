from django import forms
from django.db.models import Q
from .models import *
from evento_fogo.models import Despacho, RelatorioOcorrencia


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
    nome = forms.CharField(max_length=150, label="Nome")
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = Bombeiro
        fields = ['id_escala']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome do bombeiro'
        self.fields['email'].widget.attrs['placeholder'] = 'bombeiro@email.com'

        campo = self.fields['id_escala']
        campo.widget = forms.Select(attrs={"class": "form-select"})
        campo.empty_label = "Sem escala"
        campo.label_from_instance = lambda e: f"{e.codigo}"
        campo.queryset = Escala.objects.select_related("id_guarnicao").order_by("-data_inicio")

        if self.instance.pk:
            self.fields['nome'].initial = self.instance.id_usuario.nome
            self.fields['email'].initial = self.instance.id_usuario.email

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.id_usuario_id)
        if qs.exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        bombeiro = super().save(commit=False)
        usuario = bombeiro.id_usuario
        usuario.nome = self.cleaned_data['nome']
        usuario.email = self.cleaned_data['email']

        if commit:
            usuario.save()
            bombeiro.save()  
        return bombeiro


class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['placeholder'] = 'Número de segurança'
        self.fields['codigo'].widget.attrs['placeholder'] = 'Código de acesso'

        campo = self.fields['id_guarnicao']
        campo.widget = forms.Select(attrs={"class": "form-select"})
        campo.empty_label = "Selecione uma guarnição"
        campo.label_from_instance = lambda e: f"{e.nome}"
        campo.queryset = Guarnicao.objects.order_by("codigo")

        if self.instance and self.instance.pk:
            self.fields['id'].disabled = True

# ----------------------------  Seção para o despacho Automático ----------------------------------

class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = ['id', 'id_ro', 'estatus', 'data']
        widgets = {
            "data" : forms.DateTimeInput(
                attrs={"type" : "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'].widget.attrs['placeholder'] = 'Ex: 123'
        campoRO = self.fields['id_ro']
        campoRO.empty_label = 'Selecione o RO relacionado'
        campoRO.label_from_instance = lambda ro: (
            f"{ro.id} · {ro.data:%d/%m/%Y}"
        )
        campoRO.queryset = (
            RelatorioOcorrencia.objects.order_by("-data")
        )

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['id', 'codigo', 'id_comandante', 'estatus']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'].widget.attrs['placeholder'] = 'Ex: 123'
        self.fields['codigo'].widget.attrs['placeholder'] = 'Ex: 2026001'
        campoComandante = self.fields['id_comandante']
        campoComandante.empty_label = 'Selecione o Comandante'
        campoComandante.label_from_instance = lambda co: (
            f"{co.id_usuario.nome}"
        )
        campoComandante.queryset = (
            Bombeiro.objects.filter(id_usuario__perfil="COMANDO")
            .select_related("id_usuario").order_by("-id_usuario__nome")
        )
        

class CriteriosEquipeForm(forms.Form):
    qtd_bombeiros = forms.IntegerField(min_value=1, label='Quantidade de bombeiros')
    profi = forms.MultipleChoiceField(choices=Proficiencia.choices, required=False,
                                       widget=forms.SelectMultiple, label='Proficiências')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['qtd_bombeiros'].widget.attrs['placeholder'] = 'Ex: 2'

    def clean(self):
        dados = super().clean()
        qtd = dados.get("qtd_bombeiros")
        profs = dados.get("proficiencias", [])
        if qtd and len(profs) > qtd:
            self.add_error(
                "proficiencias",
                f"Selecione no máximo {qtd} proficiência(s), uma por bombeiro.",
            )
        return dados



