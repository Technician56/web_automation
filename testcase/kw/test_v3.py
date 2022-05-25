# -*- coding: utf-8 -*-
# @time    :2022/5/8 20:14
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :test_v3.py

from tcs_web_automation.web_automation_encapsulation.libs.keyword_encapsulation import KeywordEncapsulation


class Test_KeyWord:

    def test_add_address(self, statu_login):
        keyword = KeywordEncapsulation(statu_login)
        # 访问 地址
        keyword.key_get("http://101.34.221.219:8010/?s=useraddress/index.html")
        # 点击 新增地址
        keyword.key_click('/html/body/div[4]/div[3]/div/div[1]/button')
        # 对话框 确定
        keyword.key_alert_ok()
        # 切换到frame窗口
        keyword.key_switch_to_iframe('//iframe[@src="http://101.34.221.219:8010/?s=useraddress/saveinfo.html"]')
        # 输入 姓名、电话、详细地址
        keyword.key_input("/html/body/div[1]/form/div[2]/input", "李心艾欧亚O")
        keyword.key_input("/html/body/div[1]/form/div[3]/input", "13699995555")
        keyword.key_input('//*[@id="form-address"]', "江南皮革厂")
        # 选择 省份、城市、县区
        keyword.key_click('/html/body/div[1]/form/div[4]/div[1]')
        keyword.key_click('//ul/li[text()="浙江省"]')

        keyword.key_click('/html/body/div[1]/form/div[4]/div[2]')
        keyword.key_click('//ul/li[text()="温州市"]')

        keyword.key_click('/html/body/div[1]/form/div[4]/div[3]')
        keyword.key_click('//ul/li[text()="平阳县"]')
        # 点击 保存
        keyword.key_click('/html/body/div[1]/form/div[7]/button')
        # 获取断言的实际结果
        act_result = keyword.key_get_text("msg", '//p[@class="prompt-msg"]')
        # 获取断言的预期结果
        exc_result = "操作成功"
        # 断言的方法
        validate_method = "equal"
        # 断言
        keyword.key_assert("msg", exc_result, validate_method)
