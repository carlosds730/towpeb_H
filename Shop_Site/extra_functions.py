__author__ = 'Roly4'

import hashlib


def hash(text):
    try:
        return hashlib.sha256(text).hexdigest()
    except TypeError:
        return hashlib.sha256(text.encode()).hexdigest()

