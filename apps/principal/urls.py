from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.principal.views import *


urlpatterns = [

    #PARAMETROS FINANCIERO
    path('costos_generales/',login_required(costos), name='costos'),
    path('ajuste_financiero/',login_required(ajuste_financiero), name='ajustes'),

    #PARAMETROS ACADEMICOS
    path('programas/', login_required(programas), name='programas'),
    path('crear_modulos/', login_required(crear_modulos), name='modulos'),
    path('modulo_administrar/', login_required(modulo_administrar), name='administrar'),
    path('notas/', login_required(notas), name='notas'),
    path('parametros_externos/', login_required(otros), name='otros'),
    path('documentos/', login_required(documentos), name='documentos'),
]
















"""ESTO POR SI SE LLEGA A UTILIZAR EN ALGUN MOMENTO

    path('conceptos/', conceptos, name='conceptos'),
    path('ofertas/', costos, name='ofertas'),
    path('pagos/', pagos, name='pagos'),
    path('incrementos/', incrementos, name='incrementos'),
    path('configuracion/', configuracion, name='configuracion'),
"""