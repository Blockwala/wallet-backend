from blockcypher import get_blockchain_overview, get_block_overview
import json
import datetime
from django.http import JsonResponse
from wallet.settings import BLOCK_CHAIN #production level blockchain . btc-test in test.

'''
retrieves the block information
'''
def get_block_info_http(request):
    if 'block_number' in request.GET:
        block_info = request.GET['block_number']
        return JsonResponse(fetch_blockinfo_from_blockcypher(block_info), status=200)
    elif 'block_height' in request.GET:
        block_info = request.GET['block_height']
        return JsonResponse(fetch_blockinfo_from_blockcypher(block_info), status=200)
    else:
        return JsonResponse('Error:" Send block param', status=500)
    
'''
retrieves the blockchain status
'''
def get_status_of_blockchain_http(request):
    coin = BLOCK_CHAIN
    if 'coin' in request.GET:
        coin = request.GET['coin']
    return JsonResponse(fetch_blockchain_from_blockcypher(coin), status=200)

def get_status_of_blockchain(coin):
    return fetch_blockchain_from_blockcypher(coin);    

def fetch_blockchain_from_blockcypher(coin):
    response = get_blockchain_overview(coin)
    print(response)
    #The JSON module is mainly used to convert the python dictionary above into a JSON string that can be written into a file.
    response = json.dumps(response,  default=myconverter) 
    return response


# '''
# class to send a nice response
# '''
# class JSONResponse(HttpResponse):
#     def __init__(self, obj):
#         super().__init__(
#             json.dumps(obj, default = myconverter),
#             content_type='application/json',
#         )

'''
block_info can be height or block number!
'''
def fetch_blockinfo_from_blockcypher(block_info):
    response = get_block_overview(block_info, coin_symbol=BLOCK_CHAIN)
    print(response)
    #The JSON module is mainly used to convert the python dictionary above into a JSON string that can be written into a file.
    response = json.dumps(response,  default=myconverter) 
    return response

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()