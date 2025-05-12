from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
import holidays



DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

@api_view(['GET'])
def festivos(request, anio):
    try:
        anio= int(anio)
        if anio < 1900 or anio > 2100:
            return Response({
                'detail': 'Año inválido.'                
            }, status=400)
        
        festivo = holidays.Colombia(years=anio)
        respuesta = []

        for fecha in sorted(festivo.keys()):
            fecha_obtenida = datetime.combine(fecha, datetime.min.time())
            respuesta.append({
                'fecha': fecha_obtenida.strftime('%Y-%m-%d'),
                'dia semana': DIAS[fecha_obtenida.weekday()],
                'es festivo': True,
            })
        
        return Response(respuesta)
    
    except Exception as e:
        return Response({
            'detail': str(e)
            }, status=500)


@api_view(['GET'])
def calendario(request, anio, mes):
    try:
        anio = int(anio)
        mes = int(mes)

        fecha_inicio = datetime(anio, mes, 1)
        if mes == 12:
            fecha_fin = datetime(anio+1,1,1) - timedelta(days=1)
        else:
            fecha_fin=datetime(anio, mes +1,1) - timedelta(days=1)
        
        festivo = holidays.Colombia(years=anio)

        dias_no_festivos = []
        dias_festivos = []

        actual = fecha_inicio
        while actual <= fecha_fin:
            fecha_actual = actual.strftime('%Y-%m-%d')
            es_festivo = actual.date() in festivo
            dia_semana = DIAS[actual.weekday()]

            dia ={
                'fecha': fecha_actual,
                'dia semana': dia_semana,
                'es fectivo': es_festivo
            }

            if es_festivo:
                dias_festivos.append(dia)
            else:
                dias_no_festivos.append(dia)

            actual += timedelta(days=1)
        
        return Response({
            'dias no festivos': dias_no_festivos,
            'dias festivos': dias_festivos
        })
    
    except ValueError:
        return Response({
            'detail': 'Fecha inválida'
        }, status=400)
    except Exception as e:
        return Response({
            'detail': str(e)
        }, status=500)