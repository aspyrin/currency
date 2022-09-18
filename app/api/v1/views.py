from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.v1.filters import RateFilter, SourceFilter, ContactUsFilter
from api.v1.pagination import RatePagination
from api.v1.serializers import RateSerializer, SourceSerializer, ContactUssSerializer
from api.v1.throttles import AnonCurrencyThrottle
from currency.models import Rate, Source, ContactUs
from currency.tasks import send_contact_us_email

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['created', 'sale', 'buy']
    throttle_classes = [AnonCurrencyThrottle]


class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class SourcesView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['name']
    throttle_classes = [AnonCurrencyThrottle]


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUssSerializer
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    search_fields = ['subject', 'message']
    ordering_fields = ['sended', 'subject', 'message']
    throttle_classes = [AnonCurrencyThrottle]

    def create(self, request, *args, **kwargs):

        # get serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # save to db
        self.perform_create(serializer)

        # send email (task)
        email_from = serializer.validated_data['email_from']
        subject = serializer.validated_data['subject']
        send_contact_us_email.delay(subject, email_from)

        return Response(serializer.data)
