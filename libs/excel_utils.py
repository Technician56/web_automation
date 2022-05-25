# -*- coding: utf-8 -*-
# @time    :2022/5/10 10:06
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :excel_utils.py
import logging
import traceback
from pathlib import Path

import openpyxl

logger = logging.getLogger(__name__)


class ExcelUtils:

    def read_excel_data(self, path):
        """
        从路径下加载出所有的EXCEL文件
        读取用例后将所有用例保存在套件中，返回
        @param path: EXCEL文件的路径或文件的路径
        @return: suite
        """
        try:
            path = Path(path)
            pathname = path.name
            logger.info(f"开始从EXCEL中读取数据: {pathname}")
            # 打开EXCEL文件
            wb = openpyxl.load_workbook(path)
            # 获取文件中的所有SHEET页内容
            sheets = wb.worksheets

            for sheet in sheets:  # 遍历SHEETS，组装套件
                case_num = 0
                # 每一个SHEET生成一个套件
                _suite = {
                    "info": {  # 套件的信息
                        "name": sheet.title,  # sheet页的标题
                    },
                    "cases": {
                        # # 用例的格式
                        # f"case_{case_num}": {
                        #     "info": {},
                        #     "steps": {},
                        # }
                    }  # sheet页中全部的用例
                }

                _cases = _suite["cases"]
                # 从sheet页的第二行开始，只取值
                for (step_id, step_name, key_word, *args) in sheet.iter_rows(min_row=2, values_only=True):

                    if step_id < 0:  # 如果step_id为负数，就根据关键字将信息放入到用例的info中
                        # 如果step_id是负数，则为新的用例，num自增1
                        case_num += 1
                        _cases[f"cases_{case_num}"] = {
                            "info": {},
                            "steps": [],
                        }
                        _cases[f"cases_{case_num}"]["info"][key_word] = args[0]

                    else:  # 如果不为负数,在用例字典中新增step关键字，将步骤放入

                        _cases[f"cases_{case_num}"]["steps"].append(
                            (step_id, step_name, key_word, self.drop_none(args))
                        )
                yield _suite
            logger.info(f"从EXCEL中读取数据结束: {pathname}")
        except Exception as e:
            logger.error(f"从EXCEL中加载数据异常: {traceback.format_exc()}")
            raise e

    @staticmethod
    def drop_none(list1):
        if isinstance(list1, list):
            new_l = []
            for arg in list1:
                if arg is not None:
                    new_l.append(arg)
            return new_l
        return list1
