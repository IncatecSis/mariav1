"""
from .modelos.permisos import Permiso

PERMISOS = [
    {
        "id": 1,
        "descripcion": "Acceso completo",
        "ruta_name": "",
        "sub_vistas": [],
    },
    {
        "id": 2,
        "descripcion": "Index",
        "ruta_name": "Incatec:index",
        "sub_vistas": []
    },
    {
        "id": 3,
        "descripcion": "Académica",
        "ruta_name": "Incatec:matricula",
        "sub_vistas": [
            {
                "id": 31,
                "descripcion": "Registro y Matrícula",
                "ruta_name": "registro_matricula",
                "acciones": []
            },
        ],
    },
    {
        "id": 4,
        "descripcion": "Financiera",
        "ruta_name": "",
        "sub_vistas": [
            {"id": 41, "descripcion": "Financiación", "ruta_name": "Incatec:financiacion", "acciones": []},
            {"id": 42, "descripcion": "Pagos", "ruta_name": "Incatec:pagos", "acciones": []},
            {"id": 43, "descripcion": "Notas D y C", "ruta_name": "Incatec:notas", "acciones": []},
            {"id": 44, "descripcion": "Informes Pagos", "ruta_name": "Incatec:informes", "acciones": []},
            {"id": 45, "descripcion": "Permisos de Cartera", "ruta_name": "Incatec:permisos_cartera", "acciones": []},
            {"id": 46, "descripcion": "Seguimiento de Cartera", "ruta_name": "Incatec:seguimiento_cartera", "acciones": []},
            {"id": 47, "descripcion": "Auditoría Financiera", "ruta_name": "Incatec:auditoria_financiera", "acciones": []},
        ],
    },
    {
        "id": 5,
        "descripcion": "Control de Ingreso",
        "ruta_name": "",
        "sub_vistas": [
            {
                "id": 51,
                "descripcion": "Registro de Ingreso",
                "ruta_name": "Incatec:informes",
                "acciones": []
            },
        ],
    },
    {
        "id": 6,
        "descripcion": "Talento Humano",
        "ruta_name": "",
        "sub_vistas": [],
    },
    {
        "id": 7,
        "descripcion": "SGC",
        "ruta_name": "",
        "sub_vistas": [],
    },
    {
        "id": 8,
        "descripcion": "Utilidades",
        "ruta_name": "",
        "sub_vistas": [
            {
                "id": 81,
                "descripcion": "Financiaciones Masivas",
                "ruta_name": "Incatec:informes",
                "acciones": []
            },
        ],
    },
    {
        "id": 9,
        "descripcion": "Administrar",
        "ruta_name": "",
        "sub_vistas": [
            {"id": 91, "descripcion": "Usuarios", "ruta_name": "Incatec:usuarios", "acciones": []},
            {"id": 92, "descripcion": "Parámetros Financieros", "ruta_name": "Incatec:parametros_financieros", "acciones": []},
            {"id": 93, "descripcion": "Parámetros Académicos", "ruta_name": "Incatec:parametros_academicos", "acciones": []},
            {"id": 94, "descripcion": "Otros Parámetros", "ruta_name": "Incatec:otros_parametros", "acciones": []},
        ],
    },
]


def asignar_permiso():
    for vista in PERMISOS:
        permiso_general, creado_general = Permiso.objects.update_or_create(
            id=vista["id"],
            defaults={"descripcion": vista["descripcion"]}
        )
        if creado_general:
            print(f'Permiso creado: {permiso_general.descripcion}')
        else:
            print(f'El permiso ya existe: {permiso_general.descripcion}')

        for sub_vista in vista.get("sub_vistas", []):
            permiso_subvista, creado_subvista = Permiso.objects.update_or_create(
                id=sub_vista["id"],
                defaults={"descripcion": sub_vista["descripcion"]}
            )
            if creado_subvista:
                print(f'Subvista creada: {permiso_subvista.descripcion}')
            else:
                print(f'La subvista ya existe: {permiso_subvista.descripcion}')

            for accion in sub_vista.get("acciones", []):
                permiso_accion, creado_accion = Permiso.objects.update_or_create(
                    id=accion["id"],
                    defaults={"descripcion": accion["descripcion"]}
                )
                if creado_accion:
                    print(f'Acción creada: {permiso_accion.descripcion}')
                else:
                    print(f'La acción ya existe: {permiso_accion.descripcion}')
"""