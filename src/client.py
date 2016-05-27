#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from argparse import ArgumentParser
from requests import get
from base64 import b64decode
import logging

logging.basicConfig(level=logging.DEBUG)

def dynencget(url, rsa):
    response = get(url)

    aeskey = rsa.decrypt(b64decode(response.headers['Aes-Key']))
    logging.debug('AES KEY: %r' % aeskey)

    aesiv = b64decode(response.headers['Aes-Iv'])
    logging.debug('AES IV: %r' % aesiv)

    ctr = Counter.new(128, initial_value=long(aesiv.encode('hex'), 16))
    aes = AES.new(aeskey, mode=AES.MODE_CTR, counter=ctr)

    logging.debug('CIPHERTEXT: %r' % response.content)
    return aes.decrypt(response.content)

def getkey(pemfile):
    with open(pemfile) as pem:
        return RSA.importKey(pem.read())

if __name__ == '__main__':
    parser = ArgumentParser(description='Client for HTTP Dynamic Encryption')
    parser.add_argument('URL', help='the url to get from the server')
    parser.add_argument('PEMKEY', default='key.pem', help='PEM private RSA key')
    args = parser.parse_args()

    plaintext = dynencget(args.URL, getkey(args.PEMKEY))
    print plaintext
