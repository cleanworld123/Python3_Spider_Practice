import requests
import json

while True:
    #循环获取输入值
    content = input("请输入：")
    if content == "":
        print("没有有效输入，欢迎下次使用！")
        break

    '''
    抓取报文，可以看到如下的url
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'  
    这是反爬处理后的结果，需要删掉_o可正常使用
    '''
    #通过对比，在netwwork的XHR模块中分析请求的url和提交的表单数据
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    #准备post表单，是dict类型
    post_data = {
        'i': content
        , 'from': 'AUTO'
        , 'to': 'AUTO'
        , 'smartresult': 'dict'
        , 'client': 'fanyideskweb'
        , 'salt': '15450592848584'
        , 'sign': '76275999016ece9643161f4d6cc2e252'
        , 'ts': '1545059284858'
        , 'bv': '9920fbb76fd558e911cf93832183285b'
        , 'doctype': 'json'
        , 'version': '2.1'
        , 'keyfrom': 'fanyi.web'
        , 'action': 'FY_BY_REALTIME'
        , 'typoResult': 'false'
    }
    #提交 post数据
    response = requests.post(url, data=post_data)

    #解析翻译结果
    html = response.text
    # 因为翻译后的数据是通过json格式返回的，所以要添加json模块进行解析
    target = json.loads(html)
    print("翻译结果：")
    print(target['translateResult'][0][0]['tgt'])
    print()
