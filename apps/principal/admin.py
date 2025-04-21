from django.contrib import admin
from django import forms
from apps.principal.modelos.usuario.Usuarios import Usuarios
from apps.principal.modelos.usuario.UsuarioRol import UsuarioRoles
from apps.principal.modelos.usuario.roles import Roles
from apps.principal.modelos.usuario.contraseñas import Credenciales
from apps.principal.modelos.matricula.modelos_matriculas.generales import *
from apps.principal.modelos.rrhh.contratos import *
from apps.principal.modelos.rrhh.tipo_contrato import *
from apps.principal.modelos.rrhh.datos_adicionales import *
from apps.principal.modelos.parametros.sedes import Sedes
from apps.principal.modelos.financiera.m_financiera import *




class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
        'id_usuario', 'numero_documento', 'nombres', 'apellidos', 'correo_electronico', 
        'celular', 'id_tipo_identificacion', 'id_departamento_expedicion',
        'id_municipio_expedicion', 'fecha_nacimiento', 'id_sexo', 
        'id_departamento_nacimiento', 'id_municipio_nacimiento', 'id_tipo_sangre', 
        'id_estado_civil', 'id_sisben', 'id_departamento_residencia', 
        'id_municipio_residencia', 'direccion_residencia', 'barrio', 'telefono', 
        'id_estrato', 'id_etnia', 'id_zona_residencial', 'id_eps', 
        'id_departamento_expulsor', 'id_municipio_expulsor', 'id_tipo_discapacidad', 'estado',
    )
    search_fields = ('numero_documento', 'nombres', 'apellidos', 'correo_electronico', 'celular')
    list_filter = ('estado', 'id_sexo', 'id_tipo_identificacion', 'id_estrato', 'id_etnia', 'id_eps')
    list_editable = ('estado',)
    ordering = ('numero_documento',)


class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol')

class CredencialesAdmin(admin.ModelAdmin):
    list_display = ('id_credencial', 'id_usuario', 'username', 'password', 'fecha_creacion')
    search_fields = ('id_usuario__nombres', 'username')

class MunicipioAdminForm(forms.ModelForm):
    class Meta:
        model = Municipios
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = Municipios.objects.filter(departamento_id=departamento_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['municipio'].queryset = self.instance.departamento.municipios.all()

class MunicipiosAdmin(admin.ModelAdmin):
    form = MunicipioAdminForm
    list_display = ('id_municipio', 'municipio', 'departamento', 'estado')
    list_filter = ('departamento', 'estado')
    search_fields = ('municipio',)

admin.site.register(Departamentos)
admin.site.register(Municipios, MunicipiosAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(UsuarioRoles)
admin.site.register(Roles, RolAdmin)
admin.site.register(Credenciales, CredencialesAdmin)
admin.site.register(Sexo)
admin.site.register(Sisben)
admin.site.register(EstadoCivil)
admin.site.register(EstratoSocioeconomico)
admin.site.register(Eps)
admin.site.register(Etnia)
admin.site.register(TipoDiscapacidad)
admin.site.register(TipoIdentificacion)
admin.site.register(TipoSangre)
admin.site.register(ZonaResidencial)
admin.site.register(Sedes)
admin.site.register(Contrataciones)
admin.site.register(TiposDeContrato)
admin.site.register(Bancos)
admin.site.register(Arl)
admin.site.register(CajasCompensacion)
admin.site.register(Convenios)
admin.site.register(CostosProgramas)
admin.site.register(Descuentos)
admin.site.register(Incrementos)
admin.site.register(MatriculasFinancieras)
admin.site.register(FormaPago)
admin.site.register(Financiaciones)
admin.site.register(Cuotas)
admin.site.register(MediosPago)
admin.site.register(Cartera)
admin.site.register(ConceptosPago)
admin.site.register(Pagos)
admin.site.register(PagosCuotas)
admin.site.register(Conciliaciones)
admin.site.register(Cargo)
admin.site.register(DepartamentoLaboral)
admin.site.register(RiesgoLaboral)
admin.site.register(TipoDespido)


