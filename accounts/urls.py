from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import view

urlpatterns = [
    path('register/', view.UserRegistrationView.as_view(), name='user-register'),
    path('login/', view.UserLoginView.as_view(), name='user-login'),
    path('profile/', view.UserProfileView.as_view(), name='user-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
