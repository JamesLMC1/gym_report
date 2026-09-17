from django.db import models


class Set(models.Model):
    nombre_ejercicio = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    repeticiones = models.IntegerField()
    tiempo_descanso = models.IntegerField()
    def __str__(self):
        return f"{self.nombre_ejercicio} - {self.peso}kg x {self.repeticiones}"
