from django.db import models
from users.models import User
from info.models import Plant_Info


class Favorite(models.Model):
    favorite_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant_Info, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite {self.favorite_id}"