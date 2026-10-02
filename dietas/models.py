from django.db import models


class Comida(models.Model):
    TIPO_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snack', 'Snack'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, blank=True, default=''
    )
    calorias = models.IntegerField(null=True, blank=True)
    proteinas_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    carbos_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    grasas_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    receta = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'
