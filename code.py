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
GPIO.setmode(GPIO.BCM) #��GPIO��̷�ʽ����ΪBCMʽ
# ���ģʽ
GPIO.setup(14, GPIO.OUT) #��GPIO����11����Ϊ�������
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT) 
def send_mail(subject):
email_host = 'smtp.163.com'
sender = '*****@163.com' 
password = '**********'#��������
receiver = '*****@qq.com' 
CCADDR = ['*****@163.com']
TOADDR = ['*****@qq.com']
msg = MIMEMultipart()
22
msg['Subject'] = subject 
msg['From'] = '*********@163.com' #�ӵ�163�������䷢�� 
msg['To'] = '*********@qq.com' #�ӵ�QQ���䷢��
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
image.add_header('Content-Disposition', 'attachment', filename='ʵʱͼ��.jpg')
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
#�����ʱtime����
# BOARD��ŷ�ʽ�����ڲ������ű��
def getaccess_token():
## ��ȡaccess_token
host='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=cfX2EfL35z2DZG2oPyqukzB3&client_secret=*****************#
��ȡ���˵Ŀ�����id�����������ǺŴ�������
23
header_1 = {'Content-Type':'application/json; charset=UTF-8'}
request=requests.post(host,headers =header_1)
access_token=request.json()['access_token']
print(access_token)
return access_token
def take_picture():
#���㵱ǰͼƬ 
camera.start_preview()
time.sleep(0.5)
camera.capture('image.jpg')
camera.stop_preview()
def open_pic():
#�򿪹��������ͼƬ��ת�����ַ���
f = open('image.jpg', 'rb')
img = base64.b64encode(f.read())
return img
def search (img,access_token):
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
params =
{"image":img,"image_type":"BASE64","group_id_list":"pass","quality_control":"LOW","liveness_control":"NORMAL"}
request_url = request_url + "?access_token=" + access_token
##������������requests.post�����ķ���
response = requests.post(request_url, data=params)
##���json����
output = response.json()
return output
def chuli (output):
# print(outpu
#print(type(output)) ##�����������Ϊ���ֵ�
if output['error_msg'] == 'SUCCESS':
##�ж��Ƿ�ɹ�
##�ҵ��ֵ����result���Լ��ڲ��ֵ����user_list
user_list= output['result']['user_list']
#print(user_list)
##����������ͣ�������Ϊ�б�
print(type(user_list))
##�����б�ļ�����ʽ�ҵ��б����������������score
score = user_list[0]['score']
name = user_list[0]['user_id']
24
if(score>80):
print(name,"pass")
##���ڷ���
#ser.write(str(score).encode()) 
#panduan(score)
user = user_list[0]['user_info']
time.sleep(1)
print(user)
GPIO.output(15, True)
GPIO.output(14, GPIO.LOW) 
#ser.write(user.encode())
else:
print(output['error_msg'])#���������Ϣ
print(type(output['error_msg']))#���������Ϣ
GPIO.output(14, True)#����LED����
GPIO.output(15, GPIO.LOW)#����LED����
GPIO.output(18, GPIO.LOW)#����LED����
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
subject = now + '������Ա����'
send_mail(subject)
#("python /home/pi/Desktop/mail3.py")
#ser.write(output['error_msg'].encode())
"""
���������ݣ�������������
��֪�˴ε������Աȷ���Ϊ��93��
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
print("�����ѿ���")
camera = PiCamera()
count=0#������0
access_token=getaccess_token()
while True :
take_picture()
img=open_pic()
output = search(img,access_token)
chuli(output)
count=count+1#������һ
print(count)
#�����Զ����������ֹ��������ʱ���������
if count == 2000 :
os.system('sudo reboot')#����
count = 0
