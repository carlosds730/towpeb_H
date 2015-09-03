# -*- coding:utf8 -*-
import json

from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.shortcuts import render

from Shop_Site.extra_functions import hash
from Shop_Site import models
from Shop_Site import forms


# Create your views here.


def home(request):
    if request.method == 'GET':
        try:
            log = request.GET['pk_l']
            try:
                client = models.Clients.objects.get(pk=int(log))
                if client.name:
                    return add_info_home(request, {'login': (client.pk, client.name)})
                else:
                    return add_info_home(request, {'login': (client.pk, client.email)})
            except models.Clients.DoesNotExist:
                return add_info_home(request, {})
            except ValueError:
                return add_info_home(request, {})
        except KeyError:
            return add_info_home(request, {})


def add_info_home(request, data, url='base.html'):
    categories = models.Category.objects.all()
    data.update({
        'categories': categories
    })
    return render(request, url, data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'next': request.environ['HTTP_REFERER'].split('?')[0]})
    elif request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            try:
                client = models.Clients.objects.get(email=request.POST['email'])
                password = hash(request.POST['password'])
                if password == client.password:
                    return HttpResponseRedirect(request.POST['next'] + '?pk_l=' + str(client.pk))
                else:
                    return render(request, 'login.html', {
                        'error': 'Error en la contraseña',
                        'email': request.POST['email'],
                        'password': request.POST['password']
                    })
            except models.Clients.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'No existe ningún cliente con ese correo',
                    'email': request.POST['email'],
                    'password': request.POST['password']
                })
        else:
            return render(request, 'login.html', {
                'error': 'Falta el usuario o la contraseña',
                'email': request.POST['email'],
                'password': request.POST['password']
            })


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'next': request.environ['HTTP_REFERER'].split('?')[0]})
    elif request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():

            client = models.Clients.objects.create(name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                                                   password=form.cleaned_data['password'],
                                                   address=form.cleaned_data['address'])
            client.save()
            return HttpResponseRedirect(request.POST['next'] + '?pk_l=' + str(client.pk))
        else:
            try:
                name = form.cleaned_data['name']
            except KeyError:
                name = ''
            try:
                address = form.cleaned_data['address']
            except KeyError:
                address = ''
            return render(request, 'register.html', {
                'error': 'Correo inválido',
                'name': name,
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'address': address
            })


def categories(request, pk):
    if request.is_ajax():
        order = request.GET['order']
        result = []
        if order == 'price-ascending':
            result = models.Sale_Product.objects.order_by('price')
        elif order == 'price-descending':
            result = models.Sale_Product.objects.order_by('-price')
        elif order == 'created-ascending':
            result = models.Sale_Product.objects.order_by('pk')
        elif order == 'created-descending':
            result = models.Sale_Product.objects.order_by('-pk')
        elif order == 'title-ascending':
            result = models.Sale_Product.objects.order_by('product__name')
        elif order == 'title-descending':
            result = models.Sale_Product.objects.order_by('-product__name')
        response_data = {
            'products': [(p.pk, p.product.name, p.product.short_description, p.product.image.url, p.amount, p.price,
                          p.especial_offer) for p in result]}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    elif request.method == 'GET':
        try:
            log = request.GET['pk_l']
            log = models.Clients.objects.get(pk=int(log))
            if log.name:
                log = (log.pk, log.name)
            else:
                log = (log.pk, log.email)
        except KeyError:
            log = None
        except models.Clients.DoesNotExist:
            log = None
        except ValueError:
            log = None
        try:
            category = models.Category.objects.get(pk=int(pk))
        except models.Category.DoesNotExist:
            category = None
        except ValueError:
            category = None
        if category:
            products = models.Sale_Product.objects.filter(product__category__pk=category.pk)
            products = [(p.pk, p.product.name, p.product.short_description, p.product.image.url, p.amount, p.price,
                         p.especial_offer) for p in products.order_by('-pk')]
            return add_info_home(request, {'category': category, 'products': products, 'login': log},
                                 'products_collection.html')
        else:
            return Http404('Esa categoría no existe')


def products(request, pk):
    try:
        log = request.GET['pk_l']
        log = models.Clients.objects.get(pk=int(log))
        if log.name:
            log = (log.pk, log.name)
        else:
            log = (log.pk, log.email)
    except KeyError:
        log = None
    except models.Clients.DoesNotExist:
        log = None
    except ValueError:
        log = None
    try:
        product = models.Sale_Product.objects.get(pk=int(pk))
    except models.Sale_Product.DoesNotExist:
        product = None
    except ValueError:
        product = None
    p = models.Sale_Product.objects.filter(product__name=product.product.name)
    sizes = add_items_no_repeated(p)
    colors = add_items_no_repeated(p, 'color')
    return add_info_home(request, {'product': product, 'login': log, 'colors': colors, 'sizes': sizes},
                         'single_product.html')


def add_items_no_repeated(collection, _property='size'):
    res = []
    for e in collection:
        if _property == 'size' and e.attribute.size not in res:
            res.append(e.attribute.size)
        elif _property != 'size' and e.attribute.color not in res:
            res.append(e.attribute.color)
    return res
