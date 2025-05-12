from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib import messages
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.academico.modulos import *
from apps.principal.modelos.academico.programa import *
from django.views.decorators.cache import cache_control



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crear_modulos(request):
    if request.method == 'POST':
        context_usuario(request)
        try:
            sede = Sedes.objects.get(id_sede=request.POST.get('sedes'))
            tipo = TiposModulo.objects.get(id_tipo_modulo=request.POST.get('tipo_modulo'))

            Modulos.objects.create(
                nombre_modulo = request.POST.get('modulo_nombre'),
                descripcion = request.POST.get('descripcion_modulo'),
                estado= True,
                id_sede=sede,
                id_tipo_modulo=tipo,
                created_at=now(),
                updated_at=now()
            )
            messages.success(request, 'Modúlo creado exitosamente.🤩')
            return redirect('Incatec_administracion:modulos')
        except (Sedes.DoesNotExist, TiposModulo.DoesNotExist):
            messages.warning(request, '⚠️ Error: Sede o Tipo de Escuela no válidos.')
        except Exception as e:
            print("💥 Error inesperado:", e)
            messages.warning(request, f'🚫 Error inesperado: {str(e)}')

    return render(request, 'modulos/administrar/p_academico/v_academico/seccion_modulo/index_modulo.html', {
        'titulo':'Modúlos',
        'tipo_modulos': TiposModulo.objects.all(),
        'sedes': Sedes.objects.filter(estado=True),
    })