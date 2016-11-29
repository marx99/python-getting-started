# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import requests
from app import app
import time
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
import os

engine = Engine(app)

@engine.define
def printtest(**params):
    if 'name' in params:
        print ('Hello, {}!'.format(params['name']))
    else:
        #log.info('log.info')
        print ('Hello, LeanCloud!')

@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')

def sendmail_local(subject,content):
    sender = os.environ['sendmail_to_mail'] 
    receiver = os.environ['sendmail_from_mail'] 
    #subject = 'python email test'  
    
    smtpserver = os.environ['sendmail_smtpserver']
    username = os.environ['sendmail_from_mail']  
    password = os.environ['sendmail_from_password']  
    
    #os.environ['LEANCLOUD_APP_ID']
    
    msg = MIMEText(content,'text','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
    msg['Subject'] = Header(subject, 'utf-8')  
      
    try:   
        smtp = smtplib.SMTP()  
        smtp.connect(smtpserver)  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msg.as_string())  
        smtp.quit()  
        print('sendmail OK!')
    except smtplib.SMTPException:
        print ("Error: sendmail error")

@engine.define
def qiandao_jd():
    
    headers={
        'Host': 'gw-e.jd.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'JDRead 2.6.3 rv: (android; android OS 4.4.4; zh_CN)',
        'Cookie': 'wskey=AAFYLGPZAEBR6ylOakGVtcRiV_zeGiN1ktIVhKxd2QLVy67AGwGJnSf011hv4txqqVqCQRMTelqMkZzmqCsLT4ZWPD2ZLtPj',
        'Cookie2': '$Version=1',
        'Accept-Encoding': 'gzip'    
    }
    geturl = 'https://gw-e.jd.com/client.action?build=&osVersion=4.4.4&jds=' + str(round(time.time() * 1000)) + '&functionId=signGetScore&clientVersion=2.6.3&subunionId=yd001&appId=1&os=android&client=android&uuid=867622023933180-9c99a0b5ebd5&unionId=350268299&model=2014811&brand=Xiaomi&screen=720*1280'
    
#    print(geturl)
    jd_result = requests.get(geturl,headers = headers,verify=False)
    print(jd_result.json())  
    sendmail_local('qiandao_jd',jd_result.json())
    
@engine.define
def qiandao_115_xiaohao(**params):
    
    #115签到
    #小号：13555...
    headers={
        'Host': 'web.api.115.com',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Origin': 'http://web.api.115.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; 2014811 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 115disk/6.2.1',
        'Referer': 'http://web.api.115.com/bridge_2.0.html?namespace=FS.DataSrv&api=UDataAPI&_t=v5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'ssov_590519292=0_590519292_e41cbbf54df9d773385c0492dc79c354; OOFA=SEID=7eb6ba018b0be0e9869af0ed02957d3cc4e96181543d97ab691c2aa195349a0abb650769e034a4b0ea53c142be74ddbbb29104fcc6465c937894a842; SEID=7eb6ba018b0be0e9869af0ed02957d3cc4e96181543d97ab691c2aa195349a0abb650769e034a4b0ea53c142be74ddbbb29104fcc6465c937894a842; UID=590519292_F1_1477144725; CID=3eee667f5650c9315a1961ec7d5efcff',
    }
    
    url115 = 'http://web.api.115.com/user/sign'
    s = requests.Session()
    r1= s.post(url115,headers=headers)
    print ('qiandao_115_135555 ',r1.status_code,r1.json())

    #geturl = 'http://web.api.115.com/user/sign?start=2016-11-01&_=1478610072924'
    geturl = 'http://web.api.115.com/user/sign?start='+ time.strftime('%Y-%m-01') +'&_=' + str(round(time.time()*1000))
    getr = requests.get(geturl,headers = headers)
    
    print(getr.json())
    sendmail_local('qiandao_115_135555',str(r1.json()) + str(getr.json()))
    
@engine.define
def qiandao_guorn(**params):
    
    headers={
        'Host': 'guorn.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,zh-TW;q=0.4',
        'Cookie': 'uname="2|1:0|10:1475754767|5:uname|8:dG9zdGVt|a9f78d0bc37d7cce8652cbe6b4f904d414cd53f29b17dbd8d6eebb4828c61fa0"; account="2|1:0|10:1475754767|7:account|28:bWF4aW5nemhlOTlAMTI2LmNvbQ==|48ae16eeb3ab343544542f84f01045af70ce45fa5dd9bfd36eb285959eee3ee9"; user="2|1:0|10:1475754767|4:user|4:NDk0|d77bccb65013a45b26abc294f7d142bd0dfdabdf514092407f11ad1629259bc4"; token="2|1:0|10:1475754767|5:token|76:YzliNDZjMmE5NGE0YjA4YzRlNDg2M2U3OWM2NGUyZDk4ZGZjYWFjYTNjNThmMzlhYTI1MDUwNjk=|f67b92df4164293568d3a7826c6e05a84ff10d909c013aff6f57c54b503dc7be"; IPUSH_TS=1477397347; Hm_lvt_40ee94ccee2cf1051316f73e3fbcf8ac=1476880821,1476969871,1477399329,1477752503; _ga=GA1.2.1511779949.1442747089',
    }
    
    s = requests.Session()
    r1= s.post("https://guorn.com/score/signup",headers=headers,verify=False)

    if r1.status_code ==200:
        print ('qiandao_guorn OK')
    else:
        print ('qiandao_guorn error:' + r1.status_code)

       
#115 qiandao
cookies = {
    '15942888': 'OOFA=UID=4158054_F1_1479007096; UID=4158054_F1_1479007096; CID=9cd9bb99b3101593697536c1b6a0e233; SEID=a94f79f65a4bed45cbff606930239896f115df9d81b7bafae1f34d66b87108123c35ceed4adb846076d9e1024d5c82721e2e62fcea6693104e3378ad; ssov_4158054=0_4158054_e4b7e5bba4f3176fa4343b12dd42aa3b',
    '13555925': 'ssov_590519292=0_590519292_e41cbbf54df9d773385c0492dc79c354; OOFA=SEID=7eb6ba018b0be0e9869af0ed02957d3cc4e96181543d97ab691c2aa195349a0abb650769e034a4b0ea53c142be74ddbbb29104fcc6465c937894a842; SEID=7eb6ba018b0be0e9869af0ed02957d3cc4e96181543d97ab691c2aa195349a0abb650769e034a4b0ea53c142be74ddbbb29104fcc6465c937894a842; UID=590519292_F1_1477144725; CID=3eee667f5650c9315a1961ec7d5efcff',
    '18640815': 'CID=75a2513cf5f55d0eb20510d701e354ed; SEID=e4bee56b359d5fbe50814a98857617657ffda3200e72e804f66a9a8e22edaf851a000ee6b79bd77e2630fb9c784bfa618700d78d5f4039bfad9ab17f; ssov_592637961=0_592637961_ed7d57ec15b95004e985cae17b31a407; UID=592637961_H1_1478431292',
    '15694636714': 'CID=d88b040909b38a3d14c7fa78cc6032aa; SEID=354b4a3fc4f04389f3e5e5814e92f5d40e46893a0fcc55865d1de79f21ccb405acd2c1e73b9f311f1476cbeceebef8c5539f3f489923737acb6d2330; ssov_592637924=0_592637924_890a4b2e72593f4e25ee9a16149b45d1; UID=592637924_H1_1478958011'
}

def qiandao_115(userid):
     # 签到
   
    #login
    sign_headers = {
        'Host': '115.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; 2014811 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 115disk/6.2.1',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': cookies[userid],
        'X-Requested-With': 'com.ylmf.androidclient'    
    }
    sign_url = 'http://115.com/?ct=sign'
    
    sign_str = requests.get(sign_url,headers = sign_headers)
    
    print('sign ' + userid,sign_str.status_code)
    
    time.sleep(10)
    
    #post
    postheaders = {
        'Host': 'web.api.115.com',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-cn',
        'Accept': '*/*',
        'Origin': 'http://web.api.115.com',
        'Content-Length': '0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; 2014811 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 115disk/6.2.1',
        #'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 UPad/6.2.0',
        'Referer': 'http://web.api.115.com/bridge_2.0.html?namespace=FS.DataSrv&api=UDataAPI&_t=v5',
        'Cookie': cookies[userid]
    }
    
    posturl='http://web.api.115.com/user/sign'
    postr = requests.post(posturl,headers = postheaders)
    print( 'post ' + userid,postr.status_code,postr.json())
    
    time.sleep(2)
    
    #get result 
    #geturl = 'http://web.api.115.com/user/sign?start=2016-11-01&_=1478610072924'
    geturl = 'http://web.api.115.com/user/sign?start='+ time.strftime('%Y-%m-01') +'&_=' + str(round(time.time()*1000))
    #result output
    get_str = requests.get(geturl,headers = postheaders)
    print( 'get result ' + userid,get_str.status_code,get_str.json())
    
    #send mail
    sendmail_local('115_qiandao:' + userid , str(postr.json()) + str(get_str.json()))
 

@engine.define
def qiandao_115_15694636714():
    qiandao_115('15694636714')
    
@engine.define
def send_mail_test():
    #sendmail_local('title标题','虫哦你特纳那天')
    sender = 'from@runoob.com'
    receivers = ['15942888252@139.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
