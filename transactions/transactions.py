import json
import requests
from bitcoinlocal import transaction
from bitcoinlocal.main import privkey_to_pubkey, pubkey_to_address
from blockcypher import decodetx, create_unsigned_tx
from django.views.decorators.csrf import csrf_exempt
from helper.helper import do_sha256_hash
from django.http import JsonResponse
from bitcoin import ecdsa_tx_sign
from helper.keys import wif_to_private
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from wallet.settings import BLOCK_CHAIN, BLOCK_CHAIN_API, BTC_TEST_CHAIN_URL, DEBUG, LITE_COIN_URL, BTC_COIN_URL, DASH_COIN_URL, DOGE_COIN_URL


'''
Generates a new transaction using receiver/sender keys and amount to send
We use blockcypher for now.
'''
@csrf_exempt 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def generate_raw_transaction(request):
    user = request.user
    request = json.loads(request.body.decode('utf-8'))
    if 'receiver_key' in request and 'sender_key' in request and 'amount' in request and 'coin' in request:
        # parse json
        receiver_key = request['receiver_key']
        sender_key = request['sender_key']
        amount = request['amount']
        coin = request['coin']
        # create blockcypher json
        inputs = [{'address': sender_key}]
        outputs = [{'address':receiver_key, 'value': amount}]  # amount should be in satoshi 1btc = 10^8 satoshi
        # make call
        unsigned_tx = create_unsigned_tx(inputs=inputs, outputs=outputs, include_tosigntx=True, coin_symbol=coin, api_key=BLOCK_CHAIN_API)
        print (receiver_key + " " + sender_key + " " + str(amount))
        print(unsigned_tx)
        if  DEBUG:
            print_signed_data(unsigned_tx)
        if verify_transaction_from_blockcypher_step_1(unsigned_tx) : 
        # and verify_transaction_from_blockcypher_step_2(unsigned_tx, coin): todo when your number of api hits is not an issue use it.
            return JsonResponse(unsigned_tx, status=200)
        else:
            return JsonResponse({"error":"data has been tampered possible HACK"}, status=500)
    else:
        return JsonResponse({"error":"params missing error"}, status=500)


'''
takes in the raw transaction from blockcypher and
double hashes tosign_tx. if it same as tosign, go ahead else data has been tampered
'''


def verify_transaction_from_blockcypher_step_1(tx):
    if 'tosign_tx' in tx and 'tosign' in tx:
        unhashed_data = tx['tosign_tx'][0]
        tosign = tx['tosign'][0]
        print(unhashed_data)
        print(tosign)
        hashed_data = do_sha256_hash(do_sha256_hash(unhashed_data))  # bitcoinlocal standard
        print(hashed_data)
        if (hashed_data == tosign):
            print("verify_transaction_from_blockcypher_step_1 true")
            return True
        else:
            print("verify_transaction_from_blockcypher_step_1 false")
            return False
   
        
'''
takes in raw tx
pulls out tosign_tx
hits the api to reverse decode tx
verifies api generated data == raw tx data
if same: no tampered/hack
'''


def verify_transaction_from_blockcypher_step_2(tx, coin):
    if 'tosign_tx' in tx :
        decoded_tx = decodetx(tx_hex=tx['tosign_tx'][0], coin_symbol=coin, api_key=BLOCK_CHAIN_API)
        decoded_tx_total = decoded_tx['total']
        tx_total = tx['tx']['total']
        decoded_tx_addresses = decoded_tx['addresses']
        tx_addresses = tx['tx']['addresses']
        if(decoded_tx_total == tx_total and decoded_tx_addresses == tx_addresses):   
            print("verify_transaction_from_blockcypher_step_2 true")
            return True
        else:
            print("verify_transaction_from_blockcypher_step_2 false")
            return False

        
'''
takes in the sha256X2 data to sign and returns the signed data
'''


def sign_the_transaction(transaction_hex_uncompressed, raw_private_key):
    return transaction.signall(transaction_hex_uncompressed, raw_private_key)  # todo put check here

        
'''
send transction to bitcoin network
'''
@csrf_exempt 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def broadcast_transaction(request):
    request = json.loads(request.body.decode('utf-8'))
    print(request)
    if 'raw_transaction' in request  and  'coin' in request:
        raw_transaction = request['raw_transaction']
        coin = request['coin']

        url = BTC_COIN_URL
        if coin == 'ltc':
            url = LITE_COIN_URL
        elif coin  == 'btc-testnet':
            url = BTC_TEST_CHAIN_URL
        elif coin  == 'dash':
            url = DASH_COIN_URL
        elif coin  == 'doge':
            url = DOGE_COIN_URL

        url = url + '/txs/push'
        payload = {"tx": raw_transaction}  # Set POST fields here
        print("post_fields " + str(payload))
        response = requests.post(url, data=json.dumps(payload))
        print(response.text)
        print(response.status_code)
        return JsonResponse(json.loads(response.text), status=response.status_code)
    else:
        return JsonResponse({"error":"no tx or coin provided"}, status=500)

    
    
'''
Testing purpose only

SIGN AND PRINT DATA JUST FOR TESTING PURPOSE.
THE PVT KEY IS HARDCODED ONE FROM BTC-TESTNET

Actual signing happens on the front end
User private keys never leave the wallet

<<WARNING: THIS ONLY WORKS FOR BITCOIN>>>
'''
def print_signed_data(unsigned_tx):
    return
    # convert wallet format to hexa
    raw_private_key = wif_to_private('T6nVXLQwFqx24qnWt2EGXuksxWfPdtszh3vty7gUeRkUR79HTcER').zfill(64)
    raw_private_key = raw_private_key.decode('utf-8')
#             raw_public_key = 
    print("raw_private_key " + raw_private_key)
    for sign in unsigned_tx['tosign_tx']:
        # sign the data using bitcoinlocal library
        transaction_hex_uncompressed = sign
        print("transaction_hex_uncompressed " + transaction_hex_uncompressed)
        signed_data = sign_the_transaction(transaction_hex_uncompressed, raw_private_key)  # todo put check here
        print(" signed_data " + str(signed_data))
        pub = privkey_to_pubkey(raw_private_key)
        address = pubkey_to_address(pub)
        print(" pub: " + str(pub))
        print(" address: " + str(address))
        signed_data_2 = ecdsa_tx_sign(transaction_hex_uncompressed, raw_private_key)
        print(" signed_data_2 "+str(signed_data_2))
        # broadcast to the network
        # response = broadcast_transaction(signed_data)
        # return JSONResponse(json.loads(response.text))
