# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .tasks import send_welcome_email as send_welcome_email_task  
# from django.core.mail import send_mail
# from django.conf import settings

# # Signal for user registration
# @receiver(post_save, sender=User)
# def send_welcome_email_signal(sender, instance, created, **kwargs):
#     if created:
#         print('signal of registration send email')
#         subject = "Welcome to Our Site!"
#         message = f"Hello {instance.username}, thanks for registering!"
#         recipient_list = [instance.email]
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
#         send_welcome_email_task.delay(subject, message, recipient_list)  

# # Signal for user login
# from django.contrib.auth.signals import user_logged_in

# @receiver(user_logged_in)
# def show_login_info(sender, request, user, **kwargs):
#     print('signal of send email user login')
#     subject = "Welcome Back!"
#     message = f"Hello {user.username}, you have successfully logged in!"
#     recipient_list = [user.email]
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)

#     send_welcome_email_task.delay(subject, message, recipient_list)

# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.signals import user_logged_in


# Signal for user registration
# @receiver(post_save, sender=User)
# def send_welcome_email_signal(sender, instance, created, **kwargs):
#     if created:
#         print('signal of registration send email')
#         subject = "Welcome to Our Site!"
#         message = f"Hello {instance.username}, thanks for registering!"
#         recipient_list = [instance.email]
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)


# # Signal for user login
# @receiver(user_logged_in)
# def show_login_info(sender, request, user, **kwargs):
#     print('signal of send email user login')
#     subject = "Welcome Back!"
#     message = f"Hello {user.username}, you have successfully logged in!"
#     recipient_list = [user.email]
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)