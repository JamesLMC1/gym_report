from django.db import models


class Rutina(models.Model):
    NIVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    nivel = models.CharField(
        max_length=20, choices=NIVEL_CHOICES, blank=True, default=''
    )
    duracion_dias = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class RutinaEjercicio(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    rutina = models.ForeignKey(
        Rutina, on_delete=models.CASCADE, related_name='items'
    )
    ejercicio = models.ForeignKey(
        'gym.Ejercicio', on_delete=models.CASCADE, related_name='en_rutinas'
    )
    series = models.IntegerField(null=True, blank=True)
    repeticiones = models.CharField(max_length=50, blank=True, default='')
    descanso_segundos = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.rutina} → {self.ejercicio}'
