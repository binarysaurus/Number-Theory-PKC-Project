
from fractions import gcd
from random import randint, randrange
import binascii
import string
from flask import Flask, render_template, flash, request, url_for, make_response, Response
from flask.ext.wtf import Form
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import Required
from itertools import repeat
from functools import reduce


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


#p and q are mersenne primes.
p = 2**3217-1
q = 2**4253-1
n = p * q
phi = (p-1)*(q-1)

def encryptor(m):
    e = randint(0,phi)   
    
    while gcd(e, phi) != 1:
        e = randint(0,phi)
    
    c = pow(m,e,n)

    print("ORIGINAL BEFR: ", m)
    print("CIPHERTEXT ENC : ", c)
    
    return c, e

def decryptor(c, e):
    extend_ea = xgcd(e, phi)  
    d = extend_ea[1]%phi
    decode = pow(c,d,n)
   
    print("ORIGINAL TEXT IN: ", decode)
   
    return decode

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

# EEA from:
# https://goo.gl/J1yvGF

def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    return  b, x0, y0

@app.route('/umessage', methods=["POST"])
def encryptmessage():
    file = request.files['data_file']
    if not file:
        return "No file"
    f_contents = file.readlines()
    ciphered = []
    keyed = []
    for line in f_contents:

        line = line.decode('utf-8')
        intbin_line = int(text_to_bits(line))
        print(intbin_line)
        print('now using encryptor function\n--------\n')
        enc_line = encryptor(intbin_line)
        ciphered.append(enc_line[0])
        keyed.append(enc_line[1])
    print('GENERATED CIPHER TEXT\n')
    encrypted_file = open('static/encrypted_text.txt', 'w')
    for cipher in ciphered:
        print(cipher)
        encrypted_file.write("%s\n" % cipher)
        print('\n')
    print('GENERATED KEYS\n')
    key_file = open('static/keys.txt', 'w')
    for key in keyed:
        print(key)
        key_file.write("%s\n" % key)
        print('\n')

    return render_template('download_enc.html')

@app.route('/dmessage', methods=["POST"])
def decryptmessage():
    cipher_text = request.files['data_file']
    key_text = request.files['key_file']
    if not cipher_text or not key_text:
        return "must upload both the cipher text, and the key file"
    ciph_cont = cipher_text.readlines()
    key_cont = key_text.readlines()
    assert len(ciph_cont) == len(key_cont), "Files have been tampered with"
    dec_list = []
    decrypted_file = open('static/decrypted_text.txt', 'w')
    for i in range(len(ciph_cont)):
        ciph_line = ciph_cont[i].decode('utf-8')
        key_line = key_cont[i].decode('utf-8')
        print(ciph_line)
        print(key_line)
        dec_line = decryptor(int(ciph_line), int(key_line))
        
        print(dec_line)
        dec_dec_line = text_from_bits(str(dec_line))
        print(dec_dec_line)
        decrypted_file.write("%s" % dec_dec_line)

    return render_template('download_dec.html')
           
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

class ReusableForm(Form):
    str_encrypt = TextField('Number to encrypt :')
    str_decrypt = TextField('Encrypted text :')
    str_key     = TextField('Key of Encrypted :')


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)
