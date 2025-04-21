'''
from django import forms
from django.contrib.auth.password_validation import validate_password
from apps.principal.modelos.usuarios import Usuario
from apps.principal.modelos.rol import Roles

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'numero_documento', 'password', 'roles',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control',
                'style': 'text-transform: capitalize'
                }),

            'numero_documento': forms.TextInput(attrs={
                'class':'form-control'
                }),

            'password': forms.PasswordInput(attrs={
                'class':'form-control', 'placeholder': '*************'
                }),

            'roles': forms.Select(attrs={
                'class': 'form-select'
                }),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if self.cleaned_data.get('nombre'):
            user.nombre = ' '.join([word.capitalize() for word in self.cleaned_data['nombre'].split()])
                                    
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Roles.objects.all()
'''