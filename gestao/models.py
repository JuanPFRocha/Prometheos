from django.db import models
from django.core.validators import RegexValidator

class Estatus(models.TextChoices):
    LIVRE = "LIVRE"
    INDISPONIVEL = "INDISPONIVEL"

class Equipe(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.IntegerField()
    estatus = models.CharField(choices=Estatus, default=Estatus.LIVRE)
    id_comandante = models.ForeignKey("usuario.Bombeiro", on_delete=models.PROTECT)
    def __str__(self):
                return f"ID: {self.id}"
    

class Guarnicao(models.Model):
    num_regex = RegexValidator(
        regex=r'^\d+$',
        message='Digite o CEP',
        code='invalid_digits'      
    )

    id = models.IntegerField(primary_key=True)
    codigo = models.IntegerField()
    nome = models.CharField(max_length=50)
    cep = models.CharField(max_length=8, validators=[num_regex])
    def __str__(self):
                return f"ID: {self.id}"
    
