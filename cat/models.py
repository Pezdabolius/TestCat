from django.db import models
from django.contrib.auth.models import User


class Kitten(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['breed']),
        ]

    def __str__(self):
        return self.name
