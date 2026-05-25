from django.urls import path
from .views import add_customer, get_customers

urlpatterns = [
    path('add/', add_customer),
    path('customers/', get_customers),
]