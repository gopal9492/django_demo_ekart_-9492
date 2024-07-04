from django.db import models


# Create your models here.
class user_profiles(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images/')
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)


class user_product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')


class user_cart(models.Model):
    user = models.ForeignKey(user_profiles, on_delete=models.CASCADE)
    product = models.ForeignKey(user_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


