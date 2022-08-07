from django.db import models
from currency.model_choices import CarrencyType


class ResponseLog(models.Model):
    response_time = models.FloatField()
    request_method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    query_params = models.CharField(max_length=500)
    ip = models.CharField(max_length=20)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)


class Rate(models.Model):

    # if field has choices, we can get choice value
    # python: get_base_currency_type_display()
    # template: get_base_currency_type_display
    base_currency_type = models.CharField(
        max_length=3,
        choices=CarrencyType.choices,
        default=CarrencyType.CURRENCY_TYPE_UAH
    )
    currency_type = models.CharField(max_length=3, choices=CarrencyType.choices)
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
