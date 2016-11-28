
from fractions import gcd
from random import randint, randrange, getrandbits
import binascii
import string
from flask import Flask, render_template, flash, request, url_for, send_file, make_response, Response
from flask.ext.wtf import Form
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import Required
from itertools import repeat
from functools import reduce


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

p = 2**3217-1
q = 2**4253-1
n = p * q
phi = (p-1)*(q-1)


def text2Int(text):
    """Convert a text string into an integer"""
    #return ''.join(str(ord(c)) for c in text)
    return ''.join(format(ord(x), 'b') for x in text)

 
def int2Text(number, size):
    """Convert an integer into a text string"""
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")

def modSize(mod):
    """Return length (in bytes) of modulus"""
    modSize = len("{:02x}".format(mod)) // 2
    return modSize   





def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))



class ReusableForm(Form):
    str_encrypt = TextField('Number to encrypt :')
    str_decrypt = TextField('Encrypted text :')
    str_key     = TextField('Key of Encrypted :')


@app.route('/umessage', methods=["POST"])
def encryptmessage():
    file = request.files['data_file']
    if not file:
        return "No file"
    f_contents = file.readlines()
    ciphered = []
    for line in f_contents:
        line2 = line
        line = line.decode("utf-8")
        size = len(line2)
        nbytes = min(len(line2), size - 1)
        print(line)
        numedline = text2Int(line)
        print(numedline)
        enc_line = encryptor(int(numedline))
        ciphered.append(enc_line[0])

'''
    return Response(
        ciphered,
        mimetype="text",
        headers={"Content-disposition":
                 "attachment; filename=encrypted.txt"})
                 '''

@app.route("/", methods=['GET', 'POST'])
def main():
    form = ReusableForm(request.form)
 
    print(form.errors)
 
    if request.method == 'POST':
        if (request.form['str_encrypt']):
            str_encrypt=request.form['str_encrypt']
   
            print(str_encrypt)
     
            if form.validate():

                encrypted_data = encryptor(int(str_encrypt))
                flash('Encrypted Text: '+str(encrypted_data[0]))
                flash('Key:            '+str(encrypted_data[1]))
            else:
                flash('All the form fields are required. ')
        elif(request.form['str_decrypt']):
            str_decrypt=request.form['str_decrypt']
            str_key = request.form['str_key']
   
            print(str_decrypt)
     
            if form.validate():
                decrypted_data = decryptor(int(str_decrypt), int(str_key))
                flash('Decrypted Text: '+str(decrypted_data))
            else:
                flash('All the form fields are required. ')             
 
    return render_template('index.html', form=form)

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

def encryptor(m):
    e = randint(0,phi)   
    
    while gcd(e, phi) != 1:
        e = randint(0,phi)
   
    bezout = xgcd(e, phi)   
    d = bezout[1]%phi   
    c = pow(m,e,n)

    print("ORIGINAL BEFR: ", m)
    print("CIPHERTEXT ENC : ", c)
    
    return c, e

def decryptor(c, e):
    phi = (p-1)*(q-1)  
    extend_ea = xgcd(e, phi)  
    d = extend_ea[1]%phi
    decode = pow(c,d,n)
   
    print("ORIGINAL TEXT IN: ", decode)
   
    return decode


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)