
import dropbox
import pickle
import zlib

from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump, check
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


def update_password(master, site, new_password):

    field = Query()
    data = db.search(field.site == site)[0]['password']

    if decrypt_dump(str(master), data):
        db.update({'password': encrypt_dump(str(master), str(new_password))}, field.site == site)
        print('updated password')
    else:
        print('Incorrect Master Password')


def sync_push():
    with open('passwords.json', 'rb') as f:
        data = f.read()

    binary = zlib.compress(pickle.dumps(data))
    mode = dropbox.files.WriteMode.overwrite
    try:

        dropx.files_upload(binary, '/passwordBank/passwords.kp', mode)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None


def sync_pull():
    md, res = dropx.files_download('/passwordBank/passwords.kp')
    data = pickle.loads(zlib.decompress(res.content))
    with open('passwords.json', 'w') as f:
        f.write(data.decode('utf-8'))


