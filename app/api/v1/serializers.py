from rest_framework.serializers import ModelSerializer

from currency.models import Rate, Source, ContactUs


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'base_currency_type',
            'currency_type',
            'buy',
            'sale',
            'source',
            'created',
        )


class SourceSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'source_url',
            'name',
        )


class ContactUssSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'id',
            'email_from',
            'subject',
            'sended',
        )
