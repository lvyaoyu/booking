# -*- coding: utf-8 -*-
# @Time : 2021-12-15 9:41 
# @Author : YD
import typing
from fastapi.responses import JSONResponse


def resp_200(
        data: typing.Union[list, dict, str, int] = None,
        message: str = "Success",
        code: int = 200
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            'code': code,
            'message': message,
            'result': data
        }
    )


def resp_500(
        error: typing.Union[list, dict, str, int, Exception] = None,
        message: str = "Error",
        code: int = 500
) -> JSONResponse:
    if isinstance(error, Exception):
        error = error.__str__()
    return JSONResponse(
        status_code=200,
        content={
            'code': code,
            'message': message,
            'error': error
        }
    )
