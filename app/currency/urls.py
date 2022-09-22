from django.urls import path
from currency import views


app_name = 'currency'

urlpatterns = [
    path('rate/generator/', views.rate_generator, name='rate_generator'),
    path('contactus/generator/', views.contactus_generator, name='contactus_generator'),

    path('', views.IndexView.as_view(), name='index'),

    path('source/list/', views.SourceListView.as_view(), name='source_list'),
    path('source/create/', views.SourceCreateView.as_view(), name='source_create'),
    path('source/update/<int:pk>', views.SourceUpdateView.as_view(), name='source_update'),
    path('source/delete/<int:pk>', views.SourceDeleteView.as_view(), name='source_delete'),
    path('source/details/<int:pk>', views.SourceDetailsView.as_view(), name='source_details'),

    path('rate/list/', views.RateListView.as_view(), name='rate_list'),
    path('rate/create/', views.RateCreateView.as_view(), name='rate_create'),
    path('rate/update/<int:pk>', views.RateUpdateView.as_view(), name='rate_update'),
    path('rate/delete/<int:pk>', views.RateDeleteView.as_view(), name='rate_delete'),
    path('rate/details/<int:pk>', views.RateDetailsView.as_view(), name='rate_details'),
    path('rate/download/', views.DownloadRateView.as_view(), name='rate_download'),

    # path('contactus/list/', views.ContactUsListView.as_view(), name='contactus_list'),
    path('contactus/create/', views.ContactUsCreateView.as_view(), name='contactus_create'),
    # path('contactus/update/<int:pk>', views.ContactUsUpdateView.as_view(), name='contactus_update'),
    # path('contactus/delete/<int:pk>', views.ContactUsDeleteView.as_view(), name='contactus_delete'),
    # path('contactus/details/<int:pk>', views.ContactUsDetailsView.as_view(), name='contactus_details'),

    path('ajax/', views.AjaxPartsPageView.as_view(), name='ajax_parts_page_view'),
    # path('ajax/ajax_get_value/', views.ajax_get_value, name='ajax_get_value'),
    # path('ajax/ajax_get_table_1/', views.ajax_get_table_1, name='ajax_get_table_1'),
    path('ajax/main_frame_content_get/', views.main_frame_content_get, name='main_frame_content_get'),
    path('ajax/sub_frame_content_get/', views.sub_frame_content_get, name='sub_frame_content_get'),
]
