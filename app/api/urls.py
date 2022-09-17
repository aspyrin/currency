from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

app_name = 'api'


router = DefaultRouter()
router.register('contactuss', views.ContactUsViewSet, basename='contactus')

urlpatterns = [
    path('rates/', views.RatesView.as_view(), name='rates'),
    path('rates/<int:pk>/', views.RateDetailView.as_view(), name='rate-details'),
    path('sources/', views.SourcesView.as_view(), name='sources'),
]

urlpatterns += router.urls
