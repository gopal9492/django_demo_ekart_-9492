from django.contrib import admin

from ecart.models import user_profiles, user_product, user_cart

# Register your models here.
admin.site.register(user_profiles)
admin.site.register(user_product)
admin.site.register(user_cart)
