import random
import requests
import threading
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timedelta
import tls_client
import string
import hashlib
from uuid import uuid4
import faker
from openai import OpenAI
import pick
import csv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
import base64
public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlZokgB7v8ZfJWOZIpm+z
U37UR9c655vlUqcaLkyH7aYsosgHTmezqjhC6luz3FI157mVARivpIFzfecUi0Xu
Xw83MwyBrz+wMi+V59QPE+AKK9L4rAhzd/B0GAxhU+BIlumfjHQoc2WEaGYZfRLB
fs8y6OM0Q7wnVuCSfbDJMF0KHaTEPJ1RXuYMvjJ7DNzTXUdsmQW6HfG79dC4gVVg
pH6vZNOp+52rlWWCwfFO8igw+gYz+E+NbywmKNhj6+U+G+ZPFPGjS7QRbdLAfvmN
fakMoiuErtJFMSotgl7WRDU9xt6fFyf0aL+oRJa6gsCgmDKbQyfxnkxV12jH4ZvB
UwIDAQAB
-----END PUBLIC KEY-----
"""

# CONFIG -------------
firstName = ""
lastName = ""
address = ""
city = ""
state = ""
zipCode = ""
phoneNumber = ""
email = ""
cardNumber = ""
expMM = ""
expYY = ""
cvv = ""
# CONFIG -------------


public_key = serialization.load_pem_public_key(
    public_key_pem.encode(),
    backend=default_backend()
)

def to_hex(string):
    return ''.join(f'{byte:02x}' for byte in string.encode('utf-8'))

def rsaEncrypt(card):
    # Encrypting the message
    encrypted = public_key.encrypt(
        card.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=""
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def encryptCard(VictoriaSession):
    data = {
        "1.1": "101231236352",  # merchant_identifier
        "12.63": VictoriaSession.sessionId,  # session_id
        "1.2": "91100",  # store_id
        "1.3": "19215077",  # terminal_id
        "3.4": "00",  # language_indicator
        "3.21": "1.47",  # api_version
        "71.9": "",  # merchant_Token
        "72.18": "",  # masked_Card_Number
        "72.1": "",  # card_Type
        "4.43": "",  # K_NUMBER
        "72.16": "",  # card_Identifier
        "12.132": "3",  # page_Type
        "12.71": "1",  # ecom_url_type
        # "card": "5462910098452634",  # card
        # "expMM": "07",  # expiry_month
        # "expYY": "26",  # expiry_year
        # "cvv": "776",  # cvv
        "4.1": "102",
        "2.2": "",
        "3.7": "1.0",
        "5.6": "",
        "5.7": "",
        "5.8": "",
        "2.1": "",
        "2.3": "00.00.00.00",
        "3.1": "8",
        "3.5": "1.0",
        "3.6": "1.0",
        "3.8": "2",
        "4.2": "000000",
        "4.3": "3",
        "4.4": "encryptedDetailsPlaceholder",
        "4.63": "3",
        "4.5": "0.00",
        "4.20": "",
        "12.88": "1",  # Assuming d.split("-")[0]
        "12.59": "1000",  # Assuming d.split("-")[1]
        "12.60": "000010",  # Assuming d.split("-")[2]
        "4.15": "1",  # Assuming d.split("-")[3]
        "4.18": "11242023",  # getcdate() placeholder
        "4.19": "154502",  # getctime() placeholder
        "2.4.4": "Chrome 119",
        "2.4.2": "Win32",
        "2.4.7": "en-US",
        "2.4.13": "4g",
        "2.4.14": "10",
        "2.4.15": "",
        "2.4.5": "1080x1920",
        "2.4.16": "false",
        "2.4.17": "24",
        "2.4.18": "Desktop",
        "2.4.19": "Windows",
        "2.4.20": "178x479",
        "2.4.21": "428"  # totalLoadTime in milliseconds
    }

  

    ccDetails = f"{VictoriaSession.cardNumber}|{VictoriaSession.expMM}|{VictoriaSession.expYY}|{VictoriaSession.cvv}"
    ccLength = len(ccDetails)

    encryptedCCDetails = rsaEncrypt(ccDetails)
    fullEncrypt = f"{ccLength}|{encryptedCCDetails}"

    data["4.4"] = fullEncrypt


    return to_hex(json.dumps(data))

proxies = [
        
    ]

color = "mustard"
productId = "1119273700"

sizes = [
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]

class VictoriaSecretBot:
    def __init__(self):
        pass

        self.session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )

        chosenProxySplit = random.choice(proxies).split(":")
        chosenProxy = f"http://{chosenProxySplit[2]}:{chosenProxySplit[3]}@{chosenProxySplit[0]}:{chosenProxySplit[1]}"

        self.session.proxies = {
            "http": chosenProxy,
            "https": chosenProxy,
        }


        self.headers = {
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-modified-since': 'Thu, 23 Nov 2023 21:28:39 GMT',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        self.cardNumber = cardNumber
        self.expMM = expMM
        self.expYY = expYY
        self.cvv = cvv

    def getProduct(self):
        print(f"Getting Product Sizes...")

        response = self.session.get(f"https://api.victoriassecret.com/products/v25/page/{productId}?activeCountry=US", headers=self.headers).json()

        variantId = None
        sleepTime = 15
        firstRun = True

        while color not in str(response).lower() or variantId is None:
            print(f"Getting Product Sizes... [COLOR/SIZE NOT FOUND]")
            response = self.session.get(f"https://api.victoriassecret.com/products/v25/page/{productId}?activeCountry=US", headers=self.headers).json()
            if firstRun:
                firstRun = False
                pass
            else:
                print(f"Sleeping for {sleepTime} seconds...")
                time.sleep(sleepTime)

            # print formatted json
            # availableSizes = response["product"]["productData"]
            newProdid = response["product"]["productData"].keys().__iter__().__next__()

            for product in response["product"]["productData"][newProdid]["choices"]:
                product = response["product"]["productData"][newProdid]["choices"][product]
                if "label" not in product:
                    print("Product OOS!")
                    continue
                colorWay = product["label"]
                print(f"Colorway: {colorWay}")
                if color not in colorWay.lower():
                    continue

                print(f"Found {colorWay}...")

                self.colorWay = colorWay

                for image in product["images"]:
                    if image["type"] == "offModelFront":
                        imageUrl = image["image"]

                self.productImage = f"https://www.victoriassecret.com/p/760x1013/" + imageUrl + ".jpg"

                for size in product["availableSizes"]:
                    if size in sizes:
                        size = product["availableSizes"][size]

                        self.sizeId = size["genericId"]
                        self.variantId = size["variantId"]
                        self.price = size["originalPrice"]
                        self.size = size["size1"]
                        
                        return

    def completeCheckout(self): 
        print(f"Adding to Cart...")

        data = {
            "allOrNothing": True,
            "items": [
                {
                    "variantId": self.variantId,
                    "quantity": 1,
                    "collectionId": "",
                    "productPageInstanceId": f"{productId}"
                }
            ],
            "activeCountry": "US"
        }

        response = self.session.post('https://api.victoriassecret.com/orders/v32/bag/items/add', headers=self.headers, json=data).json()
        while response["bag"]["products"] == None:
            print("Error Adding to Cart! Retrying...")
            response = self.session.post('https://api.victoriassecret.com/orders/v32/bag/items/add', headers=self.headers, json=data).json()
            time.sleep(5)

        if len(response["bag"]["products"]) > 0:
            print(f"Added to Cart!")

        print("Loading Checkout...")

        response = self.session.get('https://www.victoriassecret.com/us/checkout#shipdelivery', headers=self.headers)
        if response.status_code == 200:
            print("Loaded Checkout!")

        # with open("checkout.html", "w") as f:
        #     f.write(response.text)

        print("Getting Shipping Method...")

        data = {
            "address": {
                "city": city,
                "countryCode": "US",
                "postalCode": zipCode,
                "region": "CA",
                "streetAddress1": address
            },
            "activeCountry": "US"
        }

        response = self.session.post(
            'https://api.victoriassecret.com/orders/v32/delivery-methods',
            headers=self.headers,
            json=data,
        )
        if response.status_code != 200:
            print("Error Getting Shipping Method!")
            exit()

        for deliveryMethod in response.json()["deliveryOptions"]:
            if deliveryMethod["shippingChargeAmount"] == 0:
                deliveryMethodTitle = deliveryMethod["title"]
                deliveryMethodId = deliveryMethod["code"]
                estimatedDeliveryDate = deliveryMethod["estimatedDeliveryDate"]
                print(f"Found Free Shipping!")
                break
            else:
                print(f"Found Shipping Method: {deliveryMethod['title']}")

        print("Applying Shipping Method...")

        data = {
            "deliveryMethod": {
                "code": deliveryMethodId
            },
            "selectVAS": {
                "giftWrap": {
                    "isApplied": False,
                    "message": ""
                },
                "invoiceMessaging": {
                    "isApplied": False,
                    "message": ""
                }
            },
            "shippingAddress": {
                "address": {
                    "countryCode": "US",
                    "firstName": firstName,
                    "lastName": lastName,
                    "streetAddress1": address,
                    "city": city,
                    "region": state,
                    "postalCode": zipCode,
                    "streetAddress2": "",
                    "phone": phoneNumber
                },
                "forceSaveAddress": False,
                "isPreferredShippingAddress": False,
                "useAsBillingAddress": True,
                "contactInfo": {
                    "email": email,
                    "phone": phoneNumber
                }
            },
            "activeCountry": "US"
        }

        response = self.session.post(
            'https://api.victoriassecret.com/orders/v32/shipping-details',
            headers=self.headers,
            json=data,
        )

        if response.status_code != 200:
            print("Error Applying Shipping Method!")
            exit()

        print("Getting Payment self.session...")

        response = self.session.get(f"https://www.victoriassecret.com/us/checkout#payment", headers=self.headers)
        if response.status_code == 200:
            print("Loaded Payment!")

        data = '{"channel":"WEB","domainId":1,"templateId":3,"terminalId":19215077,"urlType":1,"selectedLanguage":"en","refreshToken":false,"cardType":"","activeCountry":"US"}'

        response = self.session.post(
            'https://api.victoriassecret.com/checkoutpayment/v5/session/credit-card',
            headers=self.headers,
            data=data,
        )

        if response.status_code != 200:
            print("Error Getting Payment Session!")
            exit()

        response = response.json()

        sessionId = response["sessionId"]
        self.sessionId = sessionId

        # print(to_hex(json.dumps(encryptCard("1234567890"))))
        encryptedCard = "STX" + encryptCard(self) + "ETX"

        print("Encrypting Card...")

        data = {
            'formFactorId': '19215077',
            'txnDateTime': '11242023154502', 
            'encryptionFlag': '00',
            'payload': encryptedCard,
        }
        params = {
            'd1': 'es43.auruspay.com',
            'd2': 'es03.auruspay.com',
        }

        # replace tnxDateTime with current time
        data["txnDateTime"] = datetime.now().strftime("%m%d%Y%H%M%S")

        response = requests.post(
            'https://pecst03.aurusepay.com/storeservices/ecom/oneTimeToken',
            params=params,
            headers=self.headers,
            data=data,
        ).json()

        aurusTransactionId = response["aurusTransactionId"]

        print("Adding Payment Method...")

        data = {
            "channel": "WEB",
            "sessionId": sessionId,
            "aurusPaymentType": "MCC",
            "aurusSubPaymentType": "",
            "cardExpMonth": int(self.expMM[1]),
            "cardExpYear": int(self.expYY),
            "lastFourDigits": self.cardNumber[-4:],
            "oneTimeToken": aurusTransactionId,
            "saveToAccount": False,
            "activeCountry": "US"
        }
        response = self.session.post(
            'https://api.victoriassecret.com/checkoutpayment/v5/payment/ott',
            headers=self.headers,
            json=data,
        )
        if response.status_code != 204:
            print("Error Adding Payment Method!")
            exit()

        print("Placing Order...")

        params = {
            'activeCountry': 'US',
        }

        response = self.session.get('https://api.victoriassecret.com/orders/v32/drop', params=params, headers=self.headers)

        if "CHK-SUMMARY-CC-DECLINED" in response.text:
            status = ("Card Declined!")
            # red color
            color = 0xff0000

        else:
            print(response.text)
            # write to file
            with open("order.txt", "w") as f:
                f.write(response.text)
            status = ("Order Placed!")
            # green color
            color = 0x00ff00

        print(status)

        bagData = response.json()["bag"]["products"][0]
        productName = bagData["family"] + " - " + bagData["name"]
        productUrl = "https://www.victoriassecret.com" + bagData["url"]

        from discord_webhook import DiscordWebhook, DiscordEmbed

        webhook = DiscordWebhook(url='')


        embed = DiscordEmbed(title=f"{status}", color=color)
        embed.set_thumbnail(url=self.productImage)

        embed.add_embed_field(name="Product", value=f"[{productName}]({productUrl})", inline=True)
        embed.add_embed_field(name="Size", value=self.size, inline=True)
        embed.add_embed_field(name="Price", value=f"{self.price}", inline=False)
        embed.add_embed_field(name="Estimated Delivery Date", value=estimatedDeliveryDate, inline=True)
        embed.add_embed_field(name="Shipping Method", value=deliveryMethodTitle, inline=True)

        embed.set_footer(text='Victorias Secret Bot')

        webhook.add_embed(embed)
        response = webhook.execute()

def checkout():
    bot = VictoriaSecretBot()
    bot.getProduct()
    bot.completeCheckout()

def main():
    threads = []
    for i in range(10):
        t = threading.Thread(target=checkout)
        t.daemon = True
        t.start()
        threads.append(t)

    # for thread in threads:
    #     thread.join()


if __name__ == "__main__":
    main()
    time.sleep(500000)