import string
import random

from tinydb import TinyDB, Query

from main import db, dropx, encrypt, decrypt

db = TinyDB('test.json')


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def encrypt_decrypt(master, site, site_password):
    encrypt(master, site, site_password)
    password = decrypt(master, site)
    return password


def test_encrypt_decrypt():
    master = 1234
    site = random_char(5)
    site_password = 4444
    assert encrypt_decrypt(master, site, site_password) == str(site_password)
