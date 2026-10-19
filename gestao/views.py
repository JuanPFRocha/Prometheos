from django.http import request
from django.shortcuts import render
from evento_fogo.models import EventoFogo, OrdemServico, Despacho
from usuario.models import Bombeiro

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