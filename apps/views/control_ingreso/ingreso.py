from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def control_ingreso(request):
    return render(request, 'modulos/control_ingreso/ingreso.html', {
        'titulo_pagina': 'Control Administrativo'
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def control_estudiante(request):
    return render(request, 'modulos/control_ingreso/estudiantes.html', {
        'titulo_pagina': 'Control Estudiante'
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def control_docente(request):
    return render(request, 'modulos/control_ingreso/docentes.html', {
        'titulo_pagina': 'Control Docente'
    })