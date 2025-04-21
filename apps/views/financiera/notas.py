from django.views.decorators.cache import cache_control
from django.shortcuts import render




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def notas(request):
    return render(request, 'modulos/financiera/notas.html', {
        'titulo_pagina': 'Notas',
    })  