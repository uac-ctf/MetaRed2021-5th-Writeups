#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Solver for Valve Release
    (Metared 2021 - Round 5)

    @author Unterd0g (mister@unter.dog)
    December 16, 2021

Took inspiration from:
https://blog.cryptohack.org/twitter-secrets
https://0day.work/0ctf-2016-quals-writeups/
https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/

incomplete "requirements.txt"
pip install pycryptodome
"""

import base64
import binascii
import sys

from Crypto.PublicKey import RSA
from sympy import isprime, mod_inverse


def get_partial_printable(priv_key_pem):
    tmp = priv_key_pem.split('\n')
    out = ""
    for l in tmp[-6:]:
        out += l
        out += '\n'
    return out

def extract_partial(printable_partial):
    tmp = printable_partial.split('\n')
    out = ""
    for l in tmp[:5]:
        out += l
    return out

def recover_key(dp, dq, qinv, e):
    results = []
    d1p = dp * e - 1
    for k in range(3, e):
        if d1p % k == 0:
            hp = d1p // k
            p = hp + 1
            if isprime(p):
                d1q = dq * e - 1
                for m in range(3, e):
                    if d1q % m == 0:
                        hq = d1q // m
                        q = hq + 1
                    if isprime(q):
                        if (qinv * q) % p == 1 or (qinv * p) % q == 1:
                            results.append((p, q, e))
                            return results

def recover_pem(p, q, e):
    n   = p * q
    phi = (p -1)*(q-1)
    d   = mod_inverse(e, phi)
    priv_key = RSA.construct((n, e, d, p, q))
    return priv_key


def get_params_from_partial(partial):
    b_partial = base64.b64decode(partial)

    # -------------------------------------------------------
    # My shitiest code ever ! --> "so called" ASN.1 recovery
    # -------------------------------------------------------
    i    = 0
    j    = -1
    data = dict()
    data[0] = bytearray()
    for b in b_partial:
        if b != 0x2:
            if j == -1 and i != 0:
                j = int(b)
            if j >= 0 or i == 0:
                data[i].append(b)
                j = j - 1
        else:
            if j >= 0:
                data[i].append(b)
                j = j - 1
            else:
                i = i + 1
                data[i] = bytearray()
                j = -1
    # ----------------------------------------------
    if len(data) != 4:
        raise ValueError('Bad key for this :(')

    return data

# Read partial private key
f_partial_pem     = open("partial.pem", 'r')
printable_partial = f_partial_pem.read()
f_partial_pem.close()

# Extract the recoverable parameters from partial key
partial   = extract_partial(printable_partial)
data      = get_params_from_partial(partial)
q_partial = "".join("%02x" % b for b in data[0])
dp = int.from_bytes(data[1][1:], byteorder='big', signed=False)
dq = int.from_bytes(data[2][1:], byteorder='big', signed=False)
qi = int.from_bytes(data[3][1:], byteorder='big', signed=False)

# Recover the private key
e      = 0x10001  # Assume standard e
params = recover_key(dp, dq, qi, e)

# Build the PEM (entirely optional)
p, q, e  = params[0]
priv_key = recover_pem(p, q, e)

# Write recovered PEM
out = open("recovered.pem","w")
out.write(priv_key.exportKey().decode("utf-8"))
out.close()
