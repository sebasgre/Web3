from django.db import models

from reuniones.models.Usuario import Usuario


# Create your models here.
class Reunion(models.Model):
    nombre_reunion = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField()
    dueño = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reuniones'
    )
    asistentes = models.ManyToManyField(
        Usuario,
        through='Asistente',
        related_name='asistencias'
    )

    def __str__(self):
        return self.nombre_reunion
