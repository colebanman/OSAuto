import asyncio
import random
import string
import json
from faker import Faker
from task  import Task

from bmpRequest import bmpRequest

async def generate_account():
        catchall = "gmail.com"
        faker = Faker()
        session = bmpRequest(None)

        task = Task("generateAccount")

        await session.fetchDeviceId()
        await session.rotateProxy()
        
        firstName = faker.first_name()
        lastName = faker.last_name()

        endChars = ''.join(random.choice(string.ascii_letters) for i in range(10))

        
        # create random email
        email = firstName + lastName + endChars + '@' + catchall

        # create random password
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + 'A1!'

        
        createdAccount = False
        while not createdAccount:
            try:
                task.setStatus("Creating Account...", "none")
                user = (await session.post('https://api.3stripes.net/gw-api/v2/user', json_data={
                    'email': email,
                    'password': password,
                    'membership_consent': True,
                    'dormant_period': '1y',
                })).json()

                userId = user['id']
                accessToken = user['access_token']
                refreshToken = user['refresh_token']

                task.setStatus("Verifying Account...", "none")

                newSession = bmpRequest(accessToken)

                second = (await newSession.get("https://api.3stripes.net/gw-api/v2/hype/user")).json()
                if second["isVerified"] == False:
                    task.setStatus("Account Not Verified! Retrying...", "bad")
                    await asyncio.sleep(0.5)
                    continue

                createdAccount = True
            except:
                task.setStatus("Error Creating Account! Retrying...", "bad")
                await asyncio.sleep(0.5)

        # append to json file with array
        jsonData = (json.load(open('data.json')))
        jsonData["accounts"].append({
            "email": email,
            "password": password,
            "userId": userId,
            "accessToken": accessToken,
            "refreshToken": refreshToken,
            'first_name': firstName,
            'last_name': lastName
        })
        with open('data.json', 'w') as outfile:
            # json dump formatted
            json.dump(jsonData, outfile, indent=4)
        task.setStatus("Created Account!", "good")
