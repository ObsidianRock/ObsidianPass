
import dropbox
import click
import pickle
import zlib

from tinydb import TinyDB, Query

from crypto import encrypt_dump, decrypt_dump, check
from xxx import TOKEN  # dropbox api key

dbx = TinyDB('passwords.json')           #
dropx = dropbox.Dropbox(TOKEN['token'])  # put this in setup option

file_name = 'passwords'  ## need a way to specify json folder as well


@click.command()
@click.option('--master', prompt='Your master password',
              help='The master password to encrypt data.')
@click.option('--site', prompt='Your site',
              help='The site to add password.')
@click.option('--site_password', prompt='Your site Password',
              help='The password for the site')
def encrypt(master, site, site_password, db=dbx):
    data = encrypt_dump(str(master), str(site_password))
    try:
        db.insert({'site': site, 'password': data})
        click.echo('Password inserted successfully')
    except Exception as e:
        click.echo(str(e))
        click.echo('Password could not be inserted')


@click.command()
@click.option('--master', prompt='Your master password',
              help='The master password to encrypt data.')
@click.option('--site', prompt='Your site',
              help='The site to add password.')
def decrypt(master, site, db=dbx):

    field = Query()
    data = db.search(field.site == site)[0]['password']
    password = decrypt_dump(str(master), data)
    click.echo(password)


@click.command()
@click.option('--master', prompt='Your master password',
              help='The master password to encrypt data.')
@click.option('--site', prompt='Your site',
              help='The site to add password.')
@click.option('--new_password', prompt='New site Password',
              help='The new password for site')
def update(master, site, new_password, db=dbx):

    field = Query()
    data = db.search(field.site == site)[0]['password']

    if decrypt_dump(str(master), data):
        db.update({'password': encrypt_dump(str(master), str(new_password))}, field.site == site)
        click.echo('updated password')
    else:
        click.echo('Incorrect Master Password')


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


@click.group()
def main():
    pass

main.add_command(encrypt)
main.add_command(decrypt)
main.add_command(update)


if __name__ == "__main__":
    main()
