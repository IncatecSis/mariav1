from django.db import models
from apps.principal.modelos.parametros.sedes import Sedes




class Anios(models.Model):
    id_anio = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    anio_academico = models.IntegerField()
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'anio'