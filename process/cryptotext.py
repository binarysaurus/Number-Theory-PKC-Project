from process.bitmanipulation import text_to_bits, text_from_bits
from process.math import encryptor, decryptor
from process import STATICDIR

def encryptfile(file, verbose=True):
    
    f_contents = file.readlines()
    
    ciphered = []
    keyed = []
    
    for line in f_contents:

        line = line.decode('utf-8')
        intbin_line = int(text_to_bits(line))

        if verbose:
            print('ENCRYPTION IN PROGRESS:\n')
            print(intbin_line)

        enc_line = encryptor(intbin_line)
        ciphered.append(enc_line[0])
        keyed.append(enc_line[1])
    
    if verbose:
        print('GENERATED CIPHER TEXT:\n')

        for cipher in ciphered:
                print("%s\n" % cipher)
        
        print('GENERATED KEYS:\n')
        
        for key in keyed:
                print("%s\n" % key)

    encrypted_file = open(STATICDIR + 'encrypted_text.txt', 'w')
    key_file = open(STATICDIR + 'keys.txt', 'w')

    encrypted_file.writelines(str(x)+'\n' for x in ciphered)    
    key_file.writelines(str(x)+'\n' for x in keyed)

    encrypted_file.close()
    key_file.close()

def decryptfile(cipher_text, key_text, verbose=True):

    ciph_cont = cipher_text.readlines()
    key_cont = key_text.readlines()
    
    assert len(ciph_cont) == len(key_cont), "Files have been tampered with"
    
    decrypted_file = open(STATICDIR + 'decrypted_text.txt', 'w')
    dec_list = []
    
    for i in range(len(ciph_cont)):
        
        ciph_line = ciph_cont[i].decode('utf-8')
        key_line = key_cont[i].decode('utf-8')

        dec_line = decryptor(int(ciph_line), int(key_line))
        text_dec_line = text_from_bits(str(dec_line))
        
        if verbose:
            print(ciph_line)
            print(key_line)
            print(dec_line)        
            print(text_dec_line)

        dec_list.append(text_dec_line)
        
    decrypted_file.writelines(str(x) for x in dec_list)

    decrypted_file.close()