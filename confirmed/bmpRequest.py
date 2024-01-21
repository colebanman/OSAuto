import httpx
import json
import requests
import asyncio
import random
import tls_client

class bmpRequest():
    # constructor
    authToken = None

    random10DigitNum = str(random.randint(1000000000, 9999999999))

    proxy = f""
    split = proxy.split(':')
    proxy = httpx.Proxy(
        f"http://{split[0]}:{split[1]}", auth=(split[2], split[3]))

    deviceId = '26daeadc-cd7d-4d4e-b2d8-8f0a8506aa3e'


    

    def __init__(self, authToken):
        self.authToken = authToken

    async def rotateProxy(self):
        random10DigitNum = str(random.randint(1000000000, 9999999999))
        baseIsp = f""
        splitProxy = baseIsp.split(':')
        self.proxy = httpx.Proxy(
            f"http://{splitProxy[0]}:{splitProxy[1]}", auth=(splitProxy[2], splitProxy[3])
        )
        return True

    async def fetchDeviceId(self):
        async with httpx.AsyncClient(verify=False) as client:
            # implement get device id
            return

    async def genBmp(self):
        success = False
        while not success:
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    #implement 
                    bmpSolution = ""
                    return bmpSolution
            except Exception as e:
                pass
    async def post(self, url, json_data):
        error = True
        while error:
            bmpToken = await self.genBmp()
            headers = {
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'accept-language': 'en-US',
                'accept': 'application/hal+json',
                'x-acf-sensor-data': bmpToken,
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'host': 'api.3stripes.net',
                'connection': 'Keep-Alive',
                'content-type': 'application/json',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.post(url, headers=headers, json=json_data, timeout=15)
                    if response.status_code == 401 or response.status_code == 500:
                        
                        await self.rotateProxy()
                        await self.fetchDeviceId()
                        await self.genBmp()
                        continue
                    return response
            except Exception as e:
                deviceId = await self.fetchDeviceId()
                await self.rotateProxy()
                self.deviceId = deviceId
                
                print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                pass
    async def postSpecial2(self, url, json_data):
        error = True
        while error:
            bmpToken = await self.genBmp()
            headers = {
                'Host': 'api.3stripes.net',
                'Connection': 'keep-alive',
                'x-market': 'US',
                'Accept-Language': 'en-US',
                'X-acf-sensor-data': bmpToken,
                'Accept': 'application/hal+json',
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'Content-Type': 'application/json; charset=UTF-8',
                # 'Cookie': 'akacd_api_3stripes=3864239198~rv=6~id=076c97493534f1e7672b31701b4a96c8',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.post(url, headers=headers, json=json_data, timeout=15)
                    if response.status_code == 401 or response.status_code == 500:
                        await self.rotateProxy()
                        await self.fetchDeviceId()
                        await self.genBmp()
                        continue
                    return response
            except Exception as e:
                deviceId = await self.fetchDeviceId()
                await self.rotateProxy()
                self.deviceId = deviceId
                
                print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                pass
    async def patch(self, url, json_data):
        error = True
        while error:
            bmpToken = await self.genBmp()
            headers = {
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'accept-language': 'en-US',
                'accept': 'application/hal+json',
                'x-acf-sensor-data': bmpToken,
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'host': 'api.3stripes.net',
                'connection': 'Keep-Alive',
                'content-type': 'application/json',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.patch(url, headers=headers, json=json_data, timeout=15)
                    if response.status_code == 401 or response.status_code == 500:
                        await self.rotateProxy()
                        await self.fetchDeviceId()
                        await self.genBmp()
                        continue
                    return response
            except Exception as e:
                deviceId = await self.fetchDeviceId()
                self.deviceId = deviceId
                await self.rotateProxy()

                print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                pass
    async def put(self, url, json_data):
            error = True
            while error:
                bmpToken = await self.genBmp()
                headers = {
                    'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                    'accept-language': 'en-US',
                    'accept': 'application/hal+json',
                    'x-acf-sensor-data': bmpToken,
                    'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                    'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                    'x-app-info': 'platform/Android version/4.23.0',
                    'host': 'api.3stripes.net',
                    'connection': 'Keep-Alive',
                    'content-type': 'application/json',
                }
                # if authToken is not None add to headersa
                if self.authToken is not None:
                    headers['authorization'] = "Bearer " + self.authToken
                try:
                    async with httpx.AsyncClient(proxies=self.proxy) as client:
                        response = await client.put(url, headers=headers, json=json_data, timeout=15)
                        if response.status_code == 401 or response.status_code == 500:
                            await self.rotateProxy()
                            await self.fetchDeviceId()
                            await self.genBmp()
                            continue
                        return response
                except Exception as e:
                    deviceId = await self.fetchDeviceId()
                    await self.rotateProxy()
                    self.deviceId = deviceId
                    print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                    pass
    async def postData(self, url, data):
        error = True
        while error:
            bmpToken = await self.genBmp()
            headers = {
                'host': "api.3stripes.net",
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'connection': "keep-alive",
                'x-signature': self.deviceId,
                'x-market': "US",
                'accept-language': "en-US",
                'x-acf-sensor-data': bmpToken,
                'accept': "application/hal+json",
                'x-api-key': "qbSxC4cM5zqtyJ14pPIKZQFN",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
            }
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.post(url, headers=headers, data=data, timeout=15)
                    if response.status_code == 401 or response.status_code == 500:
                        await self.rotateProxy()
                        await self.fetchDeviceId()
                        await self.genBmp()
                        continue
                    
                    return response
            except Exception as e:
                deviceId = await self.fetchDeviceId()
                self.deviceId = deviceId
                await self.rotateProxy()

                print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                pass
    async def postNoBmp(self, url, json_data):
        error = True
        while error:
            headers = {
                'host': "api.3stripes.net",
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'connection': "keep-alive",
                'x-signature': self.deviceId,
                'x-market': "US",
                'accept-language': "en-US",
                'accept': "application/hal+json",
                'x-api-key': "qbSxC4cM5zqtyJ14pPIKZQFN",
            }
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.post(url, headers=headers, json=json_data, timeout=15)
                    return response
            except Exception as e:
                deviceId = await self.fetchDeviceId()
                self.deviceId = deviceId
                await self.rotateProxy()
                print("Akamai BMP Error, Switching to Device " + self.deviceId + ". " + str(e))
                pass

    async def get(self, url):
        error = True
        while error:
            headers = {
                'host': 'api.3stripes.net',
                'accept': 'application/hal+json',
                'x-device-info': 'app/CONFIRMED; os/iOS; os-version/16.5; app-version/4.23.0; buildnumber/2023.5.15.18.52; type/iPhone14,5; fingerprint/' + self.deviceId,
                'x-market': 'US',
                'x-pdata-cache': '-1634373788',
                'accept-language': 'en-US',
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'x-feed-cache': '-1634373788',
                'x-product-cache': '1535',
                'user-agent': 'CONFIRMED/2023.5.15.18.52 CFNetwork/1408.0.4 Darwin/22.5.0',
                'connection': 'keep-alive',
                'x-app-info': 'platform/iOS version/4.23.0',
                # 'cookie': 'akacd_api_3stripes=3862501431~rv=43~id=5acb8ebf0171d472534852a5b7028161',
                'content-type': 'application/x-www-form-urlencoded',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            # if specialHeaders is not None add to headers
            try:
                async with httpx.AsyncClient(proxies=self.proxy, follow_redirects=True) as client:
                    response = await client.get(url, headers=headers, timeout=10)
                    return response
            except Exception as e:
                print('Post Error - ' + url + " - " + str(e))
                pass

    async def getBmp(self, url):
        error = True
        while error:
            bmpToken = await self.genBmp()
            headers =  {
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'accept-language': 'en-US',
                'accept': 'application/hal+json',
                'x-acf-sensor-data': bmpToken,
                'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + self.deviceId,
                'x-app-info': 'platform/Android version/4.23.0',
                'host': 'api.3stripes.net',
                'connection': 'Keep-Alive',
                'content-type': 'application/json',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " + self.authToken
            # if specialHeaders is not None add to headers
            try:
                async with httpx.AsyncClient(proxies=self.proxy, follow_redirects=True) as client:
                    response = await client.get(url, headers=headers, timeout=10)
                    return response
            except Exception as e:
                print('Post Error - ' + url + " - " + str(e))
                await self.rotateProxy()
                await self.fetchDeviceId()
                pass

    async def getSpecial(self, url):
        error = True
        while error:
            headers = headers = {
                'Host': 'api.3stripes.net',
                'x-device-info': 'app/adidas; os/iOS; os-version/16.5; app-version/5.24.2; buildnumber/2023.5.23.19.12; type/iPhone14,5; fingerprint/null',
                'x-market': 'US',
                'x-signature': '6EBF666997C683BB240538631A05FCAFCC64B4EC85361B88C793554B5F07D2A3',
                'Accept-Language': 'en-US',
                'x-api-key': 'm79qyapn2kbucuv96ednvh22',
                'Accept': 'application/hal+json',
                'User-Agent': 'adidas/2023.5.23.19.12 CFNetwork/1408.0.4 Darwin/22.5.0',
                'Connection': 'keep-alive',
                'x-app-info': 'platform/iOS version/5.24.2',
                # 'Cookie': 'GCLB=CKe70KO206m-uQE; akacd_api_3stripes=3864250738~rv=10~id=fe072cde51b196922271198986dcd710',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] ="Bearer " +  self.authToken
            # if specialHeaders is not None add to headers
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.get(url, headers=headers, timeout=10)
                    return response
            except Exception as e:
                print('Post Error - ' + url + " - " + str(e))
                pass
    async def delete(self, url):
        error = True
        while error:
            headers = {
                'host': 'api.3stripes.net',
                'accept': 'application/hal+json',
                'x-app-info': 'platform/iOS version/5.24.2',
                'x-market': 'US',
                'accept-language': 'en-US',
                'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
                'user-agent': 'CONFIRMED/2023.7.26.15.5 CFNetwork/1408.0.4 Darwin/22.5.0',
                'x-app-info': 'platform/iOS version/4.27.0',
                'content-type': 'application/x-www-form-urlencoded',
            }
            # if authToken is not None add to headersa
            if self.authToken is not None:
                headers['authorization'] = "Bearer " +  self.authToken
            # if specialHeaders is not None add to headers
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.delete(url, headers=headers, timeout=10)
                    return response
            except Exception as e:
                print('Delete Error - ' + url + " - " + str(e))
                pass

    async def getPayment(self, checkoutId, cvv, month, year, holder, number):
        headers = {
            'Host': 'oppwa.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'User-Agent': 'confirmed/4.23.0 (iPhone; iOS 16.5; Scale/3.00)',
            'Accept-Language': 'en-US;q=1, ja-US;q=0.9',
            # 'Content-Length': '413',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'bm_sv=50B9AE13AB699A37791F6975EA3A83AC~YAAQGi0+F2tcWcGIAQAAvldOxRTkWvhatz6yGOmU9+6OLd4XwJRz35/AGS2No/Jc1u3AfzYLwmVe3Ba3k1Swtp5H+zNRqOi8zczSWHqLavF/P/0tzHdKK687pALEMGLtB1jlBye9/D5kVMf9fzgWpHicNgVh8YAHCLy/vrFDdjafUT8wzHTAsUZbkP5PLKtBqiiI8ypl+JuX9hokmnSPEz5y40i3gUbtepP0DtL1p/x20U/3pYbp7AnNXP17xHIK~1; ak_bmsc=172055219D8454EAAB517FD7B21C61CE~000000000000000000000000000000~YAAQFy0+F3EqGr6IAQAAegIWxRQGtjLf5FcsgUwKfRTScBdoZ2f+OpPTm7ZhyXg39pxo67jfD4uydw+rP78EuxnVXLojJ1lpGwlaMRfGvRovMjWSMjBf7/QLoJQstAqo1fNvE5VmOCdnON+rItG5iSv6P4N2Es4+LgDlURMJV7P3dYfHPvEVu/NSKJN5DMEti3h30L1rC4jHl2cB5VS4q+HX4odpaYhZD8bxVUfy10koElRFEIr0rZNRlHk+OQZEqhKVzHUPhEaPKnwnydgIcWYW4DjyQqvsRb6CI9djJ4DTS6Sn8brrE8gss9RxV/UxfvtMgDdglsXi/wZSBnX/87RwWaEfUHFLR0uparJOKEEvogq+rBuJaqZlN9RG47YgmN1pO5Ijw87Nspx26Y/kfYIEA/mrEsA=',
        }
        data = 'card.cvv=' + cvv + '&card.expiryMonth=' + month + '&card.expiryYear=' + year + '&card.holder=' + holder + '&card.number=' + number + '&customParameters%5BSHOPPER_MSDKIntegrationType%5D=Custom&customParameters%5BSHOPPER_MSDKVersion%5D=4.7.0&customParameters%5BSHOPPER_OS%5D=iOS%2016.5&customParameters%5BSHOPPER_device%5D=iPhone14%2C5&paymentBrand=MASTER&shopperResultUrl=adidas-confirmed%3A//payment&source=MSDK&threeDSecure.mobileFlow=app'
        
        url = 'https://oppwa.com/v1/checkouts/' + checkoutId + '/payment'

        async with httpx.AsyncClient(proxies=self.proxy) as client:
            response = await client.post(url, headers=headers, data=data, timeout=10)
            return response