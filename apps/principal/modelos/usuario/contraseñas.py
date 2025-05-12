from django.db import models
from apps.principal.modelos.usuario.Usuarios import *


class Credenciales(models.Model):
    id_credencial = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'credenciales'

    def __str__(self):
        return self.username