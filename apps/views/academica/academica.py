from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.principal.modelos.academico.jornadas import *
from apps.principal.modelos.usuario.Usuarios import *
from apps.principal.modelos.parametros.sedes import *
from apps.principal.modelos.academico.programa import *
from apps.principal.middleware.auditoria import *




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def matricula(request):
    if request.method == 'POST':
        context_usuario(request)
        tipo = request.POST.get('tipo')
        if tipo == 'usuarios':
            numero_documento = request.POST.get('numero_documento')
            usuario_existe = Usuarios.objects.filter(numero_documento=numero_documento).first()
            if usuario_existe:
                messages.warning(request, 'El usuario ya existe.!🫤')
                return redirect('Incatec:matricula')
            
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
                return redirect('Incatec:matricula')
            
            except (Sexo.DoesNotExist, Departamentos.DoesNotExist, Municipios.DoesNotExist,
                    TipoSangre.DoesNotExist, EstadoCivil.DoesNotExist,
                    Sisben.DoesNotExist, EstratoSocioeconomico.DoesNotExist,
                    Etnia.DoesNotExist, ZonaResidencial.DoesNotExist,
                    Eps.DoesNotExist, TipoDiscapacidad.DoesNotExist):
                messages.error(request, 'Opción seleccionada no es válida.🤥')
                return redirect('Incatec:matricula')
            
        elif tipo == 'estudiantes':
            usuario_id = request.POST.get('usuario_id')
            if not usuario_id:
                messages.warning(request, 'El usuario no existe.!🫤')
                return redirect('Incatec:matricula')
            usuario = Usuarios.objects.filter(id_usuario=usuario_id)

            try:
                pass
            except:
                pass

    departamentos = Departamentos.objects.prefetch_related('municipios').order_by('departamento')

    contexto = {
        'departamentos': departamentos,
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
        'paises': Paises.objects.all(),
        'titulo_pagina': 'Registro de Matrícula',
    }
    return render(request, 'modulos/matricula/registro_matricula.html', contexto)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def grupos_academicos(request): 
    areas = [2, 3, 4]

    modulos = ModulosCompetencias.objects.select_related(
        'id_modulo',
        'id_semestre__id_pensum__id_programa'
    ).values(
        'id_modulo',
        'id_modulo__nombre_modulo',
        'id_semestre__id_pensum__id_programa',
        'intensidad_horas',
    ).distinct()
    contexto = {
        'areas': Areas.objects.filter(id_area__in=areas),
        'ubicaciones': Ubicaciones.objects.filter(id_area__in=areas, activo=True).select_related('id_area'),
        'programas': ProgramasAcademicos.objects.all(),
        'modulos': modulos,
        'titulo_pagina': 'Grupos Académicos',
    }
    return render(request, 'modulos/matricula/grupos_academicos.html', contexto)


def buscar_estudiante(request, numero_documento):
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