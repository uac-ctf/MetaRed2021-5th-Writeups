#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Emergency Valve Release -- !! DO NOT USE THIS LIGHTLY !!

    @author Unterd0g (mister@unter.dog)
    November 17, 2021
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import base64
import requests

# ---------------------------
# Configuration Variables
# ---------------------------
HOST      = "localhost"
PORT      = "8080"
# ---------------------------

# ---------------------------
# Do not change this message
# ---------------------------
EMERGENCY_MSG = b"EMERGENCY"
# ---------------------------

def __read_key():
    pem_file    = open("recovered.pem", 'rb')
    pem         = pem_file.read()
    private_key = serialization.load_pem_private_key(pem, password=None)
    pem_file.close()
    return private_key

def main():
    # read the private key
    private_key = __read_key()

    # build the authenticate message
    signature   = private_key.sign(EMERGENCY_MSG, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

    # encode and send via REST
    url_message   = base64.urlsafe_b64encode(EMERGENCY_MSG).decode()
    url_signature = base64.urlsafe_b64encode(signature).decode()
    resp = requests.get(f"http://{HOST}:{PORT}/?msg={url_message}&sign={url_signature}")

    # print the flag
    print(resp.content)

if __name__ == '__main__':
    main()
