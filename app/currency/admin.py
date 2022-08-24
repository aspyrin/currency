from django.contrib import admin
from currency.models import Rate, Source, ContactUs

# custom datetime filter
from rangefilter.filters import DateTimeRangeFilter

# import/export plugin
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class RateAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'base_currency_type',
        'currency_type',
        'sale',
        'buy',
        'source',
        'created',
    )
    readonly_fields = (
        'id',
        'base_currency_type',
        # 'source',
        'created',
    )
    search_fields = (
        'id',
    )
    list_filter = (
        'base_currency_type',
        'currency_type',
        'source',
        ('created', DateTimeRangeFilter),
    )


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate
        fields = (
            'base_currency_type',
            'currency_type',
            'sale',
            'buy',
            'source',
        )
        export_order = (
            'base_currency_type',
            'currency_type',
            'sale',
            'buy',
            'source',
        )


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'source_url',
    )
    readonly_fields = ('id',)
    search_fields = ('id', 'name',)


class ContactUsAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'email_from',
        'email_to',
        'subject',
        'sended',
    )
    readonly_fields = (
        'id',
        'email_from',
        'email_to',
        'subject',
        'message',
        'sended',
    )
    search_fields = (
        'id',
        'email_from',
        'email_to',
        'subject',
    )
    list_filter = (
        ('sended', DateTimeRangeFilter),
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class ContactUsResource(resources.ModelResource):

    class Meta:
        model = Rate
        fields = (
            'id',
            'email_from',
            'email_to',
            'subject',
            'message',
            'sended',
        )
        export_order = (
            'id',
            'email_from',
            'email_to',
            'subject',
            'message',
            'sended',
        )


admin.site.register(Rate, RateAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
