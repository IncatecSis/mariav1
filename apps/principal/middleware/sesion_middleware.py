from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import messages


class SessionUnicaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/login/' or request.path == '/':
            return None
            
        user_id = request.session.get('user_id')
        session_key = request.session.session_key

        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        if user_id and session_key:
            cache_key = f"usuario_sesion_{user_id}"
            sesion_valida = cache.get(cache_key)
            
            print(f">>> Verificando sesión: user_id={user_id}, cache_key={cache_key}")
            print(f">>> Sesión almacenada: {sesion_valida}, Sesión actual: {session_key}")

            if sesion_valida and sesion_valida != session_key:
                print(f">>> Sesión inválida detectada. Cerrando sesión actual.")
                
                request.session.flush()
                
                messages.error(request, 'Tu sesión se cerró porque se inició otra sesión en otro dispositivo.')
                
                return redirect('login')
                
            cache.set(cache_key, session_key, timeout=43200)  # 12 horas