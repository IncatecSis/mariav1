from django.db import models


class Sedes(models.Model):
    id_sede = models.AutoField(primary_key=True)
    nombre_sede = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ciudad = models.CharField(max_length=50)
    estado = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sedes'

    def __str__(self):
        return self.nombre_sede
    
    def save(self, *args, **kwargs):
        if self.nombre_sede:
            self.nombre_sede = self.nombre_sede.upper()
        if self.direccion:
            self.direccion = self.direccion.upper()
        if self.ciudad:
            self.ciudad = self.ciudad.upper()
        super(Sedes, self).save(*args, **kwargs)

class Areas(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'areas'
        ordering = ['id_area']

    def __str__(self):
        return self.nombre_area
    
    def save(self, *args, **kwargs):
        if self.nombre_area:
            self.nombre_area = self.nombre_area.upper()
        super(Areas, self).save(*args, **kwargs)

class Pisos(models.Model):
    id_piso = models.AutoField(primary_key=True)
    nombre_piso = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'pisos'
        ordering = ['id_piso']

    def __str__(self):
        return self.nombre_piso
    
    def save(self, *args, **kwargs):
        if self.nombre_piso:
            self.nombre_piso = self.nombre_piso.upper()
        super(Pisos, self).save(*args, **kwargs)

class Ubicaciones(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    id_area = models.ForeignKey(Areas, on_delete=models.CASCADE, db_column='id_area')
    id_piso = models.ForeignKey(Pisos, on_delete=models.CASCADE, db_column='id_piso')
    nombre_ubicacion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    aforo = models.IntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'ubicaciones'
        ordering=['nombre_ubicacion']

    def __str__(self):
        return f'{self.nombre_ubicacion} {self.descripcion}'
    
    def save(self, *args, **kwargs):
        if self.nombre_ubicacion:
            self.nombre_ubicacion=self.nombre_ubicacion.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super(Ubicaciones, self).save(*args, **kwargs)