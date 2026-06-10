from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

@login_required
def google_login_jwt_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username,
        'email': user.email,
    })

#<--------test to ip addresh save-------->
# from django.http import JsonResponse
# def test_view(request):
#     return JsonResponse({
#         "ip": request.client_ip,
#         "user_agent": request.client_user_agent
#     })

from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin@123'
        )
        return HttpResponse("Superuser created!")
    return HttpResponse("Already exists")