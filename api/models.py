from django.db import models
from session.models import BillingSession

class Summary(models.Model):
    session = models.OneToOneField(BillingSession, on_delete=models.CASCADE,unique=True,null=True,blank=True)
    
    opening_balance = models.FloatField()
    cash_sales = models.FloatField()
    pos = models.FloatField()
    fonepay = models.FloatField()
    credit = models.FloatField()
    total_sales = models.FloatField()
    excess_less=models.FloatField()
    expenses = models.FloatField()
    deposited_bank = models.FloatField()
    given_other = models.FloatField()
    closing_balance = models.FloatField()


    def __str__(self):
        return str(self.session)