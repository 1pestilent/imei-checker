from aiohttp import ClientSession
import asyncio
import json
import os
from dotenv import load_dotenv

from app.imei.schemas import BalanceSchema, ServicesSchema

load_dotenv()

IMEI_API_KEY = os.getenv('IMEI_API_KEY')

async def get_balance():
    async with ClientSession() as session:

        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/account', headers=headers) as response:

            if response.status == 200:
                response_json: BalanceSchema = await response.json()
                return response_json


async def get_services():
    async with ClientSession() as session:
        
        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/services', headers=headers) as response:

            if response.status == 200:
                response_json: ServicesSchema = await response.json()
                return response_json

async def check_imei( device_id, service_id):
    async with ClientSession() as session:

        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
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