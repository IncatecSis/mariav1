from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.parametros.sedes import *


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otros_parametros(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')

        if tipo == 'piso':
            id_piso = request.POST.get('id_piso')
            nombre = request.POST.get('nombre_piso').upper()

            if id_piso:
                existe = Pisos.objects.filter(nombre_piso=nombre).exclude(id_piso=id_piso).exists()
                if existe:
                    messages.error(request,'El piso ya existe.🫥')
                else:
                    pisos = get_object_or_404(Pisos, id_piso=id_piso)
                    pisos.nombre_piso = nombre
                    pisos.save()
                    messages.success(request, 'Piso actualizado.')
            else:
                existe = Pisos.objects.filter(nombre_piso=nombre).exists()
                if existe:
                    messages.error(request,'El piso ya existe.🫥')
                else:
                    Pisos.objects.create(nombre_piso=nombre)
                    messages.success(request, 'Piso creado.🤩')

        elif tipo == 'area':
            id_area = request.POST.get('id_area')
            nombre = request.POST.get('nombre_area').upper()

            if id_area:
                existe = Areas.objects.filter(nombre_area=nombre).exclude(id_area=id_area).exists()
                if existe:
                    messages.error(request, 'El area ya existe.')
                else:
                    area = get_object_or_404(Areas, id_area=id_area)
                    area.nombre_area = nombre
                    area.save()
                    messages.success(request, 'Area actualizada correctamente.')
            else:
                existe = Areas.objects.filter(nombre_area=nombre).exists()
                if existe:
                    messages.error(request, 'El area ya existe')
                else:
                    Areas.objects.create(nombre_area=nombre)
                    messages.success(request, 'El area se ha creado correctamente.')

        elif tipo == 'ubicacion':
            id_ubicacion = request.POST.get('id_ubicacion')
            id_area = request.POST.get('area')
            id_piso = request.POST.get('piso')
            nombre = request.POST.get('nombre_ubicacion').upper()
            descripcion = request.POST.get('descripcion').upper()
            aforo = request.POST.get('aforo')

            existe = Ubicaciones.objects.filter(
                nombre_ubicacion=nombre,
                id_area_id=id_area,
                id_piso_id=id_piso
            )

            if id_ubicacion:
                existe = existe.exclude(id_ubicacion=id_ubicacion)

            if existe.exists():
                messages.error(request, 'La ubicación ya existe.')
            else:
                if id_ubicacion:
                    ubicacion = get_object_or_404(Ubicaciones, id_ubicacion=id_ubicacion)
                    ubicacion.id_area_id = id_area
                    ubicacion.id_piso_id = id_piso
                    ubicacion.nombre_ubicacion = nombre
                    ubicacion.descripcion = descripcion
                    ubicacion.aforo = aforo
                    ubicacion.save()
                    messages.success(request, 'Ubicación actualizada correctamente.')
                else:
                    Ubicaciones.objects.create(
                        id_area_id=id_area,
                        id_piso_id=id_piso,
                        nombre_ubicacion=nombre,
                        descripcion=descripcion,
                        aforo=aforo,
                        activo=True
                    )
                    messages.success(request, 'Ubicación creada correctamente.')

        return redirect('Incatec:parametros_externos')
    areas = [2,3,4]
    contexto = {
        'pisos': Pisos.objects.all(),
        'areas': Areas.objects.filter(id_area__in=areas),
        'ubicaciones': Ubicaciones.objects.all(), 
        'titulo_pagina': 'Otros Parámetros',
    }            
    return render(request, 'modulos/administrar/p_otros/index_otros_p.html', contexto)