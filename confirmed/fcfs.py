import asyncio
import random
import string
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from faker import Faker

from bmpRequest import bmpRequest
from refreshToken import refresh_token
from task import Task

async def fcfs_release(account, profile, sku, size):
    email = account["email"]
    password = account["password"]
    firstName = account["first_name"]
    lastName = account["last_name"]

    task = Task("fcfs_release")

    try:

        task.setStatus("Starting FCFS Release...", "none")

        task.setStatus("Refreshing Account Token...", "warning")
        refreshToken = account["refreshToken"]
        refreshAccount = (await refresh_token(email, refreshToken, password, task))

        accessToken = refreshAccount[0]

        task.setStatus("Fetching Session...", "none")

        session = bmpRequest(accessToken)
        await session.fetchDeviceId()
        await asyncio.sleep(0.25)
        

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
        productName = request['product_name']

        task.setStatus("Fetching Cart Parameters...", "none")

        request = (await session.get(f"https://api.3stripes.net/gw-api/v2/products/{sku}/availability?experiment_product_data=false")).json()
        
        technicalSize = None

        for variation in request['_embedded']['variations']:
            if variation['size'] == size:
                technicalSize = variation['technical_size']
                if variation['orderable'] == False:
                    task.setStatus("Size Not Orderable...", "bad")
                    return
                break

        if technicalSize == None:
            task.setStatus("Size Not Found - " + size, "bad")
            return
        
        task.setStatus("Adding FCFS Product to Cart...", "warning")

        request = (await session.post('https://api.3stripes.net/gw-api/v2/checkouts', json_data={
            'items': [
                {
                    'product_id': sku,
                    'variation_product_id': f"{sku}_{technicalSize}",
                    'quantity': 1,
                },
            ],
        }, 
        ))

        if request.status_code == 400:
            task.setStatus("Product not Available...", "bad")
            return
        if str(request.status_code)[0] != "2":
            task.setStatus("Error Adding to Cart... (" + str(request.status_code) + ")", "bad")
            raise Exception(request.json()['title'])            
        cartJson = request.json()
        cartId = cartJson['id']
        
        task.setStatus("Attaching Address to Checkout...", "none")

        request = (await session.put("https://api.3stripes.net/gw-api/v2/checkouts/" + cartId + "/delivery_options/home/location", json_data={
            "location_id": addressId
        })).json()

        shippingMethodId = request["selected"]["delivery"]["lines"][0]["shipping_method"]["id"]
        estimatedDeliveryDate = request["selected"]["delivery"]["lines"][0]["shipping_method"]["delivery_time"]["availability"]
        totalPrice = request["order_summary"]["total_price"]["value"]

        task.setStatus("Selecting Payment Method...", "none")
        
        request = (await session.put("https://api.3stripes.net/gw-api/v2/checkouts/" + cartId + "/payment_method", json_data={
            'id': 'CREDIT_CARD',
        }))

        task.setStatus("Fetching Payment Token...", "none")

        request = (await session.post("https://api.3stripes.net/gw-api/v2/orders/payments", json_data={
            "checkout_id": cartId
        })).json()

        paymentId = request["payment"]["id"]
        orderId = request["order_number"]

        task.setStatus("Submitting Payment...", "warning")

        request = (await session.getPayment(checkoutId=paymentId, cvv=profile["card_cvv"], month=profile["card_exp_month"], year=profile["card_exp_year"], holder=(firstName + " " + lastName), number=profile["card_number"]))

        task.setStatus("Payment Processing...", "good")
        request = (await session.patch("https://api.3stripes.net/gw-api/v2/orders/" + orderId + "/confirmation", json_data={
            "checkout_id": cartId
        }))
        
        if request.status_code == 200:
            task.setStatus("Checkout Success!", "good")
            # create webhook
            webhook = DiscordWebhook(url='')
            embed = DiscordEmbed(title='Successful Checkout!', description='Checkout Success', color="2ecc71")
            embed.add_embed_field(name='Site', value="Adidas / Confirmed (FCFS)", inline=False)
            embed.add_embed_field(name='Product', value=productName + f" ({size})", inline=False)
            embed.add_embed_field(name='Price', value="$" + str(totalPrice), inline=False)
            embed.add_embed_field(name='Order Number', value=orderId, inline=True)
            embed.add_embed_field(name='Estimated Delivery Date', value=estimatedDeliveryDate, inline=True)
            embed.add_embed_field(name='Account', value="||" + email + "||", inline=False)
            embed.set_footer(text='FlowAIO Confirmed')
            embed.set_timestamp()
            embed.set_thumbnail(url=productImage)
            webhook.add_embed(embed)
            webhook.execute()
            return
        elif request.status_code == 403:
            task.setStatus("Payment Declined!", "bad")
            webhook = DiscordWebhook(url='')
            embed = DiscordEmbed(title='Payment Declined', color="FF0000")
            embed.add_embed_field(name='Site', value="Adidas / Confirmed (FCFS)", inline=False)
            embed.add_embed_field(name='Product', value=productName + f" ({size})", inline=False)
            embed.add_embed_field(name='Price', value="$" + str(totalPrice), inline=False)
            embed.add_embed_field(name='Order Number', value=orderId, inline=True)
            embed.add_embed_field(name='Estimated Delivery Date', value=estimatedDeliveryDate, inline=True)
            embed.add_embed_field(name='Account', value="||" + email + "||", inline=False)

            embed.set_footer(text='FlowAIO Confirmed')
            embed.set_timestamp()
            embed.set_thumbnail(url=productImage)
            webhook.add_embed(embed)
            webhook.execute()
            return
        else:
            task.setStatus("Unknown bad on Submit!", "warning")
            return
    except Exception as e:
        task.setStatus("FATAL ERROR - " + str(e), "bad")
        return
            
