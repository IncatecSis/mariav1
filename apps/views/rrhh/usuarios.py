from django.shortcuts import render
from apps.principal.modelos.rrhh.contratos import *
from apps.principal.modelos.usuario.Usuarios import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def directivos(request):
    usuarios_rol = {}
    roles = Roles.objects.all()

    for rol in roles:
        usuarios_rol[rol.nombre_rol] = Usuarios.objects.filter(
            contrataciones__id_tipo_contrato__id_rol=rol
        ).prefetch_related('contrataciones_set').distinct().order_by('nombres')

    contratos_laborales = Contrataciones.objects.filter(
        id_tipo_contrato__id_rol__nombre_rol='COLABORADOR'
    ).select_related('id_usuario').order_by('-fecha_inicio')

    contratos_docentes = Contrataciones.objects.filter(
        id_tipo_contrato__id_rol__nombre_rol='DOCENTE'
    ).select_related('id_usuario').order_by('-fecha_inicio')

    documentos_contratos = DocumentosContrato.objects.filter(
        id_contratacion__in=contratos_laborales
    )
    docs_dict = {doc.id_contratacion.id_contratacion: doc for doc in documentos_contratos}

    for contrato in contratos_laborales:
        contrato.documentos = docs_dict.get(contrato.id_contratacion)

    contexto = {
        'usuarios_rol': usuarios_rol,
        'roles': roles,
        'contratos_laborales': contratos_laborales,
        'contratos_docentes': contratos_docentes,
        'titulo_pagina': 'Usuarios Directivos'
    }

    return render(request, 'modulos/rrhh/usuarios.html', contexto)

@require_POST
def activar_contrato(request):
    contrato_id = request.POST.get('contrato_id')
    password = request.POST.get('password')
    
    usuario = authenticate(username=request.user.username, password=password)
    if usuario is not None:
        try:
            contrato = Contrataciones.objects.get(pk=contrato_id)
            contrato.estado = True
            contrato.save()
            return JsonResponse({'success': True})
        except Contrataciones.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contrato no encontrado'})
    else:
        return JsonResponse({'success': False, 'error': 'Contraseña incorrecta'})

