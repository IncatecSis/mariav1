"""
from django.shortcuts import get_object_or_404
from apps.principal.modelos.periodo import Periodo
from apps.principal.modelos.sedes import Sede

def topbar_general(request):
    sede_id = request.session.get('sede_id')
    periodo_id = request.session.get('periodo_id')

    acceso_total = getattr(request.user, 'is_superuser', False) or \
                   (hasattr(request.user, 'roles_id') and request.user.roles_id == 2)

    if acceso_total:
        periodo_choices = [
            (p.id, f'{p.anio}-{dict(Periodo.SEMESTRE_CHOICE).get(p.semestre)}')
            for p in Periodo.obtener_todos()
        ]
        sede_choices = [
            (s.id, s.nombre) for s in Sede.objects.all()
        ]
    else:
        periodo_choices = [
            (p.id, f'{p.anio}-{dict(Periodo.SEMESTRE_CHOICE).get(p.semestre)}')
            for p in Periodo.obtener_periodos_accesibles(request.user)
            if hasattr(request.user, 'tiene_permiso') and request.user.tiene_permiso("view_periodo")
        ]
        sede_choices = [
            (s.id, s.nombre) for s in getattr(request.user, 'sedes', []).all()
            if hasattr(request.user, 'tiene_permiso') and request.user.tiene_permiso("view_sede")
        ]

    nombre_sede = get_object_or_404(Sede, id=sede_id).nombre if sede_id else 'Sede no seleccionada'
    nombre_periodo = 'Periodo no seleccionado'

    if periodo_id:
        periodo = Periodo.obtener_por_id(periodo_id)
        if periodo:
            nombre_periodo = f'{periodo.anio}-{dict(Periodo.SEMESTRE_CHOICE).get(periodo.semestre)}'
    
    return {
        'sede_choices': sede_choices,
        'periodo_choices': periodo_choices,
        'nombre_sede': nombre_sede,
        'nombre_periodo': nombre_periodo,
    }
"""

