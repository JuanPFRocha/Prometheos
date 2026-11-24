from django.shortcuts import render, redirect
from usuario.models import *
from .forms import *

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
