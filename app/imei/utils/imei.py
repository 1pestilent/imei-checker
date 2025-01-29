from aiohttp import ClientSession
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('IMEI_API_KEY')

async def get_balance(token):
    async with ClientSession() as session:

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/account', headers=headers) as response:

            if response.status == 200:
                response_json = await response.json()
                return response_json['balance']


async def get_services(token):
    async with ClientSession() as session:
        
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/services', headers=headers) as response:

            if response.status == 200:
                response_json = await response.json()
                return response_json

async def check_imei(token, device_id, service_id):
    async with ClientSession() as session:

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        body = json.dumps({
            "deviceId": device_id,
            "serviceId": service_id
        })

        async with session.post(url='https://api.imeicheck.net/v1/checks', headers=headers, data = body) as response:
            

            if response.status == 200:
                response_json = await response.json()
                return response_json

asyncio.run(check_imei(token=token, device_id='356735111052198', service_id='1')) 