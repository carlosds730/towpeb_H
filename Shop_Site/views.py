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


def order_by_price(products):
    pass


def get_all_products(products):
    res_prod = []
    for p in products.order_by('-pk'):
        prices = []
        for attr in p.attributes.all():
            if attr.price not in prices:
                res_prod.append((p.pk, p.name, p.short_description, p.image.url, attr.size, attr.color, attr.amount,
                                 attr.price, attr.especial_offer, attr.pk))
                prices.append(attr.price)
    return res_prod


def categories(request, pk):
    if request.is_ajax():
        try:
            order = request.GET['order']
        except KeyError:
            return HttpResponse(json.dumps({}), content_type='application/json')
        result = []
        try:
            product = models.Products.objects.filter(category__pk=int(pk), is_available=True)
        except Exception:
            return HttpResponse(json.dumps({}), content_type='application/json')
        if product:
            result = get_all_products(product)
        else:
            return HttpResponse(json.dumps({}), content_type='application/json')
        if order == 'price-ascending':
            result.sort(key=lambda x: x[7])
        elif order == 'price-descending':
            result.sort(key=lambda x: x[7], reverse=True)
        elif order == 'created-ascending':
            result.sort(key=lambda x: x[0])
        elif order == 'created-descending':
            result.sort(key=lambda x: x[0], reverse=True)
        elif order == 'title-ascending':
            result.sort(key=lambda x: x[1])
        elif order == 'title-descending':
            result.sort(key=lambda x: x[1], reverse=True)
        response_data = {
            'products': result}
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
            products = models.Products.objects.filter(category__pk=category.pk, is_available=True)
            return add_info_home(request,
                                 {'category': category, 'products': get_all_products(products), 'login': log},
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
        product = models.Products.objects.get(pk=int(pk), is_available=True)
    except models.Products.DoesNotExist:
        product = None
    except ValueError:
        product = None
    if product:

        return add_info_home(request, {'product': product, 'login': log},
                             'single_product.html')
    else:
        return Http404('Ese producto no existe')


def add_items_no_repeated(collection, _property='size'):
    res = []
    for e in collection.attributes.all():
        if _property == 'size' and e.size not in res:
            res.append(e.size)
        elif _property != 'size' and e.color not in res:
            res.append(e.color)
    return res


def add_to_cart(request):
    if request.method == 'POST':
        try:
            purchase_pk = request.POST['purchase']
            purchase = models.Purchase.objects.get(pk=int(purchase_pk))
        except KeyError:
            purchase = None
        except models.Purchase.DoesNotExist:
            purchase = None
    else:
        return Http404('Este url no tiene página')
