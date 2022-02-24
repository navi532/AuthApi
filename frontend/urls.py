from django.urls import path
from .views import *
urlpatterns = [
    path('login/',LoginView),
    path('register/',RegisterView),
    path('activate/<uidb64>/<token>/',ActivateView),
    path('reset/',ResetView),
    path('reset/<uidb64>/<token>/',PassewordResetView),
]