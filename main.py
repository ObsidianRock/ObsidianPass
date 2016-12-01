
import dropbox
import pickle
import zlib

from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump, check
from xxx import TOKEN  # dropbox api key

dbx = TinyDB('passwords.json')
dropx = dropbox.Dropbox(TOKEN['token'])

file_name = 'passwords'


def encrypt(master, site, site_password, db=dbx):

    data = encrypt_dump(str(master), str(site_password))
    db.insert({'site': site, 'password': data})


def decrypt(master, site, db=dbx):

    field = Query()
    data = db.search(field.site == site)[0]['password']
    password = decrypt_dump(str(master), data)

    return password


def update_password(master, site, new_password, db=dbx):

    field = Query()
    data = db.search(field.site == site)[0]['password']

    if decrypt_dump(str(master), data):
        db.update({'password': encrypt_dump(str(master), str(new_password))}, field.site == site)
        print('updated password')
    else:
        print('Incorrect Master Password')


def sync_push(file):
    with open(file + '.json', 'rb') as f:
        data = f.read()

    binary = zlib.compress(pickle.dumps(data))
    mode = dropbox.files.WriteMode.overwrite
    try:

        dropx.files_upload(binary, '/passwordBank/' + file + '.kp', mode)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None


def sync_pull(file):
    md, res = dropx.files_download('/passwordBank/' + file + '.kp')
    data = pickle.loads(zlib.decompress(res.content))
    with open('passwords.json', 'w') as f:
        f.write(data.decode('utf-8'))


