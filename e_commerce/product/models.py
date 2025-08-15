from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300,default="Not set")
    pincode = models.IntegerField(default=0)
    photo = models.ImageField(
        upload_to='profile_images/',
        default='image.png'
    )

    def __str__(self):
        return self.user.username

# Rating Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True)
    descriptions=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.rating}"

# Product Model
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='products/')
    rupees = models.DecimalField(max_digits=10, decimal_places=2)
    product_offer = models.PositiveIntegerField(null=True, blank=True)
    final_rupees=models.PositiveIntegerField(null=True, blank=True)
    review = models.TextField(blank=True,null=True)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # buyer=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.final_rupees = self.rupees - (self.rupees * self.product_offer / 100)
        super().save(*args, **kwargs)


# Cart Model
# class Cart(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     product = models.ManyToManyField(Product)
#     quantity = models.PositiveIntegerField(default=1)
#     total_price=models.PositiveIntegerField(blank=True,null=True)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product}"

class Cart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def update_totals(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.get_total_price() for item in cart_items)
        self.total_price = total
        self.save()

    def __str__(self):
        return f"{self.user.user.username}'s cart"

class Sale(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True, null=True)

# New way — using CartItem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.final_rupees * self.quantity

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity})"
    
    
class Backgroundimg(models.Model):
    image=models.ImageField(upload_to='background/')
    name=models.CharField(max_length=225)

class Specialproduct(models.Model):
    image=models.ImageField(upload_to='special')
    logo=models.ImageField(upload_to='special_logo')
    name=models.CharField(max_length=50)
    price=models.PositiveIntegerField(null=True,blank=True)
    offer=models.PositiveIntegerField(null=True,blank=True)
    final_price=models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.final_price = self.price-((self.price*self.offer)/100)
        super().save(*args, **kwargs)
