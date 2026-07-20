from django.db import models

class PredictionResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    label = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.label} ({self.confidence:.2f})"
    
    class ResultStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('finished_ai', 'Finished - AI Generated'),
        ('finished_real', 'Finished - Real'),
        ('failed', 'Failed'),
    ]

    result = models.ForeignKey(PredictionResult, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    #caption = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result_id} - {self.status}"