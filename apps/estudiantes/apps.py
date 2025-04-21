from django.apps import AppConfig


class EstudiantesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.estudiantes' #ruta configurada para enlazar con el archivo settings
    verbose_name = 'aplicacion estudiantes'
