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

from django.contrib import admin

from django.conf.urls.static import static

from Shop_Site import views
from towpeb_H import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^payment/', include('django_braintree.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/?$', views.login, name='login'),
    url(r'^categories/(?P<pk>\d+)/?$', views.categories, name='categories'),
    url(r'^product/(?P<pk>\d+)/?$', views.products, name='product'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^cart_shop/?$', views.cart_shop, name='cart shop'),
    url(r'^eliminate/?$', views.eliminate, name='eliminate'),
    url(r'^add_to_cart/?$', views.add_to_cart, name='add_to_cart'),
    url(r'^about_us/?$', views.about_us, name='about_us'),
    url(r'^sizes/?$', views.sizes, name='sizes'),
    url(r'^privacy/?$', views.privacy, name='privacy'),
    url(r'^conditions/?$', views.conditions, name='conditions'),
    url(r'^cookies/?$', views.cookies, name='cookies'),
    url(r'^shutdown/?$', views.shutdown, name='shutdown'),
    url(r'^info_client/?$', views.info_client, name='info_client'),
    url(r'^shipping_info/?$', views.shipping_info, name='shipping_info'),
    url(r'^info_card/?$', views.info_card, name='info_card'),
    url(r'^$', views.home)

]
