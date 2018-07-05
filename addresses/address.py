from threading import Thread
from blockcypher import get_address_overview, get_address_details, get_address_full
from wallet.settings import BTC_TEST_CHAIN_URL
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token


'''
get address overview for the account API
'''
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_address_balance(request):

    if 'address' in request.GET :
        address = str(request.GET['address'])
        request_type = 'balance'
        ticker = 'btc'
        if 'type' in request.GET:
            request_type = str(request.GET['type'])
        if 'ticker' in request.GET:
            ticker = str(request.GET['ticker'])
        blockchain_address_thread = BlockchainAddressThread(address, request_type, ticker)
        blockchain_address_thread.start() 
        blockchain_address_thread.join()
        response = blockchain_address_thread.response
        return JsonResponse(response, status=200)
    else:
        return JsonResponse('no address provided', status=500)


'''
Class to segregate different styles of endpoint in address
'''
class BlockchainAddressThread(Thread):
    def __init__(self, address, request_type, ticker):
        Thread.__init__(self)
        self.response = None
        self.address = address
        self.request_type = request_type
        self.ticker = ticker

    def run(self):
        if self.request_type == 'balance':
            self.response=get_address_overview(self.address, coin_symbol=self.ticker)
        elif self.request_type == 'endpoint':
            self.response = get_address_details(self.address, coin_symbol=self.ticker)
        elif self.request_type == 'full_endpoint':
            self.response = get_address_full(self.address, coin_symbol=self.ticker)
    
'''
generate address API : only for btc for now. 
check urls in settings for other.
primarly done at FE in app
'''
def generate_address(request):
    #todo fix all chains
    url = BTC_TEST_CHAIN_URL+'/addrs' # Set destination URL here
    post_fields = {}     # Set POST fields here
    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    print(json)
    return JsonResponse(json, status=200)
    

    
    
