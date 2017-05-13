from random import randint
from fractions import gcd

from secrets import N, PHI

def encryptor(m, verbose=False):
    e = randint(0,PHI)   
    
    while gcd(e, PHI) != 1:
        e = randint(0,PHI)
    
    c = pow(m,e,N)

    if verbose:
        print("ORIGINAL BEFR: ", m)
        print("CIPHERTEXT ENC : ", c)
    
    return c, e

def decryptor(c, e, verbose=False):
    extend_ea = xgcd(e, PHI)  
    d = extend_ea[1]%PHI
    decode = pow(c,d,N)
    if verbose:
        print("ORIGINAL TEXT IN: ", decode)
   
    return decode


# EEA from:
# https://goo.gl/J1yvGF
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    return  b, x0, y0