# -*- coding: utf-8 -*-
# @time    :2022/5/7 21:09
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :test_v2.py
import os
import unittest

import pytest
import yaml
from webdriver_helper import get_webdriver

from tcs_web_automation.web_automation_encapsulation.libs import pom


class ATest_A(unittest.TestCase):

    # @pytest.mark.run(order=1)
    # def test_register(self):
    #     driver = get_webdriver()
    #     driver.get("http://101.34.221.219:8010/?s=user/regInfo.html")
    #     page = pom.RegisterPage(driver)
    #     page.page_submit("tcs03", "admin123")
    #
    #     msg = page.get_msg()
    #     assert msg == "注册成功"

    @pytest.mark.run(order=2)
    def test_login(self):
        driver = get_webdriver()
        driver.get("http://101.34.221.219:8010/?s=user/logininfo.html")
        page = pom.LoginPage(driver)
        page.page_submit("tcs01", "admin123")

        msg = page.get_msg()
        assert msg == "登录成功"

        cookies = driver.get_cookies()
        # 把登录后得到的cookies保存到文件，用来跳过登录
        with open(os.getcwd() + "/cookies.yaml", mode="w", encoding="utf-8") as file:
            yaml.dump(cookies, file, allow_unicode=True)

    @pytest.mark.run(order=3)
    def test_add_to_cart(self):
        driver = get_webdriver()
        driver.get("http://101.34.221.219:8010/?s=goods/index/id/6.html")
        with open(os.getcwd() + "/cookies.yaml", mode="r", encoding="utf-8") as file:
            cookies = yaml.load(file, yaml.FullLoader)
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        print(driver.current_url)
        page = pom.Add2CartPage(driver)
        page.page_submit("3")
        msg = page.get_msg()
        assert msg == "加入成功"
