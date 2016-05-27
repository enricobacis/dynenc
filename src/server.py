#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from argparse import ArgumentParser
from bottle import route, run, response
from base64 import b64encode
from os import urandom

@route('/dynenc/<data>')
def dynenc(data):
    aeskey = urandom(32)
    encaeskey = rsa.encrypt(aeskey, '')[0]
    response.set_header('AES-key', b64encode(encaeskey))

    aesiv  = urandom(16)
    response.set_header('AES-iv', b64encode(aesiv))

    ctr = Counter.new(128, initial_value=long(aesiv.encode('hex'), 16))
    aes = AES.new(aeskey, mode=AES.MODE_CTR, counter=ctr)
    return aes.encrypt(data)

def getkey(pemfile):
    with open(pemfile) as pem:
        return RSA.importKey(pem.read())

if __name__ == '__main__':
    parser = ArgumentParser(description='HTTP Dynamic Encryption Test Server')
    parser.add_argument('PEMKEY', help='PEM RSA key')
    args = parser.parse_args()

    rsa = getkey(args.PEMKEY)
    run()
