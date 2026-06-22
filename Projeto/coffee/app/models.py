from django.db import models
from django.contrib.auth.models import User

class Produtor(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
class ProducaoCafe(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    produtor = models.ForeignKey(
        Produtor,
        on_delete=models.CASCADE
    )

    terreno = models.FloatField()
    pes = models.IntegerField()
    producao_por_pe = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"{self.produtor} - {self.total} kg"