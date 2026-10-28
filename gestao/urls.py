from django.urls import path
from gestao import views
from evento_fogo import views as fogoViews

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('eventoFogo/',fogoViews.eventoFogo, name='eventoFogo'),
    path('eventoFogo/deletar/<id>', fogoViews.excluirEventoFogo, name='excluirEventoFogo'),
    path('eventoFogo/adicionar', fogoViews.adicionaEventofogo, name='adicionaEventoFogo'),
    path('eventoFogo/editar/<id>', fogoViews.editaEventoFogo, name='editaEventoFogo'),
    path('ordemServico/', fogoViews.ordemServico, name='ordemServico'),
    path('ordemServico/adicionar', fogoViews.adicionaOrdemServico, name='adicionaOrdemServico'),
    path('ordemServico/deletar/<id>', fogoViews.excluirOrdemServico, name='excluirOrdemServico'),
    path('ordemServico/editar/<id>', fogoViews.editaOrdemServico, name='editaOrdemServico'),
    path('relatorioOcorrencia/', fogoViews.relatorioOcorrencia, name='relatorioOcorrencia'),
    path('relatorioOcorrencia/adicionar', fogoViews.adicionaRelatorioOcorrencia, name='adicionaRelatorioOcorrencia'),
    path('relatorioOcorrencia/deletar/<id>', fogoViews.excluiRelatorioOcorrencia, name='excluirRelatorioOcorrencia'),
    path('relatorioOcorrencia/editar/<id>', fogoViews.editaRelatorioOcorrencia, name='editaRelatorioOcorrencia')
]