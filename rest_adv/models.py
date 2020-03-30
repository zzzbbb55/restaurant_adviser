from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True)
    rate = models.FloatField(default = 0)
    slug = models.SlugField(unique = True)

    # current categories:
    # chinese food
    # italian
    # sushi
    # fast food
    # snack
    # ice cream
    category = models.CharField(max_length=64, default='fast food') # everyone loves junk food :)

    intro = models.TextField(default = 'nothing yet')
    picture = models.ImageField(upload_to='restaurant_images', blank=True, default="statics/images/1.jpeg")

    createdAt = models.DateTimeField("Create time",auto_now_add=True)
    updatedAt = models.DateTimeField("Update time",auto_now=True)
    deletedAt = models.DateTimeField("Delete time",null=True,default=None)

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.save()

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

    createdAt = models.DateTimeField("Create time",auto_now_add=True)
    updatedAt = models.DateTimeField("Update time",auto_now=True)
    deletedAt = models.DateTimeField("Delete time",null=True,default=None)

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.save()

    def __str__(self):
        return self.rate

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    like_restaurants = models.ManyToManyField('Restaurant')

    createdAt = models.DateTimeField("Create time",auto_now_add=True)
    updatedAt = models.DateTimeField("Update time",auto_now=True)
    deletedAt = models.DateTimeField("Delete time",null=True,default=None)

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username