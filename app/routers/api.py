# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:42 
# @Author : YD

from fastapi import APIRouter
from schemas.booking import Booking
from servers.booking import main

from extensions.json_response import resp_200


api = APIRouter()

@api.post('/booking',)
async def booking(
        data:Booking
):
   result = await main(data)
   return resp_200(data=result)