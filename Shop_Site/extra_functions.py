import hashlib
import random
import string
from decimal import Decimal
import os
# import django
#
# django.setup()
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'towpeb_H.settings'

from Shop_Site import models
from django.utils.text import slugify
from towpeb_H.settings import TPV_KEY


def hash(text):
    try:
        return hashlib.sha256(text).hexdigest()
    except TypeError:
        return hashlib.sha256(text.encode()).hexdigest()


def create_sha(merchant_amount, merchant_order, merchant_merchantcode, merchant_currency, merchant_transactiontype,
               merchant_merchanturl, secret_key=TPV_KEY):
    return hashlib.sha1((str(merchant_amount) + str(merchant_order) + str(merchant_merchantcode) + str(
        merchant_currency) + str(merchant_transactiontype) + str(merchant_merchanturl) + str(
        secret_key)).encode()).hexdigest()


def create_sha_2(merchant_amount, merchant_order, merchant_merchantcode, merchant_currency, merchant_response,
                 secret_key=TPV_KEY):
    return hashlib.sha1((str(merchant_amount) + str(merchant_order) + str(merchant_merchantcode) + str(
        merchant_currency) + str(merchant_response) + str(
        secret_key)).encode()).hexdigest()


def random_string(length=16):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def create_unique_id(pk):
    four_number = ''.join([random.choice(string.digits) for _ in range(4)])
    four_number += str(pk)
    left_characters = ''.join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(12 - len(four_number))])
    return four_number + left_characters


def slugify_all():
    print("Someone is calling me")
    for cat in models.Category.objects.all():
        cat.slug = slugify(cat.name)
        cat.save()

    for cat in models.Products.objects.all():
        cat.slug = slugify(cat.name)
        cat.save()


def fix_monto():
    print("Someone is calling me")
    for carrito in models.Purchase.objects.all():
        carrito.save()


def fix_sale_product_price():
    # set_discount()
    for x in models.Purchase.objects.all():
        for pro in x.products.all():
            if not x.on_hold:
                pro.price_sale = pro.product.price
            pro.save()
        x.save()
        # reverse_discount()


def set_discount():
    for x in models.Products.objects.all():
        x.old_price = x.price

        x.price = Decimal(0.85) * x.price
        x.save()


def reverse_discount():
    for x in models.Products.objects.all():
        x.price = x.old_price
        x.old_price = None
        x.save()


def fix_some_shops():
    alv = models.Purchase.objects.get(pk=116)
    for pro in alv.products.all():
        pro.price_sale = Decimal(45.00)
        pro.save()
    alv.save()

    noemi = models.Purchase.objects.get(pk=81)
    for pro in noemi.products.all():
        # print(pro)
        pro.price_sale = Decimal(45.00)
        pro.save()
    noemi.save()

    javier = models.Purchase.objects.get(pk=121)
    pro = javier.products.all()
    a = pro[0]
    a.price_sale = Decimal(30.00)
    a.save()
    b = pro[1]
    b.price_sale = Decimal(45.00)
    b.save()
    javier.save()

    miguel = models.Purchase.objects.get(pk=125)
    for pro in miguel.products.all():
        # print(pro)
        pro.price_sale = Decimal(45.00)
        pro.save()
    miguel.save()


def do_some_fixing():
    slugify_all()
    fix_sale_product_price()
    fix_some_shops()

    # slugify_all()
    # fix_sale_product_price()

    # No need to call you
    # fix_monto()
