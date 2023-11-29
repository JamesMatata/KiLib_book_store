from django.db import models


class LNMOnline(models.Model):
    CheckoutRequestID = models.CharField(max_length=100)
    MerchantRequestID = models.CharField(max_length=50)
    ResultCode = models.IntegerField()
    ResultDesc = models.CharField(max_length=120)
    Amount = models.FloatField()
    MpesaReceiptNumber = models.CharField(max_length=15)
    TransactionDate = models.IntegerField()
    PhoneNumber = models.CharField(max_length=13)
