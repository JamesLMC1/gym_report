from django.db import models


class Receta(models.Model):
    TIPO_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snack', 'Snack'),
        ('postre', 'Postre'),
    ]

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='almuerzo')
    calorias = models.PositiveIntegerField(default=0)
    proteinas_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbos_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grasas_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    receta = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
