import requests
import base64
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from os import urandom
import json
import pytz

class Purchase:
    def encryptAdyen(self, ccname, ccnumber, cvc, exp_month, exp_year):
            plainCardData = Purchase.gnerateCardDataJson(self,
                                                        name=ccname,
                                                        pan=ccnumber,
                                                        cvc=cvc,
                                                        expiry_month=exp_month,
                                                        expiry_year=exp_year
                                                        )
            cardDataJsonString = json.dumps(plainCardData, sort_keys=True)
            aesKey = AESCCM.generate_key(256)
            nonce = urandom(12)
            encryptedCardData = Purchase.encryptWithAesKey(
                self, aesKey, nonce, bytes(cardDataJsonString, encoding='utf8'))
            encryptedCardComponent = nonce + encryptedCardData
            adyenPublicKey = "10001|A937433C0739F986BBC33C89B803C0234E5B96872F349EDDF6F1387D36E1B13CE6FCA58D7D3764E63F0731956A6E5D51EF5DA729A8F7C43334FCEF7E7349C2429E0BF0AC5FDCFAB74821E53E6B78F562DD13E9196FC3DD2715F81DA2D2900C963858CE56F82ECC8B6C397971CD7395AE7618131B14F240CBA2A4F8BBDB068DA521BCF37FD2D4C8C7959AC9FE1A4B3AE34950203EDC00F5E34453CA27A2E4A29F2251B9BCB413203882F9673A44005F4B1FA245DB96D14EF23E37712FCA9DD8A450761631F85EAEA7CCA1DF52E45BE0F33EB2B0864BDC2C566B707AC8C102634C0AAA047F840C404484929701C1BAF0D1803A7BBDA9D1F17C0443C6847751E171"
            publicKey = Purchase.decodeAdyenPublicKey(self, adyenPublicKey)
            encryptedAesKey = Purchase.encryptWithPublicKey(
                self, publicKey, aesKey)
            encryptedAesData = "{}{}${}${}".format("adyenan", "0_1_1",
                                                (base64.standard_b64encode(
                                                    encryptedAesKey)).decode("utf-8"),
                                                (base64.standard_b64encode(encryptedCardComponent)).decode(
                                                    "utf-8"))
            return encryptedAesData

    def gnerateCardDataJson(self, name, pan, cvc, expiry_month, expiry_year):
            generation_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            return {
                "holderName": name,
                "number": pan,
                "cvc": cvc,
                "expiryMonth": expiry_month,
                "expiryYear": expiry_year,
                "generationtime": generation_time
            }
    def encryptWithAesKey(self, aes_key, nonce, plaintext):
            cipher = AESCCM(aes_key, tag_length=8)
            ciphertext = cipher.encrypt(nonce, plaintext, None)
            return ciphertext
    
    def decodeAdyenPublicKey(self, encoded_public_key):
            backend = default_backend()
            key_components = encoded_public_key.split("|")
            public_number = rsa.RSAPublicNumbers(int(key_components[0], 16), int(key_components[1], 16))
            return backend.load_rsa_public_numbers(public_number)
    def encryptWithPublicKey(self, public_key, plaintext):
            ciphertext = public_key.encrypt(plaintext, padding.PKCS1v15())
            return ciphertext