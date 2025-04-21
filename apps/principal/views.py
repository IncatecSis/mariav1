from django.shortcuts import render
#from apps.views.topbar import topbar_general


"""
SECCION DE PARAMETROS FINANCIEROS POR SI SE LLEGA A UTILIZAR EN ALGUN MOMENTO

def conceptos(request):
    return render(request, 'modulos/ventana_f/conceptos.html')


def pagos(request):
    return render(request, 'modulos/ventana_f/pagos.html')


def configuracion(request):
    return render(request, 'modulos/ventana_f/configuracion.html')

"""
def costos(request):
    '''
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Costos',
    })
    '''
    return render(request, 'modulos/administrar/p_financiero/v_financiero/costos.html')

def ajuste_financiero(request):
    '''
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Ajuste financiero',
    })
    '''
    return render(request, 'modulos/administrar/p_financiero/v_financiero/ajustes.html')

###------------------------------------------------------------###


"""
SECCION DE PARAMETROS ACADEMICOS
"""

def programas(request):
    '''
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Programas',
    })
    '''
    return render(request, 'modulos/administrar/p_academico/v_academico/programas.html')

def crear_modulos(request):
    '''
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Modúlos',
    })
    '''
    return render(request, 'modulos/administrar/p_academico/v_academico/seccion_modulo/index_modulo.html')

def modulo_administrar(request):
    '''
    
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Modúlo Administrar',
    })
    '''
    return render(request, 'modulos/administrar/p_academico/v_academico/modulo/index_administrar.html')

def notas(request):
    '''
    
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Notas',
    })
    '''
    return render(request, 'modulos/administrar/p_academico/v_academico/seccion_notas/index_notas.html')

def otros(request):
    '''
    
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Otros parametros',
    })
    '''
    return render(request, 'modulos/administrar/p_academico/v_academico/otros_p/index_p.html')

def documentos(request):
    '''
    
    contexto = topbar_general(request)
    contexto.update({
        'titulo_pagina':'Documentos',
    })
    '''
    return render(request, 'modulos/administrar/p_otros/v_otros/documentos.html')