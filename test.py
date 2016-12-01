import string
import random

from tinydb import TinyDB, Query

from main import dropx, encrypt, decrypt

dby = TinyDB('test.json')


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))


def test_encrypt_decrypt():
    master = 1234
    site = random_char(5)
    site_password = 4444
    encrypt(master, site, site_password, db=dby)
    assert decrypt(master, site, db=dby) == str(site_password)
