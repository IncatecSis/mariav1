import hashlib
from django.contrib.auth.backends import BaseBackend
from apps.principal.modelos.usuario.contraseñas import Credenciales

class Usuariobackends(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            credencial = Credenciales.objects.get(username=username)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == credencial.password:
                return credencial.id_usuario
        except Credenciales.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return Credenciales.objects.get(id_usuario=user_id).id_usuario
        except Credenciales.DoesNotExist:
            return None