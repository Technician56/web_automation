
import sys
from glob import glob
import logging
sys.path.append(r"H://pyProjects/learn")

from tcs_web_automation.web_automation_encapsulation.libs.excel_utils import ExcelUtils
from tcs_web_automation.web_automation_encapsulation.libs import case_utils

e = ExcelUtils()
logger = logging.getLogger(__name__)
file_list = glob(r"./testcase/case_datas/test_use/test*.xlsx")
logger.info(f"EXCEL文件列表: {file_list}")
logger.info("开始生成用例")

no = 0
for file in file_list:
    for suite in ExcelUtils().read_excel_data(file):
        no += 1
        logger.info(f"第 {no} 个套件: {suite}")
        logger.info(f"开始生成测试类  测试_{suite['info']['name']}")
        globals()[f"测试_{suite['info']['name']}"] = case_utils.create_case(suite, file)
        
