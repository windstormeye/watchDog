import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='pjhubs',
    appId = 'wx02fb9d00f976e7f0',
    appSecret = 'wx02fb9d00f976e7f0'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    toUserName = msg['FromUserName']
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
        return '系统正在配置中...'
 
@itchatmp.msg_register(itchatmp.content.EVENT)
def user_management(event):
    if(event['Event']=='subscribe'):
        return u'欢迎来到PJHubs，如果你想试用室内环境智能监测系统，请联系PJ'

itchatmp.run()
