from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'estudiantes'

urlpatterns = [
    path('login/', login_estudiante, name='login_estudiantes'),
    path('logout/', logout_estudiante, name='logout_estudiantes'),
    path('index/', login_required(index), name='index_estudiantes'),
]

