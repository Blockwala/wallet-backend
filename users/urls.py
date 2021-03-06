'''
Created on 20-Feb-2018

@author: karanahuja
'''


'''
Using blockCypher:

Bitcoin    Main    api.blockcypher.com/v1/btc/main
Bitcoin    Testnet3    api.blockcypher.com/v1/btc/test3
Dash    Main    api.blockcypher.com/v1/dash/main
Dogecoin    Main    api.blockcypher.com/v1/doge/main
Litecoin    Main    api.blockcypher.com/v1/ltc/main
BlockCypher    Test    api.blockcypher.com/v1/bcy/test

 Our API always returns values in satoshis, or the lowest non-divisible unit in non-Bitcoin blockchains. 
 As a friendly reminder, there are 10^8 satoshis in a single bitcoinlocal (100,000,000s = 1DASH), 
 10^8 base units per litecoin, and 10^8 koinus per dogecoin (100,000,000k = 1DOGE).


'''

from django.urls import re_path
from . import users
from rest_framework.authtoken import views as rest_framework_views


urlpatterns = [
    re_path(r'^create_user/$', users.create_user, name='create_user'),
    re_path(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token')
]