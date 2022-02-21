# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:45 
# @Author : YD

from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Cookie(TypedDict, total=False):
    name: str
    value: str
    url: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    expires: Optional[float]
    httpOnly: Optional[bool]
    secure: Optional[bool]
    sameSite: Optional[Literal["Lax", "None", "Strict"]]


class Booking(BaseModel):
    # username: str = Field(default='klpcsegea@fhbknm.tech', description='用户名')
    # pwd: str = Field(default='dkYRyX651I', description='密码')
    cookies: List[Cookie] = Field(..., description='cookies')
    origin: str = Field(..., description='起运地')
    destination: str = Field(..., description='目的地')
    email_address: str = Field(..., description='邮件通知')
    container_number: str = Field(..., description='集装箱数量')
    container_type: str = Field(..., description='集装箱类型')
    release_date: str = Field(..., description='放行日期')
    release_time: str = Field(..., description='放行时间')
    goods_description: str = Field(..., description='货物描述')
    commodity_code: str = Field(..., description='商品编码')
    weight: str = Field(..., description='货物重量')
    unit: str = Field(..., description='货物单位')

    class Config:
        schema_extra = {
            "example": {
                'origin': 'NINGBO (CNNGB)',
                'destination': 'PIRAEUS (GRPIR)',
                'email_address': 'huangyi@hi-strong.com',
                'container_number': '1',
                'container_type': '22GP|GENERAL PURPOSE CONT.',
                'release_date': '2022-02-21',
                'release_time': '10:13',
                'goods_description': 'plush toy',
                'commodity_code': '95 90 00',
                'weight': '15000',
                'unit': 'kg',
                'cookies': [
                    {'sameSite': 'Lax', 'name': '_ga', 'value': 'GA1.2.138199767.1645088780',
                     'domain': '.hapag-lloyd.cn', 'path': '/', 'expires': 1708484265, 'httpOnly': False,
                     'secure': False}, {'sameSite': 'Lax', 'name': 'TS14ae3011_27',
                                        'value': '081ecde62cab2000a7dcd7e6812a54793666819822972d23c80b54fba3f164f56f7dac4205f92cd408af7a660d11200005b7c2f79142278b4962d426123f4423517e5b3eadf754fbc768d6d25f13e8c4',
                                        'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1,
                                        'httpOnly': False, 'secure': False},
                    {'sameSite': 'Lax', 'name': '_gid', 'value': 'GA1.2.1287214687.1645410069',
                     'domain': '.hapag-lloyd.cn', 'path': '/', 'expires': 1645498665, 'httpOnly': False,
                     'secure': False}, {'sameSite': 'Lax', 'name': 'TSd35d0af5_27',
                                        'value': '081ecde62cab200071dc9acd5ec217953f302f045fc7428ca11f01a5b15ea3b9728fe8a52bba7e7d08cc70a286112000b3f3436154dc48ea5bb0feea015f7242877265e49d4bbb3140c313d0485ced32',
                                        'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1,
                                        'httpOnly': False, 'secure': False},
                    {'sameSite': 'Lax', 'name': 'TSd35d0af5_76',
                     'value': '081ecde62cab28000965236c1228a4f1f6ec9ffa0c43aad1d2c87ff20909b82d9f6af7fb3a876efdeecd8a067b5afd2f0812a7de4709e8008b7cb81398b49543b268cd871d85ceaa84b681560942b16613ee322b2c5f816b14cfe1bc95ae6c99412adc7c7269b932a1f4f8a3aa82c4bd7d725e8bf38ab2ccea1ab010933c0e934fc2665b7735e905c00873df051a2cb6a537c2e51cc58f361f6f3cc7b2a07915337104b2bd7165a8c95cc1f271ae954eeb8fcb6334560af2f13638916bca523a1de0fe530450c656f24806d0043d36b35f3202e245b334d8dfd8e590fb4f0063677cd3acaf37bb6058046eb4746448dc5813befe83a070eae097ba81902f5be3ce6e194a25a9517ca5ca9a81535079592245c941925bd64d0dba1b4b336ef229',
                     'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': 1645419450, 'httpOnly': False,
                     'secure': False}, {'sameSite': 'Lax', 'name': 'TSPD_101',
                                        'value': '081ecde62cab28000965236c1228a4f1f6ec9ffa0c43aad1d2c87ff20909b82d9f6af7fb3a876efdeecd8a067b5afd2f:081ecde62cab28000965236c1228a4f1f6ec9ffa0c43aad1d2c87ff20909b82d9f6af7fb3a876efdeecd8a067b5afd2f0812a7de47063800d33057ec511cbb08319ac84cd211eb8f8d7647ce0910f4a7be0b5b9421abfa4982e647ea852aaf1a8914d20e89280aa69dc1e3f64b750fd0',
                                        'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1,
                                        'httpOnly': False, 'secure': False},
                    {'sameSite': 'None', 'name': '__cf_bm',
                     'value': 'hvVPiy0D0FwW1El5d5WYoYPEPwwaO9QmRsmbEJxVOqo-1645412252-0-AZAAFSIVw8JnoMPhvySMNR/5WgDiX3IOfndVLPOntDqlvU7gRi+c2O9oa4UOUy1XyQxOXO/r7TsuAmkUNjk9XFg=',
                     'domain': '.hapag-lloyd.cn', 'path': '/', 'expires': 1645414052.098411, 'httpOnly': True,
                     'secure': True}, {'sameSite': 'Lax', 'name': '_gat_UA-111931200-1', 'value': '1',
                                       'domain': '.hapag-lloyd.cn', 'path': '/', 'expires': 1645412312,
                                       'httpOnly': False, 'secure': False},
                    {'sameSite': 'Lax', 'name': 'JSESSIONID', 'value': '0000etJXZ-6yFXrqLPxCCwZAKjH:1b25u3trs',
                     'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1, 'httpOnly': True,
                     'secure': True}, {'sameSite': 'Lax', 'name': 'TS01a3c52a',
                                       'value': '01541c804aac69234222e22525b9b99a98c4fb50affcfdae22ae5d078343060a529dc81a3fc48b098e782a0680601a5683cc32af84b854fbef35ab660e35321326dd48e6b0a4bdb8f1414161f89842bd29dcc118e986351dd1480ff6e85a0d282891968633301e4bae9530967a7bc2df30ef925b40',
                                       'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1,
                                       'httpOnly': False, 'secure': False},
                    {'sameSite': 'Lax', 'name': 'TS88beea46_27',
                     'value': '081ecde62cab20004e31dba37676323028bb6d7a0b0d76bfaa049587f39dd9d63a0bc1fbe871e35e08c79c9bb5112000837ad2bee81f200461cbaee28ec303f6b71419fec58568b3a5ae69e88ff18d75',
                     'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1, 'httpOnly': False,
                     'secure': False}, {'sameSite': 'Lax', 'name': 'TS01a3c52a_77',
                                        'value': '081ecde62cab28008269de4b128411c516d6f7b17c9bebfea3aac5b22a003203d9cfda00468a5585de8306b50e8a61cf08608dffff824000fe893c8008dfe21e20c09601f979f2e03c5afd55d9db80fc54d92f5a56f3ed5412fa550f0f562fb4a90a324dd265cec42115739aab92be90f402411251db1388',
                                        'domain': 'www.hapag-lloyd.cn', 'path': '/', 'expires': -1,
                                        'httpOnly': False, 'secure': False}
                ],
            }
        }
