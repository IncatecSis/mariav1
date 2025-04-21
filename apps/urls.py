from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.views.administrar.usuarios.usuario import *
from apps.views.academica.academica import *
from apps.views.financiera.financiacion import *
from apps.views.financiera.informes import *
from apps.views.financiera.notas import *
from apps.views.financiera.pagos import *
from apps.views.administrar.parametros_academicos.p_academico import *
from apps.views.administrar.parametros_financieros.p_financiero import *
from apps.views.administrar.otros_parametros.parametros import *
from apps.views.index import *
from apps.views.rrhh.rrhh import *
from apps.views.rrhh.usuarios import *
from apps.views.rrhh.contratos import *
from apps.views.control_ingreso.ingreso import *


urlpatterns = [
    path('index/',login_required(index), name='index'),

    #----- Academica ------
    path('matricula/',login_required(matricula), name='matricula'),
    path('grupos_academicos/',login_required(grupos_academicos), name='grupos_academicos'),


    path('financiacion/',login_required(financiacion), name='finanzas'),
    path('pagos/',login_required(pagos), name='pagos'),
    path('notas/',login_required(notas), name='notas'),
    path('informes/',login_required(informes), name='informes'),
    
    #-----Talento humano------
    path('talento_humano/',login_required(talento_humano), name='talento_humano'),
    path('administrativos/',login_required(usuarios_admi), name='administrativos'),
    path('usuarios_admin/<str:numero_documento>/', buscar_usuario, name='buscar_usuario'),
    path('estado/', estado, name='estado'),
    path('generar_contrato/<int:contrato_id>/', generar_contrato, name='generar_contrato'),
    path('directivos/', login_required(directivos), name='directivos'),
    path('activar-contrato/', login_required(activar_contrato), name='activar_contrato'),

    path('control_ingreso/', login_required(control_ingreso), name='control_ingreso'),
    path('control_docente/', login_required(control_docente), name='control_docente'),
    path('control_estudiante/', login_required(control_estudiante), name='control_estudiante'),

    #Administrar
    #----- Usuarios ----------
    path('usuarios/',login_required(usuario), name='usuarios'),
    path('permisos/<int:usuario_id>/',login_required(gestion_permisos), name='permisos'),
    #path('cambiar_contraseña/',login_required(cambiar_contraseña), name='cambiar_contraseña'),

    #----- Parametros--------
    path('parametros_financieros/', login_required(parametrosf), name='parametros_financieros'),
    path('parametros_academicos/', login_required(parametrosA), name='parametros_academicos'),
    path('otros_parametros/', login_required(otros_parametros), name='parametros_externos'),
]
















#https://codeconverter.io/convert/flask-to-django