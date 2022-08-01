from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from currency.models import Rate, ContactUs, Source
from currency import utils

from currency.forms import RateForm, ContactUsForm, SourceForm
from django.views import generic

from silk.profiling.profiler import silk_profile


@silk_profile(name='View Index')
class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Currency Exchange Project - Home page'
        last_rate_date = utils.get_last_rate_date()
        context['last_rate_date'] = last_rate_date
        context['currency_types_list'] = utils.get_currency_types()
        context['sources_list'] = utils.get_sources()
        context['last_rate_list'] = utils.get_last_rate_list(last_rate_date)
        return context


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
@silk_profile(name='View Source List')
class SourceListView(generic.ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source list'
        return context


@silk_profile(name='View Source Create')
class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source create'
        return context


@silk_profile(name='View Source Update')
class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source update'
        return context


@silk_profile(name='View Source Delete')
class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source delete'
        return context


@silk_profile(name='View Source Details')
class SourceDetailsView(generic.DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Source details'
        return context


# =================Rate===================
@silk_profile(name='View Rate List')
class RateListView(generic.ListView):
    queryset = Rate.objects.all()
    template_name = 'rate_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate list'
        return context


@silk_profile(name='View Rate Create')
class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate create'
        return context


@silk_profile(name='View Rate Update')
class RateUpdateView(generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate update'
        return context


@silk_profile(name='View Rate Delete')
class RateDeleteView(generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate delete'
        return context


@silk_profile(name='View Rate Details')
class RateDetailsView(generic.DetailView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate details'
        return context


# =================ContactUs===================
@silk_profile(name='View ContactUs List')
class ContactUsListView(generic.ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us list'
        return context


@silk_profile(name='View ContactUs Create')
class ContactUsCreateView(generic.CreateView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_create.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:contactus_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us create'
        return context


@silk_profile(name='View ContactUs Update')
class ContactUsUpdateView(generic.UpdateView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_update.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:contactus_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us update'
        return context


@silk_profile(name='View ContactUs Delete')
class ContactUsDeleteView(generic.DeleteView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_delete.html'
    success_url = reverse_lazy('currency:contactus_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us delete'
        return context


@silk_profile(name='View ContactUs Details')
class ContactUsDetailsView(generic.DetailView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us details'
        return context
