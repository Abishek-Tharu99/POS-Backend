# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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

            last_session = BillingSession.objects.order_by('-id').first()
            new_number = 1

            if last_session and last_session.session_id:
                try:
                    last_number= int(
                       last_session.session_id.split('-')[1]
                    )
                    new_number = last_number + 1
                   
                except(ValueError,IndexError):
                    new_number = 1
            
            year = datetime.now().year
            self.session_id = (
                f"{self.user.username}-{year}-{new_number:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.start_time}"