from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.cache import cache_control
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.academico.programa import Pensum
from apps.principal.modelos.academico.modulos import *


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def p_otros_academico(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')

        if tipo == 'semestres':
            try:
                pensum = Pensum.objects.get(id_pensum=request.POST.get('pensum'))

                SemestresPensum.objects.create(
                    id_pensum=pensum,
                    nombre_semestre = request.POST.get('nombre_semestre'),
                    numero_semestre = request.POST.get('numero_semestre')
                )
                messages.success(request, 'Semestre creado exitosamente.🤩')
                return redirect('Incatec_administracion:otros')
            except (Pensum.DoesNotExist):
                messages.warning(request, '⚠️ Error: Pensum no válido.')
            except Exception as e:
                print("💥 Error inesperado:", e)
                messages.warning(request, f'🚫 Error inesperado: {str(e)}')

    return render(request, 'modulos/administrar/p_academico/v_academico/otros_p/index_p.html', {
        'titulo': 'Otros Parametros',
        'pensum': Pensum.objects.all(),
        'semestres': SemestresPensum.objects.all(),
    })
