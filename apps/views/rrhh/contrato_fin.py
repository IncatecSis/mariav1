from django.utils.timezone import now
from apps.principal.modelos.rrhh.contratos import *

def contrato_finalizado():
    fecha_actual = now().date()
    contratos_vencidos = Contrataciones.objects.filter(
        estado=True,
        fecha_fin__lt=fecha_actual
    )

    try:
        tipo_despido = TipoDespido.objects.get(nombre_despido='TERMINACIÓN DEL CONTRATO')

        for contrato in contratos_vencidos:
            ContratoFin.objects.create(
                id_contratacion=contrato,
                fecha_fin=contrato.fecha_fin,
                id_tipo_despido=tipo_despido
            )
            contrato.estado = False
            contrato.save()

        return contratos_vencidos.count() 

    except TipoDespido.DoesNotExist:
        print("⚠️ Error: Tipo de despido 'TERMINACIÓN DEL CONTRATO' no encontrado.")
        return 0
