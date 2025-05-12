from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from apps.principal.modelos.permisos.permisos import *



def requerir_permiso(codigo_permiso):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            try:
                usuario = request.user.id_usuario
                print(">>> ID del usuario:", usuario.id_usuario)
                print(">>> Código del permiso requerido:", codigo_permiso)

                tiene_permiso = UsuarioPermisos.objects.filter(
                    id_usuario_id=usuario.id_usuario,
                    id_permiso__codigo=codigo_permiso
                ).only('id_usuario').exists()

                print(">>> ¿Tiene permiso?:", tiene_permiso)

            except Exception as e:
                print(">>> ERROR EN DECORADOR:", e)
                messages.error(request,"No tienes permiso para acceder a esta página")
                return redirect('Incatec:index')

            if tiene_permiso:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request,"No tienes permiso para acceder a esta página")
                return redirect('Incatec:index')
        return wrapper
    return decorator

