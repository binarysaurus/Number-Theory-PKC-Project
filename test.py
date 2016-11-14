import os
import math
import itertools
from fractions import gcd
from random import randint
import binascii
import struct

def is_prime(num):
	if num > 1:
		for i in range(2,num):
			if (num % i) == 0:
				return False;
				break
		else:
			return True;
	else:
		return False;

#Extended euclidean algorithm from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def toBinary(string):
    return "".join([format(ord(char),'#010b')[2:] for char in string])

def toString(binaryString):
    return "".join([chr(int(binaryString[i:i+8],2)) for i in range(0,len(binaryString),8)])

def main():
	p = 2**31-1
	q = 2**61-1
	n = p * q
	phi = (p-1)*(q-1)
	
	e = randint(0,phi)
	while gcd(e, phi) != 1:
		e = randint(0,phi)
	
	bezout = xgcd(e, phi)
	
	d = bezout[1]%phi
	
	words = 'sda'
	print("ORIGINAL STRING: ", words)



	m = toBinary(words)
	print("WORDS TO BINARY: ", m)	



	decword = toString(m)
	print("DECWORD  DECODE: ",decword)
	print("WORDS TO BINARY: ",m)
	m = int(m)
	c = pow(m,e,n)
	print("CIPHERTEXT ENC : ",c)


	decode = pow(c,d,n)
	print("FIN DECODE VAL : ", '0'+str(decode))
	print("Decoded Text is: ", toString('0'+str(decode)))


"""
	message = str(bin(decode))
	a=str.encode(message)
	print(message)
	decword = "".join([format(ord(char),'#010b')[2:] for char in a])
	print(decword)
"""

if __name__ == "__main__":
	main()