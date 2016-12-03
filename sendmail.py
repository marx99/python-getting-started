#coding: utf-8  
import requests

def sendmail(title,content):
      
    try:   
        mail_url='http://womai123.com.cn/phpmail/sendmail.php'
        data={
            #'toemail':'1',
            'title':title,
            'content':content
        }
        mail_result = requests.post(mail_url,data=data)
        if(mail_result.text == ''):
            print("Sendmail: Error")
        else:
            print("Sendmail: OK!")   
    except smtplib.SMTPException:
        print("Sendmail: Error")
