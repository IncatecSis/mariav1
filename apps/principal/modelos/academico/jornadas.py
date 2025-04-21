from django.db import models
from apps.principal.modelos.academico.modulos import Modulos, Semestres




class Jornadas(models.Model):
    id_jornada = models.AutoField(primary_key=True)
    nombre_jornada = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.CharField(max_length=250, null=False, blank=False)
    estado = models.BooleanField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'jornadas'


class ModulosCompetencias(models.Model):
    id_modulo_competencia = models.AutoField(primary_key=True)
    id_modulo = models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='id_modulo')
    id_semestre = models.ForeignKey(Semestres, on_delete=models.CASCADE, db_column='id_semestre')
    intensidad_horas = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'modulos_competencias'