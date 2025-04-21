from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from django.contrib import messages

def login_estudiante(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None and usuario.roles.id == 4:
            auth_login(request, usuario)
            return redirect('estudiantes:index_estudiantes')
        else:
            messages.error(request, 'El rol que posees no esta permitido.')
            return redirect('estudiantes:login_estudiantes')
    return render(request, 'estudiantes/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request, 'estudiantes/index.html')


def logout_estudiante(request):
    auth_logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, 'Sesión cerrada.!!')
    return redirect('estudiantes:login_estudiantes')