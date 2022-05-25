# -*- coding: utf-8 -*-
# @time    :2022/5/7 20:27
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :pom.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class FakeElement:
    def __new__(cls, args) -> WebElement:
        return args


class BasePage:
    _url = ""

    def __init__(self, driver: webdriver.Chrome):
        # 在实例化对象的时候，根据元素的表达式创建真正的元素
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.check_url()
        self.check_element()

    def check_url(self):
        assert self.driver.current_url == self._url

    def check_element(self):
        for attr in dir(self):
            if attr.startswith("_ele_"):
                xpath = getattr(self, attr)
                ele = self.find_element(xpath)
                setattr(self, attr, ele)

    def find_element(self, xpath, selector=By.XPATH):
        def f(driver):
            return self.driver.find_element(selector, xpath)

        return self.wait.until(f)


class RegisterPage(BasePage):
    _ele_username = FakeElement('/html/body/div[4]/div/div/div[2]/div/div/div/form/div[1]/input')
    _ele_password = FakeElement('/html/body/div[4]/div/div/div[2]/div/div/div/form/div[2]/div/input')
    _ele_agreement = FakeElement('/html/body/div[4]/div/div/div[2]/div/div/div/form/div[3]/label')
    _ele_register_btn = FakeElement('/html/body/div[4]/div/div/div[2]/div/div/div/form/div[4]/button')
    _url = 'http://101.34.221.219:8010/?s=user/regInfo.html'

    def page_submit(self, username, password):
        self._ele_username.send_keys(username)
        self._ele_password.send_keys(password)
        self._ele_agreement.click()
        self._ele_register_btn.click()

    def get_msg(self):
        return self.find_element("//p[@class='prompt-msg']").text


class LoginPage(BasePage):
    _url = FakeElement("http://101.34.221.219:8010/?s=user/logininfo.html")
    _ele_username = FakeElement('/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input')
    _ele_password = FakeElement('/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input')
    _ele_login_btn = FakeElement('/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button')

    def page_submit(self, username, password):
        self._ele_username.send_keys(username)
        self._ele_password.send_keys(password)
        self._ele_login_btn.click()

    def get_msg(self):
        return self.find_element("//p[@class='prompt-msg']").text


class Add2CartPage(BasePage):
    _url = "http://101.34.221.219:8010/?s=goods/index/id/6.html"
    _ele_num = FakeElement('// *[ @ id = "text_box"]')
    _ele_add_to_cart_btn = FakeElement('/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[2]')

    def page_submit(self, num):
        self._ele_num.send_keys(num)
        self._ele_add_to_cart_btn.click()

    def get_msg(self):
        return self.find_element('//p[@class="prompt-msg"]').text
