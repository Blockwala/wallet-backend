from bitcoinlocal.main  import encode_privkey, privkey_to_address, is_privkey, is_pubkey, is_address,decode_pubkey, pubkey_to_address,\
    encode_pubkey
from django.http import JsonResponse
from wallet.settings import BLOCK_CHAIN

'''
takes in a key which can be private, public, any format
and returns a sorted json object which has priv_key, pub_key
 in wif formats for front end to query
'''
def format_key(request):
    if 'key' in request.GET :
        key = request.GET['key']
        is_public_only = True
        public_key = ""
        priv_key = ""
        appendbyte = 0
        
        if BLOCK_CHAIN == 'btc': 
            appendbyte = 0
        elif BLOCK_CHAIN == 'btc-testnet':
            appendbyte = 111
            
        if is_address(key):
            public_key = key
            priv_key = None
        elif is_pubkey(key):
            key = decode_pubkey(key)
            key = encode_pubkey(key, 'hex_compressed')
            public_key = pubkey_to_address(key, magicbyte = appendbyte)
            priv_key = None
        elif is_privkey(key):
            is_public_only = False
            priv_key = encode_privkey(key, 'wif_compressed', vbyte=appendbyte) #vbyte for bitcoin is 111
            public_key = privkey_to_address(priv_key, magicbyte=appendbyte)#magicbyte for bitcoin is 111
            
        response = {'public_key':public_key, 'priv_key': priv_key, 'read_only': is_public_only}
        return(JsonResponse(response, status=200))
    else:
        return JsonResponse({'error': 'Error, no key variable provided'}, status=200 )


# class JSONResponse(HttpResponse):
#     def __init__(self, obj):
#         super().__init__(
#             json.dumps(obj, default = myconverter),
#             content_type='application/json',
#         )
#         
#         
# def myconverter(o):
#     if isinstance(o, datetime.datetime):
#         return o.__str__()
