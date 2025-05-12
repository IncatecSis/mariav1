from django.db import models
from apps.principal.modelos.usuario.Usuarios import * 

class Conversacion(models.Model):
    id_conversacion = models.AutoField(primary_key=True)
    TIPO_CHOICES = [
        ('individual', 'Individual'),
        ('grupal', 'Grupal'),
        ('anuncio', 'Anuncio'),
    ]
    
    titulo = models.CharField(max_length=255)
    tipo_conversacion = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_creacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    ultima_actividad = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    creador = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name='conversaciones_creadas', db_column='id_creador')
    
    class Meta:
        db_table = 'conversaciones'
        ordering = ['-ultima_actividad']
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        managed = False
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_conversacion_display()})"

class ParticipanteConversacion(models.Model):
    id_participante = models.AutoField(primary_key=True)
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('silenciado', 'Silenciado'),
        ('eliminado', 'Eliminado'),
    ]
    
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('miembro', 'Miembro'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='participantes', db_column='id_conversacion')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='conversaciones_participando', db_column='id_usuario')
    fecha_ingreso = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    estado_participacion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    rol_participante = models.CharField(max_length=20, choices=ROL_CHOICES, default='miembro')
    notificaciones_activas = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'participantes_conversacion'
        unique_together = ['conversacion', 'usuario']
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        managed = False

    
    def __str__(self):
        return f"{self.usuario} en {self.conversacion}"

class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('leido', 'Leído'),
        ('eliminado', 'Eliminado'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes', db_column='id_conversacion')
    remitente = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name='mensajes_enviados', db_column='id_remitente')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    editado = models.BooleanField(default=True)
    fecha_edicion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='enviado')
    mensaje_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='respuestas', db_column='mensaje_padre')
    
    class Meta:
        db_table = 'mensajes'
        ordering = ['fecha_envio']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        managed = False

    
    def __str__(self):
        return f"Mensaje de {self.remitente} ({self.fecha_envio.strftime('%d/%m/%Y %H:%M')})"

class AdjuntoMensaje(models.Model):
    id_adjunto = models.AutoField(primary_key=True)
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('documento', 'Documento'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('otro', 'Otro'),
    ]
    
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='adjuntos', db_column='id_mensaje')
    tipo_archivo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nombre_archivo = models.CharField(max_length=255, null=True)
    archivo = models.FileField(upload_to='chat/adjuntos/', db_column='ruta_archivo')
    tamaño_bytes = models.IntegerField()
    fecha_subida = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'adjuntos_mensaje'
        verbose_name = 'Adjunto'
        verbose_name_plural = 'Adjuntos'
        managed = False
    
    def __str__(self):
        return f"{self.nombre_archivo} ({self.get_tipo_archivo_display()})"

class LecturaMensaje(models.Model):
    id_lectura = models.AutoField(primary_key=True)
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='lecturas', db_column='id_mensaje')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='mensajes_leidos', db_column='id_usuario')
    fecha_lectura = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    class Meta:
        db_table = 'lecturas_mensaje'
        unique_together = ['mensaje', 'usuario']
        verbose_name = 'Lectura'
        verbose_name_plural = 'Lecturas'
        managed = False
    
    def __str__(self):
        return f"{self.usuario} leyó mensaje {self.mensaje.id_mensaje}"

class ReaccionMensaje(models.Model):
    id_reaccion = models.AutoField(primary_key=True)
    REACCION_CHOICES = [
        ('me_gusta', 'Me gusta'),
        ('importante', 'Importante'),
        ('divertido', 'Divertido'),
        ('sorprendido', 'Sorprendido'),
        ('triste', 'Triste'),
        ('enojado', 'Enojado'),
    ]
    
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='reacciones', db_column='id_mensaje')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='reacciones', db_column='id_usuario')
    tipo_reaccion = models.CharField(max_length=50, choices=REACCION_CHOICES)
    fecha_reaccion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    class Meta:
        db_table = 'reacciones_mensaje'
        unique_together = ['mensaje', 'usuario', 'tipo_reaccion']
        verbose_name = 'Reacción'
        verbose_name_plural = 'Reacciones'
        managed = False
    
    def __str__(self):
        return f"{self.usuario} reaccionó {self.get_tipo_reaccion_display()} a mensaje {self.mensaje.id_mensaje}"

class MencionMensaje(models.Model):
    id_mencion = models.AutoField(primary_key=True)
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='menciones', db_column='id_mensaje')
    usuario_mencionado = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='menciones_recibidas', db_column='id_usuario_mencionado')
    fecha_mencion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    notificado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'menciones_mensaje'
        unique_together = ['mensaje', 'usuario_mencionado']
        verbose_name = 'Mención'
        verbose_name_plural = 'Menciones'
        managed = False
    
    def __str__(self):
        return f"Mención a {self.usuario_mencionado} en mensaje {self.mensaje.id_mensaje}"

class NotificacionChat(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    TIPO_CHOICES = [
        ('mensaje_nuevo', 'Mensaje nuevo'),
        ('mencion', 'Mención'),
        ('invitacion', 'Invitación'),
        ('cambio_grupo', 'Cambio en grupo'),
    ]
    
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='notificaciones_chat', db_column='id_usuario')
    mensaje = models.ForeignKey(Mensaje, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificaciones', db_column='id_mensaje')
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='notificaciones', db_column='id_conversacion')
    tipo_notificacion = models.CharField(max_length=50, choices=TIPO_CHOICES)
    contenido = models.TextField()
    leida = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    class Meta:
        db_table = 'notificaciones_chat'
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        managed = False
    
    def __str__(self):
        return f"Notificación {self.get_tipo_notificacion_display()} para {self.usuario}"

class MensajeFavorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='favoritos', db_column='id_mensaje')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='mensajes_favoritos', db_column='id_usuario')
    fecha_marcado = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    nota = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'mensajes_favoritos'
        unique_together = ['mensaje', 'usuario']
        verbose_name = 'Mensaje favorito'
        verbose_name_plural = 'Mensajes favoritos'
        managed = False
    
    def __str__(self):
        return f"Favorito de {self.usuario}: mensaje {self.mensaje.id_mensaje}"

class GrupoChat(models.Model):
    id_grupo_chat = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.CharField(max_length=255, null=True, blank=True)
    es_oficial = models.BooleanField(default=True)
    creador = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name='grupos_creados', db_column='id_creador')
    fecha_creacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    conversaciones = models.ManyToManyField(Conversacion, through='GrupoConversacion', related_name='grupos')
    
    class Meta:
        db_table = 'grupos_chat'
        verbose_name = 'Grupo de chat'
        verbose_name_plural = 'Grupos de chat'
        managed = False
    
    def __str__(self):
        return self.nombre

class GrupoConversacion(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    grupo = models.ForeignKey(GrupoChat, on_delete=models.CASCADE, db_column='id_grupo_chat')
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, db_column='id_conversacion')
    fecha_asignacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    class Meta:
        db_table = 'grupo_conversacion'
        unique_together = ['grupo', 'conversacion']
        verbose_name = 'Relación Grupo-Conversación'
        verbose_name_plural = 'Relaciones Grupo-Conversación'
        managed = False
    
    def __str__(self):
        return f"{self.conversacion} en {self.grupo}"