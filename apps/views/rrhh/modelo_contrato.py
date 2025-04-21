from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Image, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
import os
from datetime import datetime

class ContratoLaboral:
    def __init__(self, contrato, response, logo_path=None):
        self.contrato = contrato 
        self.response = response  
        self.logo_path = logo_path
        self.width, self.height = letter
        self.c = canvas.Canvas(self.response, pagesize=letter) 
        self.styles = getSampleStyleSheet()
        self.page_number = 1
        self.total_pages = self._calcular_total_paginas()
        
        self.styles.add(ParagraphStyle(
            name='Titulo',
            parent=self.styles['Heading1'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=0.2*inch,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=0.15*inch,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='Clausula',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=0.1*inch,
            firstLineIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='DatosContrato',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=0.05*inch,
            leftIndent=20
        ))
    
    def _calcular_total_paginas(self):
        return 3
    
    def _agregar_encabezado(self):
        self.c.setStrokeColor(colors.darkblue)
        self.c.setLineWidth(2)
        self.c.line(1*cm, self.height - 1*cm, self.width - 1*cm, self.height - 1*cm)
        
        if self.logo_path and os.path.exists(self.logo_path):
            self.c.drawImage(self.logo_path, 1*cm, self.height - 3*cm, width=2*cm, height=1.5*cm, preserveAspectRatio=True)
            x_titulo = 4*cm
        else:
            x_titulo = 1*cm
        
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(colors.darkblue)
        titulo = "INCATEC - INSTITUTO TÉCNICO DE ADMINISTRACIÓN Y SALUD"
        self.c.drawCentredString(self.width/2, self.height - 2*cm, titulo)
        
        self.c.setFont("Helvetica-Bold", 12)
        subtitulo = "CONTRATO LABORAL"
        self.c.drawCentredString(self.width/2, self.height - 2.7*cm, subtitulo)
        
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(colors.black)
        self.c.drawString(self.width - 2*cm, 1*cm, f"Página {self.page_number} de {self.total_pages}")
        
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.c.drawString(1*cm, 1*cm, f"Generado: {fecha_generacion}")
        
        self.c.setStrokeColor(colors.darkblue)
        self.c.line(1*cm, 1.5*cm, self.width - 1*cm, 1.5*cm)
        
        self.c.setFillColor(colors.black)
    
    def _agregar_pie_pagina(self):
        self.c.setFont("Helvetica", 8)
        self.c.drawCentredString(self.width/2, 0.7*cm, "Documento generado digitalmente - INCATEC")
    
    def _agregar_texto_con_formato(self, texto, x, y, ancho, estilo='Normal'):
        p = Paragraph(texto, self.styles[estilo])
        w, h = p.wrap(ancho, self.height)
        
        if y - h < 2*cm:
            self.c.showPage()
            self.page_number += 1
            self._agregar_encabezado()
            self._agregar_pie_pagina()
            y = self.height - 4*cm
        
        p.drawOn(self.c, x, y - h)
        return y - h - 0.2*cm 
    
    def _agregar_seccion_datos(self):
        y = self.height - 4*cm
        
        self.c.setFont("Helvetica-Bold", 11)
        self.c.setFillColor(colors.darkblue)
        self.c.drawString(1*cm, y, "INFORMACIÓN DEL CONTRATO")
        y -= 0.7*cm
        
        color_fondo = colors.Color(0.95, 0.95, 0.95)  
        self.c.setStrokeColor(colors.lightgrey)
        self.c.setFillColor(color_fondo)
        self.c.roundRect(1*cm, y - 8*cm, self.width - 2*cm, 8*cm, 5, stroke=1, fill=1)
        
        x_col1 = 1.5*cm
        x_col2 = 11*cm
        ancho_col = 9*cm
        
        self.c.setFillColor(colors.black)
        self.c.setFont("Helvetica-Bold", 10)
        
        datos_col1 = [
            ("Nombre del Trabajador:", f"{self.contrato.id_usuario.nombres} {self.contrato.id_usuario.apellidos}"),
            ("Documento:", self.contrato.id_usuario.numero_documento),
            ("Dirección:", self.contrato.id_usuario.direccion_residencia),
            ("Ciudad Residencia:", self.contrato.id_usuario.id_municipio_residencia.municipio),
            ("Departamento Residencia:", self.contrato.id_usuario.id_departamento_residencia.departamento),
            ("EPS:", self.contrato.id_usuario.id_eps.nombre),
            ("Barrio:", self.contrato.id_usuario.barrio)
        ]
        
        datos_col2 = [
            ("Cargo:", self.contrato.id_cargo.nombre if self.contrato.id_cargo else "N/A"),
            ("Tipo de Contrato:", self.contrato.id_tipo_contrato.nombre_tipo_contrato if self.contrato.id_tipo_contrato else "N/A"),
            ("Salario:", f"${self.contrato.salario}"),
            ("Fecha de Inicio:", self.contrato.fecha_inicio.strftime('%d/%m/%Y')),
            ("Fecha de Vencimiento:", self.contrato.fecha_fin.strftime('%d/%m/%Y') if self.contrato.fecha_fin else "Indefinido"),
            ("ARL:", self.contrato.id_arl.nombre_arl if self.contrato.id_arl else "N/A"),
            ("Caja Compensación:", self.contrato.id_caja_compensacion.nombre_caja if self.contrato.id_caja_compensacion else "N/A")
        ]

        
        y_col = y - 0.5*cm
        
        for etiqueta, valor in datos_col1:
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x_col1, y_col, etiqueta)
            self.c.setFont("Helvetica", 9)
            self.c.drawString(x_col1 + 0.2*cm, y_col - 0.5*cm, valor)
            y_col -= 1*cm
        
        y_col = y - 0.5*cm
        for etiqueta, valor in datos_col2:
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x_col2, y_col, etiqueta)
            self.c.setFont("Helvetica", 9)
            self.c.drawString(x_col2 + 0.2*cm, y_col - 0.5*cm, valor)
            y_col -= 1*cm
        
        return y - 9*cm 
    
    def _agregar_clausulas(self, y):
        """Agrega las cláusulas del contrato"""
        self.c.setFont("Helvetica-Bold", 11)
        self.c.setFillColor(colors.darkblue)
        self.c.drawString(1*cm, y, "CLÁUSULAS DEL CONTRATO")
        y -= 0.7*cm
        
        intro = "Entre el empleador y el trabajador, de las condiciones ya dichas identificados como aparece al pie de sus correspondientes firmas se ha celebrado el presente contrato individual de trabajo, regido además por las siguientes cláusulas:"
        y = self._agregar_texto_con_formato(intro, 1*cm, y, self.width - 2*cm, 'Clausula')
        
        clausulas = [
            "<b>Primera.</b> El empleador contrata los servicios personales del trabajador y este se obliga: a) A poner al servicio del empleador toda su capacidad normal de trabajo, en forma exclusiva en el desempeño de las funciones propias del oficio mencionado y las labores anexas y complementarias del mismo, de conformidad con las órdenes e instrucciones que le imparta el empleador o sus representantes, y b) A no prestar directa ni indirectamente servicios laborales a otros empleadores, ni a trabajar por cuenta propia en el mismo oficio, durante la vigencia de este contrato.",
            
            "<b>Segunda.</b> El empleador pagará al trabajador por la prestación de sus servicios el salario indicado, pagadero en las oportunidades también ya señaladas. Dentro de este pago se encuentra incluida la remuneración de los descansos dominicales y festivos de que tratan los capítulos I y II del título VII del Código Sustantivo del Trabajo. Se aclara y se conviene que en los casos en los que el trabajador devengue comisiones o cualquier otra modalidad de salario variable, el 82.5% de dichos ingresos, constituye remuneración ordinaria y el 17.5% restante esta designado a remunerar el descanso en los días dominicales y festivos que tratan los capítulos I y II del título VII del Código Sustantivo de Trabajo.",
            
            "<b>Tercera.</b> Todo trabajo suplementario o en horas extras y todo trabajo en día domingo o festivo en los que legalmente debe concederse el descanso, se remunerará conforme a la Ley, así como los correspondientes recargos nocturnos. Para el reconocimiento y pago del trabajo suplementario, dominical o festivo el empleador o sus representantes deben autorizarlo previamente por escrito. Cuando la necesidad de este trabajo se presente de manera imprevista o inaplazable, deberá ejecutarse y darse cuenta de él por escrito, a la mayor brevedad, al empleador o sus representantes. El empleador, en consecuencia, no reconocerá ningún trabajo suplementario o en días de descanso legalmente obligatorio que no haya sido autorizado previamente o avisado inmediatamente, como queda dicho.",
            
            "<b>Cuarta.</b> El trabajador se obliga a laborar la jornada ordinaria en los turnos y dentro de las horas señaladas por el empleador, pudiendo hacer éste ajustes o cambios de horario cuando lo estime conveniente. Por el acuerdo expreso o tácito de las partes, podrán repartirse las horas jornada ordinaria de la forma prevista en el artículo 164 del Código Sustantivo del Trabajo, modificado por el artículo 23 de la Ley 50 de 1990, teniendo en cuenta que los tiempos de descanso entre las secciones de la jornada no se computan dentro de la misma, según el artículo 167 ibídem.",
            
            "<b>Quinta.</b> Las partes acuerdan un periodo de prueba de 30 días, que no es superior a la quinta parte del término inicial de este contrato ni excede dos meses. En caso de prórrogas o nuevo contrato entre las partes se entenderá que no hay nuevo periodo de prueba. Durante este periodo tanto el empleador como el trabajador, podrán terminar el contrato en cualquier momento en forma unilateral, de conformidad con el artículo 78 del Código Sustantivo del Trabajo, modificado por el artículo 7º de la ley 50 de 1990. Si la duración del contrato fuere superior a treinta días e inferior a un año, se entenderá por renovado por un término inicial al pactado, si antes de la fecha del vencimiento ninguna de las partes avisare por escrito la terminación de no prorrogarlo, con una antelación no inferior a treinta días.",
            
            "<b>Sexta.</b> Son justas causas para dar por terminado unilateralmente este contrato por cualquiera de las partes, las enumeradas en los artículos 62 y 63 del Código Sustantivo del Trabajo; y, además, por parte del empleado, las faltas que para el efecto se califiquen como graves en el espacio reservado para las cláusulas adicionales en el presente contrato.",
            
            "<b>Séptima.</b> Las invenciones o descubrimientos realizados por el trabajador contratado para investigar pertenecen al empleador, de conformidad con el artículo 539 del Código de Comercio, así como el artículo 20 y concordantes de la ley 23 de 1982 sobre derechos de autor. En cualquier otro caso el invento pertenece al trabajador, salvo cuando éste no haya sido contratado para investigar y realice la invención mediante datos o medios conocidos o utilizados en razón de la labor desempeñada, evento en el cual el trabajador, tendrá derecho a una compensación que se fijará dé acuerdo con el monto del salario, la importancia del invento o descubrimiento, el beneficio que reporte al empleador u otros factores similares.",
            
            "<b>Octava.</b> Las partes podrán convenir que el trabajo se preste en lugar distinto al inicialmente contratado, siempre que tales traslados no desmejoren las condiciones laborales o de remuneración del trabajador, o impliquen perjuicios para él. Los gastos que se originen con el traslado serán cubiertos por el empleador de conformidad con el numeral 8º del artículo 57 del Código Sustantivo del Trabajo. El trabajador se obliga a aceptar los cambios de oficio que decida el empleador dentro de su poder subordinante, siempre que se respeten las condiciones laborales del trabajador y no se le causen perjuicios. Todo ello sin que se afecte el honor, la dignidad y los derechos mínimos del trabajador, de conformidad con el artículo 23 del Código Sustantivo del Trabajo, modificado por el artículo 1º de la Ley 50 de 1990.",
            
            "<b>Novena.</b> Este contrato ha sido redactado estrictamente de acuerdo con la ley y la jurisprudencia y será interpretado de buena fe y en consonancia con el Código Sustantivo del Trabajo cuyo objeto, definido en su artículo 1º, es lograr la justicia en las relaciones entre empleadores y trabajadores dentro de un espíritu de coordinación económica y equilibrio social.",
            
            "<b>Décima.</b> El presente contrato reemplaza en su integridad y deja sin efecto alguno cualquiera otro contrato verbal o escrito celebrado por las partes con anterioridad. Las modificaciones que se acuerden al presente contrato se anotarán a continuación de su texto."
        ]
        
        for clausula in clausulas:
            y = self._agregar_texto_con_formato(clausula, 1*cm, y, self.width - 2*cm, 'Clausula')
            y -= 0.2*cm 
        
        return y
    
    def _agregar_firmas(self, y):
        usuario = self.contrato.id_usuario

        ciudad = usuario.id_municipio_residencia.municipio

        try:
            fecha = self.contrato.fecha_inicio
            dia = fecha.day
            mes_nombres = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            mes = mes_nombres[fecha.month - 1]
            año = fecha.year
        except:
            dia = "__"
            mes = "________"
            año = "______"

        texto_final = f"Para constancia se firma en dos o más ejemplares del mismo tenor y valor, ante testigos en la ciudad de {ciudad} a los {dia} días del mes de {mes} de {año}."
        y = self._agregar_texto_con_formato(texto_final, 1*cm, y, self.width - 2*cm, 'Normal')
        y -= 2*cm

        # 🔵 Firmas
        ancho_firma = 7*cm
        espacio_firma = 1.5*cm

        x1 = (self.width - 2*ancho_firma - espacio_firma) / 2
        x2 = x1 + ancho_firma + espacio_firma

        self.c.line(x1, y, x1 + ancho_firma, y)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(x1, y - 20, "EL EMPLEADOR")
        self.c.setFont("Helvetica", 9)
        self.c.drawString(x1, y - 35, "INSTITUTO INCATEC")

        self.c.line(x2, y, x2 + ancho_firma, y)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(x2, y - 20, "EL TRABAJADOR")
        self.c.setFont("Helvetica", 9)
        self.c.drawString(x2, y - 35, f"{usuario.nombres} {usuario.apellidos}")

    
    def generar(self):
        """Genera el PDF del contrato laboral con diseño profesional"""
        self._agregar_encabezado()
        y = self._agregar_seccion_datos()
        y = self._agregar_clausulas(y)

        if y < 5*cm:
            self.c.showPage()
            self.page_number += 1
            self._agregar_encabezado()
            y = self.height - 4*cm

        self._agregar_firmas(y)
        self._agregar_pie_pagina()
        self.c.save()


def generar_contrato_pdf(contrato, response, logo_path=None):
    """Generación de contrato laboral desde modelo Django"""
    contrato_pdf = ContratoLaboral(contrato, response, logo_path)
    contrato_pdf.generar()

