from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/<slug:username>/', views.ProfileAPIView.as_view(), name='profile'),
    # path('my_profile/<slug:username>/', views.ProfileAPIVeiew.as_view(), name='my_profile'),
    path('edit_profile/<slug:username>/', views.edit_profile, name='edit_profile'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]