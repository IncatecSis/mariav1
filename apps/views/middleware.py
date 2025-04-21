from django.shortcuts import redirect
from django.urls import reverse


class SedePeriodoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = [
            reverse('Incatec:index'),
            reverse('login'),
            reverse('logout'),
            reverse('estudiantes:login_estudiantes'),
            reverse('docentes:login_docentes'),
        ]
        self.exempt_prefixes = ['/admin']

    def __call__(self, request):
        if self._is_exempt_path(request):
            return self.get_response(request)

        if request.user.is_authenticated:
            if self._is_admin_user(request):
                return self.get_response(request)

            if request.user.roles.id == 1:
                if request.path != reverse('estudiantes:index_estudiantes'):
                    return redirect('estudiantes:login_estudiantes')

            elif request.user.roles.id == 3:
                if request.path != reverse('docentes:index_docentes'):
                    return redirect('docentes:login_docentes')

            elif request.user.roles.id == 2:
                if not self._has_selected_sede_and_periodo(request):
                    return redirect('Incatec:index') 
                if not self._has_permisos_asignados(request):
                    return redirect('Incatec:index')

        return self.get_response(request)

    def _is_exempt_path(self, request):
        return request.path in self.allowed_paths or any(request.path.startswith(prefix) for prefix in self.exempt_prefixes)

    def _is_admin_user(self, request):
        return request.user.is_superuser or request.user.tiene_acceso_completo()

    def _has_selected_sede_and_periodo(self, request):
        sede_id = request.session.get('sede_id')
        periodo_id = request.session.get('periodo_id')
        return bool(sede_id and periodo_id)

    def _has_permisos_asignados(self, request):
        return request.user.tiene_permisos()
