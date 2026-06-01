from django.db import models
from django.contrib.auth.models import User

class ProducaoCafe(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    terreno = models.FloatField()
    pes = models.IntegerField()
    producao_por_pe = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"{self.usuario} - {self.total} kg"