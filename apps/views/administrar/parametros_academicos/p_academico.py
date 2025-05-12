from django.views.decorators.cache import cache_control
from django.shortcuts import render

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def parametros_academicos(request):
    return render(request, 'modulos/administrar/p_academico/index_parametros_a.html',{
        'titulo_pagina': 'Parámetros Academicos',
    })