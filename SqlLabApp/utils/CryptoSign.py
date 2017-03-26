from django.core.signing import Signer

signer = Signer()

def encryptData(data):
    return signer.sign(str(data))

def decryptData(cipher):
    return signer.unsign(cipher)