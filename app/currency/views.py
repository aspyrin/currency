import csv
import io

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from silk.profiling.profiler import silk_profile
from django_filters.views import FilterView

from currency.filters import RateFilter
from currency.models import Rate, ContactUs, Source
from currency import utils
from currency.forms import RateForm, ContactUsForm, SourceForm
from currency.tasks import send_contact_us_email


class IndexView(generic.TemplateView):
    template_name = 'currency/index.html'

    # input point for all queries
    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     return response

    @silk_profile(name='IndexView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest exchange rates'
        context['last_rate_date'] = utils.get_last_rate_date()
        context['currency_types_list'] = utils.get_currency_types()
        sort_by_type = {
            'sale_asc': 'Sort by Sale (ASC)',
            'sale_desc': 'Sort by Sale (DESC)',
            'buy_asc': 'Sort by Buy (ASC)',
            'buy_desc': 'Sort by Buy (DESC)',
        }
        if self.request.GET:
            context['last_rate_list'] = utils.get_last_rate_list(self.request.GET['sort_params'])
            context['sort_by'] = sort_by_type.get(self.request.GET['sort_params'])
        else:
            context['last_rate_list'] = utils.get_last_rate_list()
            context['sort_by'] = sort_by_type.get('sale_asc')
        return context


@silk_profile(name='rate_generator')
def rate_generator(request):
    """
    function clear currency_rate table,
    generate random values and insert 100 records into currency_rate table
    :param
    none
    :return:
    link to rate_list
    """
    utils.rates_gen()
    return HttpResponseRedirect(reverse('currency:rate_list'))


@silk_profile(name='contactus_generator')
def contactus_generator(request):
    """
    function clear currency_contactus table,
    and insert records into currency_contactus table
    :param
    none
    :return:
    link to contactus_list
    """
    utils.contactus_gen()
    return HttpResponseRedirect(reverse('currency:contactus_list'))


# =================Source==================
class SourceListView(generic.ListView):
    queryset = Source.objects.all().order_by('name')
    template_name = 'currency/source_list.html'

    @silk_profile(name='SourceListView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source list'
        return context


class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'currency/source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceCreateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source create'
        return context


class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'currency/source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceUpdateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source update'
        return context


class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'currency/source_delete.html'
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceDeleteView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source delete'
        return context


class SourceDetailsView(generic.DetailView):
    queryset = Source.objects.all()
    template_name = 'currency/source_details.html'

    @silk_profile(name='SourceDetailsView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Source details (Id={self.object.id})'
        return context


# =================Rate===================
class RateListView(LoginRequiredMixin, FilterView):
    queryset = Rate.objects.all().select_related('source')
    filterset_class = RateFilter
    template_name = 'currency/rate_list.html'
    paginate_by = 10
    ordering = '-created'
    order_choices = {
        'created': 'Created (ASC)',
        '-created': 'Created (DESC)',
        'sale': 'Sale (ASC)',
        '-sale': 'Sale (DESC)',
        'buy': 'Buy (ASC)',
        '-buy': 'Buy (DESC)',
    }

    def get_ordering(self):
        if 'sort_by' in self.request.GET:
            ordering = self.request.GET['sort_by']
        else:
            ordering = self.ordering
        return ordering

    def get_paginate_by(self, queryset):
        if 'page_size' in self.request.GET:
            paginate_by = self.request.GET['page_size']
        else:
            paginate_by = self.paginate_by
        return paginate_by

    @silk_profile(name='RateListView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rates history'

        if self.request.GET.get('page'):
            cur_page = int(self.request.GET['page'])
        else:
            cur_page = 1

        context['pagination_get_visible_range'] = utils.pagination_get_visible_range(
            self.queryset.count(),
            self.paginate_by,
            cur_page
        )
        context['page_size'] = self.get_paginate_by(self.queryset)
        context['sort_by'] = self.get_ordering()
        context['order_by_show'] = self.order_choices.get(self.get_ordering())
        context['order_choices'] = self.order_choices

        filter_params = self.request.GET.copy()
        if self.page_kwarg in filter_params:
            del filter_params[self.page_kwarg]

        if 'page_size' in filter_params:
            del filter_params['page_size']

        if 'sort_by' in filter_params:
            del filter_params['sort_by']

        context['filter_params'] = filter_params.urlencode()
        context['filter_params_count'] = utils.filter_params_count(filter_params.dict())
        context['filtered'] = self.object_list.count()
        context['total'] = self.queryset.count()

        return context


class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'currency/rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    @silk_profile(name='RateCreateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate create'
        return context


class RateUpdateView(UserPassesTestMixin, generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'currency/rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        """only allowed for superuser"""
        return self.request.user.is_superuser

    @silk_profile(name='RateUpdateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate update'
        return context


class RateDeleteView(UserPassesTestMixin, generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'currency/rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        """only allowed for superuser"""
        return self.request.user.is_superuser

    @silk_profile(name='RateDeleteView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate delete'
        return context


class RateDetailsView(generic.DetailView):
    queryset = Rate.objects.all()
    template_name = 'currency/rate_details.html'

    @silk_profile(name='RateDetailsView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Rate details (Id={self.object.id})'
        return context


class DownloadRateView(generic.View):
    """
    class for generating csv from Rate model
    """

    def get(self, request):
        """
        function based on io lib
        :param request:
        :return: csv
        """
        csv_io = io.StringIO()
        csv_writer = csv.writer(csv_io)
        headers = ['id', 'buy', 'sale']
        csv_writer.writerow(headers)
        for rate in Rate.objects.all():
            row = [
                rate.id,
                rate.buy,
                rate.sale,
            ]
            csv_writer.writerow(row)
        csv_io.seek(0)
        return HttpResponse(csv_io.read(), content_type='text/csv')


# =================ContactUs===================
# class ContactUsListView(generic.ListView):
#     queryset = ContactUs.objects.all()
#     template_name = 'contactus_list.html'

    # @silk_profile(name='ContactUsListView: get_context_data')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Contact Us list'
    #     return context


class ContactUsCreateView(generic.CreateView):
    queryset = ContactUs.objects.all()
    template_name = 'currency/contactus_create.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:index')

    @silk_profile(name='ContactUsCreateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # call celery task
        send_contact_us_email.delay(self.object.subject, self.object.email_from)
        return response
