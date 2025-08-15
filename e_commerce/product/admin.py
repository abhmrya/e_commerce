from django.contrib import admin
from .models import Product,Profile,Rating,Sale,Cart,Backgroundimg,Specialproduct
# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Sale)
admin.site.register(Backgroundimg)
admin.site.register(Specialproduct)

