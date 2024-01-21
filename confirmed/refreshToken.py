import asyncio
import random
import string
import json
from faker import Faker

from bmpRequest import bmpRequest

async def refresh_token(email, refreshToken, password, task):
    session = bmpRequest(None)

    await session.fetchDeviceId()

    response = (await session.postData('https://api.3stripes.net/gw-api/v2/token', "grant_type=refresh_token&refresh_token=" + refreshToken))
    if response.status_code == 401:
        task.setStatus("Invalid Refresh Token, Attempting Password...", "warning")

        response = (await session.postData('https://api.3stripes.net/gw-api/v2/token', "grant_type=password&username=" + email + "&password=" + password))
        if response.status_code == 401:
            task.setStatus("Invalid Password & Refresh!", "bad")
            return
        else:
            task.setStatus("Password Accepted!", "good")

    while str(response.status_code)[0] == "5" or str(response.status_code)[0] == "4":
        task.setStatus("Error: " + str(response.status_code) + " on login, retrying...", "bad")
        await asyncio.sleep(1)
        # await session.fetchDeviceId()
        await session.rotateProxy()
        response = (await session.postData('https://api.3stripes.net/gw-api/v2/token', "grant_type=refresh_token&refresh_token=" + refreshToken))

   
    response = (response.json())
    # open data.json, find array index of email, replace refresh token and access token, then save
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i in range(len(data["accounts"])):
            if data["accounts"][i]['email'] == email:
                data["accounts"][i]['refreshToken'] = response['refresh_token']
                data["accounts"][i]['accessToken'] = response['access_token']
                break
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    return (response['access_token'], response['refresh_token'])