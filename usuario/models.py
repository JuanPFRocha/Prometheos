from datetime import timezone

from django.db import models
from gestao.models import Equipe, Guarnicao
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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
    def __str__(self):
                return self.nome
    

class Escala(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.IntegerField()
    id_guarnicao = models.ForeignKey(Guarnicao, on_delete=models.PROTECT)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    estatus = models.CharField(choices=Estatus.choices, default=Estatus.LIVRE)
    def __str__(self):
                return f"{self.data_inicio:%d/%m/%Y} a {self.data_fim:%d/%m/%Y}"

class Bombeiro(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    id_equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT, blank=True, null=True)
    id_escala = models.ForeignKey(Escala, on_delete=models.SET_NULL, null=True, blank=True, related_name="bombeiros")
    matricula = models.IntegerField(primary_key=True)
    estatus = models.CharField(choices=Estatus.choices, default=Estatus.LIVRE)
    def __str__(self):
                return self.id_usuario.nome

    def save(self, *args, **kwargs):
        self.estatus = Estatus.LIVRE if self.id_escala_id is None else Estatus.INDISPONIVEL
        super().save(*args, **kwargs)



# ATUALIZA O ESTATUS DO BOMBEIRO QUANDO APAGA UMA ESCALA
@receiver(pre_delete, sender=Escala)
def libera_bombeiros(sender, instance, **kwargs):
    Bombeiro.objects.filter(id_escala=instance).update(estatus=Estatus.LIVRE)

    
    


    


