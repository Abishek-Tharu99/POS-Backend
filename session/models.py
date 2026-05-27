# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class BillingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    session_id = models.CharField(max_length=200, blank=True,unique=True)
    is_active = models.BooleanField(default=True)

    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    cash_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    credit_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    card_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    fonepay_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_bills = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.session_id:
            
            date_part = timezone.now().strftime("%Y%m%d")
            uid = uuid.uuid4().hex[:6]

            self.session_id = f"{self.user.username}-{date_part}-{uid}"

        self.cash_sales = max(
        self.total_sales - (
        self.card_sales + self.fonepay_sales + self.credit_sales
            ),0
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.start_time}"
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["session_id"]),
        ]   