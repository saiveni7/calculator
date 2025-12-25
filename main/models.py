# main/models.py

from django.db import models
from django.contrib.auth.models import User

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_emissions = models.FloatField()
    energy_emissions = models.FloatField()
    food_emissions = models.FloatField()
    lifestyle_emissions = models.FloatField()
    total_emissions = models.FloatField()
    annual_emissions = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username}'s calculation on {self.created_at.strftime('%Y-%m-%d')}"