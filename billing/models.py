# billing/models.py

from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # 🔥 ADD THIS
    bill_no = models.CharField(max_length=50, unique=True)
    date_en = models.DateField()
    date_np = models.CharField(max_length=20)
    time = models.TimeField()
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_no = models.CharField(max_length=15, blank=True, null=True)
    customer_pan = models.CharField(max_length=20, blank=True, null=True)
    customer_addr = models.CharField(max_length=255, blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)

    tender = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.bill_no


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")

    code = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=100)

    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="payments")

    method = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
class BillSequence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=10)
    last_no = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'bill_type')