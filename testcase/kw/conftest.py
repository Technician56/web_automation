# -*- coding: utf-8 -*-
# @time    :2022/5/8 20:19
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :conftest.py
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_helper import get_webdriver


@pytest.fixture
def statu_login(cache):
    """
    1. 判断是否为登录状态
    2. 如果是则跳过，如果是否则进行登录
    3. 每次登录前添加cookie 跳过登录
    """

    driver = get_webdriver()
    driver.get("http://101.34.221.219:8010/")
    # 获取cookie后添加
    cookies = cache.get("user_cookies", {})
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()

    try:
        quite_element = driver.find_element(By.XPATH, '//a[@href="http://101.34.221.219:8010/?s=user/logout.html"]')
    except NoSuchElementException:
        quite_element = None

    # 判断是否为已登录状态: 是跳过，否进行登录
    if quite_element:
        pass
    else:
        driver.get("http://101.34.221.219:8010/?s=user/logininfo.html")
        # 输入账号
        driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input').send_keys(
            "tcs01")
        # 输入密码
        driver.find_element(By.XPATH,
                            '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input').send_keys(
            "admin123")
        # 点击登录
        driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button').click()

    # 保存cookie
    cache.set("user_cookies", driver.get_cookies())

    yield driver

    # 完成后关闭浏览器
    driver.quit()
