from django.db import models
# from PIL import Image
# Create your models here.

class Places(models.Model):
     
    img = models.ImageField(upload_to= 'pics')
    place = models.CharField(max_length=25)
    desc = models.TextField()
    price = models.IntegerField()
    
    