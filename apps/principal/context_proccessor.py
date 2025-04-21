from apps.principal.modelos.usuario.Usuarios import Usuarios
from apps.principal.modelos.usuario.contraseñas import Credenciales

def nombre_usuario(request):
    try:
        if request.user.is_authenticated:
            credencial = Credenciales.objects.get(username=request.user.username)
            usuario = Usuarios.objects.get(id_usuario=credencial.id_usuario_id)
            return {'nombre_usuario': usuario.nombres, 'usuario': usuario} 
    except (Credenciales.DoesNotExist, Usuarios.DoesNotExist, AttributeError):
        return {'nombre_usuario': '', 'usuario': None}

    return {'nombre_usuario': '', 'usuario': None}
