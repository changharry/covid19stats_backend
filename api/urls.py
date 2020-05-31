from django.urls import path
from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('global', views.global_stats),
    path('global_total', views.global_total),
    path('regional_stats', views.regional_stats),
    path('g_total', views.g_total),
    path('g_total_change', views.g_total_change),
    path('g_total_rate_change', views.g_total_rate_change),
    path('r_total/<str:country>', views.r_total),
    path('r_change/<str:country>', views.r_change),
    path('r_rate_change/<str:country>', views.r_rate_change),
    path('r_delta_rate_change/<str:country>', views.r_delta_rate_change),
    path('g_delta_rate_change', views.g_delta_rate_change)]
