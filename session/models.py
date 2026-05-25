# models.py
from django.db import models
from django.contrib.auth.models import User

class BillingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    cash_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    credit_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    card_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    fonepay_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_bills = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.start_time}"