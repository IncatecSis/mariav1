from apps.principal.modelos.permisos.permisos import UsuarioPermisos

def menu_permissions(request):
    if not request.user.is_authenticated:
        return {'usuarios_permisos': []}

    try:
        id_usuario = request.user.id_usuario.id_usuario
    except AttributeError:
        return {'usuarios_permisos': []}

    permisos = UsuarioPermisos.objects.filter(
        id_usuario=id_usuario
    ).values_list('id_permiso__codigo', flat=True)

    return {'usuarios_permisos': list(permisos)}
