from django.contrib import admin
from django.urls import path

from currency.views import index
from currency.views import rate_generator
from currency.views import contactus_generator
from currency.views import source_list, source_create, source_update, source_details, source_delete
from currency.views import rate_list, rate_create, rate_update, rate_details, rate_delete
from currency.views import contactus_create, contactus_list, contactus_details, contactus_update, contactus_delete


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),

    path('rate_generator/', rate_generator),

    path('source_list/', source_list),
    path('source_create/', source_create),
    path('source_update/<int:source_id>', source_update),
    path('source_details/<int:source_id>', source_details),
    path('source_delete/<int:source_id>', source_delete),

    path('rate_list/', rate_list),
    path('rate_create/', rate_create),
    path('rate_update/<int:rate_id>', rate_update),
    path('rate_details/<int:rate_id>', rate_details),
    path('rate_delete/<int:rate_id>', rate_delete),

    path('contactus_generator/', contactus_generator),
    path('contactus_list/', contactus_list),
    path('contactus_create/', contactus_create),
    path('contactus_details/<int:contactus_id>', contactus_details),
    path('contactus_update/<int:contactus_id>', contactus_update),
    path('contactus_delete/<int:contactus_id>', contactus_delete),
]
