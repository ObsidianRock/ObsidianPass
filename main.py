
from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump


db = TinyDB('passwords.json')


def encrypt(master, site, site_password):

    data = encrypt_dump(master, site_password)

    db.insert({'site': site, 'password': data})





