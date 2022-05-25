# -*- coding: utf-8 -*-
# @time    :2022/5/8 20:04
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :web_test.py
import mysql.connector.pooling
from webdriver_helper import get_webdriver


def create_pool():
    config = {
        "host": "101.34.221.219",
        "port": "13306",
        "user": "dev",
        "password": "dev_My_ShopPx",
        "database": "test",
    }

    pool = mysql.connector.pooling.MySQLConnectionPool(**config)
    return pool


if __name__ == '__main__':

    driver = get_webdriver()
    driver.get("http://101.34.221.219:8010/?s=user/logininfo.html")