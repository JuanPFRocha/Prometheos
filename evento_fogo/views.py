from django.shortcuts import render, redirect
from evento_fogo.models import * 
from .forms import *

def eventoFogo(request):
    eventos = EventoFogo.objects.all().order_by("-data_registro")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "descricao" : request.GET.get("descricao", ""),
        "estatus" : request.GET.get("estatus", ""),
        "data_inicio" : request.GET.get("data_inicio", ""),
        "data_fim" : request.GET.get("data_fim", ""),
        "latitude" : request.GET.get("latitude", ""),
        "longitude" : request.GET.get("longitude", "")
    }
    if filtros["codigo"]:
        eventos = eventos.filter(codigo=filtros["codigo"])
    if filtros["descricao"]:
        eventos = eventos.filter(descricao__icontains=filtros["descricao"])
    if filtros["estatus"]:
        eventos = eventos.filter(estatus=filtros["estatus"])
    if filtros["data_inicio"]:
        eventos = eventos.filter(data_registro__date__gte=filtros["data_inicio"])
    if filtros["data_fim"]:
        eventos = eventos.filter(data_registro__date__lte=filtros["data_fim"])

    for campo in ("latitude", "longitude"):
        if filtros[campo]:
            try:
                valor = float(filtros[campo].replace(",", "."))
            except ValueError:
                continue  # ignora valor inválido
            eventos = eventos.filter(**{
                f"{campo}__gte": valor - 0.03,
                f"{campo}__lte": valor + 0.03,
            })

    contexto = {
        "eventos" : eventos,
        "filtros" : filtros,
        "estatus_opcoes" : EventoFogo._meta.get_field("estatus").choices
    }

    return render(request, "evento_fogo/eventoFogo.html", contexto)

def excluirEventoFogo(request, id=None):
    evento = EventoFogo.objects.get(pk=id)
    evento.delete()
    return redirect('eventoFogo')


def adicionaEventofogo(request):
    form = EventoFogoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('eventoFogo')

    dicionario = {
        "form" : form
    }

    return render(request, 'evento_fogo/adicionaEventoFogo.html', dicionario)

def editaEventoFogo(request, id=None):
    evento = EventoFogo.objects.get(pk = id)
    form = EventoFogoForm(request.POST or None, instance=evento)
    if form.is_valid():
        form.save()
        return redirect('eventoFogo')

    dicionario = {
        "form" : form
    }

    return render(request, 'evento_fogo/editaEventoFogo.html', dicionario)


def ordemServico(request):
    return render(request, 'evento_fogo/ordemServico.html')
