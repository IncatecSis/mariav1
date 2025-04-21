from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.cache import cache_control
#from apps.principal.modelos.sedes import Sede
#from apps.principal.modelos.periodo import Periodo



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        print("✅ Usuario autenticado correctamente:", request.user.username)
    else:
        print("❌ Usuario NO autenticado")

    return render(request, 'index/index.html')

    '''
    sede_id = request.session.get('sede_id')
    periodo_id = request.session.get('periodo_id')

    sede_choices = [(s.id, s.nombre) for s in Sede.objects.all()]
    periodo_choices = [
        (p.id, f"{p.anio} - {dict(Periodo.SEMESTRE_CHOICE).get(p.semestre)}")
        for p in Periodo.objects.all()
    ]

    if request.method == 'POST' and request.POST.get('cambiar_sede_periodo') == 'true':
        request.session.pop('sede_id', None)
        request.session.pop('periodo_id', None)
        return redirect('Incatec:index')

    # Crear nueva sede
    if request.method == 'POST' and 'crear_sede' in request.POST:
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        if nombre and direccion:
            Sede.objects.create(nombre=nombre, direccion=direccion)
            messages.success(request, '¡Sede creada con éxito!')
            return redirect('Incatec:index')
        else:
            messages.error(request, 'Todos los campos son obligatorios para crear una sede.')

    # Crear nuevo periodo
    if request.method == 'POST' and 'crear_periodo' in request.POST:
        anio = request.POST.get('anio')
        semestre = request.POST.get('semestre')
        try:
            anio = int(anio)
            semestre = int(semestre)
            if semestre not in [1, 2]:
                messages.error(request, 'El semestre debe ser 1 (A) o 2 (B).')
            else:
                Periodo.objects.create(anio=anio, semestre=semestre)
                messages.success(request, '¡Periodo creado con éxito!')
                return redirect('Incatec:index')
        except ValueError:
            messages.error(request, 'El año y el semestre deben ser valores numéricos.')

    # Seleccionar sede y periodo
    if request.method == 'POST' and 'seleccionar_sede_periodo' in request.POST:
        sede_id = request.POST.get('sede')
        periodo_id = request.POST.get('periodo')

        if sede_id and periodo_id:
            request.session['sede_id'] = sede_id
            request.session['periodo_id'] = periodo_id
            return redirect('Incatec:index')
        else:
            messages.error(request, 'Se debe elegir una sede y un periodo.')

    nombre_sede = get_object_or_404(Sede, id=sede_id).nombre if sede_id else None
    nombre_periodo = None
    if periodo_id:
        periodo = get_object_or_404(Periodo, id=periodo_id)
        nombre_periodo = f"{periodo.anio} - {dict(Periodo.SEMESTRE_CHOICE).get(periodo.semestre)}"

    return render(request, 'index/index.html', {
        'sede_choices': sede_choices,
        'periodo_choices': periodo_choices,
        'nombre_sede': nombre_sede,
        'nombre_periodo': nombre_periodo,
    })

    '''