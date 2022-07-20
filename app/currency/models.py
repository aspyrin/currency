from django.db import models


class Rate(models.Model):
    base_currency_type = models.CharField(max_length=3)
    currency_type = models.CharField(max_length=3)
    sale = models.DecimalField(max_digits=10, decimal_places=4)
    buy = models.DecimalField(max_digits=10, decimal_places=4)
    source = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=30)
    email_to = models.EmailField(max_length=30)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=3000)
    sended = models.DateTimeField(auto_now_add=True)
