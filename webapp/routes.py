from flask import Flask, render_template, flash, request
from wtforms import Form, TextField

from webapp import app
from process.cryptotext import encryptfile, decryptfile

@app.route('/umessage', methods=["POST"])
def encrypt():
    
    file = request.files['data_file']
    
    if not file:
        return "No file"
    
    encryptfile(file=file, verbose=True)

    return render_template('download_enc.html')

@app.route('/dmessage', methods=["POST"])
def decrypt():
    
    cipher_text = request.files['data_file']
    key_text = request.files['key_file']
    
    if not cipher_text or not key_text:
        return "must upload both the cipher text, and the key file"
    
    decryptfile(cipher_text=cipher_text, key_text=key_text, verbose=True)

    return render_template('download_dec.html')
           
@app.route("/", methods=['GET', 'POST'])
def home():
    
    form = ReusableForm(request.form)
 
    print(form.errors)
 
    if request.method == 'POST':
        
        str_encrypt=request.form['str_encrypt']

        if (str_encrypt):
   
            print(str_encrypt)
     
            if form.validate():

                encrypted_data = encryptor(int(str_encrypt))
                flash('Encrypted Text: ' + str(encrypted_data[0]))
                flash('Key:            ' + str(encrypted_data[1]))
            
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
    str_encrypt = TextField('Number to encrypt: ')
    str_decrypt = TextField('Encrypted text: ')
    str_key = TextField('Key of Encrypted: ')