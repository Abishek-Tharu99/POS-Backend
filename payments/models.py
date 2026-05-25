from django.db import models

class PaymentTransaction(models.Model):
    bill = models.ForeignKey('billing.Bill', on_delete=models.CASCADE)
    amount = models.FloatField()
    method = models.CharField(max_length=50)  # fonepay, card, etc
    status = models.CharField(max_length=20)  # pending, success, failed
    qr_data = models.TextField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)