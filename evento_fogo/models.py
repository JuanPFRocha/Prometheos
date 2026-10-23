from django.db import models
from gestao.models import Equipe

class Estatus(models.TextChoices):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    ANDAMENTO = "ANDAMENTO"

class EventoFogo(models.Model):
    codigo = models.IntegerField()
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

    def __str__(self):
            return f"ID: {self.id}"

class OrdemServico(models.Model):
    id = models.IntegerField(primary_key=True)
    id_evento_fogo = models.OneToOneField(EventoFogo, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField()
    estatus = models.CharField(choices=Estatus, default=Estatus.ABERTA)

    @property
    def codigoFogo(self):
           if self.id_evento_fogo:
                  return self.id_evento_fogo.codigo
           return None

    def __str__(self):
                return f"ID: {self.id} | EVENTO: {self.codigoFogo}"
    

class RelatorioOcorrencia(models.Model):
    id = models.IntegerField(primary_key=True)
    id_os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    data = models.DateTimeField()
    descricao = models.CharField(max_length=200)
    def __str__(self):
                return f"ID: {self.id}"
    

class Despacho(models.Model):
    id = models.IntegerField(primary_key=True)
    id_ro = models.ForeignKey(RelatorioOcorrencia, on_delete=models.CASCADE)
    id_equipe = models.OneToOneField(Equipe, on_delete=models.PROTECT)
    data = models.DateTimeField()
    estatus = models.CharField(choices=Estatus, default=Estatus.ANDAMENTO)
    def __str__(self):
                return f"ID: {self.id}"
    

