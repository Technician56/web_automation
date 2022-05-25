# -*- coding: utf-8 -*-
# @time    :2022/5/10 13:10
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :case_utils.py
import logging
import traceback
import unittest
from pathlib import Path

import allure
import ddt
from selenium.common.exceptions import NoAlertPresentException
from webdriver_helper import get_webdriver

from tcs_web_automation.web_automation_encapsulation.libs.keyword_encapsulation import KeywordEncapsulation

logger = logging.getLogger(__name__)

not_screenshot_list = ["screenshot",
                       "sleep",
                       "assert",
                       "get_sql",
                       "execute_sql",
                       "connect_sql",
                       "exit_session",
                       ]


def create_case(testcase_suite, filename):
    file_path = Path(filename)
    filename = file_path.name  # 文件的名字

    @ddt.ddt
    @allure.epic(filename)
    @allure.feature(testcase_suite['info']['name'])
    class Test(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.driver = get_webdriver()

        @classmethod
        def tearDownClass(cls) -> None:
            cls.driver.quit()

        @ddt.data(*testcase_suite["cases"].values())
        def test_sss(self, args):
            allure.dynamic.title(args["info"]["name"])
            try:
                logger.info(f'开始测试用例  {args["info"]["name"]}')
                # 需要调用keyword封装的方法，先进行实例化
                kw = KeywordEncapsulation(self.driver)
                # 获得用例中的步骤
                steps = args["steps"]
                # 对步骤进行操作
                for step in steps:
                    logger.info(f"测试步骤 {step}")

                    @allure.step(step[1])
                    def _f(关键字=step[2], 参数=step[3]):
                        method = getattr(kw, f"key_{step[2]}")
                        method(*step[3])

                        logger.info(f"{step[0]} 关键字 {step[2]} 执行完毕,开始截图")
                        # 指定关键字不进行截图
                        # 有弹窗，不进行截图
                        if step[2] not in not_screenshot_list and kw.is_close is True:  # 截图
                            try:
                                kw.driver.switch_to.alert
                                logger.info("有弹窗，不进行截图..")
                            except NoAlertPresentException:
                                logger.info(f"满足条件，进行截图...")
                                allure.attach(kw.key_screenshot(), step[1], allure.attachment_type.PNG)
                        else:
                            logger.info(f"关键字 {step[2]} 不需要进行截图")
                    _f()
                logger.info(f'测试用例 {args["info"]["name"]} 完成')
            except Exception as e:
                logger.error(f'测试用例 {args["info"]["name"]} 异常: {traceback.format_exc()}')
                raise e

    return Test
