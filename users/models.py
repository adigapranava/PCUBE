from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length= 30, blank=True, null=True)
    phoneno = models.CharField(max_length= 13, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length= 20, blank=True, null=True)
    city = models.CharField(max_length= 20, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', height_field=None)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
