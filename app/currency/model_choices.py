# do not import from project
from django.db import models

# CURRENCY_TYPE_UAH = 'UAH'
# CURRENCY_TYPE_USD = 'USD'
# CURRENCY_TYPE_EUR = 'EUR'
# CURRENCY_TYPE_BTC = 'BTC'
#
# CURRENCY_TYPES = (
#     ('UAH', 'Hrivna'),
#     ('USD', 'Dollar'),
#     ('EUR', 'Euro'),
#     ('BTC', 'BitCoin'),
# )


class CarrencyType(models.TextChoices):
    CURRENCY_TYPE_UAH = 'UAH', 'Hrivna'
    CURRENCY_TYPE_USD = 'USD', 'Dollar'
    CURRENCY_TYPE_EUR = 'EUR', 'Euro'
    CURRENCY_TYPE_BTC = 'BTC', 'BitCoin'
