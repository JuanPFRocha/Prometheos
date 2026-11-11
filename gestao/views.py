from django.http import request
from django.shortcuts import render, redirect
from evento_fogo.models import EventoFogo, OrdemServico, Despacho
from usuario.models import Bombeiro
from gestao.models import Guarnicao
from .forms import *

def dashboard(request):
    qtd_evento_fogo = EventoFogo.objects.filter(estatus="ABERTO").count()
    qtd_ordem_servico = OrdemServico.objects.filter(estatus="ABERTA").count()
    qtd_despacho = Despacho.objects.filter(estatus="ANDAMENTO").count()
    qtd_bombeiro = Bombeiro.objects.filter(estatus="LIVRE").count()

    contexto = {
        "qtdEventoFogo" : qtd_evento_fogo,
        "qtdOrdemServico" : qtd_ordem_servico,
        "qtdDespacho" : qtd_despacho,
        "qtdBombeiro" : qtd_bombeiro
    }

    return render(request, 'gestao/dashboard.html', contexto)

def guarnicao(request):
    guarnicoes = Guarnicao.objects.all().order_by("codigo")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "nome" : request.GET.get("nome", ""),
        "cep" : request.GET.get("cep", "")
    }

    if filtros["codigo"]:
        guarnicoes = guarnicoes.filter(codigo=filtros["codigo"])

    if filtros["nome"]:
        guarnicoes = guarnicoes.filter(nome__icontains=filtros["nome"])

    if filtros["cep"]:
        guarnicoes = guarnicoes.filter(cep=filtros["cep"])

    contexto = {
        "guarnicoes" : guarnicoes,
        "filtros" : filtros
    }

    return render(request, 'gestao/guarnicoes.html', contexto)

def excluirGuarnicao(request, id=None):
    guarnicao = Guarnicao.objects.get(pk=id)
    guarnicao.delete()
    return redirect('guarnicao')

def adicionaGuarnicao(request):
    form = GuarnicaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('guarnicao')

    return render(request, 'gestao/adicionaGuarnicao.html', {"form" : form})

def editaGuarnicao(request, id=None):
    guarnicao = Guarnicao.objects.get(pk=id)
    form = GuarnicaoForm(request.POST or None, instance=Guarnicao)
    if form.is_valid():
        form.save()
        return redirect('guarnicao')

    return render(request, 'gestao/editaGuarnicao.html', {"form" : form})
