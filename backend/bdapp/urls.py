from django.urls import path
from . import views

app_name = 'bdapp'

urlpatterns = [
    path('',views.show),
    path('home',views.show),
    path('search',views.search_sequence),
    path('search_interp',views.search_InterpSelect),
    path('solve',views.solve),
    path('search_seq',views.search_SeqSelect),
    path('alg_test',views. alg_TableTitle),
    path('interp',views.interp_Select),
    path('alg',views.alg_Select),
    path('algDetails',views.alg_SelectDetails),
    
     path('main', views.main_view, name='main')
]
    