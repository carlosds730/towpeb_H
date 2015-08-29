from django.conf.urls import *

from django_braintree import views

urlpatterns = [
    url(r'payments-billing/$', views.payments_billing, name='payments_billing'),
]
