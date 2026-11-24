from django.db import transaction
from django.shortcuts import render, redirect
from usuario.models import *
from .forms import *
from django.core.exceptions import ValidationError

def bombeiro(request):
    bombeiros = Bombeiro.objects.all().order_by("-matricula")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "nome" : request.GET.get("nome", ""),
        "email" : request.GET.get("email", ""),
        "estatus" : request.GET.get("estatus", "")
    }

    if filtros["codigo"]:
        bombeiros = bombeiros.filter(matricula=filtros["codigo"])
    if filtros["nome"]:
        bombeiros = bombeiros.filter(id_usuario__nome=filtros["nome"])
    if filtros["email"]:
        bombeiros = bombeiros.filter(id_usuario__email=filtros["email"])
    if filtros["estatus"]:
        bombeiros = bombeiros.filter(estatus=filtros["estatus"])

    contexto = {
        "bombeiros" : bombeiros,
        "filtros" : filtros,
        "estatus_opcoes" : Bombeiro._meta.get_field("estatus").choices
    }


    return render(request, 'usuarios/bombeiros.html', contexto)
def editaBombeiro(request, matricula=None):
    bombeiro = Bombeiro.objects.get(pk=matricula)
    form = BombeiroEdicaoForm(request.POST or None, instance=bombeiro)

    if form.is_valid():
        form.save()
        return redirect('bombeiro')

    return render(request, 'usuarios/editaBombeiro.html', {"form" : form})

def escala(request):
    escalas = Escala.objects.all().order_by("-data_inicio")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "id_guarnicao" : request.GET.get("id_guarnicao", ""),
        "data_inicio" : request.GET.get("data_inicio", ""),
        "data_fim" : request.GET.get("data_fim"),
        "estatus" : request.GET.get("estatus", "")
    }

    if filtros["codigo"]:
        escalas = escalas.filter(codigo=filtros["codigo"])
    if filtros["id_guarnicao"]:
        escalas = escalas.filter(id_guarnicao__nome__icontains=filtros["id_guarnicao"])
    if filtros["data_inicio"]:
        escalas = escalas.filter(data_inicio__date__gte=filtros["data_inicio"])
    if filtros["data_fim"]:
        escalas = escalas.filter(data_fim__date__lte=filtros["data_fim"])
    if filtros["estatus"]:
        escalas = escalas.filter(estatus=filtros["estatus"])

    contexto = {
        "escalas" : escalas,
        "filtros" : filtros,
        "estatus_opcoes" : Escala._meta.get_field("estatus").choices
    }
    return render(request, 'usuarios/escalas.html', contexto)

def excluiEscala(request, id=None):
    escala =  Escala.objects.get(pk=id)
    escala.delete()
    return redirect('escala')

def adicionaEscala(request):
    form = EscalaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('escala')
    
    return render(request, 'usuarios/adicionaEscala.html', {"form" : form})

def editaEscala(request, id=None):
    escala = Escala.objects.get(pk=id)
    form = EscalaForm(request.POST or None, instance=escala)

    if form.is_valid():
        form.save()
        return redirect('escala')

    return render(request, 'usuarios/editaEscala.html', {"form" : form})

def escolherBombeiros(qtd, profi, excluir):
    bombLivres = Bombeiro.objects.filter(estatus=Estatus.LIVRE).exclude(pk__in=excluir)
    escolhidos = []

    for p in profi:
        candidato = (
            bombLivres.filter(proficiencia=p).exclude(pk__in=[b.pk for b in escolhidos]).first()
        )

        if candidato is None:
            raise ValidationError(f"Não há bombeiro livre com a proficiência {p}.")
        escolhidos.append(candidato)

    sobra = qtd - len(escolhidos)

    if sobra > 0:
        livres = bombLivres.exclude(pk__in=[b.pk for b in escolhidos])[:sobra]
        escolhidos.extend(livres)

    if len(escolhidos) < qtd:
        raise ValidationError("Não há bombeiros livres suficientes para a quantidade pedida.")


    return escolhidos

def criaDespacho(request):
    despachoForm = DespachoForm(request.POST or None, prefix='despacho')
    equipeForm = EquipeForm(request.POST or None, prefix='equipe')
    criterios = CriteriosEquipeForm(request.POST or None, prefix='criterios')

    valida = [
        despachoForm.is_valid(),
        equipeForm.is_valid(),
        criterios.is_valid(),
    ]

    if all(valida):
        comandante = equipeForm.cleaned_data["id_comandante"]
        try:
            with transaction.atomic():
                bombeiros = escolherBombeiros(
                    criterios.cleaned_data["qtd_bombeiros"],
                    criterios.cleaned_data["profi"],
                    excluir=[comandante.pk]
                )

                equipe = equipeForm.save()

                Bombeiro.objects.filter(pk__in=[b.pk for b in bombeiros]).update(
                    id_equipe=equipe,
                    estatus=Estatus.INDISPONIVEL,
                )
                despacho = despachoForm.save(commit=False)
                despacho.id_equipe = equipe
                despacho.save()
        except ValidationError as e:
            criterios.add_error(None, e)
        else:
            return redirect("relatorioOcorrencia")


    contexto = {
        "form_despacho" : despachoForm,
        "form_equipe" : equipeForm,
        "form_criterios" : criterios
    }
    return render(request, 'usuarios/criaDespacho.html', contexto)


