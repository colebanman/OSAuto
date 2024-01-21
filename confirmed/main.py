import time
import httpx
import asyncio
import random
import string
import json
import pick
from faker import Faker

from generateAccount import generate_account
from refreshToken import refresh_token
from enterDraw import enter_draw
from bmpRequest import bmpRequest
from fcfs import fcfs_release
from task import Task
from leaveDraw import leave_draw
from queueMode import queue_mode

import csv

# ----------------------------------------------
sku = "ID4289"
size = "9"
# ----------------------------------------------

proxy = ""
split = proxy.split(':')
proxy = httpx.Proxy(f"http://{split[0]}:{split[1]}", auth=(split[2], split[3]))


# asyncio.run(main())

title = ("""
----------------------------------------------------------------------------------------------------                                                           
    ,---,. ,--,                           ,---,                        
  ,'  .' ,--.'|                          '  .' \       ,--,            
,---.'   |  | :     ,---.          .---./  ;    '.   ,--.'|    ,---.   
|   |   .:  : '    '   ,'\        /. ./:  :       \  |  |,    '   ,'\  
:   :  : |  ' |   /   /   |    .-'-. ' :  |   /\   \ `--'_   /   /   | 
:   |  |-'  | |  .   ; ,. :   /___/ \: |  :  ' ;.   :,' ,'| .   ; ,. : 
|   :  ;/|  | :  '   | |: :.-'.. '   ' |  |  ;/  \   '  | | '   | |: : 
|   |   .'  : |__'   | .; /___/ \:     '  :  | \  \ ,|  | : '   | .; : 
'   :  ' |  | '.'|   :    .   \  ' .\  |  |  '  '--' '  : |_|   :    | 
|   |  | ;  :    ;\   \  / \   \   ' \ |  :  :       |  | '.'\   \  /  
|   :  \ |  ,   /  `----'   \   \  |--"|  | ,'       ;  :    ;`----'   
|   | ,'  ---`-'             \   \ |   `--''         |  ,   /          
`----'                        '---"                   ---`-'           
----------------------------------------------------------------------------------------------------       

Welcome to FlowAIO CLI v1.0.0 - please choose from an option below.
""")

options = [ "- GENERATE ACCOUNTS", "- CONFIRMED DRAW", "- CONFIRMED QUEUE", "- CONFIRMED FCFS", "- LEAVE DRAW"]
option, index = pick.pick(options, title, indicator='=>', default_index=0)

PURPLE = '\033[35m'

# ANSI escape code for italic text
ITALIC = '\033[3m'

# ANSI escape code to reset text formatting
RESET = '\033[0m'

with open('data.json', 'r') as f:
                data = json.load(f)
                length = len(data["accounts"])
                print(f"{length} ACCOUNTS LOADED FROM DATA")

# Text to print
text = "ENTER MAX TASKS: "

# Construct the formatted text
formatted_text = f"{PURPLE}{ITALIC}{text}{RESET}"

# Print the formatted text

maxTasks = int(input(formatted_text))

text = "ENTER TASK START PLACE (ACCOUNT INDEX): "

# Construct the formatted text
formatted_text = f"{PURPLE}{ITALIC}{text}{RESET}"

# Print the formatted text

startPlace = int(input(formatted_text))


if option == "- GENERATE ACCOUNTS":
    async def main():
        await asyncio.gather(*[generate_account() for i in range(maxTasks)])

else:
    with open('data.json', 'r') as f:
        data = json.load(f)
        sku = data["sku"]
        sizes = data["sizes"]

    async def handleFatalError(func):
        try:
            func()
        except Exception as e:
            print("FATAL ERROR")

    if option == "- CONFIRMED DRAW": 
        cards = []
        with open('cards.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cards.append(row)

        async def main():
            tasks = []
            with open('data.json', 'r') as f:
                data = json.load(f)

                # get delay to make it enter all accounts within 30 seconds, based on length of accounts and maxTasks

                started = 0

                for i in range(maxTasks):
                    if (len(data["accounts"]) < i+1):
                        break
                    
                    if i < startPlace:
                        # print(f"Skipping Account {i} [{data['accounts'][i]['email']}")
                        continue
                    
                    account = data["accounts"][i]
                    profile = random.choice(data["profiles"])

                    newProfile = profile.copy()

                    newProfile["card_number"] = cards[i]["Card Number"]
                    newProfile["card_cvv"] = cards[i]["CVV"]
                    newProfile["card_exp_month"] = cards[i]["Expiration Month"]
                    newProfile["card_exp_year"] = cards[i]["Expiration Year"]

                    # print(f"Starting Account {i} [{account['email']}] - card {cards[i]['Card Number']}")

                    tasks.append(enter_draw(account, newProfile, sku, random.choice(sizes), 0))
                    started += 1

            await asyncio.gather(*tasks)
    if option == "- CONFIRMED QUEUE": 
            cards = []
            with open('cards.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cards.append(row)

            async def main():
                tasks = []
                with open('data.json', 'r') as f:
                    data = json.load(f)

                    # get delay to make it enter all accounts within 30 seconds, based on length of accounts and maxTasks

                    started = 0

                    for i in range(maxTasks):
                        if (len(data["accounts"]) < i+1):
                            break
                        
                        if i < startPlace:
                            # print(f"Skipping Account {i} [{data['accounts'][i]['email']}")
                            continue
                        
                        account = data["accounts"][i]
                        profile = random.choice(data["profiles"])

                        newProfile = profile.copy()

                        newProfile["card_number"] = cards[i]["Card Number"]
                        newProfile["card_cvv"] = cards[i]["CVV"]
                        newProfile["card_exp_month"] = cards[i]["Expiration Month"]
                        newProfile["card_exp_year"] = cards[i]["Expiration Year"]

                        tasks.append(queue_mode(account, newProfile, sku, random.choice(sizes), 0))
                        started += 1

                await asyncio.gather(*tasks)
    if option == "- LEAVE DRAW": 
        cards = []
        with open('cards.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cards.append(row)

        async def main():
            tasks = []
            with open('data.json', 'r') as f:
                data = json.load(f)

                # get delay to make it enter all accounts within 30 seconds, based on length of accounts and maxTasks

                started = 0

                for i in range(maxTasks):
                    if (len(data["accounts"]) < i+1):
                        break
                    
                    if i < startPlace:
                        # print(f"Skipping Account {i} [{data['accounts'][i]['email']}")
                        continue
                    
                    account = data["accounts"][i]
                    profile = random.choice(data["profiles"])

                    newProfile = profile.copy()

                    newProfile["card_number"] = cards[i]["Card Number"]
                    newProfile["card_cvv"] = cards[i]["CVV"]
                    newProfile["card_exp_month"] = cards[i]["Expiration Month"]
                    newProfile["card_exp_year"] = cards[i]["Expiration Year"]

                    tasks.append(leave_draw(account, newProfile, sku, random.choice(sizes), 0))
                    started += 1

            await asyncio.gather(*tasks)

    if option == "- CONFIRMED FCFS":
        async def main():
            tasks = []
            with open('data.json', 'r') as f:
                data = json.load(f)

                for i in range(min(len(data["accounts"]), (maxTasks))):
                    account = data["accounts"][i]
                    profile = random.choice(data["profiles"])
                    tasks.append(fcfs_release(account, profile, sku, random.choice(sizes)))

            await asyncio.gather(*tasks)
                    # await enter_draw(account, profile, sku, size)

asyncio.run(main())

# load cards.csv




# error = True
# while error:
#     bmp = genBmp()
#     headers = {
#         'x-api-key': 'qbSxC4cM5zqtyJ14pPIKZQFN',
#         'accept-language': 'en-US',
#         'accept': 'application/hal+json',
#         'x-acf-sensor-data': bmp[0],
#         'user-agent': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + bmp[1],
#         'x-device-info': 'app/com.adidas.confirmed.app; os/Android; os-version/33; app-version/4.23.0; buildnumber/42300291; type/sdk_gphone64_x86_64/3.5/1440x2900; fingerprint/' + bmp[1],
#         'x-app-info': 'platform/Android version/4.23.0',
#         'host': 'api.3stripes.net',
#         'connection': 'Keep-Alive',
#         'content-type': 'application/json',
#     }

#     json_data = {
#         'email': 'myemaildwadadada3dada@gmail.com',
#         'password': 'Coco2675!!',
#         'membership_consent': True,
#         'dormant_period': '1y',
#     }
#     try:
#         response = requests.post('https://api.3stripes.net/gw-api/v2/user', headers=headers, json=json_data, timeout=3, proxies=proxies)
#         print(response.text)
#         error = False
#     except Exception as e:
#         print(e)
#         time.sleep(0.25)