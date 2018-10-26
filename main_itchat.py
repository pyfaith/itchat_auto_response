#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 2018/10/17
__author__ = "pyfaith"

import random
import platform

import itchat
import requests

KEY = ['8edce3ce905a4c1dbb965e6b35c3834d', 'eb720a8970964f3f855d863d24406576', '1107d5601866433dba9599fac1bc0083', '71f28bf79c820df10d39b4074345ef8c']
#所有的公司微信的昵称
COMPANY_WX_NICKNAME = ["股民社区", "招财大牛猫", "随风飘逝"]

def is_company_wx(msg):
    '''判断是不是公司微信'''
    print(msg)
    if hasattr(msg, "User"):
        nickname = msg["User"]['NickName']
        if nickname in COMPANY_WX_NICKNAME:
            return True
    return False



def get_response(msg):
    '''实现最简单的与图灵机器人的交互
    构造了要发送给服务器的数据
    '''

    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : random.choice(KEY),
        'info'   : msg,
        'userid' : 'wechat-robot',
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        print(r.get('text'))
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


#文本消息回复
@itchat.msg_register(itchat.content.TEXT) #注册所有可能回复的消息,文本,语音,位置...等
def tuling_reply(msg):
    if is_company_wx(msg):
        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        defaultReply = 'I received: ' + msg['Type']
        # 如果图灵Key出现问题，那么reply将会是None
        reply = get_response(msg['Text'])
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        return reply or defaultReply


#非文本消息回复
@itchat.msg_register([itchat.content.PICTURE, #图片
                      itchat.content.RECORDING, #语音
                      itchat.content.ATTACHMENT,
                      itchat.content.VIDEO #视频
                      ])
def download_files(msg):
    if is_company_wx(msg):
        #msg.download(msg['FileName'])   #这个同样是下载文件的方式
        msg['Text'](msg['FileName'])      #下载文件
        #将下载的文件发送给发送者
        itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg["FileName"]),
                    msg["FromUserName"])





def main():
    '''主函数'''
    def set_enableCmdQR():
        '''设置登录二维码显示形式
            False为打开系统默认的图片查看器显示二维码

            数值为命令行显示二维码
        '''
        os = platform.system()  # Windows, Linux, Darwin
        if os == "Linux":
            return -2
        else:
            return False  # win
    #登录登录
    itchat.auto_login(hotReload=True, #保存用户cookie,下次直接登录
                      enableCmdQR=set_enableCmdQR(), #linux系统命令行二维码,win关闭
                      )

    #启动程序
    itchat.run()



if __name__ == '__main__':
    main()