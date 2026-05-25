from django.urls import path
from .views import save_bill, get_bill

urlpatterns = [
    path('save/', save_bill),
    path('bill/<str:date>/', get_bill),
]