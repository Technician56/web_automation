# -*- coding: utf-8 -*-
# @time    :2022/5/7 20:36
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :version01.py
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_helper import get_webdriver

driver = get_webdriver()
driver.get("http://101.34.221.219:8010/?s=user/regInfo.html")
driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[1]/input').send_keys("tcs1")
driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[2]/div/input').send_keys("admin123")
driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[3]/label').click()
driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[4]/button').click()
msg = WebDriverWait(driver, 10).until(lambda x: driver.find_element(By.XPATH, "//p[@class='prompt-msg']")).text

assert msg == "注册成功"
