from django.db import models
from apps.principal.modelos.usuario.Usuarios import *
from apps.principal.modelos.usuario.roles import *



class UsuarioRoles(models.Model):
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='id_rol')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuario_roles'
        unique_together = (('id_usuario', 'id_rol'),)

    def __str__(self):
        return f'{self.id_usuario} - {self.id_rol}'