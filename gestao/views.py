from django.db import transaction
from collections import defaultdict
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

    noticias = NoticiaFogo.objects.filter(id_evento_fogo__isnull=False).order_by("-id")
    noticias_por_evento = defaultdict(list)
    for noticia in noticias:
        noticias_por_evento[noticia.id_evento_fogo].append(noticia)


    contexto = {
        "qtdEventoFogo" : qtd_evento_fogo,
        "qtdOrdemServico" : qtd_ordem_servico,
        "qtdDespacho" : qtd_despacho,
        "qtdBombeiro" : qtd_bombeiro,
        "noticias_por_evento": dict(noticias_por_evento),
    }

    return render(request, 'gestao/dashboard.html', contexto)

def adicionaNoticia(request):
    form = NoticiaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('eventoFogo')
    return render(request, 'gestao/adicionaNoticia.html', {"form" : form})

def excluirNoticia(request, id=None):
    noticia = NoticiaFogo.objects.get(pk=id)
    noticia.delete()
    return redirect('dashboard')

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
    form = GuarnicaoForm(request.POST or None, instance=guarnicao)
    if form.is_valid():
        form.save()
        return redirect('guarnicao')

    return render(request, 'gestao/editaGuarnicao.html', {"form" : form})

def equipes(request):
    equipes = Equipe.objects.all().order_by("codigo")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "estatus" : request.GET.get("estatus", ""),
        "comandante" : request.GET.get("comandante", "").strip()
    }

    if filtros["codigo"]:
        equipes = equipes.filter(codigo=filtros["codigo"])
    if filtros['estatus']:
        equipes = equipes.filter(estatus=filtros["estatus"])
    if filtros["comandante"]:
        equipes = equipes.filter(id_comandante__id_usuario__nome__icontains=filtros["comandante"])

    contexto = {
        "equipes" : equipes,
        "filtros" : filtros,
        "estatus_opcoes" : Equipe._meta.get_field("estatus").choices
    }

    return render(request, 'gestao/equipes.html', contexto)

def excluirEquipe(request, id=None):
    equipe = Equipe.objects.get(pk=id)
    with transaction.atomic():
        for b in Bombeiro.objects.filter(id_equipe=equipe):
            b.id_equipe = None
            b.save()  
        equipe.delete()
    return redirect('equipe')

def config(request):
    return render(request, 'gestao/config.html')

def listarBombeiros(request, id=None):
    equipe = Equipe.objects.get(pk=id)

    bombeiros = (
        Bombeiro.objects.filter(id_equipe=equipe)
        .select_related("id_usuario")
        .prefetch_related("id_escala")
        .order_by("id_usuario__nome")
    )

    return render(request, 'gestao/listaBombeiro.html', {"equipe" : equipe, "bombeiros" : bombeiros})
