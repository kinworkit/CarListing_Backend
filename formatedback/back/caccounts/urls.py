from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserInfoAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user_registration'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('user-info/', UserInfoAPIView.as_view(), name='user-info'),
]
