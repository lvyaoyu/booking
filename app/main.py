# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:21 
# @Author : YD

import uvicorn
from uvicorn import Server, Config
from application import app

if __name__ == '__main__':
    # uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=True, debug=True)

    import asyncio
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    cfg = Config(app=app,port=8080,loop=loop)
    server = Server(cfg)
    loop.run_until_complete(server.serve())