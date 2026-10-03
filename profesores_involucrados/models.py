from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='profesores/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
