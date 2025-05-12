from datetime import date, datetime
import json
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import timedelta, date
from django.utils.timezone import now
from decimal import Decimal
from apps.principal.middleware.auditoria import context_usuario
from apps.principal.modelos.usuario.Usuarios import Usuarios
from apps.principal.modelos.matricula.modelos_matriculas.generales import *
from apps.principal.modelos.rrhh.contratos import *
from apps.principal.modelos.rrhh.datos_adicionales import *
from apps.views.rrhh.contrato_fin import contrato_finalizado



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def talento_humano(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')

        if tipo == 'arl':
            id_arl = request.POST.get('id_arl')
            nombre = request.POST.get('nombre_arl')

            if id_arl:
                existe = Arl.objects.filter(nombre_arl=nombre).exclude(id_arl=id_arl).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje':'La Arl ya existe.🫥'})
                else:
                    arl = get_object_or_404(Arl, id_arl=id_arl)
                    arl.nombre_arl = nombre
                    arl.save()
                    return JsonResponse({'status': 'success',
                                        'mensaje': '¡Arl actualizada.!🎉',
                                        'nuevo': {
                                            'id': arl.id_arl,
                                            'nombre': arl.nombre_arl,
                                        }})
            else:
                existe = Arl.objects.filter(nombre_arl=nombre).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje': 'La Arl ya existe.🫥'})
                else:
                    nuevo = Arl.objects.create(nombre_arl=nombre)
                    return JsonResponse({'status': 'success',
                                        'mensaje': 'Arl creada.🤩',
                                        'nuevo': {
                                            'id': nuevo.id_arl,
                                            'nombre': nuevo.nombre_arl
                                        }})

        elif tipo == 'departamento_laboral':
            id_departamento = request.POST.get('id_departamento')
            nombre = request.POST.get('nombre')

            if id_departamento:
                existe = DepartamentoLaboral.objects.filter(nombre=nombre).exclude(id_departamento=id_departamento).exists()
                if existe:
                    return JsonResponse({'status': 'error', 
                                        'mensaje': 'El Área Laboral ya existe.🫥'})
                else:
                    dep = get_object_or_404(DepartamentoLaboral, id_departamento=id_departamento)
                    dep.nombre = nombre
                    dep.save()
                    return JsonResponse({'status': 'success', 'mensaje': 'Área Laboral actualizado.!🎉', 'nuevo': {
                        'id': dep.id_departamento,
                        'nombre': dep.nombre
                    }})
            else:
                existe = DepartamentoLaboral.objects.filter(nombre=nombre).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El Área Laboral ya existe.🫥'})
                else:
                    nuevo = DepartamentoLaboral.objects.create(nombre=nombre)
                    return JsonResponse({'status': 'success', 'mensaje': 'Área Laboral creada.🤩', 'nuevo': {
                        'id': nuevo.id_departamento,
                        'nombre': nuevo.nombre
                    }})

        elif tipo == 'cargo':
            id_cargo = request.POST.get('id_cargo')
            id_departamento = request.POST.get('departamento_laboral')
            nombre_cargo = request.POST.get('nombre')

            if id_cargo:
                existe = Cargo.objects.filter(nombre=nombre_cargo).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El cargo ya existe.🫥'})
                else:
                    cargo = get_object_or_404(Cargo, id_cargo=id_cargo)
                    cargo.nombre = nombre_cargo
                    cargo.id_departamento = get_object_or_404(DepartamentoLaboral, id_departamento=id_departamento)
                    cargo.save()
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': '¡Cargo actualizado.! 🎉',
                        'nuevo': {
                            'id': cargo.id_cargo,
                            'nombre': cargo.nombre,
                            'departamento': cargo.id_departamento.nombre,
                            'id_departamento': cargo.id_departamento.id_departamento
                        }
                    })
            else:
                existe = Cargo.objects.filter(nombre=nombre_cargo).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El cargo ya existe.🫥'})
                else:
                    departamento = get_object_or_404(DepartamentoLaboral, id_departamento=id_departamento)
                    nuevo = Cargo.objects.create(nombre=nombre_cargo, id_departamento=departamento, estado=True)
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': 'Cargo creado. 🤩',
                        'nuevo': {
                            'id': nuevo.id_cargo,
                            'nombre': nuevo.nombre,
                            'departamento': nuevo.id_departamento.nombre,
                            'id_departamento': nuevo.id_departamento.id_departamento
                        }
                    })
        
        elif tipo == 'caja_compensacion':
            id_caja_compensacion = request.POST.get('id_caja_compensacion')
            nombre = request.POST.get('nombre_caja')

            if id_caja_compensacion:
                existe = CajasCompensacion.objects.filter(nombre_caja=nombre).exclude(id_caja_compensacion=id_caja_compensacion).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje': 'La Caja Compensación ya existe.🫥'})
                else:
                    cjp = get_object_or_404(CajasCompensacion, id_caja_compensacion=id_caja_compensacion)
                    cjp.nombre_caja = nombre
                    cjp.save()
                    return JsonResponse({'status': 'success',
                                        'mensaje':'!Caja Compensación actualizada.!🎉',
                                        'nuevo': {
                                            'id' :cjp.id_caja_compensacion,
                                            'nombre' :cjp.nombre_caja
                                        }})
            else:
                existe = CajasCompensacion.objects.filter(nombre_caja=nombre).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje': 'La Caja Compensación ya existe.🫥'})
                else:
                    nuevo = CajasCompensacion.objects.create(nombre_caja=nombre)
                    return JsonResponse({'status': 'success',
                                        'mensaje': 'Caja Compensacion creada.🤩',
                                        'nuevo': {
                                            'id':nuevo.id_caja_compensacion,
                                            'nombre': nuevo.nombre_caja
                                        }})

        elif tipo == 'banco':
            id_banco = request.POST.get('id_banco')
            nombre = request.POST.get('nombre_banco')

            if id_banco:
                existe = Bancos.objects.filter(nombre_banco=nombre).exclude(id_banco=id_banco).exists()
                if existe:
                    return JsonResponse({'status': 'error', 
                                        'mensaje': 'El Banco ya existe.🫥'})
                else:
                    bancos = get_object_or_404(Bancos, id_banco=id_banco)
                    bancos.nombre_banco = nombre
                    bancos.save()
                    return JsonResponse({'status': 'success',
                                        'mensaje': '¡Bancos Asociados actualizado.!🎉', 
                                        'nuevo': {
                                            'id': bancos.id_banco,
                                            'nombre': bancos.nombre_banco
                                        }})
            else:
                existe = Bancos.objects.filter(nombre_banco=nombre).exists()
                if existe:
                    return JsonResponse({'status': 'error', 
                                        'mensaje': 'El Banco ya existe.🫥'})
                else:
                    nuevo = Bancos.objects.create(nombre_banco=nombre)
                    return JsonResponse({'status': 'success', 
                                        'mensaje': 'Bancos Asociados creado.🤩', 
                                        'nuevo': {
                                            'id': nuevo.id_banco,
                                            'nombre': nuevo.nombre_banco,
                                        }})

        elif tipo == 'eps':
            id_eps = request.POST.get('id_eps')
            nombre_eps = request.POST.get('nombre')

            if id_eps:
                existe = Eps.objects.filter(nombre=nombre_eps).exclude(id_eps=id_eps).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje':'La Eps ya existe.🫥'})
                else:
                    eps = get_object_or_404(Eps, id_eps=id_eps)
                    eps.nombre = nombre_eps
                    eps.save()
                    return JsonResponse({'status': 'success',
                                        'mensaje': '¡Eps actualizada.!🎉',
                                        'nuevo': {
                                            'id': eps.id_eps,
                                            'nombre': eps.nombre
                                        }})
            else:
                existe = Eps.objects.filter(nombre=nombre_eps).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje':'La Eps ya existe.🫥'})
                else:
                    nuevo=Eps.objects.create(nombre=nombre_eps)
                    return JsonResponse({'status': 'success',
                                        'mensaje': 'Eps creada.🤩',
                                        'nuevo': {
                                            'id':nuevo.id_eps,
                                            'nombre':nuevo.nombre,
                                        }})
        
        elif tipo == 'pension':
            id_pension = request.POST.get('id_administradoras_pensiones')
            nombre_pension = request.POST.get('nombre_administradora')

            if id_pension:
                existe = AdministradorasPensiones.objects.filter(nombre_administradora=nombre_pension).exclude(id_administradoras_pensiones=id_pension).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje':'El fondo de pensión ya existe.🫥'})
                else:
                    pension = get_object_or_404(AdministradorasPensiones, id_administradoras_pensiones=id_pension)
                    pension.nombre_administradora = nombre_pension
                    pension.save()
                    return JsonResponse({'status': 'success',
                                        'mensaje': '¡Fondo de Pensión actualizada.!🎉',
                                        'nuevo': {
                                            'id': pension.id_administradoras_pensiones,
                                            'nombre': pension.nombre_administradora
                                        }})
            else:
                existe = AdministradorasPensiones.objects.filter(nombre_administradora=nombre_pension).exists()
                if existe:
                    return JsonResponse({'status': 'error',
                                        'mensaje':'El fondo de pensión ya existe.🫥'})
                else:
                    nuevo = AdministradorasPensiones.objects.create(nombre_administradora=nombre_pension)
                    return JsonResponse({'status': 'success',
                                        'mensaje': 'Fondo de Pensión creada.🤩',
                                        'nuevo': {
                                            'id': nuevo.id_administradoras_pensiones,
                                            'nombre': nuevo.nombre_administradora
                                        }})

        elif tipo == 'tipo_contrato':
            id_tipo = request.POST.get('id_tipo_contrato')
            nombre_contrato = request.POST.get('nombre_tipo_contrato')
            id_rol = request.POST.get('id_rol') or None
            if id_rol == '4':
                id_rol = None
            asigna_rol = bool(id_rol)

            if id_tipo:
                existe = TiposDeContrato.objects.filter(nombre_tipo_contrato=nombre_contrato).exclude(id_tipo_contrato=id_tipo).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El tipo de contrato ya existe.🫥'})
                else:
                    contrato = get_object_or_404(TiposDeContrato, id_tipo_contrato=id_tipo)
                    contrato.nombre_tipo_contrato = nombre_contrato
                    contrato.asigna_rol = asigna_rol
                    contrato.id_rol = Roles.objects.get(id_rol=id_rol) if id_rol else None
                    contrato.save()
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': 'Tipo de contrato actualizado!',
                        'nuevo': {
                            'id': contrato.id_tipo_contrato,
                            'nombre': contrato.nombre_tipo_contrato,
                            'id_rol': contrato.id_rol.id_rol if contrato.id_rol else '',
                            'nombre_rol': contrato.id_rol.nombre_rol if contrato.id_rol else 'NO APLICA'
                        }
                    })
            else:
                existe = TiposDeContrato.objects.filter(nombre_tipo_contrato=nombre_contrato).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El tipo de contrato ya existe.🫥'})
                else:
                    nuevo = TiposDeContrato.objects.create(
                        nombre_tipo_contrato=nombre_contrato,
                        asigna_rol=asigna_rol,
                        id_rol=Roles.objects.get(id_rol=id_rol) if id_rol else None
                    )
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': 'Contrato creado. 🤩',
                        'nuevo': {
                            'id': nuevo.id_tipo_contrato,
                            'nombre': nuevo.nombre_tipo_contrato,
                            'id_rol': nuevo.id_rol.id_rol if nuevo.id_rol else '',
                            'nombre_rol': nuevo.id_rol.nombre_rol if nuevo.id_rol else 'NO APLICA'
                        }
                    })

        elif tipo == 'riesgo':
            id_riesgo = request.POST.get('id_riesgo_laboral')
            nivel_riesgos = request.POST.get('nivel_riesgo')
            porcentajes = request.POST.get('porcentaje')

            if id_riesgo:
                existe = RiesgoLaboral.objects.filter(nivel_riesgo=nivel_riesgos).exclude(id_riesgo_laboral=id_riesgo).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El riesgo laboral ya existe.🫥'})
                else:
                    riesgo = get_object_or_404(RiesgoLaboral, id_riesgo_laboral=id_riesgo)
                    riesgo.nivel_riesgo = nivel_riesgos
                    riesgo.porcentaje = porcentajes
                    riesgo.save()
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': '¡Riesgo Laboral actualizado.! 🎉',
                        'nuevo': {
                            'id': riesgo.id_riesgo_laboral,
                            'nivel': riesgo.nivel_riesgo,
                            'porcentaje': riesgo.porcentaje
                        }
                    })
            else:
                existe = RiesgoLaboral.objects.filter(nivel_riesgo=nivel_riesgos).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El riesgo laboral ya existe.🫥'})
                else:
                    nuevo = RiesgoLaboral.objects.create(
                        nivel_riesgo=nivel_riesgos,
                        porcentaje=porcentajes
                    )
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': 'Riesgo Laboral creado. 🤩',
                        'nuevo': {
                            'id': nuevo.id_riesgo_laboral,
                            'nivel': nuevo.nivel_riesgo,
                            'porcentaje': nuevo.porcentaje
                        }
                    })

        elif tipo == 'despidos':
            id_despido = request.POST.get('id_tipo_despido')
            nombre_despido = request.POST.get('nombre_despido')
            descripcion = request.POST.get('descripcion')

            if id_despido:
                existe = TipoDespido.objects.filter(nombre_despido=nombre_despido).exclude(id_tipo_despido=id_despido).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El tipo de despido ya existe.🫥'})
                else:
                    despido = get_object_or_404(TipoDespido, id_tipo_despido=id_despido)
                    despido.nombre_despido = nombre_despido
                    despido.descripcion = descripcion
                    despido.save()
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': '¡Tipo de despido actualizado! 🎉',
                        'nuevo': {
                            'id': despido.id_tipo_despido,
                            'nombre': despido.nombre_despido,
                            'descripcion': despido.descripcion
                        }
                    })
            else:
                existe = TipoDespido.objects.filter(nombre_despido=nombre_despido).exists()
                if existe:
                    return JsonResponse({'status': 'error', 'mensaje': 'El tipo de despido ya existe.🫥'})
                else:
                    nuevo = TipoDespido.objects.create(
                        nombre_despido=nombre_despido,
                        descripcion=descripcion
                    )
                    return JsonResponse({
                        'status': 'success',
                        'mensaje': 'Tipo de despido creado. 🤩',
                        'nuevo': {
                            'id': nuevo.id_tipo_despido,
                            'nombre': nuevo.nombre_despido,
                            'descripcion': nuevo.descripcion
                        }
                    })

        #return redirect('Incatec:talento_humano')       
    contexto = {
        'rol': Roles.objects.all(),
        'despido': TipoDespido.objects.all(),
        'departamento_laboral': DepartamentoLaboral.objects.all(),
        'cargo': Cargo.objects.all(),
        'arl': Arl.objects.all(),
        'caja_compensacion': CajasCompensacion.objects.all(),
        'tipo_contrato': TiposDeContrato.objects.all(),
        'banco': Bancos.objects.all(),
        'pension': AdministradorasPensiones.objects.all(),
        'epss': Eps.objects.all(),
        'riesgos': RiesgoLaboral.objects.all(),
        'titulo': 'Parámetros Talento Humano',
    }
    return render(request, 'modulos/rrhh/talento_humano.html', contexto)


@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def usuarios_admi(request):
    if request.method == 'POST' and request.POST.get('tipo') == 'registro_contratacion':
        context_usuario(request)
        print('Datos recibidos', request.POST)
        
        usuario_id = request.POST.get('usuario_id')
        contrato_id = request.POST.get('contrato_id', None)

        if not usuario_id:
            messages.error(request, 'El usuario no se encontró.')
            print("❌ Error: Usuario no encontrado.")
            return redirect('Incatec:administrativos')

        usuario = Usuarios.objects.get(id_usuario=usuario_id)

        try:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')

            salario_str = request.POST.get('salario', '0')
            salario_str = salario_str.replace('.', '').replace(',', '.')
            try:
                salario = Decimal(salario_str)
            except ValueError:
                messages.error(request, "El salario ingresado no es válido.")
                return redirect('Incatec:administrativos')

            numero_cuenta = request.POST.get('numero_cuenta')
            dpto_laboral = DepartamentoLaboral.objects.get(id_departamento=request.POST.get('departamento_laboral'))
            cargo = Cargo.objects.get(id_cargo=request.POST.get('cargo'))
            arl = Arl.objects.get(id_arl=request.POST.get('arl'))
            caja_compensacion = CajasCompensacion.objects.get(id_caja_compensacion=request.POST.get('caja_compensacion'))
            banco = Bancos.objects.get(id_banco=request.POST.get('banco'))
            tipo_contrato = TiposDeContrato.objects.get(id_tipo_contrato=request.POST.get('tipo_contrato'))
            pension = AdministradorasPensiones.objects.get(id_administradoras_pensiones=request.POST.get('pension'))
            riesgo_laboral = RiesgoLaboral.objects.get(id_riesgo_laboral=request.POST.get('riesgo'))

            if contrato_id:
                print("📝 Actualizando contrato existente con ID:", contrato_id)
                Contrataciones.objects.filter(id_contratacion=contrato_id).update(
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    salario=salario,
                    numero_cuenta=numero_cuenta,
                    id_departamento=dpto_laboral,
                    id_cargo=cargo,
                    id_caja_compensacion=caja_compensacion,
                    id_banco=banco,
                    id_tipo_contrato=tipo_contrato,
                    id_administradoras_pensiones=pension,
                    id_arl=arl,
                    id_riesgo_laboral=riesgo_laboral,
                )
                messages.success(request, '¡Contrato actualizado exitosamente! 🎉')
            else:
                print("🆕 Creando un nuevo contrato para el usuario.")
                contrato_existente = Contrataciones.objects.filter(
                    id_usuario=usuario,
                    id_tipo_contrato=tipo_contrato,
                    estado=True,
                ).exists()

                if contrato_existente:
                    messages.warning(request, 'Este usuario ya tiene un contrato activo de este tipo. ⚠️')
                    return redirect('Incatec:administrativos')
                
                nuevo_contrato = Contrataciones.objects.create(
                    id_usuario=usuario,
                    fecha_fin=fecha_fin,
                    fecha_inicio=fecha_inicio,
                    salario=salario,
                    numero_cuenta=numero_cuenta,
                    id_departamento=dpto_laboral,
                    id_cargo=cargo,
                    id_arl=arl,
                    id_riesgo_laboral=riesgo_laboral,
                    id_caja_compensacion=caja_compensacion,
                    id_banco=banco,
                    id_tipo_contrato=tipo_contrato,
                    id_administradoras_pensiones=pension,
                    estado=False
                )
                print(f"✅ Nuevo contrato creado con ID: {nuevo_contrato.id_contratacion}")
                messages.success(request, '¡Contrato registrado exitosamente! 🎉')

        except Exception as e:
            print(f"⚠️ Error general en la vista: {e}")
            messages.error(request, f'Error al procesar la solicitud: {str(e)} 🫤')

        return redirect('Incatec:administrativos')

    if request.method == 'POST' and request.POST.get('tipo') == 'anexar_documentos':
        context_usuario(request)
        contrato_id = request.POST.get('contrato_id', None)
        print(f'ID Contrato recibido: {contrato_id}')

        try:
            contrato = Contrataciones.objects.get(id_contratacion=contrato_id)
            documentos, created = DocumentosContrato.objects.get_or_create(id_contratacion=contrato)


            nueva_entrevista = request.FILES.get('entrevista')
            if nueva_entrevista:
                documentos.entrevista = nueva_entrevista

            resultados_prueba = request.FILES.get('prueba')
            if resultados_prueba:
                documentos.prueba_tecnica = resultados_prueba   
                
            nueva_remision = request.FILES.get('remision')
            if nueva_remision:
                documentos.remision = nueva_remision

            nueva_arl = request.FILES.get('arlfile')
            if nueva_arl:
                documentos.arl = nueva_arl
                
            nueva_eps = request.FILES.get('epsfile')
            if nueva_eps:
                documentos.eps = nueva_eps

            nueva_caja = request.FILES.get('cajafile')
            if nueva_caja:
                documentos.caja_compensacion = nueva_caja

            nuevo_fondo = request.FILES.get('pensionfile')
            if nuevo_fondo:
                documentos.fondo_pension = nuevo_fondo

            nuevo_banco = request.FILES.get('bancofile')
            if nuevo_banco:
                documentos.bancos = nuevo_banco

            medico = request.FILES.get('resultados')
            if medico:
                documentos.resultados_medicos = medico
            
            nuevo_resultado = request.FILES.get('resumen')
            if nuevo_resultado:
                documentos.resultados = nuevo_resultado
            
            documentos.save()
            messages.success(request, 'Documentos Anexados correctamente.📂✨')
            return redirect('Incatec:administrativos')
        
        except Contrataciones.DoesNotExist:
            print('Contrato no encontrado.')
            messages.error(request, 'Contrato no encontrado. 🚨')
            return redirect('Incatec:administrativos')
        
        except Exception as e:
            print(f"⚠️ Error general al anexar documentos: {e}")
            messages.error(request, f'Ocurrió un error al anexar documentos: {str(e)} 🫤')
            return redirect('Incatec:administrativos')
    
    contratos = Contrataciones.objects.select_related(
        'id_usuario', 'id_banco', 'id_arl', 'id_caja_compensacion',
        'id_administradoras_pensiones', 'id_tipo_contrato', 'id_departamento',
        'id_cargo', 'id_riesgo_laboral'
    )

    documento_contrato = DocumentosContrato.objects.select_related('id_contratacion')

    if request.method == 'POST' and request.POST.get('tipo') == 'actualizacion_usuario':
        context_usuario(request)
        usuario_id = request.POST.get('usuario_id', None)
        print(f"🛠️ ID Usuario recibido en POST: {usuario_id}") 
        usuario = Usuarios.objects.get(id_usuario=usuario_id)
        
        try:
            usuario.id_tipo_identificacion = TipoIdentificacion.objects.get(id_tipo_identificacion=request.POST.get('tipo_identificacion'))
            usuario.numero_documento = request.POST.get('numero_documento')
            usuario.nombres = request.POST.get('nombres')
            usuario.apellidos = request.POST.get('apellidos')
            usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                
            nueva_foto = request.FILES.get('foto_perfil')
            if nueva_foto:
                usuario.foto_perfil = nueva_foto
                usuario.id_pais = Paises.objects.get(id_pais=request.POST.get('pais'))
                usuario.id_sexo = Sexo.objects.get(id_sexo=request.POST.get('sexo'))
                usuario.id_departamento_expedicion = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_expedicion'))
                usuario.id_municipio_expedicion = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_expedicion'))
                usuario.id_departamento_nacimiento = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_nacimiento'))
                usuario.id_municipio_nacimiento = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_nacimiento'))
                usuario.id_tipo_sangre = TipoSangre.objects.get(id_tipo_sangre=request.POST.get('tipo_sangre'))
                usuario.id_estado_civil = EstadoCivil.objects.get(id_estado_civil=request.POST.get('estado_civil'))
                usuario.id_sisben = Sisben.objects.get(id_sisben=request.POST.get('sisben'))
                usuario.id_departamento_residencia = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_residencia'))
                usuario.id_municipio_residencia = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_residencia'))
                usuario.direccion_residencia = request.POST.get('direccion_residencia')
                usuario.barrio = request.POST.get('barrio')
                usuario.celular = request.POST.get('celular')
                usuario.telefono = request.POST.get('telefono')
                usuario.correo_electronico = request.POST.get('correo_electronico')
                usuario.id_estrato = EstratoSocioeconomico.objects.get(id_estrato=request.POST.get('estrato'))
                usuario.id_etnia = Etnia.objects.get(id_etnia=request.POST.get('etnia'))
                usuario.id_zona_residencial = ZonaResidencial.objects.get(id_zona_residencial=request.POST.get('zona_residencial'))
                usuario.id_eps = Eps.objects.get(id_eps=request.POST.get('eps'))
                usuario.id_departamento_expulsor = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_expulsor'))
                usuario.id_municipio_expulsor = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_expulsor'))
                usuario.id_tipo_discapacidad = TipoDiscapacidad.objects.get(id_tipo_discapacidad=request.POST.get('tipo_discapacidad'))

                usuario.save()
                messages.success(request, 'Usuario actualizado.🤩')
                return redirect('Incatec:administrativos')
        except Exception as e:
            messages.error(request, 'Error al actualizar el usuario.🫤')
            return redirect('Incatec:administrativos')

    if request.method == 'POST' and not request.POST.get('tipo'):
        context_usuario(request)
        numero_documento = request.POST.get('numero_documento')
        usuario_existente = Usuarios.objects.filter(numero_documento=numero_documento).first()
        if usuario_existente:
            messages.warning(request, 'El usuario ya existe.🫤')
            return redirect('Incatec:administrativos')

        try:
            id_pais = Paises.objects.get(id_pais=request.POST.get('pais'))
            id_tipo_identificacion = TipoIdentificacion.objects.get(id_tipo_identificacion=request.POST.get('tipo_identificacion'))
            id_sexo = Sexo.objects.get(id_sexo=request.POST.get('sexo'))
            id_departamento_expedicion = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_expedicion'))
            id_municipio_expedicion = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_expedicion'))
            id_departamento_nacimiento = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_nacimiento'))
            id_municipio_nacimiento = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_nacimiento'))
            id_tipo_sangre = TipoSangre.objects.get(id_tipo_sangre=request.POST.get('tipo_sangre'))
            id_estado_civil = EstadoCivil.objects.get(id_estado_civil=request.POST.get('estado_civil'))
            id_sisben = Sisben.objects.get(id_sisben=request.POST.get('sisben'))
            id_departamento_residencia = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_residencia'))
            id_municipio_residencia = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_residencia'))
            id_estrato = EstratoSocioeconomico.objects.get(id_estrato=request.POST.get('estrato'))
            id_etnia = Etnia.objects.get(id_etnia=request.POST.get('etnia'))
            id_zona_residencial = ZonaResidencial.objects.get(id_zona_residencial=request.POST.get('zona_residencial'))
            id_eps = Eps.objects.get(id_eps=request.POST.get('eps'))
            id_departamento_expulsor = Departamentos.objects.get(id_departamento=request.POST.get('id_departamento_expulsor'))
            id_municipio_expulsor = Municipios.objects.get(id_municipio=request.POST.get('id_municipio_expulsor'))
            id_tipo_discapacidad = TipoDiscapacidad.objects.get(id_tipo_discapacidad=request.POST.get('tipo_discapacidad'))
            foto_perfil = request.FILES.get('foto_perfil', None)

            Usuarios.objects.create(
                id_pais=id_pais,
                id_tipo_identificacion=id_tipo_identificacion,
                numero_documento=numero_documento,
                nombres=request.POST.get('nombres'),
                apellidos=request.POST.get('apellidos'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                id_sexo=id_sexo,
                id_departamento_expedicion=id_departamento_expedicion,
                id_municipio_expedicion=id_municipio_expedicion,
                id_departamento_nacimiento=id_departamento_nacimiento,
                id_municipio_nacimiento=id_municipio_nacimiento,
                id_tipo_sangre=id_tipo_sangre,
                id_estado_civil=id_estado_civil,
                id_sisben=id_sisben,
                id_departamento_residencia=id_departamento_residencia,
                id_municipio_residencia=id_municipio_residencia,
                direccion_residencia=request.POST.get('direccion_residencia'),
                barrio=request.POST.get('barrio'),
                celular=request.POST.get('celular'),
                telefono=request.POST.get('telefono'),
                correo_electronico=request.POST.get('correo_electronico'),
                id_estrato=id_estrato,
                id_etnia=id_etnia,
                id_zona_residencial=id_zona_residencial,
                id_eps=id_eps,
                id_departamento_expulsor=id_departamento_expulsor,
                id_municipio_expulsor=id_municipio_expulsor,
                id_tipo_discapacidad=id_tipo_discapacidad,
                foto_perfil=foto_perfil,
            )

            messages.success(request, 'El usuario fué creado exitosamente.🤩')
            return redirect('Incatec:administrativos')

        except (Sexo.DoesNotExist, Departamentos.DoesNotExist, Municipios.DoesNotExist,
                TipoSangre.DoesNotExist, EstadoCivil.DoesNotExist,
                Sisben.DoesNotExist, EstratoSocioeconomico.DoesNotExist,
                Etnia.DoesNotExist, ZonaResidencial.DoesNotExist,
                Eps.DoesNotExist, TipoDiscapacidad.DoesNotExist):
            messages.error(request, 'Opción seleccionada no es válida.🤥')
            return redirect('Incatec:administrativos')

    contrato_fin = contrato_finalizado()

    usuario_rol = {}
    roles = Roles.objects.all()

    for rol in roles:
        usuario_rol[rol.nombre_rol] = Usuarios.objects.filter(
            contrataciones__id_tipo_contrato__id_rol=rol
        ).prefetch_related(
            'contrataciones_set'
        ).distinct().order_by('nombres')


    fecha_actual = now().date()
    fecha_limite = fecha_actual + timedelta(days=5)

    contratos_vencimiento = Contrataciones.objects.filter(
        estado=True,
        fecha_fin__range=[fecha_actual, fecha_limite]
    ).select_related('id_usuario').order_by('fecha_fin')

    for contrato in contratos_vencimiento:
        contrato.dias_restantes = (contrato.fecha_fin - fecha_actual).days

    departamentos = Departamentos.objects.prefetch_related('municipios').order_by('departamento')
    
    contexto = {
        'usuarios_rol': usuario_rol,
        'roles': roles,
        'contratos_vencimiento': contratos_vencimiento,
        'contrato_fin': contrato_fin,
        'departamentos': departamentos,
        'contratos': contratos,
        'documento_contrato': documento_contrato,
        'tipos_identificacion': TipoIdentificacion.objects.all(),
        'sexos': Sexo.objects.all(),
        'tipos_sangre': TipoSangre.objects.all(),
        'estados_civiles': EstadoCivil.objects.all(),
        'sisbenes': Sisben.objects.all(),
        'estratos': EstratoSocioeconomico.objects.all(),
        'etnias': Etnia.objects.all(),
        'zonas_residenciales': ZonaResidencial.objects.all(),
        'epss': Eps.objects.all(),
        'tipos_discapacidad': TipoDiscapacidad.objects.all(),
        'departamento_laboral': DepartamentoLaboral.objects.all(),
        'cargo': Cargo.objects.all(),
        'arl': Arl.objects.all(),
        'caja_compensacion': CajasCompensacion.objects.all(),
        'tipo_contrato': TiposDeContrato.objects.all(),
        'banco': Bancos.objects.all(),
        'pension': AdministradorasPensiones.objects.all(),
        'riesgos': RiesgoLaboral.objects.all(),
        'paises': Paises.objects.all(),
        'titulo': 'Usuarios Administrativos',
    }

    return render(request, 'modulos/rrhh/usuario_admi.html', contexto)

def buscar_usuario(request, numero_documento):
    try:
        usuario = Usuarios.objects.filter(numero_documento=numero_documento).first()

        if usuario:
            data = {
                "success": True,
                "id_usuario": usuario.id_usuario,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos
            }
        else:
            data = {"success": False,
                    'message': 'Usuario no encontrado.😒'}
    except Exception as e:
        data = {'success': False,
                'message': f"Error en la búsqueda: {str(e)}"}

    return JsonResponse(data)



@csrf_exempt
def estado(request):
    if request.method == 'GET':
        tipos = list(TipoDespido.objects.values('id_tipo_despido', 'nombre_despido'))
        return JsonResponse({'success': True, 'tipos': tipos})

    if request.method == 'POST':
        context_usuario(request)
        try:
            data = json.loads(request.body)
            contrato_id = data.get('contrato_id')
            id_tipo_despido = data.get('id_tipo_despido')
            fecha_fin = data.get('fecha_fin')

            contrato = Contrataciones.objects.get(id_contratacion=contrato_id)

            try:
                tipo_despido = TipoDespido.objects.get(id_tipo_despido=id_tipo_despido)
            except TipoDespido.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Tipo de despido no encontrado'})

            if fecha_fin:
                try:
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Formato de fecha inválido'})
            else:
                fecha_fin = date.today() 

            ContratoFin.objects.create(
                id_contratacion=contrato,
                fecha_fin=fecha_fin,
                id_tipo_despido=tipo_despido
            )

            contrato.estado = False
            contrato.save()

            return JsonResponse({'success': True, 'estado': False, 'message': 'Contrato finalizado correctamente.🤩'})

        except Contrataciones.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contrato no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})
