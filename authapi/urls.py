from django.urls import path
from .views import LoginView, PasswordResetView, RegisterView, ActivateView, ResetView
urlpatterns = [
    path('register/',RegisterView.as_view()), # Registers a User, Sends Activation Link on successful registration
    path('login/',LoginView.as_view()), # Logins a User & returns JWT Token and password throttling for unsuccessful attempt
    path('activate/<uidb64>/<token>/',ActivateView.as_view(),name = 'activate'), #Activation of User Account
    path('reset/',ResetView.as_view(),name = 'reset'), #Sends mail to User for Password Rest
    path('reset/<uidb64>/<token>/',PasswordResetView.as_view(),name = 'passwordreset') #Resets User Password, Link invalidated after password has been changed
]