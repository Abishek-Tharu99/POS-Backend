from django.urls import path
from .views import get_items,save_bill,get_bill_no,get_recent_bills,get_bill_details

urlpatterns = [
    path('items/', get_items),
    path('save/', save_bill, name='save_bill'),
    path('bill_no/', get_bill_no, name='get_bill_no'), 
    path('bills/recent/', get_recent_bills),
    path('bills/detail/<str:bill_no>/', get_bill_details),

]