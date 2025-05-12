from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.shortcuts import redirect
from apps.principal.modelos.rrhh.contratos import Contrataciones

class ContratoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_view = resolve(request.path_info).url_name

        if current_view in ['login', 'logout']:
            return None

        user = getattr(request, 'user', None)

        if user and getattr(user, 'is_authenticated', False):
            if isinstance(user, User) and user.is_superuser:
                return None

            if hasattr(user, 'id_usuario'):
                contratos_activos = Contrataciones.objects.filter(
                    id_usuario=user.id_usuario,
                    estado=True
                )
                if not contratos_activos.exists():
                    return redirect('login')

        return None
