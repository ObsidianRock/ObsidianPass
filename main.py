from xxx import TOKEN  # dropbox api key

import dropbox
import click
import pickle
import zlib

from datetime import datetime

from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware

from crypto import encrypt_dump, decrypt_dump
from datetime_serializer import DateTimeSerializer


file_name = 'passwords.json' ## need a way to specify json folder as well

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

dbx = TinyDB(file_name, storage=serialization)
dropx = dropbox.Dropbox(TOKEN['token'])  # put this in setup option


@click.command()
@click.option('--master',
              prompt='Master password',
              hide_input=True,
              help='Master password to encrypt data.')
@click.option('--account',
              prompt='Account name',
              help='The site or account to add password.')
@click.option('--site_password',
              prompt='Account password',
              hide_input=True,
              help='Password for the account or site')
def encrypt(master, account, site_password, db=dbx):
    data = encrypt_dump(str(master), str(site_password))
    try:
        db.insert({'Account': account, 'Password': data, 'Last updated': datetime.now()})
        click.echo('Password inserted successfully')
    except:
        click.echo('Password could not be inserted')


@click.command()
@click.option('--master',
              prompt='Master password',
              hide_input=True,
              help='Master password to encrypt data.')
@click.option('--account',
              prompt='Account name',
              help='Site or account to add password.')
def decrypt(master, account, db=dbx):
    field = Query()
    try:
        data = db.search(field.Account == account)[0]['Password']
        password = decrypt_dump(str(master), data)
        if password:
            click.echo(password)
        else:
            click.echo('Incorrect master password')
    except:
        click.echo('The account does not exist')


@click.command()
@click.option('--master',
              prompt='Master password',
              hide_input=True,
              help='Master password to encrypt data.')
@click.option('--account',
              prompt='Your site',
              help='The site to add password.')
@click.option('--new_password',
              prompt='New account Password',
              hide_input=True,
              help='New password for account')
def update(master, account, new_password, db=dbx):

    field = Query()
    try:
        data = db.search(field.Account == account)[0]['Password']
        if decrypt_dump(str(master), data):
            db.update({'Password': encrypt_dump(str(master), str(new_password))}, field.Account == account)
            db.update({'Last updated': datetime.now()}, field.Account == account)
            click.echo('Updated password')
        else:
            click.echo('Incorrect Master Password')
    except:
        click.echo('Site does not exist')


@click.command()
@click.option('--master',
              prompt='Master password',
              hide_input=True,
              help='Master password to encrypt data.')
@click.option('--account',
              prompt='Your site',
              help='Account to add password.')
def delete(master, account, db=dbx):
    field = Query()
    try:
        data = db.search(field.Account == account)[0]['Password']
        if decrypt_dump(str(master), data):
            db.remove(field.Account == account)
            click.echo('Deleted password')
        else:
            click.echo('Wrong master password')
    except:
        click.echo('Account does not exist')


@click.command(help='Lists the number of sites in database')
def sites(db=dbx):
    for password in db.all():
        click.echo(password['site'])


@click.command(help='sync encrypted database to dropbox')
def sync_push():

    with open(file_name, 'rb') as f:
        data = f.read()

    binary = zlib.compress(pickle.dumps(data))
    mode = dropbox.files.WriteMode.overwrite

    try:
        dropx.files_upload(binary, '/passwordBank/passwords.kp', mode)
        click.echo('Database is sync on dropbox')
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)


@click.command(help='sync database on dropbox to local file')
def sync_pull():
    try:
        md, res = dropx.files_download('/passwordBank/passwords.kp')
        data = pickle.loads(zlib.decompress(res.content))
        with open(file_name, 'w') as f:
            f.write(data.decode('utf-8'))
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)


@click.group()
def main():
    pass

main.add_command(encrypt)
main.add_command(decrypt)
main.add_command(update)
main.add_command(delete)
main.add_command(sites)
main.add_command(sync_push)
main.add_command(sync_pull)


if __name__ == "__main__":
    main()
