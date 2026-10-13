from datetime import timezone

from django.db import models
from gestao.models import Equipe, Guarnicao

class Estatus(models.TextChoices):
    LIVRE = "LIVRE"
    INDISPONIVEL = "INDISPONIVEL"

class Usuario(models.Model):
    class perfil(models.TextChoices):
        ADMIN = "ADMIN"
        SALA_SITUACAO = "SALA_SITUACAO"
        COMANDO = "COMANDO"
        COMBATENTE = "COMBATENTE"
    
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    perfil = models.CharField(choices=perfil.choices)

class Escala(models.Model):
    id = models.IntegerField(primary_key=True)
    id_guarnicao = models.ForeignKey(Guarnicao, on_delete=models.PROTECT)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    estatus = models.CharField(choices=Estatus.choices, default=Estatus.LIVRE)

class Bombeiro(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    id_equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT)
    id_escala = models.ManyToManyField(Escala, related_name="bombeiros")
    matricula = models.IntegerField(primary_key=True)
    estatus = models.CharField(choices=Estatus.choices, default=Estatus.LIVRE)


    


