from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'docentes'

urlpatterns = [
    path('login/', login_docente, name='login_docentes'),
    path('logout/', logout_docente, name='logout_docentes'),
    path('index/', login_required(index), name='index_docentes'),
]

