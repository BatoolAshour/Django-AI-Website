from django.db import models

class PredictionResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    label = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.label} ({self.confidence:.2f})"