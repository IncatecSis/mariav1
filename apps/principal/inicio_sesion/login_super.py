import hashlib
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from django.contrib import messages
from apps.principal.modelos.rrhh.contratos import Contrataciones
from apps.principal.modelos.usuario.contraseñas import Credenciales
from apps.principal.inicio_sesion.auth_login import *



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    initialize_login_attempts(request.session)

    is_blocked, remaining_time = is_user_blocked(request.session)
    if is_blocked:
        messages.error(request, f"Has excedido el número de intentos. Intenta de nuevo en {remaining_time} segundos.")
        response = redirect('login')
        return clear_session_expiration_cookie(request, response)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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



'''
from django.urls import reverse
from django.contrib import messages
from .auth_login import *
#from apps.principal.modelos.permisos import Permiso




def login(request):
    initialize_login_attempts(request.session)

    is_blocked, remaining_time = is_user_blocked(request.session)

    if request.method == 'GET':
        if is_blocked:
            return render(request, 'auth/inicio_sesion.html', {'remaining_time': remaining_time})

        response = render(request, 'auth/inicio_sesion.html')
        response.delete_cookie('sessionid', path='/')
        response.delete_cookie('csrftoken', path='/')
        response.delete_cookie('session_expired', path='/')
        return response

    if request.method == 'POST':
        if is_blocked:
            return render(request, 'auth/inicio_sesion.html', {'remaining_time': remaining_time})

        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            request.session['failed_attempts'] = 0
            request.session['blocked_until'] = None
            auth_login(request, usuario)

            if usuario.is_superuser:
                return redirect('Incatec:index')

            if usuario.tiene_acceso_completo():
                return redirect('Incatec:index')

            permiso_index = Permiso.objects.filter(descripcion="Index").first()
            if permiso_index and permiso_index in usuario.permisos.all():
                return redirect(reverse("Incatec:index"))

            messages.error(request, 'No tienes los permisos necesarios para acceder al inicio.')
            return redirect('login')

        else:
            is_locked, feedback = handle_failed_attempt(request.session)
            if is_locked:
                return render(request, 'auth/inicio_sesion.html', {'remaining_time': feedback})
            else:
                messages.error(request, f'Usuario o contraseña incorrectos. Te quedan {feedback} intentos.')
            return render(request, 'auth/inicio_sesion.html')

    response = render(request, 'auth/inicio_sesion.html')
    clear_session_expiration_cookie(request, response)
    return response
'''

def error(request, exception):
    return render(request, 'partials/404.html', status=404)


def logout(request):
    auth_logout(request)

    request.session.flush()
    request.session.clear()

    response = redirect('login')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    response.delete_cookie('session_expired')
    return response
