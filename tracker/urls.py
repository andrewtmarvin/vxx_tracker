from django.urls import path, register_converter
from . import views, converters

app_name = 'tracker'

register_converter(converters.NegativeIntConverter, 'negint')

urlpatterns = [
    path('', views.index, name='index'),
    path('get_gpx/<int:year>/<int:day>/', views.get_gpx, name='get_gpx'),
    path('get_gpx/<int:year>/<negint:day>/', views.get_gpx, name='get_gpx'),
]


