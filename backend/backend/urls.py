from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.show),
    path('search',views.search_sequence),
    path('search_interp',views.search_InterpSelect),
    path('solve',views.solve),
]
    
