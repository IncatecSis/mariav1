from django.db import models
from apps.principal.modelos.parametros.años import Anio
from apps.principal.modelos.parametros.sedes import Sedes




class Escuelas(models.Model):
    id_escuelas = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede', blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escuelas'
        ordering = ['id_escuelas']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        if self.tipo:
            self.tipo=self.tipo.upper()
        super(Escuelas, self).save(*args, **kwargs)

class TiposProgramas(models.Model):
    id_tipos_programas = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_programas'
        ordering=['nombre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(TiposProgramas, self).save(*args, **kwargs)

class ProgramasAcademicos(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.IntegerField()
    id_periodo = models.IntegerField()
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    id_escuelas = models.ForeignKey(Escuelas, on_delete=models.CASCADE, db_column='id_escuelas', blank=True, null=True)
    id_tipos_programas = models.ForeignKey(TiposProgramas, on_delete=models.CASCADE, db_column='id_tipos_programas', blank=True, null=True)
    codigo_centro_costo = models.IntegerField(blank=True, null=True)
    codigo_siet = models.CharField(max_length=50, blank=True, null=True)
    numero_registro = models.CharField(max_length=50, blank=True, null=True)
    numero_certificacion = models.CharField(max_length=50, blank=True, null=True)
    acto_administrativo_pdf = models.ImageField(upload_to='anexos/gestion_academica/', blank=True, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'programas_academicos'
        ordering = ['id_programa']

    def save(self, *args, **kwargs):
        if self.nombre_programa:
            self.nombre_programa=self.nombre_programa.upper()
        if self.descripcion:
            self.descripcion=self.descripcion.upper()
        super(ProgramasAcademicos, self).save(*args, **kwargs)
        

class Pensum(models.Model):
    id_pensum = models.AutoField(primary_key=True)
    id_programa = models.ForeignKey(ProgramasAcademicos, on_delete=models.CASCADE, db_column='id_programa')
    anio_vigencia = models.IntegerField()
    activo = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    id_anio = models.ForeignKey(Anio, models.DO_NOTHING, db_column='id_anio', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'pensum'
        ordering = ['anio_vigencia']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Pensum, self).save(*args, **kwargs)
