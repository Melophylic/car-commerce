from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=255, default="car")
    price=models.IntegerField(default="0")
    description=models.TextField(default="a car")
    nama=models.CharField(max_length=255, default="mahasiswa")
    npm=models.IntegerField(default="0")
    kelas=models.CharField(max_length=255, default="PBP")

# class Myself(models.Model):
#     nama=models.CharField(max_length=255)
#     npm=models.IntegerField()
#     kelas=models.CharField(max_length=255)

