from django.db import models

class Proficiencia(models.TextChoices):
    RESGATE_EM_ESPACO_CONFINADO = "Resgate em espaço confinado"
    OPERACAO_DE_DRONES = "Operação de drones"
    ATENDIMENTO_PRE_HOSPITALAR = "Atendimento pré-hospitalar"
    SALVAMENTO_EM_ALTURA = "Salvamento em altura"
    RESGATE_VEICULAR = "Resgate veicular"
    SALVAMENTO_AQUATICO = "Salvamento aquático"
    PRODUTOS_PERIGOSOS = "Produtos perigosos"
    BUSCA_EM_ESTRUTURAS_COLAPSADAS = "Busca em estruturas colapsadas"
    NAVEGACAO_E_SOBREVIVENCIA_EM_MATA = "Navegação e sobrevivência em mata"
    OPERACOES_AEREAS = "Operações aéreas"
    RESGATE_COM_ANIMAL = "Resgate com animal"
    COMBATE_A_ENCHENTES = "Combate a enchentes"