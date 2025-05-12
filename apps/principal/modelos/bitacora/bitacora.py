from django.db import models



class Auditoria(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    tabla_modificada = models.CharField(max_length=100, blank=True, null=True)
    accion = models.CharField(max_length=20, blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    datos_previos = models.JSONField(blank=True, null=True)
    datos_nuevos = models.JSONField(blank=True, null=True)
    sentencia_sql = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'