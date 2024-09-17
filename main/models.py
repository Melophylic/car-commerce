from django.db import models
import uuid

class Product(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255, default="car")
    price=models.IntegerField(default="0")
    description=models.TextField(default="a car")

class Me(models.Model):
    nama=models.CharField(max_length=255, default="Muhammad Nadzim Tahara")
    npm=models.CharField(max_length=255, default="2306275430")
    kelas=models.CharField(max_length=255, default="PBP C 2024")