from django.forms import ModelForm
from .models import UploadedImage
 
 
class ImageForm(ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']