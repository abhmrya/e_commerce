from django.urls import path,include
from .views import RegisterView, LoginView
from . import views
from .views import LogoutView

urlpatterns = [
    path('apiregister/', RegisterView.as_view(), name='apiregister'),
    path('apilogin/', LoginView.as_view(), name='apilogin'),
    path('register/',views.login_register,name="register"),
    path('logoutt/',views.logout_auth,name="logoutt"),
    path('login/', views.login_auth, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
