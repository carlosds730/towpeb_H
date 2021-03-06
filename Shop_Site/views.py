# -*- coding:utf8 -*-
import json
import random
import string

import braintree
import django.utils.timezone as tz
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from Shop_Site import models
from Shop_Site import stopwords
from Shop_Site.extra_functions import hash, create_unique_id, create_sha, create_sha_2
from Shop_Site.repots import CreatePDF
from towpeb_H.settings import TPV_FUC as tpv_fuc
from towpeb_H.settings import TPV_KEY as tpv_key
from towpeb_H.settings import WEB_SITE_URL as site_url


def random_string(length=16):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def get_login(cookies):
    try:
        user = cookies['user']
        password = cookies['password']
        try:
            client = models.Clients.objects.get(email=user)
            if password == client.password:
                if client.name:
                    return client.pk, client.name
                else:
                    return client.pk, client.email
            return None
        except models.Clients.DoesNotExist:
            return None
    except KeyError:
        return None


def countdown(request):
    if request.method == 'GET':
        return render(request, 'countdown.html')
    if request.is_ajax():
        pass


def home(request):
    if request.method == 'GET':
        # from django.http import HttpResponse
        # response = HttpResponse("Hd6KCA69", content_type="text/html")
        # return response

        try:
            a = models.FrontImg.objects.all()[0:4]
        except Exception:
            a = []
        try:
            request.COOKIES['successful_shop']
            ret = add_info_home(request, {'successful_purchase': True, 'pics': a})
            ret.delete_cookie("successful_shop")
            ret.delete_cookie("purchase")
            return ret
        except KeyError:
            return add_info_home(request, {'pics': a})


def add_info_home(request, data, url='base.html'):
    categories = models.Category.objects.all()
    log = None
    try:
        log = get_login(request.COOKIES)
        cant = 0
        if log:
            p = models.Purchase.objects.filter(client__pk=int(log[0]), on_hold=True).last()
            if not p:
                cant = 0
            else:
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
                            old_purchases = models.Purchase.objects.filter(client__pk=client.pk, on_hold=True)
                            for old_purchase in old_purchases:
                                old_purchase.client = None
                                old_purchase.on_hold = False
                                old_purchase.save()
                        except models.Purchase.DoesNotExist:
                            pass
                        purchase.client = client
                        purchase.save()
                        models.Purchase.objects.filter(client=None, on_hold=False).delete()
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
                models.Clients.objects.get(email=email, is_ghost=False)
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
                    client = models.Clients.objects.get(email=email, is_ghost=True)
                    client.name = request.POST['name']
                    client.last_name = request.POST['last_name']
                    client.password = hash(password)
                    client.is_ghost = False
                except KeyError:
                    client.password = hash(password)
                    client.is_ghost = False
                except models.Clients.DoesNotExist:
                    try:
                        client = models.Clients.objects.create(name=request.POST['name'],
                                                               last_name=request.POST['last_name'],
                                                               email=email, password=hash(password))
                    except KeyError:
                        client = models.Clients.objects.create(email=email, password=hash(password))
                client.save()
                send_mail_new_client(client)
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
    finals = []
    for p in products:
        if p.sold_out():
            if p.old_price:
                res_prod.append((p.pk, p.name, p.short_description, p.get_thumb(), None, p.color, p.sold_out(),
                                 str(p.price), str(p.old_price), None, p.percent, p.slug))
            else:
                res_prod.append((p.pk, p.name, p.short_description, p.get_thumb(), None, p.color, p.sold_out(),
                                 str(p.price), None, None, p.percent, p.slug))
        else:
            if p.old_price:
                finals.append((p.pk, p.name, p.short_description, p.get_thumb(), None, p.color, p.sold_out(),
                               str(p.price), str(p.old_price), None, p.percent, p.slug))
            else:
                finals.append((p.pk, p.name, p.short_description, p.get_thumb(), None, p.color, p.sold_out(),
                               str(p.price), None, None, p.percent, p.slug))
    res_prod.extend(finals)
    return res_prod


def categories(request, slug):
    if request.is_ajax():
        log = get_login(request.COOKIES)
        try:
            order = request.GET['order']
        except KeyError:
            return HttpResponse(json.dumps({}), content_type='application/json')
        result = []
        try:
            product = models.Products.objects.filter(category__slug=slug, is_available=True)
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
            category = models.Category.objects.get(slug=slug)
        except models.Category.DoesNotExist:
            category = None
        except ValueError:
            category = None
        if category:
            products = models.Products.objects.filter(category__slug=category.slug, is_available=True)
            return add_info_home(request, {'category': category, 'products': get_all_products(products)},
                                 'products_collection.html')
        else:
            if slug == 'admin':
                return HttpResponseRedirect("/admin/")
            raise Http404('Esa categoría no existe')
    elif request.method == 'POST':
        log = None
        try:
            log = get_login(request.COOKIES)
            if log:
                purchase = models.Purchase.objects.filter(client__pk=int(log[0]), on_hold=True).last()
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
            category = models.Category.objects.get(slug=slug)
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


def products(request, slug, cat_slug):
    try:
        product = models.Products.objects.get(slug=slug, is_available=True)
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
                purchase = models.Purchase.objects.filter(client__pk=int(log[0]), on_hold=True).last()
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
                '/categories/' + request.POST['category_pk'] + '/?pk_product=' + str(product.pk) + '&pk_ammnt=' + str(
                    quantity))
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
            '/categories/' + request.POST['category_pk'] + '/?pk_product=' + str(product.pk) + '&pk_ammnt=' + str(
                purchase.amount))
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
                my_car.save()
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
                if purchase.on_hold:
                    return add_info_home(request, {'on_hold': purchase, 'shops': []}, 'cart_shop.html')
                else:
                    raise Http404('Carrito no encontrado')
            except KeyError:
                return HttpResponseRedirect('/login/')
            except models.Purchase.DoesNotExist:
                raise Http404('Carrito no encontrado')


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
    if request.method == 'GET':
        return add_info_home(request, {'no_cookies': True}, url='cookies.html')


def lookbook(request):
    if request.method == 'GET':
        pics = models.LookBookImg.objects.all()
        return add_info_home(request, {'no_cookies': True, 'pics': pics}, url='lookbook.html')


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


# DONE: SEND LOS PUTOS MAILS, DOWNLOAD LOS .tar.gz necesarios
def send_mail_owners(purchase):
    toclient = CreatePDF(purchase, True)
    message = "Estimado " + purchase.client.full_name() + "\n Le informamos que su pedido se ha completado con éxito y se encuentra en proceso de envío.\n Desde Hutton le agradecemos la confianza depositada en nuestra marca y esperamos que su experiencia de compra sea excelente. \n Para cualquier duda o consulta le facilitamos nuestro correo electrónico operativo 24H.\n info@hutton.es\n Saludos,\n Hutton."

    mail_client = EmailMessage(subject='Ticket de compra online en Hutton', body=message,
                               from_email='pedidos@hutton.es', to=[purchase.client.email], reply_to=['info@hutton.es'],
                               headers={'Message-ID': 'foo'})

    mail_client.attach_file(toclient)

    mail_client.send(fail_silently=False)

    toowner = CreatePDF(purchase, False)

    message = "Información de la compra con Id %s" % purchase.transaction_id

    mail_client = EmailMessage(subject='%s Nueva compra online' % purchase.transaction_id, body=message,
                               from_email='pedidos@hutton.es', to=['pedidos@hutton.es'], reply_to=['info@hutton.es'],
                               headers={'Message-ID': 'foo'})

    mail_client.attach_file(toowner)

    mail_client.send(fail_silently=False)


def send_mail_owners_prueba(purchase):
    toclient = CreatePDF(purchase, True)
    message = "Estimado " + purchase.client.full_name() + "\n Le informamos que su pedido se ha completado con éxito y se encuentra en proceso de envío.\n Desde Hutton le agradecemos la confianza depositada en nuestra marca y esperamos que su experiencia de compra sea excelente. \n Para cualquier duda o consulta le facilitamos nuestro correo electrónico operativo 24H.\n info@hutton.es\n Saludos,\n Hutton."

    mail_client = EmailMessage(subject='Ticket de compra online en Hutton', body=message,
                               from_email='pedidos@hutton.es', to=[purchase.client.email],
                               reply_to=['towpeb@gmail.com'],
                               headers={'Message-ID': 'foo'})

    mail_client.attach_file(toclient)

    mail_client.send(fail_silently=False)

    print("Mail client sent")

    toowner = CreatePDF(purchase, False)

    message = "Información de la compra con Id %s" % purchase.transaction_id

    mail_client = EmailMessage(subject='%s Nueva compra online' % purchase.transaction_id, body=message,
                               from_email='pedidos@hutton.es', to=['towpeb@gmail.com'], reply_to=['towpeb@gmail.com'],
                               headers={'Message-ID': 'foo'})

    mail_client.attach_file(toowner)

    mail_client.send(fail_silently=False)

    print("Mail owner sent")


# DONE: DO this
def send_mail_pass(client):
    # url = 'http://127.0.0.1:8000/change_password/?email=' + client.email + '&key=' + password
    url = site_url + 'change_password/' + '?email=' + client.email + '&key=' + client.password
    print(url)
    html_content = '<p>Estimado %s </p> <p>Haga click en el siguiente enlace para cambiar su contraseña en Hutton.es</p> <a href="%s">%s</a> <p>Atentamente,</p><p>Equipo de Hutton</p> ' % (
        client.full_name(), url, url)

    msg = EmailMessage(subject='Su nueva cuenta en Hutton.es', body=html_content, from_email='info@hutton.es',
                       reply_to=['info@hutton.es'],
                       to=[client.email])
    msg.content_subtype = "html"  # Main content is now text/html

    msg.send()
    print("message sent")


def send_mail_new_client(client):
    html_content = '<p>Estimado %s </p> <p>Muchas gracias por darse de alta en nuestra cartera de clientes. Le mantendremos informado de todas las novedades, promociones y eventos que Hutton realice.</p> <p>Aprovechamos para informarle que puede encontrarnos en nuestra #Flagshipstore en la Calle Padilla 4 (28006 Madrid) y en nuestra #Onlinestore <a href="%s">Hutton.es</a></p><p>Para cualquier aclaración o duda dispone de nuestro mail disponible 24h:</p><p><a href="mailto:%s">info@hutton.es</a></p> ' % (
        client.full_name(), "https://www.hutton.es", "info@hutton.es")

    msg = EmailMessage(subject='Su nueva cuenta en Hutton.es', body=html_content, from_email='info@hutton.es',
                       to=[client.email], reply_to=['info@hutton.es'], headers={'Message-ID': 'foo'})
    msg.content_subtype = "html"  # Main content is now text/html
    try:
        msg.send()
        print("message sent")
    except Exception as e:
        print("We couldn't send the email")
        print(e)


def info_client(request):
    if request.method == 'GET':
        log = get_login(request.COOKIES)
        already_login = False
        if log:
            already_login = True
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
                                             'email': client.email,
                                             'last_name': client.last_name,
                                             'company': client.address.company,
                                             'address': client.address.address,
                                             'country': client.address.country,
                                             'city': client.address.city,
                                             'province': client.address.province,
                                             'zip_code': client.address.postal_code,
                                             'apto': client.address.apt_suite,
                                             'phone': client.address.phone,
                                             'already_login': already_login
                                         }, 'info_client.html')
                except Exception:
                    return add_info_home(request, {'on_hold': on_hold, 'shops': shops, 'name': client.name,
                                                   'email': client.email,
                                                   'last_name': client.last_name, 'already_login': already_login},
                                         'info_client.html')
            except models.Clients.DoesNotExist:
                return HttpResponseRedirect('/login/')
        else:
            purchase = get_purchase(request.COOKIES)
            if purchase and purchase.on_hold:
                return add_info_home(request, {'on_hold': purchase, 'shops': [], 'already_login': already_login},
                                     'info_client.html')
            else:
                raise Http404('Purchase Error')
    if request.method == 'POST':
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
                raise Http404('Purchase Error')
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
            if not name or not address or not country or not city or not province or not zip_code:
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
            if save or log:
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
                    on_hold.client = client
                    on_hold.save()
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
                    purchase = get_purchase(request.COOKIES)
                    client.save()
                    purchase.client = client
                    purchase.save()
                    add = models.Address.objects.create(company=company,
                                                        address=address, country=country, city=city,
                                                        province=province,
                                                        postal_code=zip_code, apt_suite=apto, phone=phone)
                    add.save()
                    add.client = client
                    add.save()
                    # print("yuju")
                    try:
                        send_mail_pass(client)
                    except Exception:
                        pass
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
                    email = request.POST['email']
                    try:
                        client = models.Clients.objects.get(email=email)
                        client.name = name
                        client.last_name = last_name
                    except models.Clients.DoesNotExist:
                        password = random_string()
                        client = models.Clients.objects.create(email=email, name=name, last_name=last_name,
                                                               password=hash(password), is_ghost=True)

                    client.save()

                    purchase = get_purchase(request.COOKIES)
                    purchase.client = client
                    purchase.save()

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

            m, _ = models.Newsletter_Clients.objects.get_or_create(email=mail)
            m.save()
            return HttpResponse(json.dumps({'status': 1}), content_type='application/json')
        except KeyError:
            return HttpResponse(json.dumps({'status': 0}), content_type='application/json')
        except Exception as ee:
            return HttpResponse(json.dumps({'status': 0}), content_type='application/json')


# DONE: What this should do when there is no purchase
def payment_billing(request):
    if request.method == 'GET':
        print("Hellow")
        completed_pay_url = site_url + 'completed_payment'
        completed_payment_url = completed_pay_url + '/'
        try:
            token = braintree.ClientToken.generate()
            # print("token:" + token)
        except Exception:
            token = 'eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQiOiJmMDU0MTRmZTc1MGNiYmIwOGQ0YTM1MGIwZmYyYmMxMWE5ZDc0ZWMzNmMxM2QwYjkzNjExYWNiMTUyYTRmNjhhfGNyZWF0ZWRfYXQ9MjAxNS0wOS0wNFQyMDo0NTozMS4zMjE0ODU4MzErMDAwMFx1MDAyNm1lcmNoYW50X2lkPTM0OHBrOWNnZjNiZ3l3MmJcdTAwMjZwdWJsaWNfa2V5PTJuMjQ3ZHY4OWJxOXZtcHIiLCJjb25maWdVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvMzQ4cGs5Y2dmM2JneXcyYi9jbGllbnRfYXBpL3YxL2NvbmZpZ3VyYXRpb24iLCJjaGFsbGVuZ2VzIjpbXSwiZW52aXJvbm1lbnQiOiJzYW5kYm94IiwiY2xpZW50QXBpVXJsIjoiaHR0cHM6Ly9hcGkuc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbTo0NDMvbWVyY2hhbnRzLzM0OHBrOWNnZjNiZ3l3MmIvY2xpZW50X2FwaSIsImFzc2V0c1VybCI6Imh0dHBzOi8vYXNzZXRzLmJyYWludHJlZWdhdGV3YXkuY29tIiwiYXV0aFVybCI6Imh0dHBzOi8vYXV0aC52ZW5tby5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tIiwiYW5hbHl0aWNzIjp7InVybCI6Imh0dHBzOi8vY2xpZW50LWFuYWx5dGljcy5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tIn0sInRocmVlRFNlY3VyZUVuYWJsZWQiOnRydWUsInRocmVlRFNlY3VyZSI6eyJsb29rdXBVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvMzQ4cGs5Y2dmM2JneXcyYi90aHJlZV9kX3NlY3VyZS9sb29rdXAifSwicGF5cGFsRW5hYmxlZCI6dHJ1ZSwicGF5cGFsIjp7ImRpc3BsYXlOYW1lIjoiQWNtZSBXaWRnZXRzLCBMdGQuIChTYW5kYm94KSIsImNsaWVudElkIjpudWxsLCJwcml2YWN5VXJsIjoiaHR0cDovL2V4YW1wbGUuY29tL3BwIiwidXNlckFncmVlbWVudFVybCI6Imh0dHA6Ly9leGFtcGxlLmNvbS90b3MiLCJiYXNlVXJsIjoiaHR0cHM6Ly9hc3NldHMuYnJhaW50cmVlZ2F0ZXdheS5jb20iLCJhc3NldHNVcmwiOiJodHRwczovL2NoZWNrb3V0LnBheXBhbC5jb20iLCJkaXJlY3RCYXNlVXJsIjpudWxsLCJhbGxvd0h0dHAiOnRydWUsImVudmlyb25tZW50Tm9OZXR3b3JrIjp0cnVlLCJlbnZpcm9ubWVudCI6Im9mZmxpbmUiLCJ1bnZldHRlZE1lcmNoYW50IjpmYWxzZSwiYnJhaW50cmVlQ2xpZW50SWQiOiJtYXN0ZXJjbGllbnQzIiwiYmlsbGluZ0FncmVlbWVudHNFbmFibGVkIjpmYWxzZSwibWVyY2hhbnRBY2NvdW50SWQiOiJhY21ld2lkZ2V0c2x0ZHNhbmRib3giLCJjdXJyZW5jeUlzb0NvZGUiOiJVU0QifSwiY29pbmJhc2VFbmFibGVkIjpmYWxzZSwibWVyY2hhbnRJZCI6IjM0OHBrOWNnZjNiZ3l3MmIiLCJ2ZW5tbyI6Im9mZiJ9'
        log = get_login(request.COOKIES)
        if log:
            on_hold = None
            shops = []
            for purchase in models.Purchase.objects.filter(client__pk=log[0]):
                if purchase.on_hold:
                    on_hold = purchase
                else:
                    shops.append(purchase)
            if on_hold:
                on_hold.transaction_id = create_unique_id(on_hold.pk)
                on_hold.date = tz.now()
                on_hold.save()
                price = on_hold.total_price_with_taxes()[2]
                signature = create_sha(price, on_hold.transaction_id, tpv_fuc, 978, 0,
                                       completed_payment_url, tpv_key)
                # print(on_hold.transaction_id)
                # print(signature)
                return add_info_home(request,
                                     {
                                         'on_hold': on_hold, 'shops': [], 'token': token,
                                         'price_form': price,
                                         'completed_pay_url': completed_pay_url,
                                         'tpv_fuc': tpv_fuc,
                                         'name': on_hold.client.full_name,
                                         'signature': signature,
                                     }
                                     , 'info_card.html')
            else:
                raise Http404('Carrito no encontrado')
        else:
            purchase = get_purchase(request.COOKIES)

            if purchase and purchase.on_hold:
                purchase.transaction_id = create_unique_id(purchase.pk)
                purchase.date = tz.now()
                purchase.save()
                price = purchase.total_price_with_taxes()[2]
                signature = create_sha(price, purchase.transaction_id, tpv_fuc, 978, 0,
                                       completed_payment_url, tpv_key)
                return add_info_home(request, {
                    'on_hold': purchase, 'shops': [], 'token': token,
                    'price_form': price,
                    'tpv_fuc': tpv_fuc,
                    'completed_pay_url': completed_pay_url,
                    'name': purchase.client.full_name,
                    'signature': signature
                },
                                     'info_card.html')
            else:
                raise Http404('Carrito no encontrado')


def change_password(request):
    if request.method == 'GET':
        mail = request.GET['email']
        password = request.GET['key']
        try:
            client = models.Clients.objects.get(email=mail)
            if client.password == password:
                return render(request, 'change_password.html', {'email': mail})
            else:
                raise Http404('Not Found')
        except models.Clients.DoesNotExist:
            raise Http404('Not Found')
    elif request.method == 'POST':
        try:
            new_password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            mail = request.POST['email']
            if new_password != confirm_password:
                return render(request, 'change_password.html', {'email': mail, 'error': 'Las contraseñas no coinciden'})
            else:
                try:
                    client = models.Clients.objects.get(email=mail)
                    client.password = hash(new_password)
                    client.save()
                    ret = HttpResponseRedirect('/')
                    set_cookies(ret, client)
                    return ret
                except models.Clients.DoesNotExist:
                    raise Http404('Not Found')
        except KeyError:
            raise Http404('Not Found')


@csrf_exempt
def payment_methods(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            nonce = request.POST['payment_method_nonce']
        except Exception as e:
            print(e)
            # nonce = "fake-paypal-one-time-nonce"
        # nonce = Nonces.PayPalOneTimePayment
        log = get_login(request.COOKIES)
        on_hold = None
        if log:
            shops = []
            for purchase in models.Purchase.objects.filter(client__pk=log[0]):
                if purchase.on_hold:
                    on_hold = purchase
                else:
                    shops.append(purchase)
        else:
            on_hold = get_purchase(request.COOKIES)
        if on_hold and on_hold.is_valid():
            try:
                result = braintree.Transaction.sale({
                    "amount": on_hold.total_price_with_taxes()[1],
                    # "amount": on_hold.total_price_two()[1],
                    "payment_method_nonce": nonce,
                    "options": {
                        "submit_for_settlement": True
                    }
                })
                print(result)
                try:
                    on_hold.discount()
                    print("We discount")
                except Exception as e:
                    print(e)
                    transaction = braintree.Transaction.find(result.transaction.id)
                    if transaction.status == braintree.Transaction.Status.SubmittedForSettlement:
                        void_result = braintree.Transaction.void(result.transaction.id)
                        if void_result.is_success:
                            return HttpResponseRedirect('/cart_shop/')
                        else:
                            raise Http404(str(void_result.errors.deep_errors))
                    elif transaction.status == braintree.Transaction.Status.Settled:
                        refound_result = braintree.Transaction.refund(result.transaction.id)
                        if refound_result.is_success:
                            return HttpResponseRedirect('/cart_shop/')
                        else:
                            raise Http404(str(refound_result.errors.deep_errors))
                    else:
                        raise Http404(str(transaction.errors.deep_errors))

                try:
                    send_mail_owners(on_hold)
                    # send_mail_owners_prueba(on_hold)
                except Exception as e:
                    print(e)
                    print('Call owners!!!!!!!!!!!!!!!!!!!!!!!')
            except Exception as e:
                print(e)
                result = None
        else:
            return HttpResponseRedirect('/cart_shop/')

        succes_id = None
        error_message = None

        # DONE: succes_id should be saved in database.
        # UNUSED: Deleting things from the database and send the proper emails.
        if result and result.is_success:
            ret = HttpResponseRedirect('/')
            ret.set_cookie('successful_shop', True)
            try:
                succes_id = format(result.transaction.id)
                if on_hold:
                    on_hold.transaction_id = succes_id
                    on_hold.save()
                else:
                    raise Http404('Server function Error')
            except TypeError:
                raise Http404('Braintree Error')
            return ret
        else:
            try:
                error_message = format(result.message)
            except Exception as e:
                print(e)
                return add_info_home(request, {'error': e}, 'fail.html')
            try:
                token = braintree.ClientToken.generate()
            except Exception:
                token = 'eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQiOiJmMDU0MTRmZTc1MGNiYmIwOGQ0YTM1MGIwZmYyYmMxMWE5ZDc0ZWMzNmMxM2QwYjkzNjExYWNiMTUyYTRmNjhhfGNyZWF0ZWRfYXQ9MjAxNS0wOS0wNFQyMDo0NTozMS4zMjE0ODU4MzErMDAwMFx1MDAyNm1lcmNoYW50X2lkPTM0OHBrOWNnZjNiZ3l3MmJcdTAwMjZwdWJsaWNfa2V5PTJuMjQ3ZHY4OWJxOXZtcHIiLCJjb25maWdVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvMzQ4cGs5Y2dmM2JneXcyYi9jbGllbnRfYXBpL3YxL2NvbmZpZ3VyYXRpb24iLCJjaGFsbGVuZ2VzIjpbXSwiZW52aXJvbm1lbnQiOiJzYW5kYm94IiwiY2xpZW50QXBpVXJsIjoiaHR0cHM6Ly9hcGkuc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbTo0NDMvbWVyY2hhbnRzLzM0OHBrOWNnZjNiZ3l3MmIvY2xpZW50X2FwaSIsImFzc2V0c1VybCI6Imh0dHBzOi8vYXNzZXRzLmJyYWludHJlZWdhdGV3YXkuY29tIiwiYXV0aFVybCI6Imh0dHBzOi8vYXV0aC52ZW5tby5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tIiwiYW5hbHl0aWNzIjp7InVybCI6Imh0dHBzOi8vY2xpZW50LWFuYWx5dGljcy5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tIn0sInRocmVlRFNlY3VyZUVuYWJsZWQiOnRydWUsInRocmVlRFNlY3VyZSI6eyJsb29rdXBVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvMzQ4cGs5Y2dmM2JneXcyYi90aHJlZV9kX3NlY3VyZS9sb29rdXAifSwicGF5cGFsRW5hYmxlZCI6dHJ1ZSwicGF5cGFsIjp7ImRpc3BsYXlOYW1lIjoiQWNtZSBXaWRnZXRzLCBMdGQuIChTYW5kYm94KSIsImNsaWVudElkIjpudWxsLCJwcml2YWN5VXJsIjoiaHR0cDovL2V4YW1wbGUuY29tL3BwIiwidXNlckFncmVlbWVudFVybCI6Imh0dHA6Ly9leGFtcGxlLmNvbS90b3MiLCJiYXNlVXJsIjoiaHR0cHM6Ly9hc3NldHMuYnJhaW50cmVlZ2F0ZXdheS5jb20iLCJhc3NldHNVcmwiOiJodHRwczovL2NoZWNrb3V0LnBheXBhbC5jb20iLCJkaXJlY3RCYXNlVXJsIjpudWxsLCJhbGxvd0h0dHAiOnRydWUsImVudmlyb25tZW50Tm9OZXR3b3JrIjp0cnVlLCJlbnZpcm9ubWVudCI6Im9mZmxpbmUiLCJ1bnZldHRlZE1lcmNoYW50IjpmYWxzZSwiYnJhaW50cmVlQ2xpZW50SWQiOiJtYXN0ZXJjbGllbnQzIiwiYmlsbGluZ0FncmVlbWVudHNFbmFibGVkIjpmYWxzZSwibWVyY2hhbnRBY2NvdW50SWQiOiJhY21ld2lkZ2V0c2x0ZHNhbmRib3giLCJjdXJyZW5jeUlzb0NvZGUiOiJVU0QifSwiY29pbmJhc2VFbmFibGVkIjpmYWxzZSwibWVyY2hhbnRJZCI6IjM0OHBrOWNnZjNiZ3l3MmIiLCJ2ZW5tbyI6Im9mZiJ9'
            if result:
                return add_info_home(request, {'on_hold': on_hold, 'token': token, 'error': error_message},
                                     'info_card.html')
            else:
                return HttpResponseRedirect('/')
    else:
        raise Http404('Wrong Access')
        # DONE: If result.is_success this should go somewhere. Is not result.is_success then when should go back and say


@csrf_exempt
def completed_payment(request):
    print('Me estan llamando')
    if request.method == 'POST':
        try:
            amount = request.POST['Ds_Amount']
            print(amount)
            currency = request.POST['Ds_Currency']
            print(currency)
            transaction_id = request.POST['Ds_Order']
            print(transaction_id)
            merchant_code = request.POST['Ds_MerchantCode']
            print(merchant_code)
            response = request.POST['Ds_Response']
            print(response)
            signature = request.POST['Ds_Signature']
            print(signature)
            my_signature = create_sha_2(amount, transaction_id, merchant_code, currency, response,
                                        tpv_key)
            print(my_signature)
            if signature.upper() == my_signature.upper():
                try:
                    value = int(response[len(response) - 2:])
                except ValueError:
                    value = -1
                if response.startswith('00') and 0 <= value <= 99 and len(response) == 4:
                    try:
                        purchase = models.Purchase.objects.get(transaction_id=transaction_id)
                        purchase.discount()
                        purchase.save()
                        try:
                            send_mail_owners(purchase)
                        except Exception:
                            print("We couldn't send the email")
                        print('We shop!')
                    except models.Purchase.DoesNotExist:
                        print('Error in transaction!!!!! ' + str(transaction_id) + ' does not exist!!!')
                return HttpResponse(status=200)
            else:
                print('There was something wrong')
                raise Http404('Get out of my site!!!!!')
        except KeyError:
            print('Key Error')
            raise Http404('Error in POST method')
    else:
        print('Ihis is a GET')
        raise Http404('Not GET method founded')


def completed_payment_fail(request):
    if request.method == 'GET':
        codes = {
            '101': 'Tarjeta caducada',
            '102': 'Tarjeta en excepción transitoria o bajo sospecha de fraude',
            '104': 'Operación no permitida para esa tarjeta o terminal',
            '9104': 'Operación no permitida para esa tarjeta o terminal',
            '116': 'Disponible insuficiente',
            '118': 'Tarjeta no registrada',
            '129': 'Código de seguridad (CVV2/CVC2) incorrecto',
            '180': 'Tarjeta ajena al servicio',
            '184': 'Error en la autenticación del titular',
            '190': 'Denegación sin especificar Motivo',
            '191': 'Fecha de caducidad errónea',
            '202': 'Tarjeta en excepción transitoria o bajo sospecha de fraude con retirada de tarjeta',
            '912': 'Emisor no disponible',
            '913': 'Pedido repetido',
            '9912': 'Emisor no disponible'
        }
        try:
            print(request.GET)
            response = request.GET['Ds_Response']
            try:
                error = codes[response]
            except KeyError:
                error = 'Transacción denegada'
            return add_info_home(request, {'error': error}, 'fail.html')
        except KeyError:
            error = 'Transacción denegada'
            return add_info_home(request, {'error': error}, 'fail.html')
    else:
        raise Http404('Not method founded')


def completed_payment_ok_old(request):
    if request.method == 'GET':
        try:
            amount = request.GET['Ds_Amount']
            print(amount)
            currency = request.GET['Ds_Currency']
            print(currency)
            transaction_id = request.GET['Ds_Order']
            print(transaction_id)
            merchant_code = request.GET['Ds_MerchantCode']
            print(merchant_code)
            response = request.GET['Ds_Response']
            print(response)
            signature = request.GET['Ds_Signature']
            # print(signature)
            my_signature = create_sha_2(amount, transaction_id, merchant_code, currency, response,
                                        tpv_key)

            if signature == my_signature:
                ret = HttpResponseRedirect('/')
                ret.set_cookie('successful_shop', True)
                return ret
            else:
                raise Http404('Error in GET method')

        except KeyError:
            print('Key Error')
            raise Http404('Error in GET method')

    else:
        raise Http404('Not method founded')


def completed_payment_ok(request):
    if request.method == 'GET':
        ret = HttpResponseRedirect('/')
        ret.set_cookie('successful_shop', True)
        return ret
    else:
        raise Http404('Not method founded')
