from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer
# from .tasks import send_welcome_email as send_welcome_email_task  



class  RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print('login api')
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            subject = "Welcome to Our Site!"
            message = f"Hello {user.username}, thanks for login!"
            recipient_list = [user.email]
            # send_welcome_email_task.delay(subject, message, recipient_list)  

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                },
                "tokens": serializer.validated_data["tokens"]
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
# Create your views here.
def login_register(request):
    return render(request, 'register.html')

def login_auth(request):
    return render(request,'register.html')

@login_required
def logout_auth(request):
    print('session long out')
    logout(request)
    subject = "Welcome to Our Site!"
    message = f"Hello {request.user.username}, thanks for login!"
    recipient_list = [request.user.email]
    # send_welcome_email_task.delay(subject, message, recipient_list) 
    return redirect('login') 


# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         print('jwt long out')
#         try:
#             logout(request)
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except TokenError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print("JWT LOGOUT HIT")
#         print(request.data)

#         try:
#             refresh_token = request.data.get("refresh")

#             if refresh_token:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()

#             logout(request)

#             return Response(
#                 {"message": "Logout success"},
#                 status=status.HTTP_200_OK
#             )

#         except Exception as e:
#             print(e)
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("JWT LOGOUT HIT")

        logout(request)   # session bhi khatam

        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )