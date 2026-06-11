# # signals.py
# from django.db.models.signals import post_save,m2m_changed
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Profile,Cart,Product,Sale,Rating,CartItem

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         if hasattr(instance, 'profile'):
#             instance.profile.save()

# @receiver(post_save, sender=Product)
# def post_save_create_update_sale(sender, instance, created, **kwargs):
#     sale_obj, _ = Sale.objects.get_or_create(
#         product=instance,
#         defaults={
#             'cart': None,
#             'amount': instance.rupees
#         }
#     )
#     sale_obj.amount = instance.rupees
#     sale_obj.save()

# @receiver(post_save, sender=CartItem)
# def update_cart_total_on_item_save(sender, instance, **kwargs):
#     instance.cart.update_totals()
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, CartItem

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(f"Signal triggered for user: {instance.username}")

    if created:
        profile = Profile.objects.create(user=instance)
        print(f"✅ Profile created successfully. Profile ID: {profile.id}")
    else:
        print(f"ℹ️ User updated. User ID: {instance.id}")

@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    print(f"🛒 Cart updated for cart ID: {instance.cart.id}")
    instance.cart.update_totals()