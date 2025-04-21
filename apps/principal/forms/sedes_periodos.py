'''
from django import forms
from apps.principal.modelos.sedes import Sede
from apps.principal.modelos.periodo import Periodo

class SedesPeriodosForm(forms.Form):
    sede = forms.ChoiceField(label='Selecciona la sede', choices=[], required=True)
    periodo = forms.ChoiceField(label='Selecciona el periodo', choices=[], required=True)
    enviar = forms.CharField(widget=forms.HiddenInput(),required=False, initial='Guardar')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_superuser:
            sede_choices = [(s.id, s.nombre) for s in Sede.objects.all()]
            periodo_choices = [(p.id, f"{p.get_anio()} - {p.get_semestre()}") for p in Periodo.get_all_periodos()]
        elif user:
            if not user.has_perm('server.view_sede'):
                raise ValueError('El usuario debe tener permiso para acceder')
            
            sede_choices = [(s.id, s.nombre) for s in Sede.get_accessible_sedes(user)]
            periodo_choices = [(p.id, f"{p.get_anio()} - {p.get_semestre()}") for p in Periodo.get_accessible_periodos(user)]
        else:
            raise ValueError('Usuario no especificado')

        self.fields['sede'].choices = sede_choices
        self.fields['periodo'].choices = periodo_choices
'''