from django.db import models

class Estatus(models.TextChoices):
    LIVRE = "LIVRE"
    INDISPONIVEL = "INDISPONIVEL"

class Equipe(models.Model):
    id = models.IntegerField(primary_key=True)
    estatus = models.CharField(choices=Estatus, default=Estatus.LIVRE)
    id_comandante = models.ForeignKey("usuario.Bombeiro", on_delete=models.PROTECT)

class Guarnicao(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=100)
