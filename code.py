#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import requests
import base64
import sys
import serial
import os 
import time
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib
import time
GPIO.setmode(GPIO.BCM) #将GPIO编程方式设置为BCM式
# 输出模式
GPIO.setup(14, GPIO.OUT) #将GPIO引脚11设置为输出引脚
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT) 
def send_mail(subject):
email_host = 'smtp.163.com'
sender = '*****@163.com' 
password = '**********'#个人密码
receiver = '*****@qq.com' 
CCADDR = ['*****@163.com']
TOADDR = ['*****@qq.com']
msg = MIMEMultipart()
22
msg['Subject'] = subject 
msg['From'] = '*********@163.com' #从的163个人邮箱发送 
msg['To'] = '*********@qq.com' #从的QQ邮箱发送
msg['Cc'] = ', '.join(CCADDR)
signature = '''
\n\t this is auto test report!
\n\t you don't need to follow
'''
mail_msg = '''
<p>\n\t </p>
'''
msg.attach(MIMEText(mail_msg, 'text', 'utf-8'))
fp = open(r'image.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)
ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)
image = MIMEImage(open(r'/home/pi/Desktop/image.jpg', 'rb').read(), _subtype=subtype)
image.add_header('Content-Disposition', 'attachment', filename='实时图像.jpg')
msg.attach(image)
#file = MIMEBase(maintype, subtype)
#file.set_payload(open(r'C:\Users\Administrator\Desktop\320k.txt', 'rb').read())
#file.add_header('Content-Disposition', 'attachment', filename='test.txt')
#encoders.encode_base64(file)
#msg.attach(file)
smtp = smtplib.SMTP()
smtp.connect(email_host, 25)
smtp.login(sender, password)
smtp.sendmail(sender, TOADDR+CCADDR, msg.as_string())
smtp.quit()
print('success')
#引入计时time函数
# BOARD编号方式，基于插座引脚编号
def getaccess_token():
## 获取access_token
host='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=cfX2EfL35z2DZG2oPyqukzB3&client_secret=*****************#
获取个人的开发者id密码这里用星号代替密码
23
header_1 = {'Content-Type':'application/json; charset=UTF-8'}
request=requests.post(host,headers =header_1)
access_token=request.json()['access_token']
print(access_token)
return access_token
def take_picture():
#拍摄当前图片 
camera.start_preview()
time.sleep(0.5)
camera.capture('image.jpg')
camera.stop_preview()
def open_pic():
#打开工程拍摄的图片并转换成字符串
f = open('image.jpg', 'rb')
img = base64.b64encode(f.read())
return img
def search (img,access_token):
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
params =
{"image":img,"image_type":"BASE64","group_id_list":"pass","quality_control":"LOW","liveness_control":"NORMAL"}
request_url = request_url + "?access_token=" + access_token
##发送数据利用requests.post（）的方法
response = requests.post(request_url, data=params)
##输出json数据
output = response.json()
return output
def chuli (output):
# print(outpu
#print(type(output)) ##输出数据类型为－字典
if output['error_msg'] == 'SUCCESS':
##判断是否成功
##找到字典里的result－以及内层字典里的user_list
user_list= output['result']['user_list']
#print(user_list)
##输出数据类型，发现其为列表
print(type(user_list))
##利用列表的检索方式找到列表里的人脸检测分数－score
score = user_list[0]['score']
name = user_list[0]['user_id']
24
if(score>80):
print(name,"pass")
##串口发送
#ser.write(str(score).encode()) 
#panduan(score)
user = user_list[0]['user_info']
time.sleep(1)
print(user)
GPIO.output(15, True)
GPIO.output(14, GPIO.LOW) 
#ser.write(user.encode())
else:
print(output['error_msg'])#输出错误信息
print(type(output['error_msg']))#输出错误信息
GPIO.output(14, True)#控制LED灯亮
GPIO.output(15, GPIO.LOW)#控制LED灯灭
GPIO.output(18, GPIO.LOW)#控制LED灯灭
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
subject = now + '可疑人员报警'
send_mail(subject)
#("python /home/pi/Desktop/mail3.py")
#ser.write(output['error_msg'].encode())
"""
反馈的数据：利用他来解析
可知此次的人脸对比分数为：93分
{'error_code': 0, 'error_msg': 'SUCCESS', 'timestamp': , 'log_id': , 'cached': 0,
'result': {'face_token': ,
'user_list': [{ '
''}]}}
"""
#def panduan(score): 
# if score > 80:
#print(type(score))
#ser.write(str(score).encode()) 
# else :
# ser.write(b'2')
#def led():
## led
if __name__ == '__main__':
25
#ser = serial.Serial('/dev/ttyS0',115200,timeout=1)
#ser.close()
#ser.open()
GPIO.output(15, GPIO.LOW)
GPIO.output(14, GPIO.LOW)
print("串口已开启")
camera = PiCamera()
count=0#计数归0
access_token=getaccess_token()
while True :
take_picture()
img=open_pic()
output = search(img,access_token)
chuli(output)
count=count+1#计数加一
print(count)
#加入自动重启命令，防止程序运行时间过长死机
if count == 2000 :
os.system('sudo reboot')#重启
count = 0
