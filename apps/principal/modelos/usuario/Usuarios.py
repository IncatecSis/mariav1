from django.db import models
from apps.principal.modelos.matricula.modelos_matriculas.generales import *
from apps.principal.modelos.parametros.sedes import Sedes


class Paises(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'paises'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Paises, self).save(*args, **kwargs)

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    foto_perfil = models.ImageField(upload_to='foto_usuarios/', null=True, blank=True, default='usuario.png')
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    id_tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.CASCADE, db_column='id_tipo_identificacion')
    numero_documento = models.CharField(unique=True, max_length=20)
    id_pais = models.ForeignKey(Paises, on_delete=models.CASCADE, db_column='id_pais', blank=True, null=True)
    id_departamento_expedicion = models.ForeignKey(Departamentos, on_delete=models.CASCADE, db_column='id_departamento_expedicion', related_name='usuarios_expedicion')
    id_municipio_expedicion = models.ForeignKey(Municipios, on_delete=models.CASCADE, db_column='id_municipio_expedicion', related_name='usuarios_expedicion')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    id_sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, db_column='id_sexo')
    id_departamento_nacimiento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, db_column='id_departamento_nacimiento', related_name='usuarios_nacimiento')
    id_municipio_nacimiento = models.ForeignKey(Municipios, on_delete=models.CASCADE, db_column='id_municipio_nacimiento', related_name='usuarios_nacimiento')
    id_tipo_sangre = models.ForeignKey(TipoSangre, on_delete=models.CASCADE, db_column='id_tipo_sangre')
    id_estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, db_column='id_estado_civil')
    id_sisben = models.ForeignKey(Sisben, on_delete=models.CASCADE, db_column='id_sisben')
    id_departamento_residencia = models.ForeignKey(Departamentos, on_delete=models.CASCADE, db_column='id_departamento_residencia', related_name='usuarios_residencia')
    id_municipio_residencia = models.ForeignKey(Municipios, on_delete=models.CASCADE, db_column='id_municipio_residencia', related_name='usuarios_residencia')
    direccion_residencia = models.CharField(max_length=100, blank=False, null=False)
    barrio = models.CharField(max_length=100, blank=False, null=False)
    celular = models.CharField(max_length=15, blank=False, null=False)
    telefono = models.CharField(max_length=15, blank=False, null=False)
    correo_electronico = models.EmailField(unique=False, max_length=150)
    id_estrato = models.ForeignKey(EstratoSocioeconomico, on_delete=models.CASCADE, db_column='id_estrato')
    id_etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE, db_column='id_etnia')
    id_zona_residencial = models.ForeignKey(ZonaResidencial, on_delete=models.CASCADE, db_column='id_zona_residencial')
    id_eps = models.ForeignKey(Eps, on_delete=models.CASCADE, db_column='id_eps')
    id_departamento_expulsor = models.ForeignKey(Departamentos, on_delete=models.CASCADE, db_column='id_departamento_expulsor', related_name='usuarios_expulsor', null=True, blank=True)
    id_municipio_expulsor = models.ForeignKey(Municipios, on_delete=models.CASCADE, db_column='id_municipio_expulsor', related_name='usuarios_expulsor', null=True, blank=True)
    id_tipo_discapacidad = models.ForeignKey(TipoDiscapacidad, on_delete=models.CASCADE, db_column='id_tipo_discapacidad', blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=50, default='pre_registro')

    class Meta:
        managed = True
        db_table = 'usuarios'
        ordering = ['nombres']

    def save(self, *args, **kwargs):
        if self.nombres:
            self.nombres=self.nombres.upper()
        if self.apellidos:
            self.apellidos=self.apellidos.upper()
        if self.barrio:
            self.barrio=self.barrio.upper()
        if self.correo_electronico:
            self.correo_electronico=self.correo_electronico.upper()
        if self.direccion_residencia:
            self.direccion_residencia = self.direccion_residencia.upper()
        super(Usuarios, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'