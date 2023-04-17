from django.urls import path

from . import views

app_name = 'backoffice'

urlpatterns = [
    path('get_data/<str:experiment_id>', views.get_results, name="results"),
    path('get_data', views.get_only_shared, name="results"),
    path('', views.main, name="main")
]
