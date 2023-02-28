from django.urls import path
from . import views

urlpatterns = [
    path('images', views.Images.as_view(), name ='images'),
    path('answer/<int:pk>', views.Answer.as_view(), name ='answer'),
]