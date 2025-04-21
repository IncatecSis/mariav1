from django.apps import AppConfig
import os
import glob

class PrincipalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.principal'

    def ready(self):
        modelos_path = os.path.join(os.path.dirname(__file__), "modelos")
        model_files = glob.glob(os.path.join(modelos_path, "**", "*.py"), recursive=True)
        for model_file in model_files:
            if not model_file.endswith("__init__.py"):
                module_name = model_file.replace("\\", "/").split("apps/principal/")[-1].replace("/", ".").replace(".py", "")
                __import__(f"apps.principal.{module_name}")
