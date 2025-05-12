from django.db import models

class Departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    departamento = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'departamentos'
        ordering = ['departamento']

    def __str__(self):
        return self.departamento

class Eps(models.Model):
    id_eps = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'eps'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Eps, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class EstadoCivil(models.Model):
    id_estado_civil = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado_civil'
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(EstadoCivil, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class EstratoSocioeconomico(models.Model):
    id_estrato = models.AutoField(primary_key=True)
    estrato = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'estrato_socioeconomico'
        ordering = ['estrato']

    def save(self, *args, **kwargs):
        if self.estrato:
            self.estrato=self.estrato.upper()
        super(EstratoSocioeconomico, self).save(*args, **kwargs)

    def __str__(self):
        return self.estrato

class Etnia(models.Model):
    id_etnia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'etnia'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(Etnia, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Municipios(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    municipio = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name='municipios')

    class Meta:
        managed = False
        db_table = 'municipios'
        ordering =['municipio']

    def __str__(self):
        return self.municipio

class Sexo(models.Model):
    id_sexo = models.AutoField(primary_key=True)
    sexo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sexo'
        ordering = ['sexo']

    def save(self, *args, **kwargs):
        if self.sexo:
            self.sexo=self.sexo.upper()
        super(Sexo, self).save(*args, **kwargs)

    def __str__(self):
        return self.sexo

class Sisben(models.Model):
    id_sisben = models.AutoField(primary_key=True)
    sisben = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sisben'
        ordering = ['sisben']

    def save(self, *args, **kwargs):
        if self.sisben:
            self.sisben=self.sisben.upper()
        super(Sisben, self).save(*args, **kwargs)

    def __str__(self):
        return self.sisben

class TipoDiscapacidad(models.Model):
    id_tipo_discapacidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_discapacidad'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(TipoDiscapacidad, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class TipoIdentificacion(models.Model):
    id_tipo_identificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'tipo_identificacion'
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(TipoIdentificacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class TipoSangre(models.Model):
    id_tipo_sangre = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_sangre'
        ordering = ['id_tipo_sangre']

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre=self.nombre.upper()
        super(TipoSangre, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class ZonaResidencial(models.Model):
    id_zona_residencial = models.AutoField(primary_key=True)
    zona_residencial = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'zona_residencial'
        ordering = ['zona_residencial']

    def save(self, *args, **kwargs):
        if self.zona_residencial:
            self.zona_residencial=self.zona_residencial.upper()
        super(ZonaResidencial, self).save(*args, **kwargs)

    def __str__(self):
        return self.zona_residencial
