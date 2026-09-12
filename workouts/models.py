from django.db import models


class Workout(models.Model):
    # Fecha del entrenamiento
    fecha = models.DateField()

    # Duración total en minutos
    duracion = models.IntegerField()

    # Notas adicionales del entrenamiento
    notas = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Entrenamiento del {self.fecha} — {self.duracion} min"
