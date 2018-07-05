# WALLET BACKEND

 wallet backend  for multichain coins currently supports:

 ### DASH
 
 ### BTC
 
 ### LTC
 
 ### DOGE
 
 Note: Uses blockcypher internally for now



## Reference:
https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx

http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

## Setup:
Pip -r requirements.txt

Setup Nginx 9000 port to 8000 cluster forwarding (references)

Setup .ini settings file for uwsgi


### Deployment:

### DEBUG:

Sh deploy_stage.sh

### PROD:

Start : uwsgi start

Stop : uwsgi --stop /tmp/wallet.pid

Restart: uwsgi --reload /tmp/wallet.pid


## Explanation

### For standalone http direct hits to wsgi :

uwsgi --http :8000 --module wallet.wsgi

uwsgi --socket 127.0.0.1:8000 --protocol=http -w wallet.wsgi

### For nginx communication with uWsgi:

uwsgi --socket 127.0.0.1:8000 -w wsgi

## Nginx on production: 

Settings File:

sudo vi /etc/nginx/nginx.conf

Commands:
sudo service nginx restart

sudo service nginx start

sudo service nginx stop

## Important files:

WSGI : wallet/wsgi

uWsgi settings : deploy_config.ini

Nginx : sudo vi /etc/nginx/nginx.conf
