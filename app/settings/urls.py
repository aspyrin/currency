from django.contrib import admin
from django.urls import path

from currency.views import rate_generator, rate_list, contactus_list, contactus_generator

urlpatterns = [
    path('admin/', admin.site.urls),

    path('rate_generator/', rate_generator),
    path('rate_list/', rate_list),
    path('contactus_generator', contactus_generator),
    path('contactus_list/', contactus_list),
]
