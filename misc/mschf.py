import os
import json
import requests
from random import randint
from datetime import datetime
from time import sleep
import base64
from bs4 import BeautifulSoup
import datetime
import time
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

session = requests.session()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

userHomeDir = (os.path.expanduser('~'))
taskRaw = open((userHomeDir + "\\AppData\\Roaming\\flowaio\\Tasks.json"), "r")
profileRaw = open((userHomeDir + "\\AppData\\Roaming\\flowaio\\ProfileData.json"), "r")
shopRaw = open((userHomeDir + "\\AppData\\Roaming\\flowaio\\shopSolvers.json"), "r")

TaskData = json.load(taskRaw)
ProfileData = json.load(profileRaw)
ShopData = json.load(shopRaw)[0]


for x in TaskData:
        if x["id"] == "6zBdgWIiCg":
            TaskData = x
for key in ProfileData:
        if key["id"] == TaskData["profile"]["id"]:
            ProfileData = key

    # Card Variables
cardNumber = ProfileData["card"]["number"]
cardName = ProfileData["card"]["holder"]
cardExpiration = ProfileData["card"]["expiration"]
cardCvv = ProfileData["card"]["cvv"]

cardNumber = '+'.join([cardNumber[i:i+4] for i in range(0, len(cardNumber), 4)])

    # Shipping Variables
profileEmail = ProfileData["email"]
profilePhone = ProfileData["phoneNumber"]
profileFirstName = ProfileData["shipping"]["firstName"]
profileLastName = ProfileData["shipping"]["lastName"]
profileAddress1 = ProfileData["shipping"]["addressLine1"]
profileAddress2 = ProfileData["shipping"]["addressLine2"]
profileCity = ProfileData["shipping"]["city"]
profileState = ProfileData["shipping"]["state"]
profileZip = ProfileData["shipping"]["zipCode"]
profileName = ProfileData["name"]

    # Misc Variables
monitorInput = TaskData["monitorInput"]
productId = monitorInput.split(",")[1]
productHandle = monitorInput.split(",")[0]

productName = ""
productPrice = 0
productDate = ""

    # monitorInput="2b5a2ec9-3387-41dd-af99-6e739eb38b9f"
splitProxy = TaskData["proxy"]["proxy"].split(":")

proxy = {
        "https":splitProxy[2]+":"+splitProxy[3]+"@"+splitProxy[0]+":"+splitProxy[1],
        "http":splitProxy[2]+":"+splitProxy[3]+"@"+splitProxy[0]+":"+splitProxy[1]
    }

print("Fetching Product Data..")
productData = session.get("https://gw.prod.api.mschf.xyz/sneakers/v2?limit=68.99568", headers=headers).json()

for key in productData:
    if key["publicId"] == productHandle:
        productName = key["name"]
        productDate = key["liveAt"]
        break

# -------------------------------- IMPLEMENT RECAPTCHA SOLUTION HERE --------------------------------



# -------------------------------- IMPLEMENT RECAPTCHA SOLUTION HERE --------------------------------



print("Creating Auth Token...")
tokenData = '{"token":"03AFY_a8ViGrIJU7gU1kp1H0O13Gxem26rFddF9FG5tAwtNrqAPJqBUXQtlhHKYfUxZkuqc4RUrwmRh5tHqXLrOY1p1NzobK6CIhzlBGqy5vVwwy1w0fxx1kz9eGabYEuG9FmfwMx5lRryJDlf-o048JoLBIuTqAoSQ2z_Bruy97sZq6mwjlUsVTVOyybFHI-7OlkobmuFaa7eG6MZOxcmPT1ZVTEyjut5NI_X-C0B1K2GqWfkZh5V83Pzd_NVSiiNxMRVqHMupUC970Qb31D823W6NfbrS3wfr2Un8N5g1kmLlqj3jQdydYmRlwREuHIqNjYRREPF9N2Eo3wiADtCRYSw4pZhAkHJw5KhWjtl_DwItF-Ajn8vuh3mmGm2zp80me-me2oVXcHqIlW7B7xszCr0Mk5uJW5OaaUOiSEi6iWAv_Mp6HiSkTon1ON0LAtAfPTEw1w9WQSkpJ-dG6rze0EOPcveTD5kbfqJ6OxGJT5Gnkv_aoRpUduOTsHNHmSz5eMXX_hRGGRnrpHuoiaCsmbwmROusrx0cAzUhBKMxdgTKlXpJUAGF-xEMhf4MJe58LTYcQCnU0eCteidYASmEknapU_txLzzwfc81vm1XG0Yy2PMiq2J3W5sGbPJCGDZ6mqsMexH7wnej6Ry_hRJ99AIl5D6VQZY-4knQ9v2--QdAFTsGIBDvQn4ibUbQDdneFBEJ27JPK8lFavAIPRli2YGwkjzYBoVc9uaiyFPsqsAqtiVzAA1AST41W2qd0x1NCazGUhNGdo1NKiKoe5E9XsvCSySgJmn4vxshgfk9ViVKx8Dy08MLNovNP8lcvaCeLs9DYy1F8pF0bju81yJ1mW669Px2S7myXFCOaXDFVp7qghBdhyqKKkZO4swKLkhb-JRJe_NYhtNngKOLIAAk_zg-ybDSmzC26ujiN89rs_U9fKiI5fVoJhrDifhr34yByvhuLOWlhmhA0c4jMmkexWT4zEKZcA16Myy0pF6LorOABc67HV04qNUadZmHLY9LLeyDanPJ92SIwZnbjSlXCH5dbt_lvsvaeN96Wqs75aYQqeHB3PkdwRoYerD_tqZ0CsLon0LSRtxNtAWWVRrVFKK0lFPumRNmSTx250Z4uFC4rm2PDNrwlHJ6PRCMaKYP6Aa6pJpifMLn_z59ruCUr44evYtR9YMKzIO91Sv53gkN437pBIbgV2iOLakWpH3h0RIWVAsbwlr3DPfTlHhHsX6K7yULOIs02nmE02HRsIh1qhp1ymaM4XgZCLKbYxOQSU9lMv2Ek0MKrA1WVbSYNobKT5M6DK-tTrne4WaFIEfe5sWb3yPQtdjoG3zka-eDKk8idS9Zwl5Yyyc3RPwHYo9Vxa72js8uiZEomlC3Qq4K6O8_xFGiMqw6c78Zosoebed8XlwXDSGAVoMapcdB4szfnvYcjPYIX9GnAyrAX5wBOM_kFzhzttkrn1NcgLMTxG1paKS5wCC0ZpROs42_2CIrfgcTJFW3bBmFgNPWI88kKNTjBZwkT9fcAxXCTgth7kTIBrIfVDrbyqjG6IY0h_bwPqQ_SutNEeDZEvE4tM8Dmp93j1xUITecCXK-k4D1L46ESf6a1PMVK_exDvdvyjmLIMS1bXkrw","siteKey":"6LfW59QeAAAAAAvjouZ_r-LhQS3dkUuiATYIpip4"}'
response = session.post('https://gw.prod.api.mschf.xyz/checkouts/auth/guests', headers=headers, data=tokenData).json()
token = response["token"]
headers["Authorization"]=token
json_data = {
        '_type': 'direct',
        'workflow': 'patch_all',
        'version': '1.0.2',
        'dropId': productHandle,
        'lineItems': [
            {
                'type': 'item',
                'productId': productId,
                'quantity': 1,
            },
        ],
        'intent': 'payment',
        'shippingDetails': {
            'address': {
                'country': 'US',
            },
        },
    }

print("Creating Checkout Session...")

response = session.post('https://gw.prod.api.mschf.xyz/checkout-sessions', headers=headers, json=json_data).json()
print(response)
if response["status"]=="out_of_stock":
        print("OOS, Setting Timer..")
        target = (datetime.datetime.fromisoformat("2023-02-16T16:00:00.000"))
        while True:
            remaining = target - datetime.datetime.now()
            if remaining <= datetime.timedelta(0):
                print("Continuing Checkout..")
                break
            print("Sleeping " + str(remaining) + "s..")
            time.sleep(1)

response = session.post('https://gw.prod.api.mschf.xyz/checkout-sessions', headers=headers, json=json_data).json()
orderItem = response["order"]["items"][0]["listingName"]
checkoutId = response["id"]

json_data = {
        '_type': 'direct',
        'workflow': 'patch_all',
        'version': '1.0.2',
        'dropId': productHandle,
        'lineItems': [
            {
                'type': 'item',
                'productId': productId,
                'quantity': 1,
            },
        ],
        'intent': 'payment',
        'shippingDetails': {
            'phone': profilePhone,
            'email': profileEmail,
            'name': profileName,
            'address': {
                'country': 'US',
                'line1': profileAddress1,
                'city': profileState,
                'postalCode': profileZip,
                'state': profileState,
            },
        },
    }

print("Adding Shipping..")

response = session.patch(
        'https://gw.prod.api.mschf.xyz/checkout-sessions/'+checkoutId,
        headers=headers,
        json=json_data,
    ).json() 
print(response)
paymentIntentId = response["paymentIntentId"]
clientSecret = response["clientSecret"]
stripeKey = response["publishableKey"]

params = {
        'key': stripeKey,
        '_stripe_version': '2022-08-01; orders_beta=v4',
        'type': 'order',
        'locale': 'en-US',
        'client_secret': clientSecret,
    }

print("Getting Stripe Session...")
response = session.get('https://api.stripe.com/v1/elements/sessions', params=params, headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }).json()

print("Confirming Stripe Payment...")

subData = 'key='+stripeKey+'&_stripe_version=2022-08-01%3B+orders_beta%3Dv4&client_secret='+clientSecret+'&expand[0]=payment.payment_intent'

response = session.post('https://api.stripe.com/v1/orders/'+clientSecret.split("_secret_")[0]+'/submit', headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }, data=subData).json()

finalPaymentToken = response["payment"]["payment_intent"]["id"]
finalClientSecret = response["payment"]["payment_intent"]["client_secret"]
productPrice = response["amount_total"]

finalData = "return_url=https%3A%2F%2Fcheckout.mschf.com%2F%23%2Fconfirmation%2F"+checkoutId+"%3FcsToken%3D"+token+"&payment_method_data[type]=card&payment_method_data[card][number]="+cardNumber+"&payment_method_data[card][cvc]="+cardCvv+"&payment_method_data[card][exp_year]="+cardExpiration.split("/")[0]+"&payment_method_data[card][exp_month]="+cardExpiration.split("/")[1]+"&payment_method_data[billing_details][address][postal_code]="+profileZip+"&payment_method_data[billing_details][address][country]=US&payment_method_data[payment_user_agent]=stripe.js%2F4bc752f39%3B+stripe-js-v3%2F4bc752f39%3B+payment-element&payment_method_data[time_on_page]=586519&expected_payment_method_type=card&use_stripe_sdk=true&key="+stripeKey+"&_stripe_version=2022-08-01%3B+orders_beta%3Dv4&client_secret="+finalClientSecret
    
print("Submitting Order...")

response = session.post(
        'https://api.stripe.com/v1/payment_intents/'+finalPaymentToken+'/confirm',
        headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        },
        data=finalData,
    )
if response.status_code==402:
        print("Payment Failed")
elif "20" in str(response.status_code):
        print("Payment Successful")
else:
        print("Unknown Error")
        