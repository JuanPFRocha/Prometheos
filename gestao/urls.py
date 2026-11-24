from django.urls import path
from gestao import views
from evento_fogo import views as fogoViews
from usuario import views as userViews

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('guarnicoes', views.guarnicao, name='guarnicao'),
    path('guarnicoes/deletar/<id>', views.excluirGuarnicao, name='excluirGuarnicao'),
    path('guarnicoes/adicionar', views.adicionaGuarnicao, name='adicionaGuarnicao'),
    path('gaurnicoes/editar/<id>', views.editaGuarnicao, name='editaGuarnicao'),

    path('equipes', views.equipes, name='equipe'),
    path('equipes/listaBombeiro/<id>', views.listarBombeiros, name='listaBombeiro'),
    path('equipes/deletar/<id>', views.excluirEquipe, name='excluirEquipe'),

    path('eventoFogo/',fogoViews.eventoFogo, name='eventoFogo'),
    path('eventoFogo/deletar/<id>', fogoViews.excluirEventoFogo, name='excluirEventoFogo'),
    path('eventoFogo/adicionar', fogoViews.adicionaEventofogo, name='adicionaEventoFogo'),
    path('eventoFogo/editar/<id>', fogoViews.editaEventoFogo, name='editaEventoFogo'),

    path('despacho', fogoViews.despacho, name='despacho'),
    path('despacho/criar', userViews.criaDespacho, name='criaDespacho'),

    path('ordemServico/', fogoViews.ordemServico, name='ordemServico'),
    path('ordemServico/adicionar', fogoViews.adicionaOrdemServico, name='adicionaOrdemServico'),
    path('ordemServico/deletar/<id>', fogoViews.excluirOrdemServico, name='excluirOrdemServico'),
    path('ordemServico/editar/<id>', fogoViews.editaOrdemServico, name='editaOrdemServico'),

    path('relatorioOcorrencia/', fogoViews.relatorioOcorrencia, name='relatorioOcorrencia'),
    path('relatorioOcorrencia/adicionar', fogoViews.adicionaRelatorioOcorrencia, name='adicionaRelatorioOcorrencia'),
    path('relatorioOcorrencia/deletar/<id>', fogoViews.excluiRelatorioOcorrencia, name='excluirRelatorioOcorrencia'),
    path('relatorioOcorrencia/editar/<id>', fogoViews.editaRelatorioOcorrencia, name='editaRelatorioOcorrencia'),

    path('bombeiros', userViews.bombeiro, name='bombeiro'),
    path('bombeiros/editar/<matricula>', userViews.editaBombeiro, name='editaBombeiro'),

    path('escala', userViews.escala, name='escala'),
    path('escala/deletar/<id>', userViews.excluiEscala, name='excluirEscala'),
    path('escala/adicionar', userViews.adicionaEscala, name='adicionaEscala'),
    path('escala/editar/<id>', userViews.editaEscala, name='editaEscala'),
    
]