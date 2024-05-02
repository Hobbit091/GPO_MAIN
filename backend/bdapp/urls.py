from django.urls import path
from . import views

app_name = 'bdapp'

urlpatterns = [
    path('',views.show),
    path('search',views.search_sequence),
    path('search_interp',views.search_InterpSelect),
    path('solve',views.solve),
]
    