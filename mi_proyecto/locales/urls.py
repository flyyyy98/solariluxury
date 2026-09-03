from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_locales, name='lista_locales'),
    path('informacion/', views.informacion, name='informacion'),
]