import asyncio
import random
import string
import json
from faker import Faker
from discord_webhook import DiscordWebhook, DiscordEmbed
import httpx

from bmpRequest import bmpRequest
from refreshToken import refresh_token
from task import Task
from adyen import Purchase

async def queue_mode(account, profile, sku, size, delay):
    try:

        task = Task("enter_draw")

        # task.setStatus(f"Waiting {delay} seconds...", "warning")
        # await asyncio.sleep(delay)


        email = account["email"]
        password = account["password"]

        firstName = account["first_name"]
        lastName = account["last_name"]

        baseAddress = profile["address1"]
        random3 = random.choice(string.ascii_letters).upper() + random.choice(string.ascii_letters).upper() + random.choice(string.ascii_letters).upper()
        profile["address1"] = baseAddress + " " + random3
        
        if profile["address2"] == "":
            randomAptNum = random.randint(1, 100)
            profile["address2"] = "Apt " + str(randomAptNum)


        def ranDig():
            return str(random.randint(0,9))

        # generate random phone
        fake = Faker()
        profile["phone"] = "925" + ranDig() + ranDig() + ranDig() + ranDig()+ ranDig()+ ranDig()+ ranDig()

        refreshToken = account["refreshToken"]

        task.setStatus("Refreshing Account...", "none")


        refreshAccount = (await refresh_token(email, refreshToken, password, task))

        accessToken = refreshAccount[0]

        task.setStatus("Fetching Session...", "none")

        session = bmpRequest(accessToken)
        await session.fetchDeviceId()
        await session.rotateProxy()
        await asyncio.sleep(0.25)

        # task.setStatus("Fetching Account...", "none")
        # req = await session.getBmp('https://api.3stripes.net/gw-api/v2/orders?page=0&limit=0')
        # print(req.text)
        # return

        if "addressId" not in account:
                task.setStatus("Adding Address...", "warning")
                async def addAddress():
                    request = (await session.postNoBmp('https://api.3stripes.net/gw-api/v2/user/addresses', json_data={
                            "phone": profile["phone"],
                            "city": profile["city"],
                            "state_code": profile["state"],
                            "address1": profile["address1"],
                            "address2": profile["address2"],
                            "postal_code": profile["zip"],
                            "last_name": lastName,
                            "country_code": "US",
                            "type": "SHIPPING",
                            "first_name": firstName
                        }))
                    if request.status_code == 409:
                        # fetch address
                        request = (await session.get('https://api.3stripes.net/gw-api/v2/user/addresses')).json()
                        return request["addresses"][0]
                    if str(request.status_code)[0] != "2":
                        print({
                            "phone": profile["phone"],
                            "city": profile["city"],
                            "state_code": profile["state"],
                            "address1": profile["address1"],
                            "address2": profile["address2"],
                            "postal_code": profile["zip"],
                            "last_name": lastName,
                            "country_code": "US",
                            "type": "SHIPPING",
                            "first_name": firstName
                        })
                        task.setStatus("Error Adding Address... (" + str(request.status_code) + ")", "bad")
                        raise Exception(request.text)
                    return request.json()
                
                addressId = (await addAddress())["id"]
                account["addressId"] = addressId
                # append to json file with array
                jsonData = (json.load(open('data.json')))
                for i in range(len(jsonData["accounts"])):
                    if jsonData["accounts"][i]["email"] == email:
                        jsonData["accounts"][i]["addressId"] = addressId
                        break
                with open('data.json', 'w') as outfile:
                    json.dump(jsonData, outfile, indent=4)
        else:
            addressId = account["addressId"]

        task.setStatus("Fetching Product...", "none")

        request = (await session.get(f"https://api.3stripes.net/gw-api/v2/trilogy/products/{sku}?experiment_product_data=false")).json()

        productImage = request['_links']['image_large']['href']
        productName = request['product_name'] + " - " + request['color_name']
        productPrice = request['original_price']
        eventId = request['queue_pro_event']['event_id']

        task.setStatus("Fetching Queue Parameters...", "none")

        request = (await session.getSpecial(f"https://api.3stripes.net/gw-api/v2/hype/products/{sku}/availability?experiment_product_data=false")).json()

        technicalSize = None

        for variant in request['_embedded']['variations']:
            if (variant['size'] == size):
                technicalSize = variant['technical_size']
                if variant['orderable'] == False:
                    task.setStatus("Size Not Orderable!", "bad")
                    return
                break
        if technicalSize == None:
            print("Size Not Found - " + email)
            return
        
        # task.setStatus("Exiting Manual...", "good")
        # return
    
        task.setStatus("Adding Queue Product to Cart - " + size + " - " + technicalSize, "warning")

        request = (await session.post('https://api.3stripes.net/gw-api/v2/hype/basket', json_data={
            'items': [
                {
                    'product_id': sku,
                    'variation_product_id': f"{sku}_{technicalSize}",
                    'quantity': 1,
                },
            ],
            'event_id': eventId,
        }, 
        ))

        if request.status_code != 200:
            task.setStatus("Error Adding Queue Product to Cart! - " + request.json()["detail"], "bad")
            return
        data = request.json()

        basketId = data["basket_id"]
        totalPrice = data["total_price"]

        task.setStatus("Attaching Address to Checkout...", "warning")

        request = (await session.put(f"https://api.3stripes.net/gw-api/v2/hype/basket/{basketId}", json_data={
            "items": [
                {
                "product_id": sku,
                "variation_product_id": f"{sku}_{technicalSize}",
                "quantity": 1
                }
            ],
            "invoice_info": {
                "type": "0"
            },
            "selected_shipping_type_id": "home_delivery",
            "billing_info": {
                "id": addressId,
                "personal_id": "",
                "tax_administration": "",
                "address1": profile["address1"],
                "phone": "+1" + profile["phone"],
                "house_number": "",
                "colony": "",
                "address2": profile["address2"],
                "middle_name": "",
                "address3": "",
                "first_name": profile["full_name"].split(" ")[0],
                "city": profile["city"],
                "document_type_id": "",
                "district": "",
                "postal_code": profile["zip"],
                "last_name": profile["full_name"].split(" ")[1],
                "state_code": profile["state"],
                "country_code": "US",
                "business_name": ""
            },
            "selected_carrier_service_id": "Standard",
            "shipping_info": {
                "id": addressId,
                "personal_id": "",
                "tax_administration": "",
                "address1": profile["address1"],
                "phone": "+1" + profile["phone"],
                "house_number": "",
                "colony": "",
                "address2": profile["address2"],
                "middle_name": "",
                "address3": "",
                "first_name": profile["full_name"].split(" ")[0],
                "city": profile["city"],
                "document_type_id": "",
                "district": "",
                "postal_code": profile["zip"],
                "last_name": profile["full_name"].split(" ")[1],
                "state_code": profile["state"],
                "country_code": "US",
                "business_name": ""
            },
            "prefix_payment_method": profile["card_number"][0:6],
            "selected_invoice_type_id": "0",
            "event_id": eventId,
            "selected_payment_method_id": "CREDIT_CARD"
        }))
        
        if request.status_code != 200:
            task.setStatus("Error Attaching Address to Checkout!", "bad")
            
            task.setStatus("Adding Address...", "warning")
            async def addAddress():
                    request = (await session.postNoBmp('https://api.3stripes.net/gw-api/v2/user/addresses', json_data={
                            "phone": profile["phone"],
                            "city": profile["city"],
                            "state_code": profile["state"],
                            "address1": profile["address1"],
                            "address2": profile["address2"],
                            "postal_code": profile["zip"],
                            "last_name": lastName,
                            "country_code": "US",
                            "type": "SHIPPING",
                            "first_name": firstName
                        }))
                    if request.status_code == 409:
                        # fetch address
                        request = (await session.get('https://api.3stripes.net/gw-api/v2/user/addresses')).json()
                        return request["addresses"][0]
                    if str(request.status_code)[0] != "2":
                        print({
                            "phone": profile["phone"],
                            "city": profile["city"],
                            "state_code": profile["state"],
                            "address1": profile["address1"],
                            "address2": profile["address2"],
                            "postal_code": profile["zip"],
                            "last_name": lastName,
                            "country_code": "US",
                            "type": "SHIPPING",
                            "first_name": firstName
                        })
                        task.setStatus("Error Adding Address... (" + str(request.status_code) + ")", "bad")
                        raise Exception(request.text)
                    return request.json()
                
            addressId = (await addAddress())["id"]
            account["addressId"] = addressId
                # append to json file with array
            jsonData = (json.load(open('data.json')))
            for i in range(len(jsonData["accounts"])):
                    if jsonData["accounts"][i]["email"] == email:
                        jsonData["accounts"][i]["addressId"] = addressId
                        break
            with open('data.json', 'w') as outfile:
                    json.dump(jsonData, outfile, indent=4)

            task.setStatus("Attaching Address to Checkout... [2]", "warning")

            request = (await session.put(f"https://api.3stripes.net/gw-api/v2/hype/basket/{basketId}", json_data={
                "items": [
                    {
                    "product_id": sku,
                    "variation_product_id": f"{sku}_{technicalSize}",
                    "quantity": 1
                    }
                ],
                "invoice_info": {
                    "type": "0"
                },
                "selected_shipping_type_id": "home_delivery",
                "billing_info": {
                    "id": addressId,
                    "personal_id": "",
                    "tax_administration": "",
                    "address1": profile["address1"],
                    "phone": "+1" + profile["phone"],
                    "house_number": "",
                    "colony": "",
                    "address2": profile["address2"],
                    "middle_name": "",
                    "address3": "",
                    "first_name": profile["full_name"].split(" ")[0],
                    "city": profile["city"],
                    "document_type_id": "",
                    "district": "",
                    "postal_code": profile["zip"],
                    "last_name": profile["full_name"].split(" ")[1],
                    "state_code": profile["state"],
                    "country_code": "US",
                    "business_name": ""
                },
                "selected_carrier_service_id": "Standard",
                "shipping_info": {
                    "id": addressId,
                    "personal_id": "",
                    "tax_administration": "",
                    "address1": profile["address1"],
                    "phone": "+1" + profile["phone"],
                    "house_number": "",
                    "colony": "",
                    "address2": profile["address2"],
                    "middle_name": "",
                    "address3": "",
                    "first_name": profile["full_name"].split(" ")[0],
                    "city": profile["city"],
                    "document_type_id": "",
                    "district": "",
                    "postal_code": profile["zip"],
                    "last_name": profile["full_name"].split(" ")[1],
                    "state_code": profile["state"],
                    "country_code": "US",
                    "business_name": ""
                },
                "prefix_payment_method": profile["card_number"][0:6],
                "selected_invoice_type_id": "0",
                "event_id": eventId,
                "selected_payment_method_id": "CREDIT_CARD"
            }))
            if request.status_code != 200:
                task.setStatus("Error Attaching Address to Checkout!", "bad")
                return

        
        totalPrice = request.json()["total_price"]
        
        
        
        task.setStatus("Encrypting Card...", "warning")
        
        encrypter = Purchase()
        encryptedCard = encrypter.encryptAdyen(profile["full_name"], profile["card_number"], profile["card_cvv"], profile["card_exp_month"], profile["card_exp_year"])
        
        task.setStatus("Submitting Draw Entry...", "warning")

        drawJson = {
            "items": [
                {
                    "product_id": sku,
                    "variation_product_id": f"{sku}_{technicalSize}",
                    "quantity": 1
                    }
            ],
            "invoice_info": {
                "type": "0"
            },
            "selected_shipping_type_id": "home_delivery",
            "billing_info": {
                    "id": addressId,
                    "personal_id": "",
                    "tax_administration": "",
                    "address1": profile["address1"],
                    "phone": "+1" + profile["phone"],
                    "house_number": "",
                    "colony": "",
                    "address2": profile["address2"],
                    "middle_name": "",
                    "address3": "",
                    "first_name": profile["full_name"].split(" ")[0],
                    "city": profile["city"],
                    "document_type_id": "",
                    "district": "",
                    "postal_code": profile["zip"],
                    "last_name": profile["full_name"].split(" ")[1],
                    "state_code": profile["state"],
                    "country_code": "US",
                    "business_name": ""
                },
            "selected_carrier_service_id": "Standard",
            "shipping_info": {
                    "id": addressId,
                    "personal_id": "",
                    "tax_administration": "",
                    "address1": profile["address1"],
                    "phone": "+1" + profile["phone"],
                    "house_number": "",
                    "colony": "",
                    "address2": profile["address2"],
                    "middle_name": "",
                    "address3": "",
                    "first_name": profile["full_name"].split(" ")[0],
                    "city": profile["city"],
                    "document_type_id": "",
                    "district": "",
                    "postal_code": profile["zip"],
                    "last_name": profile["full_name"].split(" ")[1],
                    "state_code": profile["state"],
                    "country_code": "US",
                    "business_name": ""
                },
            "prefix_payment_method": profile["card_number"][0:6],
            "selected_invoice_type_id": "0",
            "event_id": eventId,
            "payment_info": {
                "amount": totalPrice,
                "payment_card_encrypted": encryptedCard,
                "payment_card_type": "master",
                "event_id": eventId,
                "save_payment_card": False,
                "currency": "USD",
                "payment_method_id": "CREDIT_CARD"
            },
            "selected_payment_method_id": "CREDIT_CARD"
        }

        request = (await session.post(f"https://api.3stripes.net/gw-api/v2/hype/basket/{basketId}/order", json_data=drawJson))
        while str(request.status_code)[0] == "5":
                task.setStatus("Error Submitting Draw Entry [Server Error]! Retrying...", "bad")
                request = (await session.post(f"https://api.3stripes.net/gw-api/v2/hype/basket/{basketId}/order", json_data=drawJson))


        if '"is_3d_secure":true' in request.text:
            task.setStatus("3D Secure Required, Posting to API...", "warning")

            client = httpx.AsyncClient()
            request = (await client.post("http://127.0.0.1:3000/3ds", json={
                "html": request.json()["3d_secure"]["3d_secure_base64_html"],
            }, timeout=120))

                

            task.setStatus("3D Secure Completed, Fetching Returned...", "warning")

            request = await session.getBmp(request.text)

            if "adidas-confirmed" in request.text:
                task.setStatus("Successfully Solved 3DS!", "good")
            else:
                task.setStatus("Error Solving 3DS!", "bad")


        if request.status_code != 200:
            task.setStatus("Error Submitting Draw Entry! - " + request.json()["detail"] + "-" + profile["card_number"], "bad")
            print(request.text)
            print(request.status_code)
            return

        task.setStatus("Successfully Entered Queue!", "good")
        webhook = DiscordWebhook(url='')
        embed = DiscordEmbed(title='Entered Draw', description='Your account has been entered for ' + sku + '.', color="2ecc71")
        embed.add_embed_field(name='Site', value="Adidas / Confirmed (QUEUE)", inline=False)
        embed.add_embed_field(name='Product', value=productName + f" ({size})", inline=False)
        embed.add_embed_field(name='Price', value="$" + str(totalPrice), inline=False)
        embed.add_embed_field(name='Account', value="||" + email + "||", inline=False)
        embed.add_embed_field(name='AutoJig', value="On", inline=False)

        embed.set_footer(text='FlowAIO Confirmed')
        embed.set_timestamp()
        embed.set_thumbnail(url=productImage)
        webhook.add_embed(embed)
        webhook.execute()
        
        task.setStatus("Attempting to poll queue....", "warning")

        request = (await session.get(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventId}/participations"))
        while str(request.status_code)[0] == "5":
                task.setStatus("Error Polling Queue [Server Error]! Retrying...", "bad")
                request = (await session.get(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventId}/participations"))

        request = request.json()
        queueStatus=  request["participations"][0]["status"]
        count = 0

        while True:
            count += 1
            task.setStatus("Polling Queue... " + str(count), "warning")
            if count > 100:
                task.setStatus("Polling Queue Max!", "bad")
                return
            
            request = (await session.get(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventId}/participations"))
            while str(request.status_code)[0] == "5":
                    task.setStatus("Error Polling Queue [Server Error]! Retrying...", "bad")
                    request = (await session.get(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventId}/participations"))

            request = request.json()

            newQueueStatus=  request["participations"][0]["status"]

            
            
            if newQueueStatus != queueStatus:   
                    if newQueueStatus == "ALLOCATING":
                        task.setStatus("Queue Almost Complete - Allocating Stock!","good")

                    elif queueStatus == "PAYMENT_FAILED":
                        task.setStatus("Payment Failure!", "bad")
                        webhook = DiscordWebhook(url='')
                        embed = DiscordEmbed(title="Payment Declined!", color="ff0000")
                        embed.add_embed_field(name='Site', value="Adidas / Confirmed (QUEUE)", inline=False)
                        embed.add_embed_field(name='Product', value=productName + f" ({size})", inline=False)
                        embed.add_embed_field(name='Price', value="$" + str(totalPrice), inline=False)
                        embed.add_embed_field(name='Account', value="||" + email + "||", inline=False)
                        embed.add_embed_field(name='AutoJig', value="On", inline=False)

                        embed.set_footer(text='FlowAIO Confirmed')
                        embed.set_timestamp()
                        embed.set_thumbnail(url=productImage)
                        webhook.add_embed(embed)
                        webhook.execute()
                        return
                    
                    else:
                        task.setStatus("Queue Status Changed! - " + newQueueStatus, "good")

                        webhook = DiscordWebhook(url='')
                        embed = DiscordEmbed(title='Queue Status - ' + newQueueStatus, color="2ecc71")
                        embed.add_embed_field(name='Site', value="Adidas / Confirmed (QUEUE)", inline=False)
                        embed.add_embed_field(name='Product', value=productName + f" ({size})", inline=False)
                        embed.add_embed_field(name='Price', value="$" + str(totalPrice), inline=False)
                        embed.add_embed_field(name='Account', value="||" + email + "||", inline=False)
                        embed.add_embed_field(name='AutoJig', value="On", inline=False)

                        embed.set_footer(text='FlowAIO Confirmed')
                        embed.set_timestamp()
                        embed.set_thumbnail(url=productImage)
                        webhook.add_embed(embed)
                        webhook.execute()
                        return
            else:
                task.setStatus("Queue Status Same! - " + newQueueStatus + f" [{count}]", "none")
            
            await asyncio.sleep(10)


             

    except Exception as e:
        task.setStatus("Fatal Error Entering Draw - " + str(e), "bad")
        return