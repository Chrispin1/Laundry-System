from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('clients/', clients, name='clients'),
    path('clients/<int:id>/update/', editClient, name='edit'),
    path('clients/<int:id>/delete/', clientDelete, name='delete'),
    path('access/token/', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa/', lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # path('payment/validation/', validation, name='validation'),
    # path('payment/confirmation/', confirmation, name='confirmation'),
    # path('payment/register', register_urls, name="register_mpesa_validation"),
    


]