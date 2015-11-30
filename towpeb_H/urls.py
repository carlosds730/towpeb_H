"""towpeb_H URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from Shop_Site import views
from towpeb_H import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/?$', views.login, name='login'),
    url(r'^change_password/?$', views.change_password, name='change_password'),
    url(r'^payment/payments-billing/?$', views.payment_billing, name='payment'),
    url(r'^payment-methods/?$', views.payment_methods, name='payment_method'),
    url(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/?$', views.products, name='product'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^completed_payment/?$', views.completed_payment, name='completed_payment'),
    url(r'^completed_payment_ok/?$', views.completed_payment_ok, name='completed_payment_ok'),
    url(r'^completed_payment_fail/?$', views.completed_payment_fail, name='completed_payment_fail'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^cart_shop/?$', views.cart_shop, name='cart shop'),
    url(r'^eliminate/?$', views.eliminate, name='eliminate'),
    # url(r'^add_to_cart/?$', views.add_to_cart, name='add_to_cart'),
    url(r'^about_us/?$', views.about_us, name='about_us'),
    url(r'^sizes/?$', views.sizes, name='sizes'),
    url(r'^privacy/?$', views.privacy, name='privacy'),
    url(r'^conditions/?$', views.conditions, name='conditions'),
    url(r'^cookies/?$', views.cookies, name='cookies'),
    url(r'^lookbook/?$', views.lookbook, name='lookbook'),
    url(r'^shutdown/?$', views.shutdown, name='shutdown'),
    url(r'^info_client/?$', views.info_client, name='info_client'),
    # url(r'^shipping_info/?$', views.shipping_info, name='shipping_info'),
    url(r'^info_card/?$', views.info_card, name='info_card'),
    url(r'^shop/?$', views.shop, name='shop'),
    url(r'^add_mail/?$', views.add_mail, name='add_mail'),
    url(r'^(?P<slug>[-\w]+)/?$', views.categories, name='categories'),
    url(r'^$', views.home)
]
