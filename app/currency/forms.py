from django import forms
from currency.models import Rate, ContactUs, Source


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'base_currency_type',
            'currency_type',
            'sale',
            'buy',
            'source',
        )


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            # 'email_to',
            'subject',
            'message',
        )
        widgets = {
            'subject': forms.Textarea(attrs={'cols': 100, 'rows': 2}),
            'message': forms.Textarea(attrs={'cols': 100, 'rows': 5}),
        }


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'source_url',
            'name',
        )
