# -*- coding: utf-8 -*-
# @Time : 2022-02-17 16:40 
# @Author : YD

# -*- coding: utf-8 -*-
# @Time : 2022-02-15 16:30
# @Author : YD

import time
import re
import datetime
import os
from hashlib import md5
from typing import Union, Literal

from playwright.async_api import async_playwright, Page, Frame, Route
from playwright.sync_api import sync_playwright, Page, Frame, Route
from extensions.logger import logger
from schemas.booking import Booking
from config import settings


async def intercept_route(route: Route):
    url = route.request.url
    # intercept_url_suffix = ['.svg', '.jpg', '.jpeg', '.css', '.png', '.gif']
    # # logger.debug(url)
    # if any(map(lambda suffix: url.endswith(suffix), intercept_url_suffix)):
    #     await route.abort()
    #     # logger.debug('拦截')
    # else:
    #     await route.continue_()
    #     # logger.debug('继续')
    await route.continue_()


async def process_page(page: Page):
    await page.route('**/*', intercept_route)


class DC:
    def __init__(self, data: Booking):
        self.url = 'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html'
        self.data = data
        # self.username = self.data.username
        # self.pwd = self.data.pwd
        #
        # self.cookies_dir = 'cookies'
        # self.cookies_file = os.path.join(self.cookies_dir, md5(self.username.encode('utf-8')).hexdigest() + '.json')

    async def new_obj(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            downloads_path='data',
        )

        # if not os.path.exists(self.cookies_dir):
        #     os.mkdir(self.cookies_dir)
        # if os.path.exists(self.cookies_file):
        #     self.context = await self.browser.new_context(
        #         accept_downloads=True,
        #         storage_state=self.cookies_file,
        #         # viewport={'width': 1920, 'height': 1080}
        #     )
        # else:
        #     self.context = await self.browser.new_context(
        #         accept_downloads=True,
        #         # viewport={'width': 1920, 'height': 1080}
        #     )
        self.context = await self.browser.new_context(
            accept_downloads=True,
            # viewport={'width': 1920, 'height': 1080}
        )
        self.context.on('page', process_page)
        self.page = await self.context.new_page()
        await self.context.add_cookies(cookies=self.data.cookies)

    async def del_obj(self):
        await self.page.close()
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def wait_loading(
            self,
            element: Union[Page, Frame],
            state: Literal["domcontentloaded", "load", "networkidle"] = 'networkidle',
            second: float = 1,
    ) -> None:
        try:
            await element.wait_for_load_state(state=state)
            await element.wait_for_timeout(second * 1000)
        except TimeoutError as e:
            print(e)

    async def login(self):
        logger.info('正在打开网站...')
        try:
            async with self.page.expect_navigation():
                await self.page.goto(self.url)

            if await self.page.is_visible('//*[@id="hal-cookieconsent-button"]'):
                await self.page.click('//*[@id="hal-cookieconsent-button"]')

        except Exception as e:
            pass
        await self.wait_loading(self.page, second=5)

        if await self.page.is_visible('//*[@id="hal-cookieconsent-button"]'):
            await self.page.click('//*[@id="hal-cookieconsent-button"]')

        if await self.page.is_visible('//div[@class="hal-navigation-top-login"]//span[contains(text(),"你好")]'):
            logger.info('登陆成功')
            # print(await self.context.cookies())
            # await self.context.storage_state(path=self.cookies_file)
            return True

        # await self.page.fill('//input[@id="loginReq_f:hl24"]', self.username)
        # await self.page.fill('//input[@id="loginReq_f:hl29"]', self.pwd)
        # await self.page.click('//button[@id="loginReq_f:hl50"]')
        # await self.wait_loading(self.page)
        #
        # if await self.page.is_visible('//div[@class="hal-navigation-top-login"]//span[contains(text(),"你好")]'):
        #     print(await self.context.cookies())
        #     logger.info('登陆成功')
        #     await self.context.storage_state(path=self.cookies_file)
        #     return True

        return False

    async def fak(self):

        # 清除
        await self.page.click('//button[@id="R1014_f:hl101"]')
        await self.wait_loading(self.page)
        origin = self.data.origin
        destination = self.data.destination

        # if await self.page.get_attribute('//input[@id="R1014_f:hl13"]', 'value') != origin:
        async with self.page.expect_response(
                'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html?_sR1014=_raction&action=getTypeAheadService') as resp_info:
            await self.page.fill('//input[@id="R1014_f:hl13"]', '')
            await self.page.type('//input[@id="R1014_f:hl13"]', origin.split(' ')[0], delay=0.1)

        resp = await resp_info.value
        resp_json = await resp.json()
        if not resp_json['rows']:
            raise Exception(f'未搜索到该起始地：{origin}')
        # await self.page.fill('//input[@id="R1014_f:hl13"]', '')
        # await self.page.type('//input[@id="R1014_f:hl13"]', origin.split(' ')[0], delay=0.1)
        await self.page.click(f'//span[text()="{origin}"]')

        # if await self.page.get_attribute('//input[@id="R1014_f:hl38"]', 'value') != destination:
        async with self.page.expect_response(
                'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html?_sR1014=_raction&action=getTypeAheadService') as resp_info:
            await self.page.fill('//input[@id="R1014_f:hl38"]', '')
            await self.page.type('//input[@id="R1014_f:hl38"]', destination.split(' ')[0], delay=0.1)
        resp = await resp_info.value
        resp_json = await resp.json()
        if not resp_json['rows']:
            raise Exception(f'未搜索到该起始地：{destination}')
        # await self.page.fill('//input[@id="R1014_f:hl38"]', '')
        # await self.page.type('//input[@id="R1014_f:hl38"]', destination.split(' ')[0], delay=0.1)
        await self.page.click(f'//span[text()="{destination}"]')

        await self.page.check('//input[@id="R1014_f:hl96"]')
        await self.page.click('//button[@id="R1014_f:hl99"]')
        await self.wait_loading(self.page)

        # 订舱
        async with self.page.expect_navigation():
            await self.page.click('//button[@id="R1014_f:hl481"]')
        await self.wait_loading(self.page)

        await self.page.fill('//input[@id="booking_f:hl64"]', self.data.email_address)

        # 下一步
        await self.page.click('//input[@id="booking_f:hl71"]')
        await self.wait_loading(self.page)
        # 下一步
        await self.page.click('//input[@id="booking_f:hl229"]')
        await self.wait_loading(self.page)
        # 查询船期
        async with self.page.expect_navigation():
            await self.page.click('//button[@id="booking_f:hl365"]')
        await self.wait_loading(self.page)

        # 选择订舱
        try:
            booking_xpath = '(//table[@id="booking_f:hl146"]/tbody/tr[not(contains(.,"Vessel space not available"))])[1]'
            await self.page.wait_for_selector(booking_xpath, timeout=3000)
            await self.page.click(f'{booking_xpath}//div[@class="hl-radio"]')
        except Exception as e:
            raise Exception('没有合适的订舱')
        async with self.page.expect_navigation():
            await self.page.click('//button[@id="booking_f:hl146:hl180"]')
        await self.wait_loading(self.page)

        # 下一步
        await self.page.click('//input[@id="booking_f:hl403"]')
        await self.wait_loading(self.page)

        # 数量
        await self.page.fill('//input[@id="booking_f:hl420"]', self.data.container_number)
        await self.page.click('(//table[@id="booking_f:hl433"]//img[contains(@id,"ext-gen")])[1]')
        await self.page.click(f'//div[@id="ext-gen770"]//div[text()="{self.data.container_type}"]')

        # 放行
        # if self.page.get_attribute('//input[@id="booking_f:hl544"]','value'):
        await self.page.fill('//input[@id="booking_f:hl544"]', '')
        dt = datetime.datetime.now()
        await self.page.type('//input[@id="booking_f:hl544"]', self.data.release_date, delay=0.1)
        await self.page.fill('//input[@id="booking_f:hl548"]', '')
        await self.page.type('//input[@id="booking_f:hl548"]', self.data.release_time, delay=0.1)

        # 描述
        await self.page.fill('//input[@id="booking_f:hl514"]', self.data.destination)
        # 商品编码
        commodity_codes = self.data.commodity_code.split(' ')
        await self.page.fill('//input[@id="booking_f:hl520"]', commodity_codes[0])
        await self.page.fill('//input[@id="booking_f:hl521"]', commodity_codes[1])
        await self.page.fill('//input[@id="booking_f:hl522"]', commodity_codes[2])

        # 预配信息
        await self.page.click('//button[@id="booking_f:hl559"]')
        await self.wait_loading(self.page)

        if await self.page.is_visible('//span[@id="booking_f:hl2"]'):
            logger.error(await self.page.text_content('//span[@id="booking_f:hl2"]'))
            raise Exception(await self.page.text_content('//span[@id="booking_f:hl2"]'))

        await self.page.fill('//input[@id="booking_f:hl750"]', self.data.weight)
        await self.page.click('(//table[@id="booking_f:hl759"]//img[contains(@id,"ext-gen")])[1]')
        await self.page.click(f'//div[@id="ext-gen339"]/div[text()="{self.data.unit}"]')

        # 下一步
        await self.page.click('//input[@id="booking_f:hl3221"]')
        await self.wait_loading(self.page)

        # 下一步
        await self.page.click('//input[@id="booking_f:hl3355"]')
        await self.wait_loading(self.page)

        # 提交预定
        # await self.page.click('//input[@id="booking_f:hl5023"]')
        # await self.wait_loading(self.page)
        print('over')
        # result = await self.page.text_content('//div[@id="book_success"]', timeout=120000)
        # logger.info(result)
        # return result

    async def run(self):
        try:
            await self.new_obj()
            if not await self.login():
                logger.info('登陆失败')
                raise Exception('登陆失败')
            await self.fak()
        except Exception as e:
            raise e
        finally:
            await self.del_obj()


def intercept_route_(route: Route):
    url = route.request.url
    intercept_url_suffix = ['.svg', '.jpg', '.jpeg', '.css', '.png', '.gif']
    # logger.debug(url)
    if any(map(lambda suffix: url.endswith(suffix), intercept_url_suffix)):
        route.abort()
        # logger.debug('拦截')
    else:
        route.continue_()
        # logger.debug('继续')


def process_page_(page: Page):
    page.route('**/*', intercept_route)


class DC_:
    def __init__(self, data: Booking):
        self.url = 'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html'
        self.data = data
        # self.username = self.data.username
        # self.pwd = self.data.pwd
        #
        # self.cookies_dir = 'cookies'
        # self.cookies_file = os.path.join(self.cookies_dir, md5(self.username.encode('utf-8')).hexdigest() + '.json')

    def new_obj(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            downloads_path='data',
        )

        # if not os.path.exists(self.cookies_dir):
        #     os.mkdir(self.cookies_dir)
        # if os.path.exists(self.cookies_file):
        #     self.context = self.browser.new_context(
        #         accept_downloads=True,
        #         storage_state=self.cookies_file,
        #         # viewport={'width': 1920, 'height': 1080}
        #     )
        # else:
        #     self.context = self.browser.new_context(
        #         accept_downloads=True,
        #         # viewport={'width': 1920, 'height': 1080}
        #     )
        self.context = self.browser.new_context(
            accept_downloads=True,
            # viewport={'width': 1920, 'height': 1080}
        )
        self.context.on('page', process_page_)
        self.page = self.context.new_page()
        self.context.add_cookies(cookies=self.data.cookies)

    def del_obj(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def wait_loading(
            self,
            element: Union[Page, Frame],
            state: Literal["domcontentloaded", "load", "networkidle"] = 'networkidle',
            second: float = 1,
    ) -> None:
        try:
            element.wait_for_load_state(state=state)
            element.wait_for_timeout(second * 1000)
        except TimeoutError as e:
            print(e)

    def login(self):
        logger.info('正在打开网站...')
        try:
            with self.page.expect_navigation():
                self.page.goto(self.url)

            if self.page.is_visible('//*[@id="hal-cookieconsent-button"]'):
                self.page.click('//*[@id="hal-cookieconsent-button"]')

        except Exception as e:
            pass
        self.wait_loading(self.page, second=5)

        if self.page.is_visible('//*[@id="hal-cookieconsent-button"]'):
            self.page.click('//*[@id="hal-cookieconsent-button"]')

        if self.page.is_visible('//div[@class="hal-navigation-top-login"]//span[contains(text(),"你好")]'):
            logger.info('登陆成功')
            # print(self.context.cookies())
            # self.context.storage_state(path=self.cookies_file)
            return True

        # self.page.fill('//input[@id="loginReq_f:hl24"]', self.username)
        # self.page.fill('//input[@id="loginReq_f:hl29"]', self.pwd)
        # self.page.click('//button[@id="loginReq_f:hl50"]')
        # self.wait_loading(self.page)
        #
        # if self.page.is_visible('//div[@class="hal-navigation-top-login"]//span[contains(text(),"你好")]'):
        #     print(self.context.cookies())
        #     logger.info('登陆成功')
        #     self.context.storage_state(path=self.cookies_file)
        #     return True

        return False

    def fak(self):

        # 清除
        self.page.click('//button[@id="R1014_f:hl101"]')
        self.wait_loading(self.page)
        origin = self.data.origin
        destination = self.data.destination

        # if self.page.get_attribute('//input[@id="R1014_f:hl13"]', 'value') != origin:
        with self.page.expect_response(
                'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html?_sR1014=_raction&action=getTypeAheadService') as resp_info:
            self.page.fill('//input[@id="R1014_f:hl13"]', '')
            self.page.type('//input[@id="R1014_f:hl13"]', origin.split(' ')[0], delay=0.1)

        resp = resp_info.value
        resp_json = resp.json()
        if not resp_json['rows']:
            raise Exception(f'未搜索到该起始地：{origin}')
        # self.page.fill('//input[@id="R1014_f:hl13"]', '')
        # self.page.type('//input[@id="R1014_f:hl13"]', origin.split(' ')[0], delay=0.1)
        self.page.click(f'//span[text()="{origin}"]')

        # if self.page.get_attribute('//input[@id="R1014_f:hl38"]', 'value') != destination:
        with self.page.expect_response(
                'https://www.hapag-lloyd.cn/zh/online-business/quotation/quick-quotes-solution.html?_sR1014=_raction&action=getTypeAheadService') as resp_info:
            self.page.fill('//input[@id="R1014_f:hl38"]', '')
            self.page.type('//input[@id="R1014_f:hl38"]', destination.split(' ')[0], delay=0.1)
        resp = resp_info.value
        resp_json = resp.json()
        if not resp_json['rows']:
            raise Exception(f'未搜索到该起始地：{destination}')
        # self.page.fill('//input[@id="R1014_f:hl38"]', '')
        # self.page.type('//input[@id="R1014_f:hl38"]', destination.split(' ')[0], delay=0.1)
        self.page.click(f'//span[text()="{destination}"]')

        self.page.check('//input[@id="R1014_f:hl96"]')
        self.page.click('//button[@id="R1014_f:hl99"]')
        self.wait_loading(self.page)

        # 订舱
        with self.page.expect_navigation():
            self.page.click('//button[@id="R1014_f:hl481"]')
        self.wait_loading(self.page)

        self.page.fill('//input[@id="booking_f:hl64"]', self.data.email_address)

        # 下一步
        self.page.click('//input[@id="booking_f:hl71"]')
        self.wait_loading(self.page)
        # 下一步
        self.page.click('//input[@id="booking_f:hl229"]')
        self.wait_loading(self.page)
        # 查询船期
        with self.page.expect_navigation():
            self.page.click('//button[@id="booking_f:hl365"]')
        self.wait_loading(self.page)

        # 选择订舱
        try:
            booking_xpath = '(//table[@id="booking_f:hl146"]/tbody/tr[not(contains(.,"Vessel space not available"))])[1]'
            self.page.wait_for_selector(booking_xpath, timeout=3000)
            self.page.click(f'{booking_xpath}//div[@class="hl-radio"]')
        except Exception as e:
            raise Exception('没有合适的订舱')
        with self.page.expect_navigation():
            self.page.click('//button[@id="booking_f:hl146:hl180"]')
        self.wait_loading(self.page)

        # 下一步
        self.page.click('//input[@id="booking_f:hl403"]')
        self.wait_loading(self.page)

        # 数量
        self.page.fill('//input[@id="booking_f:hl420"]', self.data.container_number)
        self.page.click('(//table[@id="booking_f:hl433"]//img[contains(@id,"ext-gen")])[1]')
        self.page.click(f'//div[@id="ext-gen770"]//div[text()="{self.data.container_type}"]')

        # 放行
        # if self.page.get_attribute('//input[@id="booking_f:hl544"]','value'):
        self.page.fill('//input[@id="booking_f:hl544"]', '')
        dt = datetime.datetime.now()
        self.page.type('//input[@id="booking_f:hl544"]', self.data.release_date, delay=0.1)
        self.page.fill('//input[@id="booking_f:hl548"]', '')
        self.page.type('//input[@id="booking_f:hl548"]', self.data.release_time, delay=0.1)

        # 描述
        self.page.fill('//input[@id="booking_f:hl514"]', self.data.destination)
        # 商品编码
        commodity_codes = self.data.commodity_code.split(' ')
        self.page.fill('//input[@id="booking_f:hl520"]', commodity_codes[0])
        self.page.fill('//input[@id="booking_f:hl521"]', commodity_codes[1])
        self.page.fill('//input[@id="booking_f:hl522"]', commodity_codes[2])

        # 预配信息
        self.page.click('//button[@id="booking_f:hl559"]')
        self.wait_loading(self.page)

        if self.page.is_visible('//span[@id="booking_f:hl2"]'):
            logger.error(self.page.text_content('//span[@id="booking_f:hl2"]'))
            raise Exception(self.page.text_content('//span[@id="booking_f:hl2"]'))

        self.page.fill('//input[@id="booking_f:hl750"]', self.data.weight)
        self.page.click('(//table[@id="booking_f:hl759"]//img[contains(@id,"ext-gen")])[1]')
        self.page.click(f'//div[@id="ext-gen339"]/div[text()="{self.data.unit}"]')

        # 下一步
        self.page.click('//input[@id="booking_f:hl3221"]')
        self.wait_loading(self.page)

        # 下一步
        self.page.click('//input[@id="booking_f:hl3355"]')
        self.wait_loading(self.page)

        # 提交预定
        # self.page.click('//input[@id="booking_f:hl5023"]')
        # self.wait_loading(self.page)

        print('over')
        # result = self.page.text_content('//div[@id="book_success"]', timeout=120000)
        # logger.info(result)
        # return result

    def run(self):
        try:
            self.new_obj()
            if not self.login():
                logger.info('登陆失败')
                raise Exception('登陆失败')
            return self.fak()
        except Exception as e:
            raise e
        finally:
            self.del_obj()


async def get_dc(data: Booking):
    try:
        dc = DC(data)
        return await dc.run()
    except Exception as e:
        logger.error(e)
        return e.__str__()


def task(data: Booking):
    try:
        dc = DC_(data)
        return dc.run()
    except Exception as e:
        logger.error(e)
        return e.__str__()


async def main(data: Booking):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    futures = []
    result = []
    with ThreadPoolExecutor(max_workers=settings.max_workers) as pool:
        for i in range(settings.max_workers):
            futures.append(pool.submit(task, data))

        for future in as_completed(futures):
            result.append(future.result())
    return result
