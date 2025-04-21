'''
from django import forms
from apps.principal.modelos.usuarios import Usuario

class reset_password_form(forms.Form):
    usuario_id = forms.IntegerField(widget=forms.HiddenInput())
    nueva_contraseña = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'}),
                label='Nueva Contraseña'
    )

    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}),
            label='Confirmar contraseña'   
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get('nueva_contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        if nueva_contraseña and confirmar_contraseña:
            if nueva_contraseña != confirmar_contraseña:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            if len(nueva_contraseña) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return cleaned_data

    def save(self):
        usuario_id = self.cleaned_data['usuario_id']
        nueva_contraseña = self.cleaned_data['nueva_contraseña']
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            usuario.set_password(nueva_contraseña)
            usuario.save() 
        except Usuario.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")


'''