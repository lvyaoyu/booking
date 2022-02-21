# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:42 
# @Author : YD

from fastapi import APIRouter
from schemas.booking import Booking
from servers.booking import get_dc,main


api = APIRouter()

@api.post('/booking',)
async def booking(
        data:Booking
):
   return await main(data)