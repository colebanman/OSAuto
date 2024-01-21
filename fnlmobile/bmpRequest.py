import asyncio
import random
import string
import httpx
import datetime

async def genBmp():
    client = httpx.AsyncClient(verify=False)
    
    # Implement Sensor Data
    
    return

class bmpClient:
    def __init__(self):
        self.headers = {
            'welove': 'maltliquor',
            'x-api-version': '3.0',
            'user-agent': 'Finish Line/2.7.3  (Android 13; Build/TE1A.220922.012)',
            'x-banner': 'JDSP',
            'host': 'prodmobloy2.jdsports.com',
            'connection': 'Keep-Alive',
            'content-type': 'application/json; charset=UTF-8',
        }
        # generate 10 digit random number
        strtt = ''.join(random.choices(string.digits, k=10))

        self.client = httpx.AsyncClient(proxies=httpx.Proxy("", auth=(f"", "")))
    
    async def getCaptcha(self):
        
        poster = httpx.AsyncClient()
        req = await poster.post("https://api.capsolver.com/createTask", json={
        "clientKey": "",
        "task": {
            "type": "ReCaptchaV3EnterpriseTaskProxyLess",
            "websiteURL": "https://www.finishline.com/store/product/womens-air-jordan-retro-1-elevate-low-casual-shoes/prod2846043?styleId=DH7004&colorId=006",
            "websiteKey": "6LcPD74ZAAAAAFtuJvnpIV5VjKE16Ma7oRCcENIN",
            "isInvisible": True,
            "apiDomain": "http://www.google.com/",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "cookies": []
        }})
        if "taskId" not in req.json():
            print(req.json())
        taskId = req.json()["taskId"]

        waiting = True
        while waiting:
            req =( await poster.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey":"",
                "taskId": taskId
            })).json()
            if req["status"] == "ready":
                waiting = False
            else:
                print("Polling Captcha Solve...")
                await asyncio.sleep(1)
        response = req["solution"]["gRecaptchaResponse"]

        self.headers["x-rec"] = response

    async def refreshBmp(self):
        self.headers['x-acf-sensor-data'] = await genBmp()
    async def freshRiskified(self):
        # get timestamp in ms
        timestamp = int(datetime.datetime.now().timestamp() * 1000)

        if "x-cookie" not in self.headers:
            sessionCookie = "null"
        else:
            sessionCookie = self.headers["x-cookie"]

        self.headers["riskifiedid"] = f"{sessionCookie}{timestamp}"
        self.headers["riskified-user-agent"] = self.headers["user-agent"]

    async def postBmp(self, **kwargs):
        # await self.refreshBmp()
        await self.freshRiskified()

        response = await self.client.post(kwargs["url"], headers=self.headers, json=kwargs["json"], timeout=10)

        
        
        
        count = 0
        while response.status_code == 403 or response.status_code == 499:
            print(response.text)
            count += 1
            if count > 20:
                break
            if "Item Out Of Stock" in response.text:
                return False
            if "Your transaction could not be authorized" in response.text:
                return response
            else:
                print(f"{response.status_code}  - Refreshing BMP & Retrying...")

            
            count += 1
            

            await asyncio.sleep(1)

            await self.refreshBmp()
            await self.freshRiskified()

            response = await self.client.post(kwargs["url"], headers=self.headers, json=kwargs["json"], timeout=10)
        # counter = 0
        # while "Index was out of range." in response.text:
        #     counter+=1
        #     print(f"499 Error - Retrying...")
        #     await self.refreshBmp()

        #     response = await self.client.post(kwargs["url"], headers=self.headers, json=kwargs["json"], timeout=10)
        #     if counter > 5:
        #         break

        return response
    
    async def get(self, **kwargs):
        await self.freshRiskified()

        response = await self.client.get(kwargs["url"], headers=self.headers, timeout=10)
        return response