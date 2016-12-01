import string
import random

from tinydb import TinyDB, Query

from main import dropx, encrypt, decrypt, sync_push, sync_pull, update_password

dby = TinyDB('test.json')
file_name = 'test'


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))


def test_encrypt_decrypt():
    master = 1234
    site = random_char(5)
    site_password = 4444
    encrypt(master, site, site_password, db=dby)
    assert decrypt(master, site, db=dby) == str(site_password)


def test_update_password():
    site = 'LwAhR'
    master = 1234
    new_password = random.randint(1, 10000)
    update_password(master, site, new_password, db=dby)
    assert decrypt(master, site, db=dby) == str(new_password)




