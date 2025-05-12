from django.db import models
from apps.principal.modelos.academico.jornadas import *
from apps.principal.modelos.academico.programa import *
from apps.principal.modelos.usuario.Usuarios import *
from apps.principal.modelos.parametros.sedes import Sedes
from apps.principal.modelos.parametros.años import Anio




class Convenios(models.Model):
    id_convenio = models.AutoField(primary_key=True)
    nombre_convenio = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'convenios'


class CostosProgramas(models.Model):
    id_costo = models.AutoField(primary_key=True)
    id_programa = models.ForeignKey(ProgramasAcademicos, on_delete=models.CASCADE, db_column='id_programa')
    id_anio = models.ForeignKey(Anio, on_delete=models.CASCADE, db_column='id_anio')
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'costos_programas'


class Descuentos(models.Model):
    id_descuento = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    nombre_descuento = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'descuentos'



class Incrementos(models.Model):
    id_incremento = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')
    nombre_incremento = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'incrementos'


class TipoIngresoEstudiante(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_ingreso_estudiante'


class TipoMatriculaFin(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_matricula_fin'


class SemestresProgramas(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'semestres_programas'


class MatriculasFinancieras(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    estado = models.BooleanField(blank=True, null=True)
    fecha_matricula = models.DateTimeField()
    id_anio = models.ForeignKey(Anio, on_delete=models.CASCADE, db_column='id_anio')
    id_convenio = models.ForeignKey(Convenios, on_delete=models.CASCADE, db_column='id_convenio', blank=True, null=True)
    id_costo = models.ForeignKey(CostosProgramas, on_delete=models.CASCADE, db_column='id_costo')
    id_jornada = models.ForeignKey(Jornadas, on_delete=models.CASCADE, db_column='id_jornada')
    id_programa = models.ForeignKey(ProgramasAcademicos, on_delete=models.CASCADE, db_column='id_programa')
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    id_tipo_matricula_fin = models.ForeignKey(TipoMatriculaFin, on_delete=models.CASCADE, db_column='id_tipo_matricula_fin', blank=True, null=True)
    id_semestre = models.ForeignKey(SemestresProgramas, on_delete=models.CASCADE, db_column='id_semestre', blank=True, null=True)
    id_tipo_ingreso = models.ForeignKey(TipoIngresoEstudiante, on_delete=models.CASCADE, db_column='id_tipo_ingreso', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matriculas_financieras'

class FormaPago(models.Model):
    id_forma_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'forma_pago'

class Financiaciones(models.Model):
    id_financiacion = models.AutoField(primary_key=True)
    id_matricula = models.OneToOneField(MatriculasFinancieras, on_delete=models.CASCADE, db_column='id_matricula')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    id_descuento = models.ForeignKey(Descuentos, on_delete=models.CASCADE, db_column='id_descuento', blank=True, null=True)
    id_incremento = models.ForeignKey(Incrementos, on_delete=models.CASCADE, db_column='id_incremento', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuotas = models.IntegerField()
    dia_pago_1 = models.IntegerField(blank=True, null=True)
    dia_pago_2 = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id_forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE, db_column='id_forma_pago')
    estado_financiacion = models.CharField(max_length=20, default='Pendiente')

    class Meta:
        managed = False
        db_table = 'financiaciones'

class Cuotas(models.Model):
    id_cuota = models.AutoField(primary_key=True)
    id_financiacion = models.ForeignKey(Financiaciones, on_delete=models.CASCADE, db_column='id_financiacion')
    numero_cuota = models.IntegerField()
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(blank=True, null=True)
    estado_cuota = models.CharField(max_length=20, default='Pendiente')

    class Meta:
        managed = False
        db_table = 'cuotas'

class MediosPago(models.Model):
    id_medio_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'medios_pago'

class Cartera(models.Model):
    id_cartera = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    id_financiacion = models.ForeignKey(Financiaciones, on_delete=models.CASCADE, db_column='id_financiacion')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Pendiente')
    saldo_a_favor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'cartera'

class ConceptosPago(models.Model):
    id_concepto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conceptos_pago'

class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    referencia_pago = models.CharField(unique=True, max_length=20)
    estado = models.CharField(max_length=20)
    fecha_pago = models.DateTimeField()
    rc_numero = models.CharField(unique=True, max_length=10)
    id_cartera = models.ForeignKey(Cartera, on_delete=models.CASCADE, db_column='id_cartera', blank=True, null=True)
    id_concepto = models.ForeignKey(ConceptosPago, on_delete=models.CASCADE, db_column='id_concepto', blank=True, null=True)
    id_medio_pago = models.ForeignKey(MediosPago, on_delete=models.CASCADE, db_column='id_medio_pago')
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'pagos'


class PagosCuotas(models.Model):
    id_pago_cuota = models.AutoField(primary_key=True)
    id_pago = models.IntegerField()
    id_cuota = models.ForeignKey(Cuotas, on_delete=models.CASCADE, db_column='id_cuota')
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'pagos_cuotas'


class Conciliaciones(models.Model):
    id_conciliacion = models.AutoField(primary_key=True)
    id_pago = models.ForeignKey(Pagos, on_delete=models.CASCADE, db_column='id_pago')
    estado_conciliacion = models.CharField(max_length=20, blank=True, null=True)
    fecha_conciliacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'conciliaciones'



class ConsecutivosTipoPago(models.Model):
    tipo_pago = models.CharField(primary_key=True, max_length=10)
    ultimo_numero = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consecutivos_tipo_pago'


