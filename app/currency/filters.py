import django_filters
from currency.models import Rate


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'base_currency_type': ('exact',),
            'currency_type': ('exact',),
            'source': ('exact',),
            'created': ('gte', 'lte',),
        }
