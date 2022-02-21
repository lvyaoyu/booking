# -*- coding: utf-8 -*-
# @Time : 2021-12-14 17:10 
# @Author : YD

from pydantic import BaseSettings


class Settings(BaseSettings):
    max_workers = 10


settings = Settings()
