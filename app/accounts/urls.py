from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.UserActivateView.as_view(), name='user_activate'),
    path('my_profile/', views.UserProfileView.as_view(), name='my_profile'),
]
