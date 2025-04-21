from django.utils.deprecation import MiddlewareMixin
from apps.principal.modelos.usuario.contraseñas import Credenciales

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')

        if user_id:
            try:
                credencial = Credenciales.objects.get(id_credencial=user_id)
                request.user = credencial
                request.user.is_authenticated = True
            except Credenciales.DoesNotExist:
                request.user.is_athenticated = False