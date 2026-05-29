from django.urls import path
from .views import save_bill, get_bill

urlpatterns = [
    path('save/', save_bill),
    path('bill/<str:session_id>/', get_bill),
]