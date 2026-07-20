from django.forms import ModelForm
from .models import PredictionResult


class ImageForm(ModelForm):
    class Meta:
        model = PredictionResult
        fields = ['image']