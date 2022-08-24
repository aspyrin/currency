from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from accounts.forms import SignUpForm


class SignUpView(generic.CreateView):
    queryset = get_user_model().objects.all()
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('currency:index')


class UserActivateView(generic.RedirectView):
    pattern_name = 'currency:index'

    def get(self, request, *args, **kwargs):
        username = kwargs.pop('username')
        user = get_object_or_404(get_user_model(), username=username)

        if user.is_active:
            pass
        else:
            user.is_active = True
            user.save()

        response = super().get(request, *args, **kwargs)
        return response


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    queryset = get_user_model().objects.all()
    template_name = 'accounts/my_profile.html'
    success_url = reverse_lazy('currency:index')
    fields = (
        'first_name',
        'last_name',
    )

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(id=self.queryset.user.id)
    #     return queryset

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Profile'
        return context
