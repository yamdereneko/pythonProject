#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/pycharm_project/ymProject/Data")
sys.path.append("/home/pycharm_project/")
sys.path.append("/home/pycharm_project/ymProject/*")
sys.path.append("/home/pycharm_project/ymProject/API")
import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.log import logger, default_format
import ymProject.API.jx3Main as jxAPI

# You can pass some keyword args config to init function
nonebot.init(_env_file=".env.dev")
app = jxAPI.app
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("ym_bot/plugins")
# Custom your logger
#
logger.add("logs/error.log",
           rotation="00:00",
           diagnose=False,
           level="INFO",
           format=default_format)

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app=app, host="0.0.0.0", port=8080)
