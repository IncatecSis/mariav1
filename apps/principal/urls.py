from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.principal.views import *
from apps.views.academica.programas import *
from apps.views.academica.modulos import *
from apps.views.academica.p_otros_academico import *
from apps.views.academica.modulo_administrar import *


urlpatterns = [

    #PARAMETROS FINANCIERO
    path('costos_generales/',login_required(costos), name='costos'),
    path('ajuste_financiero/',login_required(ajuste_financiero), name='ajustes'),

    #PARAMETROS ACADEMICOS
    path('programas/', login_required(programas), name='programas'),
    path('crear_modulos/', login_required(crear_modulos), name='modulos'),
    path('modulo_administrar/', login_required(modulo_administrar), name='administrar'),
    path('notas/', login_required(notas), name='notas'),
    path('parametros_externos/', login_required(p_otros_academico), name='otros'),
    path('documentos/', login_required(documentos), name='documentos'),
]