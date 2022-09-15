from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.serializers import RateSerializer, SourceSerializer, ContactUssSerializer
from currency.models import Rate, Source, ContactUs
from currency.tasks import send_contact_us_email


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class SourcesView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUssSerializer

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
