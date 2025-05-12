## ESTE SI LO MOVI
# Vista completa para apps/views/permisos/permisos.py
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from apps.principal.decoradores.decorador import requerir_permiso
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.permisos.permisos import *
from apps.principal.modelos.usuario.Usuarios import Usuarios



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def gestion_permisos(request, usuario_id=None):
    if usuario_id == 0 and request.GET.get('q'):
        termino = request.GET.get('q', '').strip()
        usuarios_busqueda = []
        
        if len(termino) >= 3:
            usuarios_busqueda = Usuarios.objects.filter(
                models.Q(numero_documento__icontains=termino) |
                models.Q(nombres__icontains=termino) |
                models.Q(apellidos__icontains=termino)
            ).values('id_usuario', 'numero_documento', 'nombres', 'apellidos', 'correo_electronico')[:10]
        
        context = {
            'titulo': 'Resultados de búsqueda',
            'mostrar_solo_busqueda': True,
            'usuarios_busqueda': usuarios_busqueda,
        }
        return render(request, 'modulos/permisos/permiso.html', context)
    
    if usuario_id is None or usuario_id == 0:
        context = {
            'titulo': 'Buscar Usuario para Gestión de Permisos',
            'mostrar_solo_busqueda': True,
        }
        return render(request, 'modulos/permisos/permiso.html', context)
    
    usuario = get_object_or_404(Usuarios, id_usuario=usuario_id)
    
    permisos_por_modulo = {}
    for permiso in Permisos.objects.all().order_by('modulo', 'nombre'):
        if permiso.modulo not in permisos_por_modulo:
            permisos_por_modulo[permiso.modulo] = []
        permisos_por_modulo[permiso.modulo].append(permiso)
    
    permisos_usuario = UsuarioPermisos.objects.filter(
        id_usuario=usuario
    ).values_list('id_permiso__id_permiso', flat=True)
    
    if request.method == 'POST':
        context_usuario(request)
        permisos_seleccionados = request.POST.getlist('permisos')
        
        permisos_seleccionados_ids = [int(id) for id in permisos_seleccionados]
        
        permisos_a_anadir = set(permisos_seleccionados_ids) - set(permisos_usuario)
        
        permisos_a_eliminar = set(permisos_usuario) - set(permisos_seleccionados_ids)
        
        # Corregido: Usamos id_usuario.id_usuario para obtener el ID numérico
        for permiso_id in permisos_a_anadir:
            UsuarioPermisos.objects.create(
                id_usuario_id=usuario.id_usuario,  # Aquí especificamos que es el ID
                id_permiso_id=permiso_id,
                asignado_por_id=request.user.id_usuario.id_usuario  # También aquí
            )

        UsuarioPermisos.objects.filter(
            id_usuario=usuario,
            id_permiso__id_permiso__in=permisos_a_eliminar
        ).delete()
        
        messages.success(request, f'Permisos actualizados para {usuario.nombres} {usuario.apellidos}')
        return redirect('Incatec:permisos', usuario_id=usuario.id_usuario)
    
    context = {
        'usuario': usuario,
        'permisos_por_modulo': permisos_por_modulo,
        'permisos_usuario': list(permisos_usuario),
        'titulo': 'Gestión de Permisos',
        'mostrar_solo_busqueda': False,
    }
    
    return render(request, 'modulos/permisos/permiso.html', context)