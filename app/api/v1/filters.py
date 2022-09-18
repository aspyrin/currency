import django_filters
from currency.models import Rate, Source, ContactUs


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'base_currency_type': ('exact',),
            'currency_type': ('exact',),
            'source': ('exact',),
            'created': ('gte', 'lte',),
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'name': ('contains',),
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'subject': ('contains',),
            'message': ('contains',),
            'sended': ('gte', 'lte',),
        }
