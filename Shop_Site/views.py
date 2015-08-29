# -*- coding:utf8 -*-
import json

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect

from Shop_Site.extra_functions import hash
from Shop_Site import models
from Shop_Site import stopwords


# Create your views here.


def get_login(cookies):
    try:
        user = cookies['user']
        password = cookies['password']
        client = models.Clients.objects.get(email=user)
        if password == client.password:
            if client.name:
                return client.pk, client.name
            else:
                return client.pk, client.email
        return None
    except KeyError:
        return None


def home(request):
    if request.method == 'GET':
        return add_info_home(request, {})


def add_info_home(request, data, url='base.html'):
    categories = models.Category.objects.all()
    log = None
    try:
        log = get_login(request.COOKIES)
        cant = 0
        if log:
            p = models.Purchase.objects.get(client__pk=int(log[0]), on_hold=True)
            cant = p.amount
    except KeyError:
        cant = 0
    except models.Purchase.DoesNotExist:
        cant = 0
    data.update({
        'categories': categories,
        'purchases': cant,
        'login': log
    })
    return render(request, url, data)


def set_cookies(_render, client):
    _render.set_cookie('user', str(client.email))
    _render.set_cookie('password', str(client.password))
    return _render


def login(request):
    if request.method == 'GET':
        try:
            return render(request, 'login.html', {'next': request.environ['HTTP_REFERER'].split('?')[0]})
        except KeyError:
            return render(request, 'login.html', {'next': '/'})
    elif request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            try:
                client = models.Clients.objects.get(email=request.POST['email'])
                password = hash(request.POST['password'])
                if password == client.password:
                    value = redirect(request.POST['next'])
                    tmp = set_cookies(value, client)
                    return tmp
                else:
                    return render(request, 'login.html', {
                        'error': 'Error en el usuario o la contraseña',
                        'email': request.POST['email'],
                        'password': request.POST['password'],
                        'next': request.POST['next']
                    })
            except models.Clients.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'Error en el usuario o la contraseña',
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                    'next': request.POST['next']
                })
        else:
            return render(request, 'login.html', {
                'error': 'Falta el usuario o la contraseña',
                'email': request.POST['email'],
                'password': request.POST['password'],
                'next': request.POST['next']
            })


def shutdown(request):
    if request.method == 'GET':
        categories = models.Category.objects.all()
        value = HttpResponseRedirect('/')
        value.delete_cookie('user')
        value.delete_cookie('password')
        return value


def register(request):
    if request.method == 'GET':
        try:
            return render(request, 'register.html', {'next': request.environ['HTTP_REFERER'].split('?')[0]})
        except KeyError:
            return render(request, 'register.html', {'next': '/'})
    elif request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            try:
                models.Clients.objects.get(email=email)
                return render(request, 'register.html', {
                    'error': 'Ya existe un usuario registrado con ese correo',
                    'name': request.POST['name'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                    'address': request.POST['address'],
                    'next': request.POST['next']
                })
            except models.Clients.DoesNotExist:
                client = models.Clients.objects.create(name=request.POST['name'], email=email,
                                                       password=hash(password),
                                                       address=request.POST['address'])
                client.save()
                value = redirect(request.POST['next'])
                tmp = set_cookies(value, client)
                return tmp
        except KeyError:
            try:
                name = request.POST['name']
            except KeyError:
                name = ''
            try:
                address = request.POST['address']
            except KeyError:
                address = ''
            return render(request, 'register.html', {
                'error': 'Error en el envio',
                'name': name,
                'email': request.POST['email'],
                'password': request.POST['password'],
                'address': address,
                'next': request.POST['next']
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
        log = get_login(request.COOKIES)
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
            'products': result,
            'login': log}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    elif request.method == 'GET':
        try:
            category = models.Category.objects.get(pk=int(pk))
        except models.Category.DoesNotExist:
            category = None
        except ValueError:
            category = None
        if category:
            products = models.Products.objects.filter(category__pk=category.pk, is_available=True)
            return add_info_home(request,
                                 {'category': category, 'products': get_all_products(products)},
                                 'products_collection.html')
        else:
            raise Http404('Esa categoría no existe')


def products(request, pk):
    try:
        product = models.Products.objects.get(pk=int(pk), is_available=True)
    except models.Products.DoesNotExist:
        product = None
    except ValueError:
        product = None
    if product:
        return add_info_home(request, {'product': product},
                             'single_product.html')
    else:
        raise Http404('Ese producto no existe')


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
        log = None
        try:
            log = get_login(request.COOKIES)
            if log:
                purchase = models.Purchase.objects.get(client__pk=int(log[0]), on_hold=True)
            else:
                purchase = None
        except KeyError:
            purchase = None
        except models.Purchase.DoesNotExist:
            purchase = None
        try:
            product_pk = request.POST['product_pk']
            attr_pk = request.POST['attr_pk']
            quantity = int(request.POST['quantity'])
        except KeyError:
            raise Http404('Not Found')
        try:
            product = models.Products.objects.get(pk=int(product_pk))
        except models.Products.DoesNotExist:
            raise Http404('Not Found')
        try:
            attr = models.Attribute.objects.get(pk=int(attr_pk))
        except models.Attribute.DoesNotExist:
            raise Http404('Not Found')
        if purchase:
            try:
                sale_product = purchase.products.get(product=product, attribute=attr)
                sale_product.amount += quantity
                sale_product.save()
            except:
                sale_product = models.Sale_Product.objects.create(product=product, attribute=attr)
                sale_product.amount += quantity
                sale_product.save()
                purchase.products.add(sale_product)
                purchase.amount += 1
            purchase.save()
            return HttpResponseRedirect(
                '/categories/' + request.POST['category_pk'] + '/')
        else:
            try:
                if log:
                    client = models.Clients.objects.get(pk=log[0])
                else:
                    raise Http404('Client Not Found')
            except models.Clients.DoesNotExist:
                raise Http404('Client Not Found')
            sale_product = models.Sale_Product.objects.create(product=product, attribute=attr)
            sale_product.amount += quantity
            sale_product.save()
            purchase = models.Purchase.objects.create()
            purchase.products.add(sale_product)
            purchase.client = client
            purchase.amount = 1
            purchase.save()
        return HttpResponseRedirect(
            '/categories/' + request.POST['category_pk'] + '/')
    else:
        raise Http404('Este url no tiene página')


def search(request):
    if request.method == 'POST':
        categories_all = models.Category.objects.all()
        try:
            query = request.POST['query']
            selected_products = []
            if query:
                words = stopwords.word_tokenize(query)
                words = stopwords.remove_stopwords(words)
                for product in models.Products.objects.all():
                    exist = True
                    for word in words:
                        if not exist:
                            break
                        if word not in product.name.lower() and word not in product.short_description.lower() and word not in product.description.lower() and word not in product.category.name.lower() and word not in product.mark.lower() and word not in product.label.split(
                                ','):
                            exist = False
                            for attr in product.attributes.all():
                                if word in str(
                                        attr.price).lower() or word in attr.color.lower() or word in attr.size.lower():
                                    exist = True
                                    break

                    if exist:
                        selected_products.append(product)
            if len(selected_products):
                return add_info_home(request, {'results': selected_products}, 'search.html')
            else:
                return add_info_home(request, {'no_result': True}, 'search.html')
                # return render(request, 'search.html',
                #               {'results': selected_products, 'login': log, 'categories': categories_all,
                #                'purchases': cant})
        except KeyError:
            raise Http404('Wrong request!!!!!!!')
    if request.method == 'GET':
        return add_info_home(request, {'no_data': True}, 'search.html')


def cart_shop(request):
    if request.method == 'GET':
        log = get_login(request.COOKIES)
        if log:
            on_hold = None
            shops = []
            for purchase in models.Purchase.objects.filter(client__pk=log[0]):
                if purchase.on_hold:
                    on_hold = purchase
                else:
                    shops.append(purchase)
            return add_info_home(request, {'on_hold': on_hold, 'shops': shops}, 'cart_shop.html')
        else:
            return HttpResponseRedirect('/login/')


def about_us(request):
    if request.method == 'GET':
        return add_info_home(request, {}, url='about_us.html')


def finish_views(request, html):
    if request.method == 'GET':
        return add_info_home(request, {}, url=html)


def sizes(request):
    return finish_views(request, 'guia_tallas.html')


def privacy(request):
    return finish_views(request, 'privacy.html')


def conditions(request):
    return finish_views(request, 'conditions.html')


def cookies(request):
    return finish_views(request, 'cookies.html')


def eliminate(request):
    if request.is_ajax():
        try:
            log = get_login(request.COOKIES)
            pk = request.GET['pk']
            purchase = models.Purchase.objects.get(client__pk=log[0], on_hold=True)
            sale_product = purchase.products.get(pk=int(pk))
            purchase.products.remove(sale_product)
            purchase.amount -= 1
            purchase.save()
            return HttpResponse(json.dumps({'cant': purchase.amount, 'total': purchase.total_price()}),
                                content_type='application/json')
        except KeyError:
            raise Http404('')
        except models.Sale_Product.DoesNotExist:
            raise Http404('')
