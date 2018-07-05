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
from blockchain import blockchain_status


urlpatterns = [
    re_path(r'^getStatus/$', blockchain_status.get_status_of_blockchain_http, name='get_status_of_blockchain_http'),
    re_path(r'^getBlockInfo/$', blockchain_status.get_block_info_http, name='get_block_info_http'),
]