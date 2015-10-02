# -*- coding:utf8 -*-
import json
import random
import string

from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.shortcuts import render, redirect

from django.core.validators import validate_email

from Shop_Site.extra_functions import hash
from Shop_Site import models
from Shop_Site import stopwords


def random_string(length=16):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

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
        else:
            _pk = int(request.COOKIES['purchase'])
            p = models.Purchase.objects.get(pk=_pk)
            cant = p.amount
    except KeyError:
        cant = 0
    except models.Purchase.DoesNotExist:
        cant = 0
    try:
        cant = data['purchase']
        del data['purchase']
    except KeyError:
        pass
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


def get_purchase(cookies):
    try:
        _pk = int(cookies['purchase'])
        purchase = models.Purchase.objects.get(pk=_pk)
        return purchase
    except KeyError:
        return None
    except ValueError:
        return None
    except models.Purchase.DoesNotExist:
        return None


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
                    purchase = get_purchase(request.COOKIES)
                    if purchase:
                        try:
                            old_purchase = models.Purchase.objects.get(client__pk=client.pk, on_hold=True)
                            old_purchase.client = None
                            old_purchase.on_hold = False
                            old_purchase.save()
                        except models.Purchase.DoesNotExist:
                            pass
                        purchase.client = client
                        purchase.save()
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

        value = HttpResponseRedirect('/')
        value.delete_cookie('user')
        value.delete_cookie('purchase')
        value.delete_cookie('address')
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
                    'last_name': request.POST['last_name'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                    'next': request.POST['next']
                })
            except models.Clients.DoesNotExist:
                try:
                    client = models.Clients.objects.create(name=request.POST['name'],
                                                           last_name=request.POST['last_name'],
                                                           email=email, password=hash(password))
                except KeyError:
                    client = models.Clients.objects.create(email=email, password=hash(password))
                client.save()
                purchase = get_purchase(request.COOKIES)
                if purchase:
                    purchase.client = client
                    purchase.save()
                try:
                    next = request.POST['next']
                    if '/login/' in next:
                        value = redirect('/')
                    else:
                        value = redirect(request.POST['next'])
                    tmp = set_cookies(value, client)
                    return tmp
                except KeyError:
                    value = redirect('/')
                    tmp = set_cookies(value, client)
                    return tmp
        except KeyError:
            try:
                name = request.POST['name']
            except KeyError:
                name = ''
            return render(request, 'register.html', {
                'error': 'Error en el envio',
                'name': name,
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'password': request.POST['password'],
                'next': request.POST['next']
            })


def order_by_price(products):
    pass


def get_all_products(products):
    res_prod = []
    for p in products.order_by('-pk'):
        if p.old_price:
            res_prod.append((p.pk, p.name, p.short_description, p.image.url, None, p.color, p.sold_out(),
                             str(p.price), str(p.old_price), None, p.percent))
        else:
            res_prod.append((p.pk, p.name, p.short_description, p.image.url, None, p.color, p.sold_out(),
                             str(p.price), None, None, p.percent))
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
            result.sort(key=lambda x: float(x[7]))
        elif order == 'price-descending':
            result.sort(key=lambda x: float(x[7]), reverse=True)
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
            return add_info_home(request, {'category': category, 'products': get_all_products(products)},
                                 'products_collection.html')
        else:
            raise Http404('Esa categoría no existe')

    elif request.method == 'POST':
        log = None
        try:
            log = get_login(request.COOKIES)
            if log:
                purchase = models.Purchase.objects.get(client__pk=int(log[0]), on_hold=True)
            else:
                artificial_purchase = int(request.COOKIES['purchase'])
                purchase = models.Purchase.objects.get(pk=artificial_purchase)
        except KeyError:
            purchase = None
        except models.Purchase.DoesNotExist:
            purchase = None
        try:
            product_pk = request.POST['product_pk']
            attr_pk = request.POST['size']
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
        try:
            category = models.Category.objects.get(pk=int(pk))
        except models.Category.DoesNotExist:
            category = None
            raise Http404('Not Found')
        except ValueError:
            category = None
            raise Http404('Not Found')
        mark = None
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
        else:
            try:
                if log:
                    client = models.Clients.objects.get(pk=log[0])
                else:
                    client = None
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
            if not client:
                mark = purchase.pk
        products = models.Products.objects.filter(category__pk=category.pk, is_available=True)
        if quantity == 1:
            to_send = "1 " + product.name + " se ha añadido al carrito"
        else:
            to_send = str(quantity) + " " + product.name + " se han añadido al carrito"
        if mark:
            ret = add_info_home(request,
                                {
                                    'category': category,
                                    'products': get_all_products(products),
                                    'notification': product,
                                    'message': to_send,
                                    'purchase': 1
                                },
                                'products_collection.html')
            ret.set_cookie('purchase', str(mark))
            return ret
        return add_info_home(request,
                             {
                                 'category': category,
                                 'products': get_all_products(products),
                                 'notification': product,
                                 'message': to_send
                             },
                             'products_collection.html')


def products(request, pk):
    try:
        product = models.Products.objects.get(pk=int(pk), is_available=True)
    except models.Products.DoesNotExist:
        product = None
    except ValueError:
        product = None
    if product:
        related_products = []
        for x in models.Category.objects.all():
            if x.pk == product.category.pk:
                a, b = x.get_random_product(), x.get_random_product()
                if a.pk == b.pk:
                    related_products.append(a)
                else:
                    related_products.append(a)
                    related_products.append(b)
            else:
                related_products.append(x.get_random_product())
        return add_info_home(request, {'product': product, 'related_products': related_products},
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
                '/categories/' + request.POST['category_pk'] + '/?pk_product=' + str(product.pk) + '&pk_ammnt=' + str(quantity))
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
            '/categories/' + request.POST['category_pk'] + '/?pk_product=' + str(product.pk) + '&pk_ammnt=' + str(purchase.amount))
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
                                        product.price).lower() or word in product.color.lower() or word in attr.size.lower():
                                    exist = True
                                    break

                    if exist:
                        selected_products.append(product)
            if len(selected_products):
                return add_info_home(request, {'results': selected_products}, 'search.html')
            else:
                return add_info_home(request, {'no_result': True}, 'search.html')
                # return render(request, 'search.html',
                # {'results': selected_products, 'login': log, 'categories': categories_all,
                # 'purchases': cant})
        except KeyError:
            raise Http404('Wrong request!!!!!!!')
    if request.method == 'GET':
        return add_info_home(request, {'no_data': True}, 'search.html')


def cart_shop(request):
    if request.is_ajax():
        try:
            pk = int(request.GET['pk'])
            amonut = int(request.GET['amonut'])

            sale_prod = models.Sale_Product.objects.get(pk=pk)

            my_car = None

            cliente = get_login(request.COOKIES)
            if cliente:
                cliente = cliente[0]

            for carrito in sale_prod.purchase.all():
                if carrito.on_hold and cliente and cliente == carrito.client.pk:
                    sale_prod.amount = amonut
                    sale_prod.save()
                    my_car = carrito
                    break
                else:
                    sale_prod.amount = amonut
                    sale_prod.save()
                    my_car = carrito
                    break

            if my_car:
                return HttpResponse(json.dumps(
                    {'valid': sale_prod.valid(), 'prod_price': sale_prod.price(), 'total': my_car.total_price(),
                     'valid_com': my_car.is_valid()}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({}), content_type='application/json')

        except models.Sale_Product.DoesNotExist:
            return HttpResponse(json.dumps({}), content_type='application/json')

        except ValueError:
            return HttpResponse(json.dumps({}), content_type='application/json')

        except KeyError:
            return HttpResponse(json.dumps({}), content_type='application/json')

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
            try:
                _pk = int(request.COOKIES['purchase'])
                purchase = models.Purchase.objects.get(pk=_pk)
                return add_info_home(request, {'on_hold': purchase, 'shops': []}, 'cart_shop.html')
            except KeyError:
                return HttpResponseRedirect('/login/')
            except models.Purchase.DoesNotExist:
                return Http404('Purchase not found')


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


def shop(request):
    return finish_views(request, 'tienda.html')


def cookies(request):
    return finish_views(request, 'cookies.html')


def eliminate(request):
    if request.is_ajax():
        try:
            log = get_login(request.COOKIES)
            pk = request.GET['pk']
            if log:
                purchase = models.Purchase.objects.get(client__pk=log[0], on_hold=True)
            else:
                purchase = models.Purchase.objects.get(pk=int(request.COOKIES['purchase']))
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


def send_mail():
    pass


def info_client(request):
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
            try:
                client = models.Clients.objects.get(pk=log[0])
                try:
                    _ = client.address
                    return add_info_home(request,
                                         {
                                             'on_hold': on_hold,
                                             'shops': shops,
                                             'name': client.name,
                                             'last_name': client.last_name,
                                             'company': client.address.company,
                                             'address': client.address.address,
                                             'country': client.address.country,
                                             'city': client.address.city,
                                             'province': client.address.province,
                                             'zip_code': client.address.postal_code,
                                             'apto': client.address.apt_suite,
                                             'phone': client.address.phone,
                                         }, 'info_client.html')
                except Exception:
                    return add_info_home(request, {'on_hold': on_hold, 'shops': shops}, 'info_client.html')
            except models.Clients.DoesNotExist:
                return HttpResponseRedirect('/login/')
        else:
            purchase = get_purchase(request.COOKIES)
            if purchase:
                return add_info_home(request, {'on_hold': purchase, 'shops': []}, 'info_client.html')
            else:
                return Http404('Purchase Error')
    if request.method == 'POST':
        # TODO: Do this POST method. Right now it goes where it should but it doesn't verify anything
        log = get_login(request.COOKIES)
        on_hold = None
        shops = []
        if log:
            for purchase in models.Purchase.objects.filter(client__pk=log[0]):
                if purchase.on_hold:
                    on_hold = purchase
                else:
                    shops.append(purchase)
        else:
            on_hold = get_purchase(request.COOKIES)
            if not on_hold:
                return Http404('Purchase Error')
        try:
            save = request.POST['checkout']
        except KeyError:
            save = None
        try:
            company = request.POST['company']
        except KeyError:
            company = ''
        try:
            name = request.POST['name']
            last_name = request.POST['last_name']
            company = request.POST['company']
            address = request.POST['address']
            country = request.POST['country']
            city = request.POST['city']
            province = request.POST['province']
            zip_code = request.POST['zip_code']
            apto = request.POST['apartment']
            phone = request.POST['phone']
            if save:
                try:
                    client = models.Clients.objects.get(email=request.POST['email'])
                    try:
                        client.address.company = company
                        client.address.address = address
                        client.address.country = country
                        client.address.city = city
                        client.address.province = province
                        client.address.postal_code = zip_code
                        client.address.apt_suite = apto
                        client.address.phone = phone
                        client.address.save()
                    except Exception:
                        add = models.Address.objects.create(company=company,
                                                            address=address, country=country, city=city,
                                                            province=province,
                                                            postal_code=zip_code, apt_suite=apto, phone=phone)
                        add.save()
                        add.client = client
                        add.save()
                    client.save()
                    if log:
                        return HttpResponseRedirect('/payment/payments-billing/')
                    else:
                        ret = HttpResponseRedirect('/payment/payments-billing/')
                        ret.set_cookie('address', str(client.address.pk))
                        ret.set_cookie('name_shipment', str(name))
                        ret.set_cookie('last_name_shipment', str(last_name))
                        ret.set_cookie('company_shipment', str(client.address.company))
                        ret.set_cookie('mail_shipment', str(client.email))
                        return ret
                except models.Clients.DoesNotExist:
                    email = request.POST['email']
                    password = random_string()
                    client = models.Clients.objects.create(email=email, name=name, last_name=last_name,
                                                           password=hash(password))
                    client.save()
                    add = models.Address.objects.create(company=company,
                                                        address=address, country=country, city=city,
                                                        province=province,
                                                        postal_code=zip_code, apt_suite=apto, phone=phone)
                    add.save()
                    add.client = client
                    add.save()
                    send_mail()
                    if log:
                        return HttpResponseRedirect('/payment/payments-billing/')
                    else:
                        ret = HttpResponseRedirect('/payment/payments-billing/')
                        ret.set_cookie('address', str(client.address.pk))
                        ret.set_cookie('name_shipment', str(name))
                        ret.set_cookie('last_name_shipment', str(last_name))
                        ret.set_cookie('company_shipment', str(client.address.company))
                        ret.set_cookie('mail_shipment', str(client.email))
                        return ret
            else:
                add = models.Address.objects.create(company=company,
                                                    address=address, country=country, city=city,
                                                    province=province,
                                                    postal_code=zip_code, apt_suite=apto, phone=phone)
                add.save()
                if log:
                    client = models.Clients.objects.get(pk=int(log[0]))
                    client.address = add
                    client.save()
                    return HttpResponseRedirect('/payment/payments-billing/')
                else:
                    ret = HttpResponseRedirect('/payment/payments-billing/')
                    ret.set_cookie('address', str(add.pk))
                    ret.set_cookie('name_shipment', str(name))
                    ret.set_cookie('last_name_shipment', str(last_name))
                    ret.set_cookie('company_shipment', str(company))
                    ret.set_cookie('mail_shipment', str(request.POST['email']))
                    return ret
        except KeyError:
            return add_info_home(request,
                                 {
                                     'error': True,
                                     'on_hold': on_hold,
                                     'shops': shops,
                                     'name': request.POST['name'],
                                     'last_name': request.POST['last_name'],
                                     'company': request.POST['company'],
                                     'address': request.POST['address'],
                                     'country': request.POST['country'],
                                     'city': request.POST['city'],
                                     'province': request.POST['province'],
                                     'zip_code': request.POST['zip_code'],
                                     'apto': request.POST['apartment'],
                                     'phone': request.POST['phone'],
                                 }
                                 , 'info_client.html')


def info_card(request):
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
            return add_info_home(request, {'on_hold': on_hold, 'shops': shops}, 'info_card.html')
        else:
            return HttpResponseRedirect('/login/')


def add_mail(request):
    if request.is_ajax():
        try:
            mail = request.POST['mail']

            validate_email(mail)

            m = models.Newsletter_Clients.objects.create(email=mail)
            m.save()
            return HttpResponse(json.dumps({'status': 1}), content_type='application/json')
        except KeyError:
            return HttpResponse(json.dumps({'status': 0}), content_type='application/json')
        except Exception:
            return HttpResponse(json.dumps({'status': 0}), content_type='application/json')
