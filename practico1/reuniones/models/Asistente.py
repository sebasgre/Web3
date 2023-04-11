from django.db import models

from reuniones.models.Reunion import Reunion
from reuniones.models.Usuario import Usuario


class Asistente(models.Model):
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    asistente = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.reunion.nombre_reunion + ' - ' + self.asistente.username
