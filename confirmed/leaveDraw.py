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

async def leave_draw(account, profile, sku, size, delay):
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
                
                # addressId = (await addAddress())["id"]
                # account["addressId"] = addressId
                # # append to json file with array
                # jsonData = (json.load(open('data.json')))
                # for i in range(len(jsonData["accounts"])):
                #     if jsonData["accounts"][i]["email"] == email:
                #         jsonData["accounts"][i]["addressId"] = addressId
                #         break
                # with open('data.json', 'w') as outfile:
                #     json.dump(jsonData, outfile, indent=4)
        else:
            addressId = account["addressId"]

        task.setStatus("Fetching Product...", "none")

        request = (await session.get(f"https://api.3stripes.net/gw-api/v2/trilogy/products/{sku}?experiment_product_data=false")).json()

        productImage = request['_links']['image_large']['href']
        productName = request['product_name'] + " - " + request['color_name']
        productPrice = request['original_price']
        eventId = request['hype_event']['event_id']

        task.setStatus("Fetching Draw Parameters...", "none")

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
        
        task.setStatus("Getting Draw Status...", "none")

        response = await session.getBmp(
            f'https://api.3stripes.net/gw-api/v2/hype/events/{eventId}/participations',
        )

        if response.status_code == 404:
            task.setStatus("Not Entered Before!", "bad")
            return
        
        reqJson = response.json()
        if "participations" not in reqJson:
            task.setStatus("Not Entered Before!", "bad")
            return
        if len(reqJson["participations"]) == 0:
            task.setStatus("Not Entered Before!", "bad")
            return
        
        # print(reqJson["participations"][0]["status"] + " - " +str(reqJson["participations"][0]["progress"]))
        
        productId = reqJson["participations"][0]["product_id"]
        eventIdNew = reqJson["participations"][0]["event_id"]
        
        task.setStatus("Leaving Draw...", "warning")

        response = await session.delete(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventIdNew}/participation/{productId}")
        while response.status_code == 401 or response.status_code == 403:
            task.setStatus("Akamai Error - Retrying...", "warning")
            await session.rotateProxy()
            response = await session.delete(f"https://api.3stripes.net/gw-api/v2/hype/events/{eventIdNew}/participation/{productId}")
            await asyncio.sleep(2)
       
        if response.status_code != 204:
            task.setStatus(f"Unable to Leave Draw - {response.text}", "bad")
            return
        else:
            task.setStatus("Left Draw!", "good")
            return



        
    except Exception as e:
        task.setStatus("Fatal Error Entering Draw - " + str(e), "bad")
        return