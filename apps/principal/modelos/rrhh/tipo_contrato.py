from django.db import models
from apps.principal.modelos.usuario.roles import *



class TiposDeContrato(models.Model):
    id_tipo_contrato = models.AutoField(primary_key=True)
    nombre_tipo_contrato = models.CharField(max_length=100)
    asigna_rol = models.BooleanField()
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='id_rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_de_contrato'
        ordering = ['nombre_tipo_contrato']

    def save(self, *args, **kwargs):
        if self.nombre_tipo_contrato:
            self.nombre_tipo_contrato= self.nombre_tipo_contrato.upper()
        super(TiposDeContrato, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_tipo_contrato
