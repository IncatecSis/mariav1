from django.apps import AppConfig


class DocentesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.docentes' #ruta configurada para enlazar con el archivo settings
    verbose_name = 'aplicacion docentes'
