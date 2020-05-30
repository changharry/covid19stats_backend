from django.urls import path
from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('global', views.global_stats),
    path('global_total', views.global_total),
    path('regional_stats', views.regional_stats),
    path('g_total', views.g_total),
    path('g_total_change', views.g_total_change),
    path('g_total_rate_change', views.g_total_rate_change)
]