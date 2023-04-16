from django.urls import path

from . import views

app_name = 'backoffice'

urlpatterns = [
    path('get_data/<int:experiment_id>', views.get_results, name="get_results"),
]
