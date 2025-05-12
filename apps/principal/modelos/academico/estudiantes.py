from django.db import models
from apps.principal.modelos.usuario.Usuarios import *
from apps.principal.modelos.academico.programa import *



class ContadorEstudiantes(models.Model):
    anio_ingreso = models.IntegerField(primary_key=True)
    ultimo_consecutivo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'contador_estudiantes'


class Estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    codigo_estudiante = models.CharField(unique=True, max_length=100, blank=True, null=True)
    fecha_ingreso = models.DateField()
    semestre_actual = models.IntegerField()
    id_programa = models.ForeignKey(ProgramasAcademicos, on_delete=models.CASCADE, db_column='id_programa')
    estado_estudiante = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estudiantes'


class DocumentosEstudiantes(models.Model):
    id_documento_estudiante = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, db_column='id_estudiante')
    tipo_documento = models.CharField(max_length=100)
    ruta_archivo = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentos_estudiantes'



class Ocupaciones(models.Model):
    id_ocupacion = models.AutoField(primary_key=True)
    nombre_ocupacion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocupaciones'
        ordering = ['id_ocupacion']

    def save(self, *args, **kwargs):
        if self.nombre_ocupacion:
            self.nombre_ocupacion=self.nombre_ocupacion.upper()
        if self.descripcion:
            self.descripcion=self.descripcion.upper()
        super(Ocupaciones, self).save(*args, **kwargs)


class EstadosInscripcion(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'estados_inscripcion'



class InscripcionesEstudiantes(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, db_column='id_estudiante')
    fecha_inscripcion = models.DateField()
    id_programa = models.ForeignKey(ProgramasAcademicos, on_delete=models.CASCADE, db_column='id_programa')
    semestre = models.IntegerField()
    id_estado = models.ForeignKey(EstadosInscripcion, on_delete=models.CASCADE, db_column='id_estado')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inscripciones_estudiantes'

