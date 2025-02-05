'''
 # @ : logger.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: Define the logger object.
 '''

import datetime
import os
import sys

from loguru import logger


def start_logger(
    file_name: str = datetime.datetime.now(),
    path: str = None,
    level: str = "INFO"
):

    logger.remove()

    logs_format = '<fg 255,215,0>{time:YYYY-MM-DD HH:mm:ss}</fg 255,215,0> ' \
                  '| <fg 49,140,231>{message}</fg 49,140,231>'

    if path and file_name != 'pytest' and file_name != 'pytest_logger':
        logger.add(
            sys.stderr,
            level=level,
            colorize=True,
            format=logs_format,
        )

        sink_name = os.path.join(path, 'logs', f'{file_name}.txt')
        logger.add(sink=sink_name, level=level, )

    if file_name == 'pytest_logger':

        logs_format = 'PYTEST | {message}'
        logger.add(
            sys.stderr,
            level=level,
            colorize=True,
            format=logs_format,
        )

        sink_name = f"{path}/logs/pytest_logger.txt"
        logger.add(sink=sink_name, level=level)

    return logger