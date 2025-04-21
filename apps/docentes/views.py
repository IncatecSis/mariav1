from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from django.contrib import messages


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_docente(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None and usuario.roles.id == 3:
            auth_login(request, usuario)
            return redirect('docentes:index_docentes')
        else:
            messages.error(request, 'El rol que posees no esta permitido.')
            return redirect('docentes:login_docentes')
    return render(request, 'docentes/login.html')

def index(request):
    return render(request, 'docentes/index.html')

def logout_docente(request):
    auth_logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, 'Sesión cerrada.!!')
    return redirect('docentes:login_docentes')