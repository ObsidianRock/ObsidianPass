
import dropbox
import pickle
import zlib

from base64 import b64decode, b64encode
from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump
from xxx import TOKEN  # the drop api key is here

db = TinyDB('passwords.json')

def encrypt(master, site, site_password):

    data = encrypt_dump(master, site_password)

    db.insert({'site': site, 'password': data})


def decrypt(master, site):

    field = Query()
    data = db.search(field.site == site)[0]['password']
    password = decrypt_dump(str(master), data)

    return password


def sync_push():

    dropx = dropbox.Dropbox(TOKEN['token'])

    with open('passwords.json', 'rb') as f:
        data = f.read()

    k = zlib.compress(pickle.dumps(data))

    try:
        dropx.files_upload(k, '/passwordBank/passwords.txt')
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None

