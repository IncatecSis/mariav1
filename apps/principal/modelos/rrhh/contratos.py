from django.db import models
from apps.principal.modelos.rrhh.datos_adicionales import *
from apps.principal.modelos.usuario.Usuarios import *
from apps.principal.modelos.rrhh.tipo_contrato import *


class Contrataciones(models.Model):
    id_contratacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    id_banco = models.ForeignKey(Bancos, on_delete=models.CASCADE, db_column='id_banco', blank=True, null=True)
    numero_cuenta = models.CharField(max_length=20, blank=True, null=True)
    id_arl = models.ForeignKey(Arl, on_delete=models.CASCADE, db_column='id_arl', blank=True, null=True)
    id_caja_compensacion = models.ForeignKey(CajasCompensacion, on_delete=models.CASCADE, db_column='id_caja_compensacion', blank=True, null=True)
    id_administradoras_pensiones = models.ForeignKey(AdministradorasPensiones, on_delete=models.CASCADE, db_column='id_administradoras_pensiones', blank=True, null=True)
    id_tipo_contrato = models.ForeignKey(TiposDeContrato, on_delete=models.CASCADE, blank=True, null=True,  db_column='id_tipo_contrato')
    id_departamento = models.ForeignKey(DepartamentoLaboral, on_delete=models.CASCADE, blank=True, null=True,  db_column='id_departamento')
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,blank=True, null=True, db_column='id_cargo')
    id_riesgo_laboral = models.ForeignKey(RiesgoLaboral, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, blank=True, null=True, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'contrataciones'

    def __str__(self):
        return f'{self.id_contratacion} - {self.id_usuario} - {"ACTIVO" if self.estado else "RETIRADO"}'
    

class TipoDespido(models.Model):
    id_tipo_despido = models.AutoField(primary_key=True)
    nombre_despido = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_despido'
        ordering = ['nombre_despido']

    def save(self, *args, **kwargs):
        if self.nombre_despido:
            self.nombre_despido = self.nombre_despido.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super(TipoDespido, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_despido


class ContratoFin(models.Model):
    id_contrato_fin = models.AutoField(primary_key=True)
    id_contratacion = models.ForeignKey(Contrataciones, on_delete=models.CASCADE, db_column='id_contratacion')
    fecha_fin = models.DateField()
    id_tipo_despido = models.ForeignKey(TipoDespido, on_delete=models.CASCADE, db_column='id_tipo_despido')

    class Meta:
        managed = False
        db_table = 'contrato_fin'

    def __str__(self):
        return f'{self.id_contrato_fin} - {self.id_contratacion}'
    

class DocumentosContrato(models.Model):
    id_documento_contrato = models.AutoField(primary_key=True)
    id_contratacion = models.ForeignKey(Contrataciones, on_delete=models.CASCADE, db_column='id_contratacion')
    entrevista = models.ImageField(upload_to='anexos', null=True, blank=True)
    prueba_tecnica = models.ImageField(upload_to='anexos', null=True, blank=True)
    remision = models.ImageField(upload_to='anexos', null=True, blank=True)
    arl = models.ImageField(upload_to='anexos', null=True, blank=True)
    eps = models.ImageField(upload_to='anexos', null=True, blank=True)
    caja_compensacion = models.ImageField(upload_to='anexos', null=True, blank=True)
    fondo_pension = models.ImageField(upload_to='anexos', null=True, blank=True)
    bancos = models.ImageField(upload_to='anexos', null=True, blank=True)
    resultados_medicos = models.ImageField(upload_to='anexos', null=True, blank=True)
    resultados = models.ImageField(upload_to='anexos', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'anexo_documentos'

    def __str__(self):
        return f'{self.id_contratacion}'