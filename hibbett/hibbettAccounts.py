import httpx
import json
from faker import Faker
import string
import random


async def createAccount(session:httpx.AsyncClient):
    catchall = "gmail.com"

    fake = Faker()
    firstName = fake.first_name()
    lastName = fake.last_name()
    email = (firstName + lastName + "@" + catchall).lower()
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + "asds!123"

    params = ''

    json_data = {
        'lastName': lastName,
        'subscribeToEmail': False,
        'phone': f"925651{random.randint(1000, 9999)}",
        'agreeToTerms': True,
        'login': email,
        'firstName': firstName,
        'password': password,
        'email': email,
    }

    print("Creating Account... - " + email + " - " + password + " - " + json_data["phone"] + " - " + json_data["firstName"] + " " + json_data["lastName"])

    response = (await session.post(
        'https://hibbett-mobileapi.prolific.io/users/register',
        json=json_data
    )).json()

    if "code" in response:
        print("Error Creating Account! - " + response["message"])
        return False
    
    print("Account Created!")

    with open("data.json", "r") as f:
        accounts = json.load(f)

    response["password"] = password

    accounts["accounts"].append(response)

    with open("data.json", "w") as f:
        json.dump(accounts, f, indent=4)

    return response