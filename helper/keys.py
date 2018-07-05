from helper.utils import change_endianness, int2bytes
from bitcoin.core.script import SIGHASH_ALL, SIGHASH_SINGLE, SIGHASH_NONE

from binascii import hexlify, unhexlify
from hashlib import sha256
from ecdsa.util import sigencode_der_canonize, number_to_string
import hashlib
import base58
import binascii


def private_to_wif(key):
    '''
    ref: https://en.bitcoinlocal.it/wiki/Wallet_import_format
    '''
    extended_key = "80"+key
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # add checksum to end of extended key
    final_key = extended_key+second_sha256[:8]
    # Wallet Import Format = base 58 encoded final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    return WIF

def wif_to_private(key):
    '''
    ref: https://en.bitcoinlocal.it/wiki/Wallet_import_format
    takes in the WIF key example : cVe4tA6QHduboeSiQD6Y6nzV1QjaVpDVG2YHbqbtJiSCxsNDYYUF
    step 1 :decode wif to baase 58 to string byte
    step 2: hexify
    step 3: drop last 4 byte and first byte
    '''
    first_encode = base58.b58decode(key)
    private_key_full = binascii.hexlify(first_encode)
    private_key = private_key_full[2:-8]
    return private_key
    

def serialize_pk(pk, compressed=True):
    """ Serializes a ecdsa.VerifyingKey (public key).

    :param compressed: Indicates if the serialized public key will be either compressed or uncompressed.
    :type compressed: bool
    :param pk: ECDSA VerifyingKey object (public key to be serialized).
    :type pk: ecdsa.VerifyingKey
    :return: serialized public key.
    :rtype: hex str
    """

    # Updated with code based on PR #54 from python-ecdsa until the PR gets merged:
    # https://github.com/warner/python-ecdsa/pull/54

    x_str = number_to_string(pk.pubkey.point.x(), pk.pubkey.order)

    if compressed:
        if pk.pubkey.point.y() & 1:
            prefix = '03'
        else:
            prefix = '02'

        s_key = prefix + hexlify(x_str)
    else:
        s_key = '04' + hexlify(pk.to_string())

    return s_key


def serialize_sk(sk):
    """ Serializes a ecdsa.SigningKey (private key).

    :param sk: ECDSA SigningKey object (private key to be serialized).
    :type sk: ecdsa.SigningKey
    :return: serialized private key.
    :rtype: hex str
    """
    return hexlify(sk.to_string())


def ecdsa_tx_sign(unsigned_tx, sk, hashflag=SIGHASH_ALL, deterministic=True):
    """ Performs and ECDSA sign over a given transaction using a given secret key.
    :param unsigned_tx: unsigned transaction that will be double-sha256 and signed.
    :type unsigned_tx: hex str
    :param sk: ECDSA private key that will sign the transaction.
    :type sk: SigningKey
    :param hashflag: hash type that will be used during the signature process and will identify the signature format.
    :type hashflag: int
    :param deterministic: Whether the signature is performed using a deterministic k or not. Set by default.
    :type deterministic: bool
    :return:
    """

    # Encode the hash type as a 4-byte hex value.
    if hashflag in [SIGHASH_ALL, SIGHASH_SINGLE, SIGHASH_NONE]:
        hc = int2bytes(hashflag, 4)
        print("hc>>>>> "+hc)
    else:
        raise Exception("Wrong hash flag.")

    # ToDo: Deal with SIGHASH_ANYONECANPAY

    # sha-256 the unsigned transaction together with the hash type (little endian).
    h = sha256(unhexlify(unsigned_tx + change_endianness(hc)).decode('utf-8')).digest()
    # Sign the transaction (using a sha256 digest, that will conclude with the double-sha256)
    # If deterministic is set, the signature will be performed deterministically choosing a k from the given transaction
    if deterministic:
        s = sk.sign_deterministic(h, hashfunc=sha256, sigencode=sigencode_der_canonize)
    # Otherwise, k will be chosen at random. Notice that this can lead to a private key disclosure if two different
    # messages are signed using the same k.
    else:
        s = sk.sign(h, hashfunc=sha256, sigencode=sigencode_der_canonize)

    # Finally, add the hashtype to the end of the signature as a 2-byte big endian hex value.
    return hexlify(s) + hc[-2:]
