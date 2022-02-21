# -*- coding: utf-8 -*-
# @Time    : 2021/8/4 8:04 下午
# @Author  : CC

import os
import time
from loguru import logger

# 日志文件存放目录
log_path = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
logger.add(log_path_info, rotation="00:00", encoding='utf-8', enqueue=True, level='INFO')
logger.add(log_path_warning, rotation="00:00", encoding='utf-8', enqueue=True, level='WARNING')
logger.add(log_path_error, rotation="00:00", encoding='utf-8', enqueue=True, level='ERROR')

__all__ = ["logger"]
