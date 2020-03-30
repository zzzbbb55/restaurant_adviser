from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True)
    rate = models.FloatField(default = 0)
    slug = models.SlugField(unique = True)
    intro = models.TextField(default = 'nothing yet')
    picture = models.ImageField(upload_to='restaurant_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default = 0)
    message = models.TextField(default = 'nothing yet')

    def __str__(self):
        return self.rate

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username