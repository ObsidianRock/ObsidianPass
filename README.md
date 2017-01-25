# ObsidianPass

Experiment password manager that syncs to dropbox

## Packages Used

* Click (for creating beautiful command line interfaces )
* Cryptography (provides cryptographic recipes and primitives)
* Dropbox
* Tinydb


## Getting Started

### Install Packages

```
pip install virtualenv
virtualenv venv
source venv/bin/activate (for windows venv\Scripts\activate)
pip install -r requirements.txt
```

[get drop developer api](https://www.dropbox.com/developers)

## Running Application

### Help
```
python main.py --help
```

### Encrypt

```
python main.py encrypt
```
![link to image](https://github.com/ObsidianRock/ObsidianPass/blob/master/img/encrypt_2.jpg  "Encrypting demo")


### Decrypt

```
python main.py decrypt
```

### Update password

```
python main.py update
```

### Delete password

```
python main.py delete
```

### List of sites

```
python main.py sites
```
![link to image](https://github.com/ObsidianRock/ObsidianPass/blob/master/img/sites_2.jpg  "show list of sites")

### sync encrypted database to dropbox

```
python main.py sync_push
```

### sync database on dropbox to local file

```
python main.py sync_pull
```