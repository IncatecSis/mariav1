from django.db import models
from apps.principal.modelos.academico.programa import *
from apps.principal.modelos.parametros.sedes import Sedes




class TiposModulo(models.Model):
    id_tipo_modulo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipos_modulo'

class Modulos(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    nombre_modulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    id_tipo_modulo = models.ForeignKey(TiposModulo, on_delete=models.CASCADE, db_column='id_tipo_modulo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modulos'
        ordering = ['id_modulo']

    def save(self, *args, **kwargs):
        if self.nombre_modulo:
            self.nombre_modulo = self.nombre_modulo.upper()
        if self.descripcion:
            self.descripcion= self.descripcion.upper()
        super(Modulos, self).save(*args, **kwargs)

class SemestresPensum(models.Model):
    id_semestre = models.AutoField(primary_key=True)
    id_pensum = models.ForeignKey(Pensum, on_delete=models.CASCADE, db_column='id_pensum')
    numero_semestre = models.IntegerField()
    nombre_semestre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'semestres_pensum'