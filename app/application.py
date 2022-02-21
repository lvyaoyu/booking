# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:39 
# @Author : YD

from fastapi import FastAPI
from routers.api import api

app = FastAPI(
    debug=True,
    title="Game",
    version="0.0.1",
    docs_url="/v1/docs",
)

app.include_router(api,prefix='/api')

__all__ = ['app']