from django.views.decorators.cache import cache_control
from django.shortcuts import render




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def informes(request):
    return render(request, 'modulos/financiera/informes.html',{
        'titulo_pagina': 'Informes',
    })