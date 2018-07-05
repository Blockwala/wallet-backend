import json
import datetime
import hashlib
import binascii
from django.http import HttpResponse
from helper import ecdsa_ssl

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    
def convert_to_json(data):
    return json.loads(data,  default=myconverter)

def convert_to_string(data):
    return json.dumps(data,  default=myconverter)


class FormatResponse(HttpResponse):
    def __init__(self, obj):
        super().__init__(
            json.dumps(obj, default = myconverter),
            content_type='application/json',
        )
    
def do_sha256_hash(data):
    data = binascii.unhexlify(data)
    data = hashlib.sha256(data)
    return data.hexdigest()

#HARDWARE WALLET OR HERE : --->
def sign_transaction(PRIVATE_KEY, data_to_sign, SIGHASH_ALL=1):
    ##now we begin with the ECDSA stuff.
    ## we create a private key from the provided private key data, and sign hash_scriptless with it
    ## we also check that the private key's corresponding public key can actually redeem the specified output
    
    k = ecdsa_ssl.KEY()
#     k.generate(('%064x' % PRIVATE_KEY).decode('hex')) error : TypeError: %x format: an integer is required, not bytes . it is used to remove 0x
#     k.generate(PRIVATE_KEY.decode('hex'))
    pvt_key_dehex = binascii.unhexlify(PRIVATE_KEY)
    print("pvt_key_dehex "+str(pvt_key_dehex) )
    k.generate(pvt_key_dehex)
    #here we retrieve the public key data generated from the supplied private key
    pubkey_data = k.get_pubkey()
    print("pubkey_data "+str(pubkey_data) )
    #then we create a signature over the hash of the signature-less transaction
    sig_data=k.sign(data_to_sign)
    #a one byte "hash type" is appended to the end of the signature (https://en.bitcoinlocal.it/wiki/OP_CHECKSIG)
    sig_data = sig_data + chr(SIGHASH_ALL)
    print("sig_data "+sig_data )
    
    ##now we need to write the actual scriptSig.
    ## this consists of the DER-encoded values r and s from the signature, a one-byte hash code type, and the public key in uncompressed format
    ## we also need to prepend the length of these two data pieces (encoded as a single byte
    ## containing the length), before each data piece. this length is a script opcode that tells the
    ## Bitcoin script interpreter to push the x following bytes onto the stack
    scriptSig = chr(len(sig_data)) + sig_data + chr(len(pubkey_data)) + pubkey_data 
    
    print("scriptSig "+scriptSig)
    return scriptSig
    