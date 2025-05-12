import json
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Count, Prefetch
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse

from apps.principal.modelos.usuario.Usuarios import Usuarios
from apps.principal.modelos.chat.chats import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chat(request):
    # Obtenemos el número de documento del usuario autenticado
    numero_documento = request.user.username  # Asumiendo que usas el número de documento como username
    
    try:
        # Obtenemos la instancia de Usuarios que corresponde al usuario autenticado
        usuario = Usuarios.objects.get(numero_documento=numero_documento)
        
        # Ahora usamos la instancia de Usuarios para nuestras consultas
        participaciones = ParticipanteConversacion.objects.filter(
            usuario=usuario,
            estado_participacion='activo'
        ).select_related('conversacion')
        
        # Obtenemos las conversaciones donde el usuario participa
        conversaciones_ids = participaciones.values_list('conversacion', flat=True)
        
        # Obtenemos las últimas conversaciones activas
        conversaciones = Conversacion.objects.filter(estado=True,
            id_conversacion__in=conversaciones_ids
        ).annotate(
            ultimo_mensaje_fecha=Max('mensajes__fecha_envio'),
            mensajes_no_leidos=Count(
                'mensajes',
                filter=Q(mensajes__estado='enviado') & 
                      ~Q(mensajes__remitente=usuario) & 
                      ~Q(mensajes__lecturas__usuario=usuario)
            )
        ).order_by('-ultima_actividad')
        
        # Conversación activa (podría ser pasada por parámetros)
        conversacion_activa_id = request.GET.get('conversacion')
        conversacion_activa = None
        mensajes = []
        archivos_recientes = []
        contactos_disponibles = []
        
        if conversacion_activa_id:
            # Buscar la conversación por su clave primaria
            conversacion_activa = get_object_or_404(
                Conversacion, 
                id_conversacion=conversacion_activa_id
            )
            
            # Verificar que el usuario es participante de esta conversación
            es_participante = ParticipanteConversacion.objects.filter(
                conversacion=conversacion_activa,
                usuario=usuario,
                estado_participacion='activo'
            ).exists()
            
            if not es_participante:
                return redirect('chat')  # Redirigir si no es participante
            
            # Cargar mensajes de la conversación activa con paginación
            mensajes_query = Mensaje.objects.filter(
                conversacion=conversacion_activa
            ).select_related(
                'remitente'
            ).prefetch_related(
                'adjuntos',
                'reacciones',
                'menciones',
                Prefetch(
                    'lecturas',
                    queryset=LecturaMensaje.objects.filter(usuario=usuario),
                    to_attr='leido_por_usuario_actual'
                )
            ).order_by('fecha_envio')
            
            # Obtener mensajes
            paginator = Paginator(mensajes_query, 20)
            page = request.GET.get('page', paginator.num_pages)
            mensajes = paginator.get_page(page)
            
            # Marcar mensajes como leídos
            for mensaje in mensajes:
                if (mensaje.remitente != usuario and 
                    mensaje.estado == 'enviado' and 
                    not hasattr(mensaje, 'leido_por_usuario_actual')):
                    
                    LecturaMensaje.objects.create(
                        mensaje=mensaje,
                        usuario=usuario
                    )
                    mensaje.estado = 'leido'
                    mensaje.save(update_fields=['estado'])
            
            # Obtener archivos recientes para el panel de información
            mensajes_con_adjuntos = Mensaje.objects.filter(
                conversacion=conversacion_activa,
                adjuntos__isnull=False
            ).order_by('-fecha_envio').distinct()[:10]
            
            archivos_recientes = []
            for mensaje in mensajes_con_adjuntos:
                adjuntos = mensaje.adjuntos.all()
                if adjuntos.exists():
                    archivos_recientes.append(mensaje)
            
            # Obtener IDs de usuarios que ya están en la conversación
            participantes_ids = ParticipanteConversacion.objects.filter(
                conversacion=conversacion_activa
            ).values_list('usuario', flat=True)
            
            # Filtrar contactos que no están en la conversación
            contactos_disponibles = Usuarios.objects.exclude(
                id_usuario__in=participantes_ids
            ).exclude(
                id_usuario=usuario.id_usuario
            ).order_by('nombres')
        
        # Contactos para iniciar nuevas conversaciones
        contactos = Usuarios.objects.exclude(id_usuario=usuario.id_usuario).order_by('nombres')
        
        return render(request, 'modulos/chat/chat.html', {
            'titulo': 'Chat',
            'conversaciones': conversaciones,
            'conversacion_activa': conversacion_activa,
            'mensajes': mensajes,
            'contactos': contactos,
            'usuario_actual': usuario,  # Pasamos el usuario a la plantilla
            'archivos_recientes': archivos_recientes,  # Archivos para el panel de información
            'contactos_disponibles': contactos_disponibles  # Contactos que no están en la conversación activa
        })
        
    except Usuarios.DoesNotExist:
        # Si el usuario no existe, redirigimos al login
        return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def crear_conversacion(request):
    if request.method == 'POST':
        numero_documento = request.user.username

        try:
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            try:
                datos = json.loads(request.body)
            except Exception as e:
                print("⛔ Error parseando JSON del request.body:")
                traceback.print_exc()
                return JsonResponse({'error': 'JSON inválido'}, status=400)

            titulo = datos.get('titulo', '').strip()
            tipo = datos.get('tipo', 'individual')
            participantes_ids = datos.get('participantes', [])

            if not participantes_ids:
                return JsonResponse({'error': 'Debe seleccionar al menos un participante'}, status=400)

            conversacion = Conversacion.objects.create(
                titulo=titulo if titulo else 'Nueva conversación',
                tipo_conversacion=tipo,
                creador=usuario
            )

            ParticipanteConversacion.objects.create(
                conversacion=conversacion,
                usuario=usuario,
                rol_participante='admin'
            )

            for participante_id in participantes_ids:
                try:
                    participante = Usuarios.objects.get(id_usuario=participante_id)
                    ParticipanteConversacion.objects.create(
                        conversacion=conversacion,
                        usuario=participante
                    )

                    NotificacionChat.objects.create(
                        usuario=participante,
                        conversacion=conversacion,
                        tipo_notificacion='invitacion',
                        contenido=f"{usuario.nombres} te ha añadido a la conversación '{conversacion.titulo}'"
                    )
                except Usuarios.DoesNotExist:
                    pass

            return JsonResponse({
                'id': conversacion.id_conversacion,
                'titulo': conversacion.titulo,
                'redirect': reverse('Incatec:chat') + '?conversacion=' + str(conversacion.id_conversacion)
            })

        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            print("⛔ Error inesperado al crear la conversación:")
            traceback.print_exc()
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def enviar_mensaje(request):
    if request.method == 'POST':
        numero_documento = request.user.username

        try:
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            conversacion_id = request.POST.get('conversacion')
            contenido = request.POST.get('contenido', '').strip()
            mensaje_padre_id = request.POST.get('respuesta_a')
            adjuntos = request.FILES.getlist('adjuntos')

            if not contenido and not adjuntos:
                return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)

            try:
                conversacion = Conversacion.objects.get(
                    pk=conversacion_id,
                    participantes__usuario=usuario,
                    participantes__estado_participacion='activo'
                )

                mensaje_padre = None
                if mensaje_padre_id:
                    mensaje_padre = get_object_or_404(Mensaje, id_mensaje=mensaje_padre_id, conversacion=conversacion)

                mensaje = Mensaje.objects.create(
                    conversacion=conversacion,
                    remitente=usuario,
                    contenido=contenido,
                    mensaje_padre=mensaje_padre
                )

                conversacion.ultima_actividad = timezone.now()
                conversacion.save(update_fields=['ultima_actividad'])

                for archivo in adjuntos:
                    tipo_archivo = determinar_tipo_archivo(archivo.name)

                    AdjuntoMensaje.objects.create(
                        mensaje=mensaje,
                        tipo_archivo=tipo_archivo,
                        nombre_archivo=archivo.name,
                        archivo=archivo,
                        tamaño_bytes=archivo.size
                    )

                procesar_menciones(mensaje, contenido)
                notificar_mensaje(mensaje)

                return JsonResponse({
                    'id': mensaje.id_mensaje,
                    'contenido': mensaje.contenido,
                    'fecha': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
                    'remitente': {
                        'id': usuario.id_usuario,
                        'nombre': usuario.nombres
                    }
                })

            except Conversacion.DoesNotExist:
                return JsonResponse({'error': 'Conversación no encontrada o no tienes acceso'}, status=404)

        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cargar_mensajes_anteriores(request):
    # Obtenemos el usuario actual
    numero_documento = request.user.username
    
    try:
        usuario = Usuarios.objects.get(numero_documento=numero_documento)
        conversacion_id = request.GET.get('conversacion')
        page = request.GET.get('page', 1)
        
        try:
            conversacion = get_object_or_404(
                Conversacion, 
                pk=conversacion_id,
                participantes__usuario=usuario
            )
            
            mensajes_query = Mensaje.objects.filter(
                conversacion=conversacion
            ).select_related(
                'remitente'
            ).prefetch_related(
                'adjuntos',
                'reacciones'
            ).order_by('fecha_envio')
            
            paginator = Paginator(mensajes_query, 20)
            mensajes = paginator.get_page(page)
            
            mensajes_data = []
            for mensaje in mensajes:
                mensajes_data.append({
                    'id': mensaje.id,
                    'contenido': mensaje.contenido,
                    'fecha': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
                    'remitente': {
                        'id': mensaje.remitente.id_usuario,
                        'nombre': mensaje.remitente.nombres
                    },
                    'editado': mensaje.editado,
                    'tiene_adjuntos': mensaje.adjuntos.exists()
                })
            
            return JsonResponse({
                'mensajes': mensajes_data,
                'hay_mas': mensajes.has_previous(),
                'pagina_anterior': mensajes.previous_page_number() if mensajes.has_previous() else None
            })
            
        except Conversacion.DoesNotExist:
            return JsonResponse({'error': 'Conversación no encontrada'}, status=404)
    
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reaccionar_mensaje(request):
    if request.method == 'POST':
        # Obtenemos el usuario actual
        numero_documento = request.user.username
        
        try:
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            datos = json.loads(request.body)
            
            mensaje_id = datos.get('mensaje')
            tipo_reaccion = datos.get('reaccion')
            
            try:
                mensaje = Mensaje.objects.get(
                    id=mensaje_id,
                    conversacion__participantes__usuario=usuario,
                    conversacion__participantes__estado_participacion='activo'
                )
                
                # Verificar si ya existe la reacción para este usuario y mensaje
                reaccion, creada = ReaccionMensaje.objects.get_or_create(
                    mensaje=mensaje,
                    usuario=usuario,
                    tipo_reaccion=tipo_reaccion
                )
                
                # Si no fue creada, significa que ya existía, entonces la eliminamos
                if not creada:
                    reaccion.delete()
                    return JsonResponse({'accion': 'eliminada'})
                
                return JsonResponse({'accion': 'agregada'})
                
            except Mensaje.DoesNotExist:
                return JsonResponse({'error': 'Mensaje no encontrado'}, status=404)
        
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Funciones de utilidad para el chat

def determinar_tipo_archivo(nombre_archivo):
    """Determina el tipo de archivo basado en su extensión"""
    extension = nombre_archivo.split('.')[-1].lower()
    
    # Mapeo de extensiones comunes
    if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
        return 'imagen'
    elif extension in ['doc', 'docx', 'pdf', 'txt', 'xls', 'xlsx', 'ppt', 'pptx']:
        return 'documento'
    elif extension in ['mp3', 'wav', 'ogg', 'aac']:
        return 'audio'
    elif extension in ['mp4', 'avi', 'mov', 'wmv', 'mkv']:
        return 'video'
    else:
        return 'otro'

def procesar_menciones(mensaje, contenido):
    """Identifica menciones en el contenido y registra notificaciones"""
    # Buscar patrones de mención: @usuario
    menciones = []
    palabras = contenido.split()
    
    for palabra in palabras:
        if palabra.startswith('@'):
            nombre_usuario = palabra[1:].strip('.,!?;:')
            try:
                # Buscar por nombres en lugar de nombre
                usuario = Usuarios.objects.filter(nombres__icontains=nombre_usuario).first()
                
                if usuario:
                    # Verificar que el usuario sea participante de la conversación
                    if ParticipanteConversacion.objects.filter(
                        conversacion=mensaje.conversacion,
                        usuario=usuario,
                        estado_participacion='activo'
                    ).exists():
                        # Evitar duplicados
                        if usuario not in menciones:
                            menciones.append(usuario)
                            
                            # Crear registro de mención
                            MencionMensaje.objects.create(
                                mensaje=mensaje,
                                usuario_mencionado=usuario
                            )
            except Exception:
                # Ignorar errores
                pass

def notificar_mensaje(mensaje):
    """Crea notificaciones para los participantes de la conversación"""
    # Obtener todos los participantes activos excepto el remitente
    participantes = ParticipanteConversacion.objects.filter(
        conversacion=mensaje.conversacion,
        estado_participacion='activo'
    ).exclude(
        usuario=mensaje.remitente
    ).select_related('usuario')
    
    for participante in participantes:
        # Solo notificar si tienen notificaciones activas
        if participante.notificaciones_activas:
            NotificacionChat.objects.create(
                usuario=participante.usuario,
                mensaje=mensaje,
                conversacion=mensaje.conversacion,
                tipo_notificacion='mensaje_nuevo',
                contenido=f"Nuevo mensaje de {mensaje.remitente.nombres} en {mensaje.conversacion.titulo}"
            )

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def salir_conversacion(request):
    if request.method == 'POST':
        try:
            # Obtener el usuario actual
            numero_documento = request.user.username
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            
            # Obtener datos de la solicitud
            datos = json.loads(request.body)
            conversacion_id = datos.get('conversacion')
            
            if not conversacion_id:
                return JsonResponse({'error': 'ID de conversación no proporcionado'}, status=400)
            
            # Verificar que la conversación existe
            conversacion = get_object_or_404(Conversacion, id_conversacion=conversacion_id)
            
            # Verificar que el usuario es participante de la conversación
            participante = get_object_or_404(
                ParticipanteConversacion,
                conversacion=conversacion,
                usuario=usuario,
                estado_participacion='activo'
            )
            
            # Si es el único participante o es el creador y es un chat grupal, ofrecer eliminar la conversación
            es_unico = ParticipanteConversacion.objects.filter(
                conversacion=conversacion,
                estado_participacion='activo'
            ).count() == 1
            
            es_admin = participante.rol_participante == 'admin'
            
            if es_unico:
                # Si es el único, marcar la conversación como eliminada
                # Usamos False para indicar que está inactiva/eliminada
                conversacion.estado = False
                conversacion.save(update_fields=['estado'])
                return JsonResponse({'success': True, 'eliminada': True})
            
            elif es_admin and conversacion.tipo_conversacion in ['grupal', 'anuncio']:
                # Si es administrador de un grupo, puede salir pero mantener la conversación
                # Cambiar su estado de participación a 'inactivo'
                participante.estado_participacion = 'inactivo'
                participante.save(update_fields=['estado_participacion'])
                
                # Verificar si hay otros administradores
                hay_otros_admins = ParticipanteConversacion.objects.filter(
                    conversacion=conversacion, 
                    rol_participante='admin',
                    estado_participacion='activo'
                ).exclude(usuario=usuario).exists()
                
                # Si no hay otros administradores, asignar a otro participante como admin
                if not hay_otros_admins:
                    # Obtener otro participante activo
                    otro_participante = ParticipanteConversacion.objects.filter(
                        conversacion=conversacion,
                        estado_participacion='activo'
                    ).first()
                    
                    if otro_participante:
                        otro_participante.rol_participante = 'admin'
                        otro_participante.save(update_fields=['rol_participante'])
                        
                        # Notificar al nuevo administrador
                        NotificacionChat.objects.create(
                            usuario=otro_participante.usuario,
                            conversacion=conversacion,
                            tipo_notificacion='cambio_rol',
                            contenido=f"Ahora eres administrador de la conversación '{conversacion.titulo}'"
                        )
                
                # Crear mensaje para notificar la salida utilizando el usuario actual como remitente
                Mensaje.objects.create(
                    conversacion=conversacion,
                    remitente=usuario,
                    contenido=f"{usuario.nombres} ha salido de la conversación"
                )
                
                return JsonResponse({'success': True})
            
            else:
                # Para chats individuales o participantes regulares, simplemente salir
                participante.estado_participacion = 'inactivo'
                participante.save(update_fields=['estado_participacion'])
                
                # Crear mensaje para notificar la salida utilizando el usuario actual como remitente
                Mensaje.objects.create(
                    conversacion=conversacion,
                    remitente=usuario,
                    contenido=f"{usuario.nombres} ha salido de la conversación"
                )
                
                return JsonResponse({'success': True})
            
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            print("Error al salir de la conversación:", e)
            traceback.print_exc()
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def eliminar_conversacion(request):
    if request.method == 'POST':
        try:
            # Obtener el usuario actual
            numero_documento = request.user.username
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            
            # Obtener datos de la solicitud
            datos = json.loads(request.body)
            conversacion_id = datos.get('conversacion')
            
            if not conversacion_id:
                return JsonResponse({'error': 'ID de conversación no proporcionado'}, status=400)
            
            # Verificar que la conversación existe
            conversacion = get_object_or_404(Conversacion, id_conversacion=conversacion_id)
            
            # Verificar que el usuario es administrador de la conversación
            es_admin = ParticipanteConversacion.objects.filter(
                conversacion=conversacion,
                usuario=usuario,
                rol_participante='admin',
                estado_participacion='activo'
            ).exists()
            
            # Verificar que es el creador de la conversación
            es_creador = conversacion.creador == usuario
            
            if not (es_admin or es_creador):
                return JsonResponse({'error': 'No tienes permisos para eliminar esta conversación'}, status=403)
            
            # Marcar la conversación como eliminada cambiando el valor booleano a False
            # ya que en tu modelo es un BooleanField
            conversacion.estado = False
            conversacion.save(update_fields=['estado'])
            
            # Notificar a todos los participantes
            participantes = ParticipanteConversacion.objects.filter(
                conversacion=conversacion,
                estado_participacion='activo'
            ).exclude(usuario=usuario)
            
            for participante in participantes:
                # Marcar como inactivo
                participante.estado_participacion = 'inactivo'
                participante.save(update_fields=['estado_participacion'])
                
                # Crear notificación
                if participante.notificaciones_activas:
                    NotificacionChat.objects.create(
                        usuario=participante.usuario,
                        conversacion=conversacion,
                        tipo_notificacion='conversacion_eliminada',
                        contenido=f"La conversación '{conversacion.titulo}' ha sido eliminada por {usuario.nombres}"
                    )
            
            # Añadir mensaje a la conversación para notificar la eliminación
            Mensaje.objects.create(
                conversacion=conversacion,
                remitente=usuario,
                contenido=f"La conversación ha sido eliminada por {usuario.nombres}"
            )
            
            return JsonResponse({'success': True})
            
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            print("Error al eliminar la conversación:", e)
            traceback.print_exc()
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def agregar_participantes(request):
    if request.method == 'POST':
        try:
            # Obtener el usuario actual
            numero_documento = request.user.username
            usuario = Usuarios.objects.get(numero_documento=numero_documento)
            
            # Obtener datos de la solicitud
            datos = json.loads(request.body)
            conversacion_id = datos.get('conversacion')
            nuevos_participantes_ids = datos.get('participantes', [])
            
            if not conversacion_id:
                return JsonResponse({'error': 'ID de conversación no proporcionado'}, status=400)
                
            if not nuevos_participantes_ids:
                return JsonResponse({'error': 'Debes seleccionar al menos un participante'}, status=400)
            
            # Verificar que la conversación existe
            conversacion = get_object_or_404(Conversacion, id_conversacion=conversacion_id)
            
            # Verificar que el usuario es administrador de la conversación
            es_admin = ParticipanteConversacion.objects.filter(
                conversacion=conversacion,
                usuario=usuario,
                rol_participante='admin',
                estado_participacion='activo'
            ).exists()
            
            # Solo administradores pueden añadir participantes
            if not es_admin:
                return JsonResponse({'error': 'No tienes permisos para añadir participantes a esta conversación'}, status=403)
            
            # Obtener participantes actuales para evitar duplicados
            participantes_actuales = ParticipanteConversacion.objects.filter(
                conversacion=conversacion
            ).values_list('usuario_id', flat=True)
            
            participantes_agregados = 0
            participantes_reactivados = 0
            
            for participante_id in nuevos_participantes_ids:
                try:
                    nuevo_participante = Usuarios.objects.get(id_usuario=participante_id)
                    
                    # Verificar si ya existe pero está inactivo
                    participante_existente = ParticipanteConversacion.objects.filter(
                        conversacion=conversacion,
                        usuario=nuevo_participante
                    ).first()
                    
                    if participante_existente:
                        # Si existe pero está inactivo, reactivarlo
                        if participante_existente.estado_participacion != 'activo':
                            participante_existente.estado_participacion = 'activo'
                            participante_existente.save(update_fields=['estado_participacion'])
                            participantes_reactivados += 1
                    else:
                        # Si no existe, crear nuevo participante
                        ParticipanteConversacion.objects.create(
                            conversacion=conversacion,
                            usuario=nuevo_participante,
                            rol_participante='miembro'
                        )
                        participantes_agregados += 1
                    
                    # Crear notificación para el nuevo participante
                    NotificacionChat.objects.create(
                        usuario=nuevo_participante,
                        conversacion=conversacion,
                        tipo_notificacion='invitacion',
                        contenido=f"{usuario.nombres} te ha añadido a la conversación '{conversacion.titulo}'"
                    )
                    
                except Usuarios.DoesNotExist:
                    continue
            
            # Crear mensaje de sistema sobre los nuevos participantes
            if participantes_agregados > 0 or participantes_reactivados > 0:
                mensaje = f"{usuario.nombres} ha añadido {participantes_agregados + participantes_reactivados} participante(s) a la conversación"
                Mensaje.objects.create(
                    conversacion=conversacion,
                    remitente=usuario,
                    contenido=mensaje
                )
            
            return JsonResponse({
                'success': True,
                'agregados': participantes_agregados,
                'reactivados': participantes_reactivados
            })
            
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            print("Error al añadir participantes:", e)
            traceback.print_exc()
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def nuevos_mensajes(request):
    numero_documento = request.user.username
    
    try:
        usuario = Usuarios.objects.get(numero_documento=numero_documento)
        conversacion_id = request.GET.get('conversacion')
        ultimo_id = request.GET.get('ultimo_id', '0')
        
        if not conversacion_id:
            return JsonResponse({'error': 'ID de conversación no proporcionado'}, status=400)
        
        # Convertir a entero
        ultimo_id = int(ultimo_id) if ultimo_id.isdigit() else 0
        
        # Verificar que la conversación existe y el usuario es participante
        conversacion = get_object_or_404(
            Conversacion, 
            id_conversacion=conversacion_id,
            estado=True,
            participantes__usuario=usuario,
            participantes__estado_participacion='activo'
        )
        
        # Obtener mensajes nuevos (con ID mayor al último recibido)
        mensajes_nuevos = Mensaje.objects.filter(
            conversacion=conversacion,
            id_mensaje__gt=ultimo_id
        ).select_related('remitente').order_by('fecha_envio')
        
        # Formatear mensajes para la respuesta JSON
        mensajes_data = []
        for mensaje in mensajes_nuevos:
            # Marcar el mensaje como leído si el remitente no es el usuario actual
            if mensaje.remitente != usuario and mensaje.estado == 'enviado':
                LecturaMensaje.objects.get_or_create(
                    mensaje=mensaje,
                    usuario=usuario
                )
                mensaje.estado = 'leido'
                mensaje.save(update_fields=['estado'])
            
            # Añadir datos del mensaje al array
            mensajes_data.append({
                'id': mensaje.id_mensaje,
                'contenido': mensaje.contenido,
                'fecha': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
                'editado': mensaje.editado,
                'remitente': {
                    'id': mensaje.remitente.id_usuario,
                    'nombre': mensaje.remitente.nombres
                }
            })
        
        return JsonResponse({'nuevos_mensajes': mensajes_data})
        
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        print("Error al verificar nuevos mensajes:", e)
        traceback.print_exc()
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)