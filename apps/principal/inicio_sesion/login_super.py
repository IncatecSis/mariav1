from django.utils import timezone
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login as django_login, logout as auth_logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.rrhh.contratos import Contrataciones
from apps.principal.modelos.usuario.contraseñas import Credenciales
from apps.principal.inicio_sesion.auth_login import *
import hashlib


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    initialize_login_attempts(request.session)

    is_blocked, remaining_time = is_user_blocked(request.session)
    if is_blocked:
        messages.error(request, f"Has excedido el número de intentos. Intenta de nuevo en {remaining_time} segundos.")
        return render(request, 'auth/inicio_sesion.html', {'remaining_time': remaining_time})

    if request.method == 'POST':
        context_usuario(request)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and isinstance(user, User) and user.is_superuser:
            django_login(request, user)
            request.session['is_authenticated'] = True
            messages.success(request, '¡Ingreso como superusuario exitoso! 👑')
            return redirect('Incatec:index')

        try:
            credencial = Credenciales.objects.get(username=username)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == credencial.password:
                contratos_activos = Contrataciones.objects.filter(
                    id_usuario=credencial.id_usuario,
                    estado=True,
                )
                if not contratos_activos.exists():
                    messages.error(request, '¡Acceso denegado.!😢')
                    response = redirect('login')
                    return clear_session_expiration_cookie(request, response)

                request.session['user_id'] = credencial.id_credencial
                request.session['username'] = credencial.username
                request.session['failed_attempts'] = 0
                request.session['is_authenticated'] = True
                request.session.modified = True
                request.session.save()

                user_cache_key = f"usuario_sesion_{credencial.id_credencial}"
                sesion_anterior = cache.get(user_cache_key)
                sesion_actual = request.session.session_key

                print(">>> Clave cache actual:", user_cache_key)
                print(">>> Sesión anterior:", sesion_anterior)
                print(">>> Sesión actual:", sesion_actual)

                if sesion_anterior and sesion_anterior != sesion_actual:
                    try:
                        Session.objects.get(session_key=sesion_anterior).delete()
                    except Session.DoesNotExist:
                        pass

                cache.set(user_cache_key, sesion_actual, timeout=None)
                print(">>> Nueva sesión guardada en cache:", cache.get(user_cache_key))

                messages.success(request, '¡Ingreso exitoso.!🤩')
                response = redirect('Incatec:index')
                return clear_session_expiration_cookie(request, response)

            else:
                is_locked, attempts_left = handle_failed_attempt(request.session)
                if is_locked:
                    messages.error(request, f'Demasiados intentos fallidos. Tu cuenta está bloqueada por {BLOCK_TIME} segundos.')
                    response = redirect('login')
                    return clear_session_expiration_cookie(request, response)
                else:
                    messages.warning(request, f'Contraseña incorrecta. Intentos restantes: {attempts_left}')
        except Credenciales.DoesNotExist:
            messages.error(request, '¡Acceso denegado.!😢')

    return render(request, 'auth/inicio_sesion.html', {'remaining_time': remaining_time})


def error(request, exception):
    return render(request, 'partials/404.html', status=404)



def logout(request):
    user_id = request.session.get('user_id')
    
    print(f">>> Iniciando logout para usuario con ID: {user_id}")
    
    auth_logout(request)
    
    if user_id:
        cache_key = f"usuario_sesion_{user_id}"
        cache.delete(cache_key)
        print(f">>> Limpiando caché de sesión para usuario {user_id}")
    else:
        print(">>> No se encontró user_id en la sesión al cerrar")
    
    request.session.flush()
    request.session.clear()
    
    response = redirect('login')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    response.delete_cookie('session_expired')

    Session.objects.filter(expire_date__lt=timezone.now()).delete()

    return response
