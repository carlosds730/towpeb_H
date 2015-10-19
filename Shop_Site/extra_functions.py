
import hashlib
import random
import string


def hash(text):
    try:
        return hashlib.sha256(text).hexdigest()
    except TypeError:
        return hashlib.sha256(text.encode()).hexdigest()


def create_sha(merchant_amount, merchant_order, merchant_merchantcode, merchant_currency, merchant_transactiontype,
               merchant_merchanturl, secret_key='qwertyasdf0123456789'):
    return hashlib.sha1((str(merchant_amount) + str(merchant_order) + str(merchant_merchantcode) + str(
        merchant_currency) + str(merchant_transactiontype) + str(merchant_merchanturl) + str(
        secret_key)).encode()).hexdigest()


def create_sha_2(merchant_amount, merchant_order, merchant_merchantcode, merchant_currency, merchant_response,
                 secret_key='qwertyasdf0123456789'):
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


print(create_sha(1235, 29292929, 201920191, 978, '', '', 'h2u282kMks01923kmqpo'))
print(create_unique_id(25))
print(create_unique_id(486))
