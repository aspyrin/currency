import csv
import io

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from silk.profiling.profiler import silk_profile

from currency.models import Rate, ContactUs, Source
from currency import utils
from currency.forms import RateForm, ContactUsForm, SourceForm
from currency.tasks import send_contact_us_email


class IndexView(generic.TemplateView):
    template_name = 'index.html'

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
        if self.request.META['QUERY_STRING']:
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
    template_name = 'source_list.html'

    @silk_profile(name='SourceListView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source list'
        return context


class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceCreateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source create'
        return context


class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceUpdateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source update'
        return context


class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')

    @silk_profile(name='SourceDeleteView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source delete'
        return context


class SourceDetailsView(generic.DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'

    @silk_profile(name='SourceDetailsView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Source details (Id={self.object.id})'
        return context


# =================Rate===================
class RateListView(LoginRequiredMixin, generic.ListView):
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    template_name = 'rate_list.html'

    @silk_profile(name='RateListView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rates history'
        return context


class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    @silk_profile(name='RateCreateView: get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate create'
        return context


class RateUpdateView(UserPassesTestMixin, generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'rate_update.html'
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
    template_name = 'rate_delete.html'
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
    template_name = 'rate_details.html'

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
    template_name = 'contactus_create.html'
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
