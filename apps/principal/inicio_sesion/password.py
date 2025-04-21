'''
from modelos.usuarios import Usuario

def cambiar_contraseña(usuario_id, nueva_contraseña, confirmar_contraseña, user_request):

    if nueva_contraseña != confirmar_contraseña:
        return False, 'Las contraseñas no coinciden.'
    
    if not (user_request.is_superuser or user_request.tiene_acceso_completo()):
        return False, 'No tienes permisos para realizar esta acción'
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.set_password(nueva_contraseña)
        usuario.save()
        return True, f'Contraseña actualizada a {usuario.nombre}'
    
    except Usuario.DoesNotExist:
        return False, 'Usuario no encontrado'
    
'''
        