from django.utils.deprecation import MiddlewareMixin
from apps.principal.inicio_sesion.auth_login import clear_session_expiration_cookie


class ClearSessionExpirationCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response = clear_session_expiration_cookie(request, response)
        if request.session.get('session_expired'):
            request.session.pop('session_expired', None)

        return response
