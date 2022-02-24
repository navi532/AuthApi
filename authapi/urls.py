from django.urls import path
from .views import LoginView, PasswordResetView, RegisterView, ActivateView, ResetView
urlpatterns = [
    path('register/',RegisterView.as_view()), 
    path('login/',LoginView.as_view()), 
    path('activate/<uidb64>/<token>/',ActivateView.as_view(),name = 'activate'), 
    path('reset/',ResetView.as_view(),name = 'reset'), 
    path('reset/<uidb64>/<token>/',PasswordResetView.as_view(),name = 'passwordreset')
]