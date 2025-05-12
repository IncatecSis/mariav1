from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.views.administrar.usuarios.usuario import *
from apps.views.academica.academica import *
from apps.views.chat.chat import *
from apps.views.financiera.financiacion import *
from apps.views.financiera.informes import *
from apps.views.financiera.notas import *
from apps.views.financiera.pagos import *
from apps.views.administrar.parametros_academicos.p_academico import *
from apps.views.administrar.parametros_financieros.p_financiero import *
from apps.views.administrar.otros_parametros.parametros import *
from apps.views.index import *
from apps.views.permisos.permisos import *
from apps.views.rrhh.rrhh import *
from apps.views.rrhh.usuarios import *
from apps.views.rrhh.contratos import *
from apps.views.control_ingreso.ingreso import *
from .principal.decoradores.decorador import requerir_permiso

urlpatterns = [
    path('index/', login_required(index), name='index'),
    
    #----- Academica ------
    path('matricula/', login_required(requerir_permiso('REGISTRO_MATRICULA')(matricula)), name='matricula'),
    path('grupos_academicos/', login_required(requerir_permiso('GRUPOS_ACADEMICOS')(grupos_academicos)), name='grupos_academicos'),
    path('buscar_estudiante/<str:numero_documento>/', login_required(requerir_permiso('REGISTRO_MATRICULA')(buscar_estudiante)), name='buscar_estudiante'),
    
    #----- Financiera ------
    path('financiacion/', login_required(requerir_permiso('FINANCIACION')(financiacion)), name='finanzas'),
    path('pagos/', login_required(requerir_permiso('PAGOS')(pagos)), name='pagos'),
    path('notas/', login_required(requerir_permiso('NOTAS_DYC')(notas)), name='notas'),
    path('informes/', login_required(requerir_permiso('INFORMES_PAGOS')(informes)), name='informes'),
    
    #----- Talento humano ------
    path('talento_humano/', login_required(requerir_permiso('TALENTO_HUMANO_GENERAL')(talento_humano)), name='talento_humano'),
    path('administrativos/', login_required(requerir_permiso('ADMINISTRATIVOS')(usuarios_admi)), name='administrativos'),
    path('usuarios_admin/<str:numero_documento>/', login_required(requerir_permiso('ADMINISTRATIVOS')(buscar_usuario)), name='buscar_usuario'),
    path('estado/', login_required(requerir_permiso('TALENTO_HUMANO_GENERAL')(estado)), name='estado'),
    path('generar_contrato/<int:contrato_id>/', login_required(requerir_permiso('GESTION_CONTRATOS')(generar_contrato)), name='generar_contrato'),
    path('directivos/', login_required(requerir_permiso('DIRECTIVOS')(directivos)), name='directivos'),
    path('activar-contrato/', login_required(requerir_permiso('GESTION_CONTRATOS')(activar_contrato)), name='activar_contrato'),
    
    #----- Control de Ingreso ------
    path('control_ingreso/', login_required(requerir_permiso('CONTROL_ADMINISTRATIVO')(control_ingreso)), name='control_ingreso'),
    path('control_docente/', login_required(requerir_permiso('CONTROL_DOCENTE')(control_docente)), name='control_docente'),
    path('control_estudiante/', login_required(requerir_permiso('CONTROL_ESTUDIANTE')(control_estudiante)), name='control_estudiante'),
    
    #----- Usuarios ----------
    path('usuarios/', login_required(requerir_permiso('GESTION_USUARIOS')(usuario)), name='usuarios'),

    #----- Permisos ----------
    path('permisos/<int:usuario_id>/', login_required(requerir_permiso('GESTION_PERMISOS')(gestion_permisos)), name='permisos'),
    
    #----- Parametros ------
    path('parametros_financieros/', login_required(requerir_permiso('PARAMETROS_FINANCIEROS')(parametros_financiero)), name='parametros_financieros'),
    path('parametros_academicos/', login_required(requerir_permiso('PARAMETROS_ACADEMICOS')(parametros_academicos)), name='parametros_academicos'),
    path('otros_parametros/', login_required(requerir_permiso('OTROS_PARAMETROS')(otros_parametros)), name='parametros_externos'),

    #----- Apartado de Chat ----
    path('chat/', login_required(requerir_permiso('CHAT')(chat)), name='chat'),
    path('crear_chat/', login_required(requerir_permiso('CHAT')(crear_conversacion)), name='chat_conversacion'),
    path('enviar_mensaje/', login_required(requerir_permiso('CHAT')(enviar_mensaje)), name='enviar_msj'),
    path('agregar_participantes/', login_required(requerir_permiso('CHAT')(agregar_participantes)), name='agregar_participantes'),
    path('reaccionar_mensaje/', login_required(requerir_permiso('CHAT')(reaccionar_mensaje)), name='reaccion'),
    path('salir_conversacion/', login_required(requerir_permiso('CHAT')(salir_conversacion)), name='salir_conversacion'),
    path('eliminar_conversacion/', login_required(requerir_permiso('CHAT')(eliminar_conversacion)), name='eliminar_conversacion'),
    path('nuevos_mensajes/', login_required(requerir_permiso('CHAT')(nuevos_mensajes)), name='nuevos_mensajes'),
] 