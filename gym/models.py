from django.db import models


class Set(models.Model):
    # Nombre del ejercicio realizado en el gym (ej: "Press de banca", "Sentadilla")
    nombre_ejercicio = models.CharField(max_length=100)

    # Peso utilizado en el ejercicio, en kilogramos (ej: 80.50)
    peso = models.DecimalField(max_digits=6, decimal_places=2)

    # Cantidad de repeticiones completadas en la serie
    repeticiones = models.IntegerField()

    # Tiempo de descanso antes de la siguiente serie, en minutos (ej: 2)
    tiempo_descanso = models.IntegerField()

    # Representación en texto del modelo
    # Se muestra en el admin y en la consola
    # Ejemplo: "Press de banca - 80.00kg x 12"
    def __str__(self):
        return f"{self.nombre_ejercicio} - {self.peso}kg x {self.repeticiones}"
