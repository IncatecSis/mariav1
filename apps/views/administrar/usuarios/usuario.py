from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_control
#from apps.principal.modelos.usuarios import Usuario
#from apps.principal.modelos.permisos import Permiso
#from apps.principal.forms.Usuario_form import UsuarioForm
#from apps.principal.forms.reset_password import reset_password_form#


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def usuario(request):
    return render(request, 'modulos/administrar/usuarios/usuario.html', {
        'titulo_pagina': 'Usuarios',
    })

'''
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = reset_password_form(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "La contraseña fue cambiada exitosamente.")
            except forms.ValidationError as e:
                messages.error(request, e.messages[0])
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
        return redirect('Incatec:usuarios')
'''


def gestion_permisos(request):
    return render(request, 'modulos/administrar/usuarios/permisos.html')

'''
def lista_permiso(permisos, permisos_asignados):
    permisos_organizados = []
    for vista in PERMISOS:
        nodo = {
            "id": vista["id"],
            "descripcion": vista["descripcion"],
            "ruta_name": vista.get("ruta_name", ""),
            "sub_vistas": [],
            "asignado": vista["id"] in permisos_asignados,
        }

        for sub_vista in vista.get("sub_vistas", []):
            nodo_subvista = {
                "id": sub_vista["id"],
                "descripcion": sub_vista["descripcion"],
                "ruta_name": sub_vista.get("ruta_name", ""),
                "acciones": [],
                "asignado": sub_vista["id"] in permisos_asignados,
            }

            for accion in sub_vista.get("acciones", []):
                nodo_accion = {
                    "id": accion["id"],
                    "descripcion": accion["descripcion"],
                    "ruta_name": accion.get("ruta_name", ""),
                    "asignado": accion["id"] in permisos_asignados,
                }
                nodo_subvista["acciones"].append(nodo_accion)

            nodo["sub_vistas"].append(nodo_subvista)

        permisos_organizados.append(nodo)

    return permisos_organizados

'''