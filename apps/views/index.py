from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.parametros.sedes import Sedes
from apps.principal.modelos.permisos.permisos import UsuarioPermisos




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.method == 'POST' and request.POST.get('seleccionar_sede'):
        context_usuario(request)
        sede_id = request.POST.get('sede')
        if sede_id:
            request.session['sede_id'] = sede_id
            return redirect('Incatec:index')
    
    if request.user.is_authenticated and not request.session.get('permisos'):
        permisos_usuario = UsuarioPermisos.objects.filter(
            id_usuario=request.user.id_usuario.id_usuario
        ).values_list('id_permiso__codigo', flat=True)
        request.session['permisos'] = list(permisos_usuario)

    sede = Sedes.objects.filter(estado=True)
    return render(request, 'index/index.html', {
        'sedes': sede,
    })