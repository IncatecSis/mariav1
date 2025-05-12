from django.db import models
from apps.principal.modelos.parametros.sedes import Sedes

class Arl(models.Model):
    id_arl = models.AutoField(primary_key=True)
    nombre_arl = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'arl'
        ordering = ['nombre_arl']

    def save(self, *args, **kwargs):
        if self.nombre_arl:
            self.nombre_arl = self.nombre_arl.upper()
        super(Arl, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_arl
    
class RiesgoLaboral(models.Model):
    id_riesgo_laboral = models.AutoField(primary_key=True)
    nivel_riesgo = models.CharField(max_length=20, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'riesgo_laboral'
        ordering = ['nivel_riesgo']

    def save(self, *args, **kwargs):
        if self.nivel_riesgo:
            self.nivel_riesgo = self.nivel_riesgo.upper()
        super(RiesgoLaboral, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nivel_riesgo}-{self.porcentaje}'

class Bancos(models.Model):
    id_banco = models.AutoField(primary_key=True)
    nombre_banco = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'bancos'
        ordering = ['nombre_banco']

    def save(self, *args, **kwargs):
        if self.nombre_banco:
            self.nombre_banco=self.nombre_banco.upper()
        super(Bancos, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_banco

class CajasCompensacion(models.Model):
    id_caja_compensacion = models.AutoField(primary_key=True)
    nombre_caja = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cajas_compensacion'
        ordering = ['nombre_caja']

    def save(self, *args, **kwargs):
        if self.nombre_caja:
            self.nombre_caja=self.nombre_caja.upper()
        super(CajasCompensacion, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre_caja
    
class AdministradorasPensiones(models.Model):
    id_administradoras_pensiones = models.AutoField(primary_key=True)
    nombre_administradora = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'administradoras_pensiones'
        ordering = ['nombre_administradora']

    def save(self, *args, **kwargs):
        if self.nombre_administradora:
            self.nombre_administradora = self.nombre_administradora.upper()
        super(AdministradorasPensiones, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_administradora

class DepartamentoLaboral(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    estado = models.BooleanField(blank=True, null=True, default=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamento_laboral'
        ordering = ['nombre']
        
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(DepartamentoLaboral, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(DepartamentoLaboral, on_delete=models.CASCADE, db_column='id_departamento')
    nombre = models.CharField(unique=True, max_length=100)
    estado = models.BooleanField(blank=True, null=True, default=True)
    id_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, db_column='id_sede', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargo'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Cargo, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre