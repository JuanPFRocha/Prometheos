from django.db import models
from gestao.models import Equipe

class Estatus(models.TextChoices):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    ANDAMENTO = "ANDAMENTO"

class EventoFogo(models.Model):
    id = models.IntegerField(primary_key=True)
    data_registro = models.DateTimeField()
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    class estatus(models.TextChoices):
        ABERTO = "ABERTO"
        COMBATE = "COMBATE"
        ENCERRADO = "ENCERRADO"
    estatus = models.CharField(choices=estatus, default=estatus.ABERTO)
    descricao = models.CharField(max_length=200)

class OrdemServico(models.Model):
    id = models.IntegerField(primary_key=True)
    data_emissao = models.DateField()
    estatus = models.CharField(choices=Estatus, default=Estatus.ABERTA)

class RelatorioOcorrencia(models.Model):
    id = models.IntegerField(primary_key=True)
    id_os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    data = models.DateTimeField()
    descricao = models.CharField(max_length=200)

class Despacho(models.Model):
    id = models.IntegerField(primary_key=True)
    id_ro = models.ForeignKey(RelatorioOcorrencia, on_delete=models.CASCADE)
    id_equipe = models.OneToOneField(Equipe, on_delete=models.PROTECT)
    data = models.DateTimeField()
    estatus = models.CharField(choices=Estatus, default=Estatus.ANDAMENTO)

