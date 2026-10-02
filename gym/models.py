from django.db import models


class Ejercicio(models.Model):
    DIFICULTAD_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=200)
    grupo_muscular = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    dificultad = models.CharField(
        max_length=20, choices=DIFICULTAD_CHOICES, blank=True, default=''
    )
    imagen_url = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
