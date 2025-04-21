from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.principal.inicio_sesion.login_super import login, logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('logout/', login_required(logout), name='logout'),
    path('incatec/', include(('apps.urls', 'Incatec'))),
    path('incatec_administracion/', include(('apps.principal.urls', 'Incatec_administracion'))),
    path('portal_docentes/', include(('apps.docentes.urls', 'docentes'))),
    path('portal_estudiantes/', include(('apps.estudiantes.urls', 'estudiantes'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.principal.inicio_sesion.login_super.error'



'''
"""
URL configuration for maria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.principal.inicio_sesion.login_super import login,logout
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('logout/', login_required(logout), name='logout'),
    path('incatec/', include(('apps.urls', 'Incatec'))),
    path('incatec_administracion/', include(('apps.principal.urls', 'Incatec_administracion'))),
    path('portal_docentes/', include(('apps.docentes.urls', 'docentes'))),
    path('portal_estudiantes/', include(('apps.estudiantes.urls', 'estudiantes'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.principal.inicio_sesion.login_super.error'
'''