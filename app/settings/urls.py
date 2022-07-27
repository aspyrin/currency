from django.contrib import admin
from django.urls import include, path

from currency.views import rate_generator
from currency.views import contactus_generator
from currency import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view()),

    path('rate_generator/', rate_generator),
    path('contactus_generator/', contactus_generator),

    path('source_list/', views.SourceListView.as_view()),
    path('source_create/', views.SourceCreateView.as_view()),
    path('source_update/<int:pk>', views.SourceUpdateView.as_view()),
    path('source_delete/<int:pk>', views.SourceDeleteView.as_view()),
    path('source_details/<int:pk>', views.SourceDetailsView.as_view()),

    path('rate_list/', views.RateListView.as_view()),
    path('rate_create/', views.RateCreateView.as_view()),
    path('rate_update/<int:pk>', views.RateUpdateView.as_view()),
    path('rate_delete/<int:pk>', views.RateDeleteView.as_view()),
    path('rate_details/<int:pk>', views.RateDetailsView.as_view()),

    path('contactus_list/', views.ContactUsListView.as_view()),
    path('contactus_create/', views.ContactUsCreateView.as_view()),
    path('contactus_update/<int:pk>', views.ContactUsUpdateView.as_view()),
    path('contactus_delete/<int:pk>', views.ContactUsDeleteView.as_view()),
    path('contactus_details/<int:pk>', views.ContactUsDetailsView.as_view()),

    path('__debug__/', include('debug_toolbar.urls')),
]
