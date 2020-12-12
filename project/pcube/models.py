from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length= 30)
    post_type = models.CharField(max_length= 30)
    brand = models.CharField(max_length= 20)
    discription = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    address = models.CharField(max_length= 60)
    state = models.CharField(max_length= 20)
    city = models.CharField(max_length= 20)
    phone = models.CharField(max_length= 15)
    oldprice = models.PositiveIntegerField()
    newprice = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='placeholder.jpg', upload_to='Posts', height_field=None)

    def __str__(self):
        return self.title
    
    def save(self):
        super().save()

        img = Image.open(self.image.path)
        
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Buy(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.post_id.title