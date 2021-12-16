#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Emergency Valve Release Server
    (INTERNAL TO THE CTF)

    @author Unterd0g (mister@unter.dog)
    November 17, 2021
"""

import base64
import cherrypy

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ---------------------------
# Do not change this message
# ---------------------------
EMERGENCY_MSG = b"EMERGENCY"
FLAG          = "CTFUA{8251219ca77c9a046374ebe5a839135b3cd450bd8db6641fcba4ce79de44c3c2}"
# ---------------------------

def __read_key():
    pem_file    = open("secret.pem", 'rb')
    pem         = pem_file.read()
    private_key = serialization.load_pem_private_key(pem, password=None)
    pem_file.close()
    return private_key

class Root:

    def __init__(self, pub_key):
        self.__pub_key  = pub_key

    @cherrypy.expose
    def index(self, msg=None, sign=None):
        if cherrypy.request.method != 'GET':
            cherrypy.serving.response.status = 405
            return #"Unsupported Method!"

        if not msg or not sign:
            cherrypy.serving.response.status = 400
            return #"Invalid Request"

        try:
            b_msg  = base64.urlsafe_b64decode(msg)
            b_sign = base64.urlsafe_b64decode(sign)
        except:
            cherrypy.serving.response.status = 400
            return #"Invalid Request"


        if b_msg != EMERGENCY_MSG:
            cherrypy.serving.response.status = 400
            return #"Invalid request"

        try:
            self.__pub_key.verify(b_sign, b_msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        except:
            cherrypy.serving.response.status = 401
            return #"Unauthorized"

        return FLAG


def main():
    priv_key = __read_key()
    pub_key  = priv_key.public_key()

    cherrypy.config.update({'environment': 'production'})
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.tree.mount(Root(pub_key))
    cherrypy.server.start()

if __name__ == '__main__':
    main()
