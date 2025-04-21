from django.views.decorators.cache import cache_control
from django.shortcuts import render
#from apps.views.topbar import topbar_general


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otros_parametros(request):
    return render(request, 'modulos/administrar/p_otros/index_otros_p.html',{
        'titulo_pagina': 'Otros Parámetros',
    })