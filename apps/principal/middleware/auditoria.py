from django.db import connection
from apps.principal.modelos.usuario.Usuarios import Usuarios
from apps.principal.modelos.usuario.contraseñas import Credenciales

def context_usuario(request):
    if request.user.is_authenticated:
        try:
            credencial = Credenciales.objects.get(username=request.user.username)
            usuario = Usuarios.objects.get(id_usuario=credencial.id_usuario_id)
            nombre_completo = f"{usuario.nombres} {usuario.apellidos}"

            with connection.cursor() as cursor:
                cursor.execute("SELECT set_config('app.usuario_actual', %s, false);", [nombre_completo])

        except (Credenciales.DoesNotExist, Usuarios.DoesNotExist):
            pass 
