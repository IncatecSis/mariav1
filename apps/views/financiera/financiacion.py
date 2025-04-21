from django.views.decorators.cache import cache_control
from django.shortcuts import render




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def financiacion(request):
    return render(request, 'modulos/financiera/financiacion.html',{
        'titulo_pagina': 'Financiación',
    })    