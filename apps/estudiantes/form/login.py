from django import forms
from django.contrib.auth import authenticate


class LoginEstudiante(forms.Form):
    numero_documento = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, roles=None,**kwargs):
        self.roles = roles
        super().__init__(*args, **kwargs)

    def clean(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        password = self.cleaned_data.get('password')

        user = authenticate(numero_documento=numero_documento, password=password)
        if not user:
            raise forms.ValidationError('Contraseña incorrecta.!!')
        
        if self.rol:
            if user.is_superuser:
                self.user = user
                return self.cleaned_data
            
        if not user.roles or user.roles.nombre != self.roles:
            raise forms.ValidationError(f'No tienes permisos para acceder a este login {self.rol}')
        

        self.user = user
        return self.cleaned_data
    
    def get_user(self):
        return self.user