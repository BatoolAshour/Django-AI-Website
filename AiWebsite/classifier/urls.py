from django.urls import path
from .views import ClassifyImageView, PredictionHistoryView
 
app_name = "classifier"
 
urlpatterns = [
    path('', ClassifyImageView.as_view(), name='classify'),
    path('history/', PredictionHistoryView.as_view(), name='history'),
]
 