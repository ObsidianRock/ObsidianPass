
from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump


db = TinyDB('passwords.json')


def encrypt(master, site, site_password):

    data = encrypt_dump(master, site_password)

    db.insert({'site': site, 'password': data})


def decrypt(master, site):

    field = Query()
    data = db.search(field.site == site)[0]['password']
    password = decrypt_dump(str(master), data)

    return password


