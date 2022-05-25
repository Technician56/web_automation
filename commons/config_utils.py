# -*- coding: utf-8 -*-
# @time    :2022/5/12 13:53
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :config_utils.py
import os

import yaml


class ConfigUtils:

    @staticmethod
    def get_obj_path():
        return os.getcwd()

    def get_case_dir(self):
        with open(self.get_obj_path() + "/config_yaml.yaml", mode="r", encoding="utf-8") as f:
            return yaml.load(f, yaml.FullLoader)["testcase"]["base_dir"]
