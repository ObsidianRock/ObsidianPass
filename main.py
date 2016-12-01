
import dropbox
import pickle
import zlib

from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump
from xxx import TOKEN  # dropbox api key

db = TinyDB('passwords.json')
dropx = dropbox.Dropbox(TOKEN['token'])


def encrypt(master, site, site_password):

    data = encrypt_dump(master, site_password)

    db.insert({'site': site, 'password': data})


def decrypt(master, site):

    field = Query()
    data = db.search(field.site == site)[0]['password']
    password = decrypt_dump(str(master), data)

    return password


def sync_push():
    with open('passwords.json', 'rb') as f:
        data = f.read()

    k = zlib.compress(pickle.dumps(data))

    try:
        dropx.files_upload(k, '/passwordBank/passwords.kp')
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None


def sync_pull():
    md, res = dropx.files_download('/passwordBank/passwords.kp')
    data = pickle.loads(zlib.decompress(res.content))
    with open('passwords.json', 'w') as f:
        f.write(data.decode('utf-8'))

