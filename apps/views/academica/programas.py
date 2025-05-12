from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.academico.programa import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def programas(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')

        if tipo == 'programas':
            try:
                tipo = TiposProgramas.objects.get(id_tipos_programas=request.POST.get('tipo_programa'))
                sede = Sedes.objects.get(id_sede=request.POST.get('sedess'))
                escuela = Escuelas.objects.get(id_escuelas=request.POST.get('escuelas'))

                ProgramasAcademicos.objects.create(
                    nombre_programa=request.POST.get('nombre_programa'),
                    descripcion=request.POST.get('descripcion'),
                    codigo_siet=request.POST.get('codigo_siet'),
                    fecha_inicio=request.POST.get('fecha_inicio'),
                    duracion=int(request.POST.get('duracion') or 0),
                    fecha_fin=request.POST.get('fecha_vencimiento'),
                    id_periodo=request.POST.get('periodo'),
                    numero_registro=request.POST.get('numero_registro'),
                    numero_certificacion=request.POST.get('certificacion'),
                    codigo_centro_costo=request.POST.get('centro_costo') or None,
                    acto_administrativo_pdf=request.FILES.get('acto_admi'),
                    id_tipos_programas=tipo,
                    id_sede=sede,
                    id_escuelas=escuela,
                    estado=True
                )

                messages.success(request, 'Programa creado exitosamente.🤩')
                return redirect('Incatec_administracion:programas')

            except (TiposProgramas.DoesNotExist, Sedes.DoesNotExist, Escuelas.DoesNotExist):
                messages.warning(request, '⚠️ Error: Tipo, sede o escuela no válidos.')
            except Exception as e:
                print("💥 Error inesperado:", e)
                messages.warning(request, f'🚫 Error inesperado: {str(e)}')

        elif tipo == 'pensum': 
            try:
                programa = ProgramasAcademicos.objects.get(id_programa=request.POST.get('programas'))
                Pensum.objects.create(
                    nombre = request.POST.get('nombre_pensum'),
                    id_programa = programa,
                    anio_vigencia=request.POST.get('anio_vigencia'),
                    activo = True,
                )
                messages.success(request, 'Pensum creado exitosamente.🤩')
                return redirect('Incatec_administracion:programas')
            except (ProgramasAcademicos.DoesNotExist):
                messages.warning(request, '⚠️ Error: Pensum no válido.')
            except Exception as e:
                print("💥 Error inesperado:", e)
                messages.warning(request, f'🚫 Error inesperado: {str(e)}')

        elif tipo == 'desactivar_pensum':
            id_pensum = request.POST.get('id_pensum')
            try:
                pensum = Pensum.objects.get(id_pensum=id_pensum, activo=True)
                pensum.activo = False
                pensum.save()
                return JsonResponse({'success': True, 
                                    'message': 'Pensum desactivado correctamente.'
                                    })
            except Pensum.DoesNotExist:
                return JsonResponse({'success': False, 
                                    'message': 'El Pensum ya estaba inactivo o no existe.'
                                    })
            except Exception as e:
                return JsonResponse({'success': False, 
                                    'message': f'Ocurrió un error: {str(e)}'
                                    })


    contexto = {
        'tipos_programas': TiposProgramas.objects.all(),
        'sedes': Sedes.objects.all(),
        'escuelas': Escuelas.objects.all(),
        'programas': ProgramasAcademicos.objects.all(),
        'pensum': Pensum.objects.filter(activo=True),
        'titulo': 'Programas Académicos'
    }
    return render(request, 'modulos/administrar/p_academico/v_academico/programas.html', contexto)
