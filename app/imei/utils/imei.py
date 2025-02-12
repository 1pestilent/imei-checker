from aiohttp import ClientSession, ClientResponse
from fastapi import HTTPException, status
import json
import os
from dotenv import load_dotenv

from app.imei.schemas import BalanceSchema, ServicesSchema

load_dotenv()

IMEI_API_KEY = os.getenv('IMEI_API_KEY')

async def response_handler(response: ClientResponse):

    response_json = await response.json()
    
    if response.status == 200:
        return response_json
    
    if response.status == 402:
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED,
                            detail=response_json['message'],
                            )
    
    if response.status == 404:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=response_json['message'],
                           )
    
    if response.status == 422:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=response_json['errors']['deviceId'][0],
                            )
    else:
        print(f"--- Error ---\n\n{response_json}\n\n--------------")
    


async def get_balance() -> BalanceSchema:
    async with ClientSession() as session:

        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/account', headers=headers) as response:
            return await response_handler(response)


async def get_services() -> ServicesSchema:
    async with ClientSession() as session:
        
        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
            'Content-Type': 'application/json'
        }

        async with session.get(url='https://api.imeicheck.net/v1/services', headers=headers) as response:
            return await response_handler(response)
        
async def get_service(number):
    async with ClientSession() as session:
        
        headers = {
            'Authorization': 'Bearer ' + IMEI_API_KEY,
            'Content-Type': 'application/json'
        }

        async with session.get(url=f'https://api.imeicheck.net/v1/services/{number}', headers=headers) as response:
            return await response_handler(response)


async def check_imei(service_id: int, device_id: str):
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
            return await response_handler(response)