from django.urls import path
from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('global', views.global_stats),
    path('global_total', views.global_total),
    path('regional_stats', views.regional_stats),
    path('graph', views.graph_data)
]