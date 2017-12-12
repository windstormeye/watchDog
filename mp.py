import itchatmp

import test

# 配置微信公众号信息
itchatmp.update_config(itchatmp.WechatConfig(
    token='pjhubs',
    appId = 'wx02fb9d00f976e7f0',
    appSecret = 'wx02fb9d00f976e7f0'))

# 接收用户消息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    toUserName = msg['FromUserName']
    content = msg['Content']
    isContain = 0;
    # pjhubs.txt为有权限的用户列表
    f = open("pjhubs.txt","r")  
    lines = f.readlines()  
    for line in lines:
        if line[:-1] == toUserName:
            isContain = 1;
    if isContain == 0:
        return '该系统并未对您开放，请联系PJ进行配置'
    else:
        if content == '添加':
            # test.addNewUnit('tempUnit', 1, 2)
             return '操作成功!'
        elif content == '开灯':
             return test.updateStatusWithHardware('hardware', 1, 'redLED', 1)
        elif content == '关灯':
            return test.updateStatusWithHardware('hardware', 1, 'redLED', 0)
        elif content == '温度':
            unit = test.updateStatusWithHardware('hardware', 0, 'tempUnit', 1)
            returnString = '当前温度为：' + str(unit.num) + '°'
            return returnString
        elif content == '开风扇':
            return test.updateStatusWithHardware('hardware', 1, 'tempUnit', 1)
        elif content == '关风扇':
            return test.updateStatusWithHardware('hardware', 1, 'tempUnit', 0)

# 新用户关注公众号时
@itchatmp.msg_register(itchatmp.content.EVENT)
def user_management(event):
    if(event['Event']=='subscribe'):
        return u'欢迎来到PJHubs，如果你想试用室内环境智能监测系统，请联系PJ'

itchatmp.run()
