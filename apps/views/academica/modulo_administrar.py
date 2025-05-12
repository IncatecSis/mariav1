from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.views.decorators.cache import cache_control
from django.contrib import messages
from apps.principal.modelos.academico.jornadas import ModulosCompetencias
from apps.principal.modelos.academico.modulos import *
from apps.principal.modelos.academico.programa import *
from apps.principal.middleware.auditoria import *




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modulo_administrar(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')
        try:
            if tipo == 'asignar_modulo':
                id_modulo = request.POST.get('modulos')
                id_semestre = request.POST.get('semestres')
                intensidad_horaria = request.POST.get('intensidad')

                modulo = Modulos.objects.get(id_modulo=id_modulo)
                semestre = SemestresPensum.objects.get(id_semestre=id_semestre)

                ModulosCompetencias.objects.create(
                    id_modulo=modulo,
                    id_semestre=semestre,
                    intensidad_horas=intensidad_horaria
                )

                messages.success(request, '✅ Módulo asignado correctamente al semestre.')
                return redirect('Incatec_administracion:administrar')

        except IntegrityError:
            messages.error(request, '😥 Este módulo ya está asignado a ese semestre del pensum.')
        except (Modulos.DoesNotExist, SemestresPensum.DoesNotExist):
            messages.warning(request, '⚠️ Selección inválida.')
        except Exception:
            messages.error(request, '🚫 Error inesperado. Intenta de nuevo.')

    programas = ProgramasAcademicos.objects.filter(estado=True)
    pensum = Pensum.objects.select_related('id_programa').filter(activo=True)
    semestres = SemestresPensum.objects.select_related('id_pensum', 'id_pensum__id_programa')
    modulos = Modulos.objects.filter(estado=True)

    return render(request, 'modulos/administrar/p_academico/v_academico/modulo/index_administrar.html', {
        'titulo': 'Modúlo Administrar',
        'programas': programas,
        'modulos': modulos,
        'semestre': semestres,
        'pensum': pensum,
    })
