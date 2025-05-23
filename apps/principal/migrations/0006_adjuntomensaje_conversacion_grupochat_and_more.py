# Generated by Django 5.1.2 on 2025-05-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0005_permisos_usuariopermisos'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjuntoMensaje',
            fields=[
                ('id_adjunto', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_archivo', models.CharField(choices=[('imagen', 'Imagen'), ('documento', 'Documento'), ('audio', 'Audio'), ('video', 'Video'), ('otro', 'Otro')], max_length=50)),
                ('nombre_archivo', models.CharField(max_length=255, null=True)),
                ('archivo', models.FileField(db_column='ruta_archivo', upload_to='chat/adjuntos/%Y/%m/%d/')),
                ('tamaño_bytes', models.IntegerField()),
                ('fecha_subida', models.DateTimeField(auto_now_add=True, null=True)),
                ('metadata', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Adjunto',
                'verbose_name_plural': 'Adjuntos',
                'db_table': 'adjuntos_mensaje',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id_conversacion', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
                ('tipo_conversacion', models.CharField(choices=[('individual', 'Individual'), ('grupal', 'Grupal'), ('anuncio', 'Anuncio')], max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('ultima_actividad', models.DateTimeField(auto_now=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Conversación',
                'verbose_name_plural': 'Conversaciones',
                'db_table': 'conversaciones',
                'ordering': ['-ultima_actividad'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GrupoChat',
            fields=[
                ('id_grupo_chat', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('icono', models.CharField(blank=True, max_length=255, null=True)),
                ('es_oficial', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Grupo de chat',
                'verbose_name_plural': 'Grupos de chat',
                'db_table': 'grupos_chat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GrupoConversacion',
            fields=[
                ('id_grupo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Relación Grupo-Conversación',
                'verbose_name_plural': 'Relaciones Grupo-Conversación',
                'db_table': 'grupo_conversacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LecturaMensaje',
            fields=[
                ('id_lectura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_lectura', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Lectura',
                'verbose_name_plural': 'Lecturas',
                'db_table': 'lecturas_mensaje',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MencionMensaje',
            fields=[
                ('id_mencion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_mencion', models.DateTimeField(auto_now_add=True, null=True)),
                ('notificado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Mención',
                'verbose_name_plural': 'Menciones',
                'db_table': 'menciones_mensaje',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True, null=True)),
                ('editado', models.BooleanField(default=True)),
                ('fecha_edicion', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('enviado', 'Enviado'), ('entregado', 'Entregado'), ('leido', 'Leído'), ('eliminado', 'Eliminado')], default='enviado', max_length=20)),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'db_table': 'mensajes',
                'ordering': ['fecha_envio'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MensajeFavorito',
            fields=[
                ('id_favorito', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_marcado', models.DateTimeField(auto_now_add=True, null=True)),
                ('nota', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Mensaje favorito',
                'verbose_name_plural': 'Mensajes favoritos',
                'db_table': 'mensajes_favoritos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotificacionChat',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_notificacion', models.CharField(choices=[('mensaje_nuevo', 'Mensaje nuevo'), ('mencion', 'Mención'), ('invitacion', 'Invitación'), ('cambio_grupo', 'Cambio en grupo')], max_length=50)),
                ('contenido', models.TextField()),
                ('leida', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_lectura', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Notificación',
                'verbose_name_plural': 'Notificaciones',
                'db_table': 'notificaciones_chat',
                'ordering': ['-fecha_creacion'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipanteConversacion',
            fields=[
                ('id_participante', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, null=True)),
                ('estado_participacion', models.CharField(choices=[('activo', 'Activo'), ('silenciado', 'Silenciado'), ('eliminado', 'Eliminado')], default='activo', max_length=20)),
                ('rol_participante', models.CharField(choices=[('admin', 'Administrador'), ('miembro', 'Miembro')], default='miembro', max_length=20)),
                ('notificaciones_activas', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Participante',
                'verbose_name_plural': 'Participantes',
                'db_table': 'participantes_conversacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReaccionMensaje',
            fields=[
                ('id_reaccion', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_reaccion', models.CharField(choices=[('me_gusta', 'Me gusta'), ('importante', 'Importante'), ('divertido', 'Divertido'), ('sorprendido', 'Sorprendido'), ('triste', 'Triste'), ('enojado', 'Enojado')], max_length=50)),
                ('fecha_reaccion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Reacción',
                'verbose_name_plural': 'Reacciones',
                'db_table': 'reacciones_mensaje',
                'managed': False,
            },
        ),
    ]
