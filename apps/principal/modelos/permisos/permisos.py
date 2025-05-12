from django.db import models
from apps.principal.modelos.usuario.Usuarios import Usuarios



class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    modulo = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True ,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permisos'



class UsuarioPermisos(models.Model):
    id_usuario_permiso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    id_permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='id_permiso')
    fecha_asignacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True)
    asignado_por = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='asignado_por', related_name='usuariopermisos_asignado_por_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_permisos'
        unique_together = (('id_usuario', 'id_permiso'),)