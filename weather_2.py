import json
import requests
import csv
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from lxml import etree
import os

mail = os.environ["MAIL"]
password = os.environ["PWD"]
token = os.environ["TOKEN"]

#天气预报
sojsonurl = 'http://t.weather.sojson.com/api/weather/city/101020100'
# 101020100  上海
# 101010100  北京
# 101181601  zmd
# 101181301  py
sojson = requests.get(sojsonurl) 
sojson = json.loads(sojson.text)  
datas = sojson['data']['forecast']  #天气情况
today = sojson['data']              #天气实况
time = sojson['cityInfo']           #获取更新时间
timeupdate = time['updateTime']     #获取更新时间
print ("更新时间:",timeupdate)
shidu = today['shidu']
pm25 = today['pm25']
quality = today['quality']
wendu = today['wendu']
ganmao = today['ganmao']
info = '空气湿度:'+str(shidu)+' PM2.5浓度'+str(pm25)+' 空气质量:'+str(quality)+' 温度:'+str(wendu)+'℃ '+str(ganmao)


#3天天气		
oneday = datas[0]['ymd']+"("+datas[0]['week']+")"+" "+datas[0]['type']+" "+datas[0]['high']+" "+datas[0]['low']+" "+datas[0]['fx']+datas[0]['fl']+" "+"日出时间:"+datas[0]['sunrise']+" "+"日落时间:"+datas[0]['sunset']+" "+datas[0]['notice']
twoday = datas[1]['ymd']+"("+datas[1]['week']+")"+" "+datas[1]['type']+" "+datas[1]['high']+" "+datas[1]['low']+" "+datas[1]['fx']+datas[1]['fl']+" "+"日出时间:"+datas[1]['sunrise']+" "+"日落时间:"+datas[1]['sunset']+" "+datas[1]['notice']
threeday = datas[2]['ymd']+"("+datas[2]['week']+")"+" "+datas[2]['type']+" "+datas[2]['high']+" "+datas[2]['low']+" "+datas[2]['fx']+datas[2]['fl']+" "+"日出时间:"+datas[2]['sunrise']+" "+"日落时间:"+datas[2]['sunset']+" "+datas[2]['notice']
fourday = datas[3]['ymd']+"("+datas[3]['week']+")"+" "+datas[3]['type']+" "+datas[3]['high']+" "+datas[3]['low']+" "+datas[3]['fx']+datas[3]['fl']+" "+"日出时间:"+datas[3]['sunrise']+" "+"日落时间:"+datas[3]['sunset']+" "+datas[3]['notice']


#每日古诗
shi = requests.get('https://v2.jinrishici.com/one.json')
shi = json.loads(shi.text)
tishi = shi['data']['origin']['title']
reshi = shi['data']['content']
dynasty = shi['data']['origin']['dynasty']
author = shi['data']['origin']['author']

#发送邮件
def sendHtml_email(msg):
    '''
    当用户发送信息过来时，发送邮件告知开发者
    :return:
    '''
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'html', 'utf-8')
    message['from'] = mail		#发件人
    message['to'] = mail		#收件人
    password = token			#授权码
    message['subject'] = Header(u'Today', 'utf-8').encode()
    smtp_server = "smtp.qq.com"
    server = smtplib.SMTP(smtp_server, 25)  
 
    # 登录SMTP服务器
    server.login(mail, password)
    # 发邮件，由于可以一次发给多个人，所以传入一个list;
    # 邮件正文是一个str，as_string()把MIMEText对象变成str。
    #server.sendmail(message['from'],receivers, message.as_string())
    server.sendmail(message['from'],[message['to']], message.as_string())
    server.quit()






if __name__ == '__main__':
    sendHtml_email('''
<style type="text/css">

.label{
display: inline-block;
padding: 2px 4px;
font-size: 11.844px;
font-weight: bold;
line-height: 14px;
color: #ffffff;
vertical-align: baseline;
white-space: nowrap;
text-shadow: 0 -1px 0 rgba(0,  0,  0,  0.25);
background-color: #9e77c4;
}
.label {
-webkit-border-radius: 3px;
-moz-border-radius: 3px;
border-radius: 3px;
}
h3 small {
font-size: 13px;
}
h2 {
    font-size: 31.5px;
}
h1, h2, h3 {
    line-height: 40px;
}
h1, h2, h3, h4, h5, h6, .h1, .h2, .h3, .h4, .h5, .h6 {
    color: inherit;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-weight: 500;
    line-height: 1.1;
}

tr,td{font-size:12px;color:#000000;background:#ffffff;}

table {
max-width: 100%;
background-color: transparent;
border-collapse: collapse;
border-spacing: 0;
}



.table {
width: 100%;
margin-bottom: 20px;
}

.table th, .table td {
padding: 8px;
line-height: 20px;
text-align: left;
vertical-align: top;
border-top: 1px solid #dddddd;
}



.table th {
font-weight: bold;
}



.table thead th {
vertical-align: bottom;
}

</style>
<div class="container-fluid">
<div class="row clearfix">
		<div class="col-md-12 column">
			<p style="diaplay:inline-block;font-size: 18px;">	上海天气    </p> 
                <span class="label label-primary" style="text-align:right;">更新时间 '''+timeupdate+'''</span><br>
  
		<table class="table table-striped">
			<thead>
			<tr>
				<th>
					时间
				</th>
				<th>
					天气
				</th>
				<th>
					温度
				</th>
				<th>
					风向
				</th>
				<th>
					概要
				</th>
   
	    
			</tr>
    			</thead>
			<tbody>
			<tr>
				<td>
					'''+datas[0]['ymd']+"("+datas[0]['week']+")"+'''【今天】
				</td>
				<td>
					'''+datas[0]['type']+'''
				</td>
				<td>
					'''+datas[0]['high']+" "+datas[0]['low']+'''
				</td>
				<td>
					'''+datas[0]['fx']+datas[0]['fl']+'''
				<td>
					'''+datas[0]['notice']+'''
				</td>
			</tr>
		<tr class="success">
                        <td>
				'''+datas[1]['ymd']+"("+datas[1]['week']+")"+'''
			</td>
			<td>
				'''+datas[1]['type']+'''
			</td>
			<td>
				'''+datas[1]['high']+" "+datas[1]['low']+'''
			</td>
			<td>
				'''+datas[1]['fx']+datas[1]['fl']+'''
                        </td>
                        <td>
				'''+datas[1]['notice']+'''
			</td>
		</tr>
		<tr class="error">
			<td>
				'''+datas[2]['ymd']+"("+datas[2]['week']+")"+'''
			</td>
			<td>
				'''+datas[2]['type']+'''
			</td>
			<td>
				'''+datas[2]['high']+" "+datas[2]['low']+'''
			</td>
			<td>
				'''+datas[2]['fx']+datas[2]['fl']+'''
                        </td>
                        <td>
				'''+datas[2]['notice']+'''
			</td>
		</tr>
		<tr class="warning">
			<td>
				'''+datas[3]['ymd']+"("+datas[3]['week']+")"+'''
			</td>
			<td>
				'''+datas[3]['type']+'''
			</td>
			<td>
				'''+datas[3]['high']+" "+datas[3]['low']+'''
			</td>
			<td>
				'''+datas[3]['fx']+datas[3]['fl']+'''
                        </td>
                        <td>
				'''+datas[3]['notice']+'''
			</td>
		</tr>
  	</tbody>
	</table>
	</div>
	</div>
</div>










<hr class="hr0" />
<div class="page-header">
<center>
				<h3>《'''+tishi+''' 》<br><small>'''+dynasty+' '+author+'''</small></h3>
				<h5>'''+reshi+'''</h5>
</center>
<br>




<hr class="hr0" />
<center>
				<h2>
					END
				</h2>
				
</center>
	''')
