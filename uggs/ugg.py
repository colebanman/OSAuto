import random
import requests
import threading
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import tls_client
import string
import hashlib
from uuid import uuid4
import faker
from openai import OpenAI
import pick
import csv
from bs4 import BeautifulSoup
import uuid
import time

# CONFIG  ------------------------------
cardNumber = ""
cardMonth = ""
cardYear = ""
cardCVV = ""
firstName = ""
lastName = ""
address1 = ""
address2 = ""
city = ""
state = ""
zipCode = ""
phoneNumber = ""
email = ""
# --------------------------------------


proxies = [

    ]


def getForter(custom_tag="UDF43-mnts-ants", sequential_number=6):
    # Generate a UUID
    uuid_str = str(uuid.uuid4()).replace('-', '')

    # Generate a timestamp or large numerical identifier
    timestamp = int(time.time() * 1000)  # Milliseconds since epoch

    # Combine all parts into the final string
    return f"{uuid_str}_{timestamp}__{custom_tag}_{sequential_number}"

productUrl = "https://www.ugg.com/women-slippers/tasman-regenerate/1136733.html"
productId = productUrl.split(".html")[0].split("/")[-1]
print(f"Product ID: {productId}")

sizes = [
    "6",
    "7",
    "8",
    "9",
    "10",
    "11"
]
color = "CHESTNUT"

session = tls_client.Session(
    client_identifier="safari_ios_16_0",
    random_tls_extension_order=True
)

chosenProxy = random.choice(proxies)
print(f"Using Proxy: {chosenProxy}")

splitProxy = chosenProxy.split(":")
formattedProxy = f"{splitProxy[2]}:{splitProxy[3]}@{splitProxy[0]}:{splitProxy[1]}"
session.proxies = {
    'https': f'https://{formattedProxy}',
    'http': f'http://{formattedProxy}'
}

headers ={
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1',
}
xmlHeaders = {
    'host': 'www.ugg.com',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
    'accept-language': 'en-US,en;q=0.9',
    'sec-fetch-mode': 'cors',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1',
    'connection': 'keep-alive',
    'referer': productUrl,
    'sec-fetch-dest': 'empty',
    'content-type': 'application/x-www-form-urlencoded',
}

session.cookies.set('forterToken', getForter())

print("Fetching Product Page...")

response = session.post(
    productUrl,
    headers=headers,
)

inStock = False

notFound = True
while notFound:
    print("Getting Product Variants...")

    params = {
        'pid': productId,
        'quantity': '1',
    }

    response = session.get(
        'https://www.ugg.com/on/demandware.store/Sites-UGG-US-Site/en_US/Product-Variation',
        params=params,
        headers=xmlHeaders,
    )
    if response.status_code != 200:
        print("Error getting product variants")
        exit()

    response = response.json()
    product = response['product']

    productName = product['productName']
    for variantAttribute in product['variationAttributes']:
        if variantAttribute["attributeId"] == "color":
            for value in variantAttribute["values"]:
                print(value["displayValue"])
                if value["displayValue"] == color:
                    colorId = value["id"]
                    varianturl = value["url"]
                    notFound = False
                    break
    if notFound:
        print("Color not found, Sleeping... (45s)")
        time.sleep(20)
        session.cookies.set('forterToken', getForter())
        chosenProxy = random.choice(proxies)
        print(f"Using Proxy: {chosenProxy}")

        splitProxy = chosenProxy.split(":")
        formattedProxy = f"{splitProxy[2]}:{splitProxy[3]}@{splitProxy[0]}:{splitProxy[1]}"
        session.proxies = {
            'https': f'https://{formattedProxy}',
            'http': f'http://{formattedProxy}'
        }


print(f"Product Name: {productName}")


print("Getting Size Variants...")

sizeDisplayValue = None

while sizeDisplayValue == None:
    response = session.get(varianturl, headers=xmlHeaders)
    response = response.json()
    product = response['product']

    for variantAttribute in product['variationAttributes']:
        if variantAttribute["attributeId"] == "size":
            for value in variantAttribute["values"]:
                if value["displayValue"] in sizes and value["availability"]["type"] != "outofstock":
                    sizeId = value["id"]
                    sizeUrl = value["url"]
                    sizeDisplayValue = value["displayValue"]
                    break
    if sizeDisplayValue == None:
        print("Chosen Size OOS, Sleeping... (45s)")
        time.sleep(45)
        session.cookies.set('forterToken', getForter())
        chosenProxy = random.choice(proxies)
        print(f"Using Proxy: {chosenProxy}")

        splitProxy = chosenProxy.split(":")
        formattedProxy = f"{splitProxy[2]}:{splitProxy[3]}@{splitProxy[0]}:{splitProxy[1]}"
        session.proxies = {
            'https': f'https://{formattedProxy}',
            'http': f'http://{formattedProxy}'
        }

print(f"Found Size: {sizeDisplayValue}")
print(f"Getting Size Variants...")
response = session.get(sizeUrl, headers=xmlHeaders)
response = response.json()
product = response['product']
productImage=  product['images']["default"]["large"][0]["url"]

variantId = product["quantities"][0]["url"].split("pid=")[1].split("&")[0]

print(f"Variant ID: {variantId}")

print("Adding to Cart...")
data = {
    'pid': variantId,
    'quantity': '1',
    'options': '[]',
}

response = session.post(
    'https://www.ugg.com/on/demandware.store/Sites-UGG-US-Site/en_US/Cart-AddProduct',
    headers=xmlHeaders,
    data=data,
)
if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    print("Error adding to cart")
    exit()

response = response.json()
if response["error"]:
    print(response)
    print("Error adding to cart")
    exit()

print("Loading Checkout....")
response = session.get("https://www.ugg.com/checkout", headers=headers)
if response.status_code != 200:
    print("Error loading checkout")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

shipment_uuid = soup.find("div", {"data-shipment-uuid": True})["data-shipment-uuid"]
print(f"Shipment UUID: {shipment_uuid}")    

# find all CSRF tokens
csrfs = soup.find_all("input", {"name": "csrf_token"})
csrf_token1 = csrfs[0]["value"]
csrf_token2 = csrfs[1]["value"]

print(f"CSRF Token: {csrf_token1}")

print("Submitting Shipping Information...")

data = {
    'originalShipmentUUID': shipment_uuid,
    'shipmentUUID': shipment_uuid,
    'dwfrm_shippingOption_shippingOptionID': 'delivery',
    'search-hubbox': '',
    'shipmentSelector': shipment_uuid,
    'dwfrm_shipping_shippingAddress_addressFields_email': email,
    'dwfrm_shipping_shippingAddress_addressFields_phone': phoneNumber,
    'dwfrm_shipping_smsOptIn': 'true',
    'dwfrm_shipping_shippingAddress_addressFields_firstName': firstName,
    'dwfrm_shipping_shippingAddress_addressFields_lastName': lastName,
    'dwfrm_shipping_shippingAddress_addressFields_address1': address1,
    'dwfrm_shipping_shippingAddress_addressFields_address2': address2,
    'dwfrm_shipping_shippingAddress_addressFields_country_countryCode': 'US',
    'dwfrm_shipping_shippingAddress_addressFields_postalCode': zipCode,
    'dwfrm_shipping_shippingAddress_addressFields_city': city,
    'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': state,
    'dwfrm_billing_shippingAddressUseAsBillingAddress': 'true',
    'dwfrm_shipping_shippingAddress_shippingMethodID': 'STG',
    'dwfrm_shipping_shippingAddress_giftMessageRecipientsEmail': '',
    'dwfrm_shipping_shippingAddress_digitalGiftMessage': '',
    'csrf_token': csrf_token1,
}

response = session.post(
    'https://www.ugg.com/on/demandware.store/Sites-UGG-US-Site/en_US/CheckoutShippingServices-SubmitShipping',
    headers=headers,
    data=data,
)

print("Submitting Billing Information...")

data = [
    ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
    ('dwfrm_billing_creditCardFields_cardType', 'Master Card'),
    ('dwfrm_billing_creditCardFields_cardNumber', cardNumber),
    ('dwfrm_billing_creditCardFields_expirationMonth', cardMonth),
    ('dwfrm_billing_creditCardFields_expirationYear', cardYear),
    ('dwfrm_billing_creditCardFields_securityCode', cardCVV),
    ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
    ('dwfrm_billing_paymentMethod', 'CREDIT_CARD'),
    ('dwfrm_billing_shippingAddressUseAsBillingAddress', 'true'),
    ('dwfrm_billing_addressFields_email', email),
    ('dwfrm_billing_addressFields_phone', phoneNumber),
    ('dwfrm_billing_addressFields_firstName', firstName),
    ('dwfrm_billing_addressFields_lastName', lastName),
    ('dwfrm_billing_addressFields_address1', address1),
    ('dwfrm_billing_addressFields_address2', address2),
    ('dwfrm_billing_addressFields_country_countryCode', 'US'),
    ('dwfrm_billing_addressFields_postalCode', zipCode),
    ('dwfrm_billing_addressFields_city', city),
    ('dwfrm_billing_addressFields_states_stateCode', state),
    ('csrf_token', csrf_token2),
    ('skipShipping', 'false'),
    ('contactOnlyShipping', 'null'),
]

response = session.post(
    'https://www.ugg.com/on/demandware.store/Sites-UGG-US-Site/en_US/CheckoutServices-SubmitPayment',
    headers=xmlHeaders,
    data=data,
)
if response.status_code != 200:
    print("Error submitting billing")
    exit()

response = response.json()
orderTotal = response["order"]["priceTotal"]

print(f"Order Total: {orderTotal}")

print("Getting Captcha Token...")

# get array of cookies
cookies = session.cookies.get_dict()
cookieArray = []
for key in cookies:
    cookieArray.append({
        "name": key,
        "value": cookies[key]
    })

callCaptcha = requests.post("https://api.capsolver.com/createTask", json={
  "clientKey": "",
  "task": {
    "type": "ReCaptchaV2Task",
    "websiteURL": "https://www.ugg.com/checkout?stage=payment#payment",
    "websiteKey": "6LevGxsUAAAAAHWmSafPfoXy0In7GB66mQhj4N3-",
    # "isInvisible": True,
    # "pageAction": "submit",
    "apiDomain": "http://www.google.com/",
    "userAgent": headers["user-agent"],
    "cookies": cookieArray,
  }
})

while True:
    response = requests.post("https://api.capsolver.com/getTaskResult", json={
        "clientKey": "",
        "taskId": callCaptcha.json()["taskId"]
    })
    if response.json()["status"] == "ready":
        break
    time.sleep(1)

captchaToken = response.json()["solution"]["gRecaptchaResponse"]

print("Submitting Order...")

data = {
    'dwfrm_billing_emailOptIn': 'true',
    'csrf_token': csrf_token2,
    'g-recaptcha-response': captchaToken,
}

response = session.post(
    'https://www.ugg.com/on/demandware.store/Sites-UGG-US-Site/en_US/CheckoutServices-PlaceOrder',
    cookies=cookies,
    headers=xmlHeaders,
    data=data,
)
if response.status_code != 200:
    print("Error submitting order")
    print(response.text)
    exit()

response = response.json()

if response["error"]:
    title = "Payment Declined!"
    embedColor = "FF0000"
else:
    title = "Order Submitted!"
    embedColor = "00FF00"



webhook = DiscordWebhook(url='')

print("WEBHOOK INFO ------------------")
print(f"Product: {productName}")
print(f"Size: {sizeDisplayValue}")
print(f"Price: {orderTotal}")
print(f"Color: {color}-{colorId}")
print(f"Image: {productImage}")
print("-------------------------------")

embed = DiscordEmbed(title=f"{title}", color=embedColor)
embed.set_thumbnail(url=productImage)

embed.add_embed_field(name="Product", value=f"[{productName}]({productUrl}) | Color: {color}-{colorId}", inline=True)
embed.add_embed_field(name="Size", value=sizeDisplayValue, inline=False)
embed.add_embed_field(name="Price", value=f"{orderTotal}", inline=False)

embed.set_footer(text='UGG Bot')

webhook.add_embed(embed)
response = webhook.execute()