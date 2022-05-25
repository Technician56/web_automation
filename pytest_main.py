# -*- coding: utf-8 -*-
# @time    :2022/5/8 10:31
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :pytest_main.py
import os
import time

import pytest

pytest.main()
time.sleep(3)
os.system("allure generate .allure_result -o ./allure_report --clean")