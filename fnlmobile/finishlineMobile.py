import datetime
import json
import time
import requests
import httpx
import string
import random
from fnlmobile.bmpRequest import bmpClient
import asyncio
from discord_webhook import DiscordWebhook, DiscordEmbed
from faker import Faker
import sys

session = httpx.Client()

headers = {
    'welove': 'maltliquor',
    'x-api-version': '3.0',
    'user-agent': 'Finish Line/2.7.3  (Android 13; Build/TE1A.220922.012)',
    'x-banner': 'JDSP',
    'host': 'prodmobloy2.jdsports.com',
    'connection': 'Keep-Alive',
    'content-type': 'application/json; charset=UTF-8',
}


# config ----=---=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=-
pid = "prod2847166"
styleId = "DH9765G"
colorId = "600"

# get argument that is passed to script
profiles = {
    "test":"cardname,cardnum,cardmm,cardyy,cardcvv"
}

profile = "test"

# create random task id like xx-xx-xx
taskId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

async def checkout():
    try:
        client = bmpClient()

        fake = Faker()
        firstName = fake.first_name()
        lastName = fake.last_name()
        # get phone number in format (xxx) xxx-xxxx
        phoneNumber = f"412-412-{random.randint(1000,9999)}"

        # create task id from random string ex: 54-123-51
        def changeStatus(status):
            # changeStatus time in [HH:MM:SS] format
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] | {taskId} | {status}")
            # with open("tasks.json", "r") as f:
            #     tasks = json.load(f)
            #     for task in tasks:
            #         print(task["id"])
            #         if task["id"] == taskId:
            #             task["status"] = status
            #             break
            # with open("tasks.json", "w") as f:
            #     json.dump(tasks, f, indent=4)


        card = profiles[profile].split(",")

        cardNickname = card[0]
        cardNumber = card[1]
        cardMonth = card[2]
        cardYear = card[3]
        cardCvv = card[4]

        changeStatus("Fetching Guest Session...")

        req = await client.get(url="https://prodmobloy2.jdsports.com/api/Account/Guest")
        count = 0

        heads = req.headers
        

        while req.status_code == 206:
            await asyncio.sleep(5)
            count += 1
            changeStatus(f"Polling Queue [{count}]")
            req = await client.get(url="https://prodmobloy2.jdsports.com/api/Account/Guest")



        heads = req.headers
        
        client.headers["x-session"] = heads["x-session"]
        client.headers["x-cookie"] = heads["x-cookie"]
        client.headers["akamaicookie"] = heads["set-cookie"].split(";")[0]


        changeStatus("Fetching Product...")

        productUrl = f"https://prodmobloy2.jdsports.com/api/Products/v2/{pid}"
        req = (await client.get(url = productUrl))
        req = req.json()

        productName = req["displayName"]

        for cw in req["colorWays"]:
            if cw["styleId"] == styleId and cw["colorId"] == colorId:
                productCw = cw
                break

        stock = 0
        skuId = ""

        for sku in productCw["skus"]:
                if sku["quantityAvailable"] > stock:
                    skuId = sku["skuId"]
                    stock = sku["quantityAvailable"]
                    size = sku["size"]

                # skuId = sku["skuId"]
                # stock = str(sku["quantityAvailable"])
        
        stock = str(stock)

        changeStatus(f"Found Product | {productName} | {size} - {stock} In Stock")


        changeStatus("Fetching Cart..")

        req = (await client.get(url="https://prodmobloy2.jdsports.com/api/Cart")).json()


        await client.getCaptcha()


        changeStatus("Adding Product to Cart...")

        await client.refreshBmp()
        req = (await client.postBmp(url="https://prodmobloy2.jdsports.com/api/Cart/Add", json={
            "productId":pid,
            "quantity": 1,
            "skuId": skuId
        }))

        while req == False:
            changeStatus("Size OOS, Retrying...")

            sku = random.choice(productCw["skus"])
            skuId = sku["skuId"]
            stock = sku["quantityAvailable"]
            size = sku["size"]

            changeStatus(f"Found Product | {productName} | {size} - {stock} In Stock")

            req = (await client.postBmp(url="https://prodmobloy2.jdsports.com/api/Cart/Add", json={
                "productId":pid,
                "quantity": 1,
                "skuId": skuId
            }))

        while ("418 Error" in req.text) or ('"itemCount":0' in req.text):
            print("Empty Cart, Retrying...")
            await asyncio.sleep(1)
            await client.refreshBmp()

            req = (await client.postBmp(url="https://prodmobloy2.jdsports.com/api/Cart/Add", json={
                "productId":pid,
                "quantity": 1,
                "skuId": skuId
            }))


                
        # while cartLength == 0:
        #     changeStatus("Cart Empty, Retrying...")
        #     await client.getCaptcha()

        #     req = (await client.postBmp(url="https://prodmobloy2.jdsports.com/api/Cart/Add", json={
        #         "productId":pid,
        #         "quantity": 1,
        #         "skuId": skuId
        #         })).json()
            
        #     if "418 Error" in str(req):
        #         changeStatus("ATC Error, Retrying...")
                
        #     else:
        #         cartLength = (req["itemCount"])
        #     await asyncio.sleep(1)

        # else:
        #     changeStatus(f"Added to Cart | {cartLength} Items")

        client.headers.pop("x-rec")

        changeStatus("Creating Checkout...")

        json_data = {
            'inStorePickup': False,
            'items': [
                {
                    'skuId': skuId,
                    'quantity': 1
                }
            ],
        }

        response = (await client.postBmp(url='https://prodmobloy2.jdsports.com/api/Checkout/Guest', json=json_data, timeout=10)).json()


        
        if "orderId" not in response:
            if "items" in response:
                changeStatus("Created Checkout v2")
            else:
                changeStatus("Error Creating Checkout [v1]")
                print(response)
                return

        changeStatus("Adding Email...")
        response = await client.postBmp(url='https://prodmobloy2.jdsports.com/api/Checkout/Guest/email/true', headers=headers, json={})

        changeStatus("Adding Shipping Address...")

        addyJson = {
            "address1": "",
            "address2": "",
            "city": "",
            "email": "",
            "firstName": firstName,
            "lastName": lastName,
            "phoneNumber": phoneNumber,
            "postalCode": "",
            "shippingMethod": "Economy",
            "state": ""
        }

        response = await client.postBmp(url='https://prodmobloy2.jdsports.com/api/Checkout/Guest/AddShippingGroup', json=addyJson, timeout=10)

        changeStatus("Adding CC...")

        nickName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) 

        cardData = {
            'address': {
                'firstName': firstName,
                'lastName': lastName,
                'address1': '',
                'address2': '',
                'address3': '',
                'city': '',
                'state': '',
                'postalCode': '',
                'phoneNumber': phoneNumber,
                'emailAddress': '',
                'nickName': '',
                'primary': False,
                'sameAsBilling': False,
                'isResidential': False,
            },
            'creditCardExpirationMonth': cardMonth,
            'creditCardExpirationYear': cardYear,
            'creditCardNickname': 'card-' + nickName,
            'creditCardNumber': cardNumber,
            # 'newCreditCardVerificationNumber':cardCvv,
            'newCreditCardVerificationNumber':"641",

        }

        response = await client.postBmp(
            url='https://prodmobloy2.jdsports.com/api/Checkout/Billing/NewAddressNewCard',
            json=cardData
        )
        if response.status_code == 499:
            changeStatus("Error Adding CC!")
            exit()
            
            
        toParse = response.json()

        item = toParse["items"][0]

        thumbnailUrl = item["thumbnailURL"]
        productSku = item["styleId"] + "-" + item["colorId"]
        totalPrice = str(toParse["orderTotalCents"] / 100)


        changeStatus("Placing Order...")

        json_data = {
            'donation': False,
            'isAfterpayExpress': False,
            'isResidential': False,
            'launchItems': False,
            'storeId': ''
        }

        response = (await client.postBmp(
            url='https://prodmobloy2.jdsports.com/api/Checkout/CommitOrder',
            json=json_data
        ))
        if response.status_code == 499:
            changeStatus("Checkout Failed!")

            reason = response.json()["message"]

            webhook = DiscordWebhook(url='s')
            embed = DiscordEmbed(title='Checkout Failed', description='Server Response: ' + reason, color="ff0000")

            embed.add_embed_field(name='Product', value=productName, inline=True)
            embed.add_embed_field(name='Size (Stock)', value=f"{size} ({stock})", inline=False)
            embed.add_embed_field(name='SKU', value=productSku, inline=False)
            embed.add_embed_field(name='Price', value=totalPrice, inline=False)
        
            embed.add_embed_field(name='Proxy', value="||hidden||", inline=False)
            embed.add_embed_field(name='Card Nickname', value="||" + cardNickname + "||", inline=False)



            embed.set_thumbnail(url=thumbnailUrl)
            


            embed.set_footer(text='', icon_url='')
            webhook.add_embed(embed)
            webhook.execute()
        else:
            changeStatus("Checkout Success!")

            reason = response.json()["message"]

            webhook = DiscordWebhook(url='')
            embed = DiscordEmbed(title='Checkout Success', color="00ff00")

            embed.add_embed_field(name='Product', value=productName, inline=True)
            embed.add_embed_field(name='Size (Stock)', value=f"{size} ({stock})", inline=False)
            embed.add_embed_field(name='SKU', value=productSku, inline=False)
            embed.add_embed_field(name='Price', value=totalPrice, inline=False)
        
            embed.add_embed_field(name='Proxy', value="||hidden||", inline=False)
            embed.add_embed_field(name='Card Nickname', value="||" + cardNickname + "||", inline=False)



            embed.set_thumbnail(url=thumbnailUrl)
            


            embed.set_footer(text='', icon_url='')
            webhook.add_embed(embed)
            webhook.execute()
    except Exception as e:
        print("Error: " + str(e))







async def main():
    tasks = []
    for i in range(1):
        tasks.append(asyncio.create_task(checkout()))
    await asyncio.gather(*tasks)

asyncio.run(main())

