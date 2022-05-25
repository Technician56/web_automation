# -*- coding: utf-8 -*-
# @time    :2022/5/10 16:23
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :conftest.py


# 在执行用例时，自动新建py文件
# 执行完成用例后，自动删除py文件
import logging
from pathlib import Path

import pytest

from tcs_web_automation.web_automation_encapsulation.commons.config_utils import ConfigUtils

base_dir = Path(ConfigUtils().get_obj_path())
path = base_dir / "test_tcs_encapsulation.py"
logger = logging.getLogger(__name__)


def pytest_configure():
    """
    测试开始前，创建py文件
    :return:
    """

    case_dir = ConfigUtils().get_case_dir()
    code = f"""
import sys
from glob import glob
import logging
sys.path.append(r"H://pyProjects/learn")

from tcs_web_automation.web_automation_encapsulation.libs.excel_utils import ExcelUtils
from tcs_web_automation.web_automation_encapsulation.libs import case_utils

e = ExcelUtils()
logger = logging.getLogger(__name__)
file_list = glob(r"{case_dir}/test*.xlsx")
logger.info(f"EXCEL文件列表: {{file_list}}")
logger.info("开始生成用例")

no = 0
for file in file_list:
    for suite in ExcelUtils().read_excel_data(file):
        no += 1
        logger.info(f"第 {{no}} 个套件: {{suite}}")
        logger.info(f"开始生成测试类  测试_{{suite['info']['name']}}")
        globals()[f"测试_{{suite['info']['name']}}"] = case_utils.create_case(suite, file)
        
"""
    path.write_text(code, encoding="utf-8")


def pytest_terminal_summary():
    """
    pytest 执行完成的之后，自动调用
    :return:
    """
    path.unlink()


@pytest.fixture(scope="session", autouse=True)
def tcs_encapsulation():
    logger.info("开始执行框架 test_tcs_encapsulation.py")
    yield
    logger.info("框架执行结束 test_tcs_encapsulation.py")
