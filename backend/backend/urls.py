from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.show),
    path('search',views.search),
    path('search1',views.search1),
    path('solve',views.solve),
]
