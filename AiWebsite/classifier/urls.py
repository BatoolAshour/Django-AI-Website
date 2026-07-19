from django.urls import path
from . import views

urlpatterns = [
    path('', views.classify_image, name='classify'),
    path('history/', views.prediction_history, name='history'),
]