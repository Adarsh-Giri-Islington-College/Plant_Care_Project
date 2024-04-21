from django.db import models
from users.models import User
import pytz
from datetime import datetime


class Prediction(models.Model):
    prediction_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    predicted_label = models.CharField(max_length=100)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    recommended_products = models.JSONField(default=list)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        nepal_timezone = pytz.timezone('Asia/Kathmandu')
        current_time = nepal_timezone.localize(datetime.now())
        self.timestamp = current_time
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Prediction{self.prediction_id}"