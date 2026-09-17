from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    estatura = models.IntegerField(help_text="En centímetros")

    def __str__(self):
        return f"{self.nombre} — {self.peso}kg — {self.estatura}cm"
