from django.urls import path
from gestao import views
from evento_fogo import views as fogoViews

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('eventoFogo/',fogoViews.eventoFogo, name='eventoFogo'),
    path('eventoFogo/deletar/<id>', fogoViews.excluirEventoFogo, name='excluirEventoFogo'),
    path('eventoFogo/adicionar', fogoViews.adicionaEventofogo, name='adicionaEventoFogo'),
    path('eventoFogo/editar/<id>', fogoViews.editaEventoFogo, name='editaEventoFogo')
]