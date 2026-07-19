from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"


class PredictionResult(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='predictions')
    label = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} ({self.confidence:.2f})"