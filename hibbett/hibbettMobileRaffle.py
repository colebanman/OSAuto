import asyncio
import httpx
import json
import random
import csv

from hibbett.hibbettAccounts import createAccount

product = "F1412"
size = "12"
raffleType = "instore"

def generate_device_id():
    characters = '0123456789ABCDEF'
    device_id = []
    
    for _ in range(36):
        if _ in [8, 13, 18, 23]:
            device_id.append('-')
        else:
            if _ % 2 == 0:
                device_id.append(random.choice(characters))
            else:
                if device_id[_ - 1] in '0123456789':
                    device_id.append(random.choice(characters[:16]))
                else:
                    device_id.append(random.choice(characters[10:]))

    return ''.join(device_id)


async def genCookies():
    async with httpx.AsyncClient(timeout=20) as client:
        # IMPLEMENT PX SOLUTION HERE

        return {
            'cookie': 'cookie',
            'proxy': 'proxy'
        }
    
async def main(account, accountIndex, cardData):

    profileName = cardData["Profile Name"]
    cardNumber = cardData["Card Number"]
    expirationMonth = cardData["Expiration Month"]
    expirationYear = cardData["Expiration Year"]
    cvv = cardData["CVV"]

    userId = account["customerId"]
    firstName = account["firstName"]
    lastName = account["lastName"]
    phone = account["phone"]
    email = account["email"]

    sessionId = account["sessionId"]


    headers =  {
        'Host': 'hibbett-mobileapi.prolific.io',
        'Accept': '*/*',
        'version': '6.5.0',
        # 'Authorization': f'Bearer {sessionId}',
        'x-api-key': '0PutYAUfHz8ozEeqTFlF014LMJji6Rsc8bpRBGB0',
        'platform': 'ios',
        'Accept-Language': 'en-US;q=1.0, ja-US;q=0.9',
        'User-Agent': 'Hibbett | CG/6.5.0 (com.hibbett.hibbett-sports; build:11914; iOS 16.6.0) Alamofire/5.0.0-rc.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=utf-8',
        
    }

    print("Generating PX Session...")

    pxSession = await genCookies()
    headers['X-PX-AUTHORIZATION'] = '3:' + pxSession['cookie']

    pxProxy = pxSession["proxy"].split("http://")[1]

    server = pxProxy.split("@")[1]
    username = pxProxy.split("@")[0].split(":")[0]
    password = pxProxy.split("@")[0].split(":")[1]

    proxy = httpx.Proxy(f"http://{server}", auth=(username, password))

    session = httpx.AsyncClient(headers=headers, proxies=proxy, timeout=20)

    print("Fetching User Data...")

    response = (await session.get("https://hibbett-mobileapi.prolific.io/users/" + userId))


    if "customerNumber" not in response.json():
        if response.status_code == 401:
            print("Logging In...")

            response = (await session.post("https://hibbett-mobileapi.prolific.io/users/login", json={
                "password": account["password"],
                "login": account["email"]
            })).json()

            if "sessionId" not in response:
                print(response)
                return
            
            sessionId = response["sessionId"]

            with(open("data.json", "r")) as f:
                data = json.load(f)

            data["accounts"][accountIndex]["sessionId"] = sessionId

            with(open("data.json", "w")) as f:
                json.dump(data, f, indent=4)

            headers['Authorization'] = f'Bearer {sessionId}'
            session = httpx.AsyncClient(headers=headers, proxies=proxy)

        return
    
    response = response.json()

    customerNumber = response["customerNumber"]
    userNonce = response["nonce"]

    if "addressId" not in account:

        print("Adding User Address..")

        userAddressId = f"main-{random.randint(100000, 999999)}"

        json_data = {
            'address1': '',
            'country': 'US',
            'id': userAddressId,
            'isPrimary': False,
            'firstName': firstName,
            'state': '',
            'city': '',
            'lastName': lastName,
            'zip': '',
            'address2': '',
            'phone': phone,
        }

        random3Letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))

        json_data["address1"] = json_data["address1"] + " " + random3Letters

        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/users/{userId}/addresses", json=json_data))
        
        if response.status_code == 200:
            print("Address Added!")

            with(open("data.json", "r")) as f:
                data = json.load(f)

            data["accounts"][accountIndex]["addressId"] = userAddressId

            with(open("data.json", "w")) as f:
                json.dump(data, f, indent=4)
    
    else:
        userAddressId = account["addressId"]

    if "paymentId" not in account:

        print("Getting Card Encryption Key...")

        response = (await session.post(f"https://hostedpayments.radial.com/hosted-payments/pan/tokenize?access_token={userNonce}", json={
            "paymentAccountNumber": cardNumber
        })).json()

        if "account_token" not in response:
            print(response)
            return
        
        accountToken = response["account_token"]

        print("Posting CVV and Card Data...")

        response = (await session.post(f"https://hostedpayments.radial.com/hosted-payments/encrypt/pancsc?access_token={userNonce}", json={
            "cardSecurityCode": cvv,
            "paymentAccountNumber": cardNumber
        })).json()

        if "encryptedPaymentAccountNumber" not in response:
            print(response)
            return
        
        encryptedPaymentAccountNumber = response["encryptedPaymentAccountNumber"]
        encryptedCardSecurityCode = response["encryptedCardSecurityCode"]

        print("Adding Payment Method...")

        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/users/{userId}/payment_methods?addressId=" + userAddressId, json={
            "paymentObject": {
                "creditCardToken": accountToken,
                "nameOnCard": firstName + " " + lastName,
                "cardType": "Master Card",
                "number": "************" + cardNumber[-4:],
                "expirationMonth": int(expirationMonth.replace("0", "")),
                "expirationYear": int(expirationYear),
                "encryptedCVNValue": encryptedCardSecurityCode
            },
            "type": "CREDIT_CARD"
        })).json()

        paymentId = response[0]["id"]

        with(open("data.json", "r")) as f:
            data = json.load(f)

        data["accounts"][accountIndex]["paymentId"] = paymentId

        with(open("data.json", "w")) as f:
            json.dump(data, f, indent=4)
    else:
        paymentId = account["paymentId"]

    print("Checking Phone Validity...")

    response = (await session.post(f"https://hibbett-mobileapi.prolific.io/raffles/users/{userId}/checkIfVerified", json={
        "phone": phone
    })).json()

    if response["verified"] == False:
        phone = input("Enter Phone Number: ")

        with(open("data.json", "r")) as f:
            data = json.load(f)

        data["accounts"][accountIndex]["phone"] = phone
        
        with(open("data.json", "w")) as f:
            json.dump(data, f, indent=4)

        print("Checking new Number Validity...")

        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/raffles/users/{userId}/checkIfVerified", json={
            "phone": phone
        })).json()

        code = input("Enter Phone Code: ")
        
        print("Verifying Phone...")

        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/raffles/users/{userId}/verifyPhone", json={
            "code": code,
            "phone": phone
        }))

    # gen device id like 41400542-8961-41D5-9B5D-9D67E42D6AE2

    deviceId = generate_device_id()
    

    if raffleType == "instore":

        print("Fetching Raffle Stores...")

        response = (await session.get(f"https://hibbett-mobileapi.prolific.io/raffles/{product}/stores?query=zip&distanceUnit=mi&maxDistance=200")).json()

        storeIds =""
        for store in response["raffleStores"]:
            storeIds += store["id"] + ","

        storeIds = storeIds[:-1]

        print(f"Entering Raffle... [Instore] - " + deviceId + " - " + storeIds)
        
        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/raffles/{product}/users/{userId}/register", json={
            "phone": phone,
            "size": size,
            "storeIds": storeIds,
            "deviceId": deviceId,
            "online": False,
            "customerNumber": customerNumber,
            "textOptIn": False,
            "lightningRound": False
        })).json()

        productName = response["name"]
        status = response["registration"]["status"]

        print(f"Entered Raffle for {productName}! Status: {status}")

    else:

        print("Entering Raffle... [Online]")

        response = (await session.post(f"https://hibbett-mobileapi.prolific.io/raffles/{product}/users/{userId}/register", json={
            "online": True,
            "shippingAddressId": userAddressId,
            "deviceId": deviceId,
            "billingAddressId": userAddressId,
            "size": size,
            "lightningRound": True,
            "textOptIn": False,
            "customerNumber": customerNumber,
            "shippingMethodId": "ANY_GND",
            "shippingMethodName": "Standard Typically arrives in 3-7 days",
            "paymentInstrumentId": paymentId,
            "cardSecurityCode": cvv,
            "phone": phone
        }))

        productName = response["name"]
        status = response["registration"]["status"]

        print(f"Entered Raffle for {productName}! Status: {status}")


    

    # req = await session.get(f"https://hibbett-mobileapi.prolific.io/users/{userId}/basketId")
    # print(req.json())

    # print('Creating Account...')




async def setupAccounts():
    cards = []

    with open('cards.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cards.append(row)

    with open("data.json", "r") as f:
        accounts = json.load(f)

    tasks = []
    limit = 5

    count = 0

    for account in accounts["accounts"]:
        if count == limit:
            break

        tasks.append(main(account, count, cards[count]))

        count += 1

    # tasks = tasks[:limit]

    await asyncio.gather(*tasks)


asyncio.run(setupAccounts())


    