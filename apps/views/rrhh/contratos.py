import os
from django.conf import settings
from django.http import HttpResponse
from apps.views.rrhh.modelo_contrato import *
from apps.principal.modelos.rrhh.contratos import Contrataciones 


def generar_contrato(request, contrato_id):
    contrato = Contrataciones.objects.get(id_contratacion=contrato_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Contrato_{contrato.id_contratacion}.pdf"'

    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo3.png')

    pdf = ContratoLaboral(contrato, response, logo_path=logo_path)
    pdf.generar()

    return response

