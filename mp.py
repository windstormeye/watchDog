import itchatmp

import test

# 配置微信公众号信息
itchatmp.update_config(itchatmp.WechatConfig(
    token='pjhubs',
    appId = 'wx02fb9d00f976e7f0',
    appSecret = 'wx02fb9d00f976e7f0'))

# 接用户消息
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
        return '该系统并未对您开放，请联系PJ进行配置室内环境智能监测系统'
    else:
        if content == '加灯':
            test.addNewUnit()
            return '操作成功!'
        elif content == '开灯':
            return test.updateStatusWithHardware('hardware', 1, 1, 1)
        elif content == '关灯':
            return test.updateStatusWithHardware('hardware', 1, 1, 0)

# 新用户关注公众号时
@itchatmp.msg_register(itchatmp.content.EVENT)
def user_management(event):
    if(event['Event']=='subscribe'):
        return u'欢迎来到PJHubs，如果你想试用室内环境智能监测系统，请联系PJ'

itchatmp.run()
