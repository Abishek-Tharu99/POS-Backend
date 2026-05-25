from django.urls import path
from .views import signup,login,profile

urlpatterns = [
    path('register/', signup, name='signup'),  
    path('login/', login),
    path('profile/', profile),
  
]