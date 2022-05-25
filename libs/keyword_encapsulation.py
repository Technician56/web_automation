# -*- coding: utf-8 -*-
# @time    :2022/5/8 19:09
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :keyword_encapsulation.py
import time

import mysql.connector.pooling
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_helper import get_webdriver


class KeywordEncapsulation:
    keyword = []
    _pool = None  # 数据库连接池
    _connect = None  # 数据库的连接
    is_close = False  # 浏览器是否已经关闭

    def __init__(self, driver: webdriver.Chrome):
        driver.maximize_window()
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.__vars = {}  # 存储变量

        self.driver.stop_client = (self.driver_stop_client())

    def find_element(self, xpath, selector=By.XPATH) -> WebElement:
        def f(driver):
            ele = self.driver.find_element(selector, xpath)
            if ele.is_enabled():
                return self.driver.find_element(selector, xpath)
            else:
                return False

        return self.wait.until(f)

    def driver_stop_client(self):
        self.is_close = True

    @classmethod
    def get_all_keyword(cls):
        # 循环类中的所有属性
        for attr in dir(cls):
            if attr.startswith("key_"):
                method = getattr(cls, attr)
                if callable(method):
                    cls.keyword.append(attr[4:])
        return cls.keyword

    @staticmethod
    def alert_accept():
        def f(driver: webdriver.Chrome):
            try:
                alert_frame = driver.switch_to.alert
                alert_frame.accept()
            except UnexpectedAlertPresentException:
                return False
            except NoAlertPresentException:
                return False

            return True

        return f

    def key_get(self, url):
        """
        关键字: get
        跳转到指定的网页
        @param url: 网页的链接
        @return:
        """
        self.driver.get(url)

    def key_click(self, xpath, force=False, selector=By.XPATH):
        """
        关键字: click
        鼠标左键单击元素
        @param force: 是否启用强制点击元素
        @param xpath: XPATH或者selector
        @param selector: 选择器的类型
        @return:
        """
        ele = self.find_element(xpath, selector)
        if force:
            # 强制点击元素
            self.driver.execute_script("return arguments[0].click()", ele)
        else:
            ele.click()

    def key_input(self, xpath, word, force=False, selector=By.XPATH):
        """
        关键字: input
        向元素输入数据
        @param force: 是否使用JS强制输入
        @param xpath: XPATH或者selector
        @param word: 输入的内容
        @param selector: 选择器的类型
        @return:
        """
        ele = self.find_element(xpath, selector)
        if force:
            self.driver.execute_script(f"arguments[0].value={word}", ele)
        else:
            ele.clear()
            ele.send_keys(word)

    def key_get_text(self, var_name, xpath, selector=By.XPATH):
        """
        关键字: get_text
        获取需要的文本信息进行保存
        @param var_name: 要保存的变量名
        @param xpath: XPATH或者selector
        @param selector: 选择器的类型
        @return: 文本信息
        """
        msg = self.find_element(xpath, selector).text
        self.__vars[var_name] = msg

    def key_new_session(self):
        """
        关键字: new_session
        重新打开一个浏览器
        @return:
        """
        self.driver = get_webdriver()

    def key_exit_session(self):
        """
        关键字: exit_session
        关闭打开的浏览器
        @return:
        """
        self.driver.quit()

    def key_connect_sql(self, host, port, user, password, database_name):
        """
        关键字: connect_sql
        如果没有数据库连接池，创建数据库连接池
        创建数据库连接
        @param host: 数据库服务IP地址
        @param port: 数据库服务端口
        @param user: 数据库服务的账号
        @param password: 数据库服务的密码
        @param database_name: 数据库的名称
        @return:
        """

        if self._pool is None:
            self._pool = mysql.connector.pooling.MySQLConnectionPool(host=host, port=port, user=user, password=password,
                                                                     database=database_name)
        self._connect = self._pool.get_connection()

    def key_execute_sql(self, sql):
        """
        关键字: execute_sql
        执行SQL语句
        @param sql: 要执行的SQL语句
        @return:
        """
        cursor = self._connect.cursor()
        cursor.execute(sql)
        self._connect.commit()

    def key_get_sql(self, var_name, sql, fetchall=None):
        """
        关键字: get_sql
        执行SQL语句，将结果进行保存
        @param var_name: 要保存的变量名
        @param sql: 要执行的SQL语句
        @param fetchall: 是否需要获取多条结果
        @return:
        """
        assert self._connect
        cursor = self._connect.cursor()
        cursor.execute(sql)

        if fetchall:
            result = cursor.fectchall()
        else:
            result = cursor.fetchone()
        self._connect.commit()

        self.__vars[var_name] = str(result)

    def key_alert_ok(self):
        """
        关键字: alert_ok
        切换到对话框，单击确定
        @return:
        """
        self.wait.until(self.alert_accept())

    def key_switch_to_iframe(self, xpath):
        """
        关键字: switch_to_iframe
        切换到frame窗口
        @param xpath: iframe窗口的路径
        @return:
        """
        frame = self.find_element(xpath)
        self.driver.switch_to.frame(frame)

    def key_iframe_exit(self):
        """
        关键字: iframe_exit
        切换到frame窗口的父窗口
        @return:
        """
        self.driver.switch_to.parent_frame()

    def key_iframe_top(self):
        """
        关键字: iframe_top
        切换回顶层页面
        @return:
        """
        self.driver.switch_to.default_content()

    def key_assert(self, actual_result, expect_result, method):
        """
        关键字: assert
        @param actual_result: 实际结果
        @param expect_result: 预期结果
        @param method: 断言方法
        @return:
        """
        actual_result = self.__vars[actual_result]
        validate = Validate(actual_result, expect_result, method)

        validate.validate()

    def key_screenshot(self):
        """
        关键字: screenshot
        截图，保存为二进制格式
        @return:
        """
        return self.driver.get_screenshot_as_png()

    @staticmethod
    def key_sleep(times=10):
        """
        关键字: sleep
        强制等待
        @return:
        """
        time.sleep(int(times))


class Validate:

    def __init__(self, sj_result, yq_result, assert_method: str):
        # print(sj_result, yq_result, assert_method)
        # print(type(sj_result), type(yq_result), )
        self.sj_result = sj_result
        self.yq_result = yq_result
        self.method = assert_method

    def validate(self):
        method = getattr(self, f'assert_{self.method}')

        method()

    def assert_equal(self):
        assert self.sj_result == self.yq_result
