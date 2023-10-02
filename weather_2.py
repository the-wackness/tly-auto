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

#百度热搜
head = {}
duurl = "http://top.baidu.com/buzz?b=1"
head["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0"
head["Accept"]= "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
head["Accept-Language"]= "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
head["Connection"] = "keep-alive"
dures = requests.get(duurl , headers = head)
with open("html.txt", "wb") as f:
    f.write(dures.content)
html = etree.parse('html.txt' , etree.HTMLParser(encoding='gbk'))
top_list = html.xpath('//a[@class="list-title"]/text()')
num_search = html.xpath('//span[@class="icon-rise"]/text()')
urlinfo = html.xpath('//a[@class="list-title"]/@href')
i1 = '<a href='+urlinfo[0]+">"+top_list[0]+"</a>   搜索指数为："+num_search[0]
i2 = '<a href='+urlinfo[1]+">"+top_list[1]+"</a>   搜索指数为："+num_search[1]
i3 = '<a href='+urlinfo[2]+">"+top_list[2]+"</a>   搜索指数为："+num_search[2]
i4 = '<a href='+urlinfo[3]+">"+top_list[3]+"</a>   搜索指数为："+num_search[3]
i5 = '<a href='+urlinfo[4]+">"+top_list[4]+"</a>   搜索指数为："+num_search[4]
i6 = '<a href='+urlinfo[5]+">"+top_list[5]+"</a>   搜索指数为："+num_search[5]
i7 = '<a href='+urlinfo[6]+">"+top_list[6]+"</a>   搜索指数为："+num_search[6]
i8 = '<a href='+urlinfo[7]+">"+top_list[7]+"</a>   搜索指数为："+num_search[7]
i9 = '<a href='+urlinfo[8]+">"+top_list[8]+"</a>   搜索指数为："+num_search[8]
i10 = '<a href='+urlinfo[9]+">"+top_list[9]+"</a>   搜索指数为："+num_search[9]
i = i1+'<br>'+i2+'<br>'+i3+'<br>'+i4+'<br>'+i5+'<br>'+i6+'<br>'+i7+'<br>'+i8+'<br>'+i9+'<br>'+i10

#发送邮件
def sendHtml_email(msg):
    '''
    当用户发送信息过来时，发送邮件告知开发者
    :return:
    '''
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'html', 'utf-8')
    message['from'] = mail
    message['to'] = mail
    password = token
    message['subject'] = Header(u'Today', 'utf-8').encode()
    smtp_server = "smtp.qq.com"
    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    # 打印出和SMTP服务器交互的所有信息。
    #server.set_debuglevel(1)
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
p {

    margin: 0 0 10px;

}
h1 {
    font-size: 38.5px;
}
h1 small {
    font-size: 24.5px;
}
h1 small, h2 small, h3 small, h4 small, h5 small, h6 small {
    font-weight: normal;
    line-height: 1;
    color: #999999;
}
body {

    margin: 0;

    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;

    font-size: 14px;

    line-height: 20px;

    color: #333333;

    background-color: #ffffff;

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
 body {

color: #333333;

font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;

font-size: 14px;

line-height: 1.42857;

}



.list-group {

margin-bottom: 20px;

padding-left: 0;

}

.list-group-item:first-child {

border-top-left-radius: 4px;

border-top-right-radius: 4px;

}

a.list-group-item {

color: #555555;

}

a.list-group-item.active, a.list-group-item.active:hover, a.list-group-item.active:focus {

text-dectoration:none;

background-color: #428BCA;

border-color: #428BCA;

color: #FFFFFF;

z-index: 2;

}

a.list-group-item:hover, a.list-group-item:focus{

text-decoration:none;

}

a.list-group-item.active > .badge, .nav-pills > .active > a > .badge {

background-color: #FFFFFF;

color: #428BCA;

}

.list-group-item {

background-color: #FFFFFF;

border: 1px solid #DDDDDD;

display: block;

margin-bottom: -1px;

padding: 10px 15px;

position: relative;

}

.list-group-item > .badge {

float: right;

}

.list-group-item-heading {

margin-bottom: 5px;

margin-top: 0;

}





.panel-body {

padding: 15px;

}




.panel > .list-group {

margin-bottom: 0;

}



.panel > .list-group .list-group-item {

border-width: 1px 0;
}



.panel > .list-group .list-group-item:first-child {

border-top-right-radius: 0;

border-top-left-radius: 0;

}



.panel > .list-group .list-group-item:last-child {

border-bottom: 0;

}



.panel-heading + .list-group .list-group-item:first-child {

border-top-width: 0;

}



.panel > .table,

.panel > .table-responsive > .table {

margin-bottom: 0;

}



.panel > .panel-body + .table,

.panel > .panel-body + .table-responsive {

border-top: 1px solid #dddddd;

}



.panel > .table > tbody:first-child th,

.panel > .table > tbody:first-child td {

border-top: 0;

}



.panel > .table-bordered,

.panel > .table-responsive > .table-bordered {

border: 0;

}



.panel > .table-bordered > thead > tr > th:first-child,

.panel > .table-responsive > .table-bordered > thead > tr > th:first-child,

.panel > .table-bordered > tbody > tr > th:first-child,

.panel > .table-responsive > .table-bordered > tbody > tr > th:first-child,

.panel > .table-bordered > tfoot > tr > th:first-child,

.panel > .table-responsive > .table-bordered > tfoot > tr > th:first-child,

.panel > .table-bordered > thead > tr > td:first-child,

.panel > .table-responsive > .table-bordered > thead > tr > td:first-child,

.panel > .table-bordered > tbody > tr > td:first-child,

.panel > .table-responsive > .table-bordered > tbody > tr > td:first-child,

.panel > .table-bordered > tfoot > tr > td:first-child,

.panel > .table-responsive > .table-bordered > tfoot > tr > td:first-child {

border-left: 0;

}



.panel > .table-bordered > thead > tr > th:last-child,

.panel > .table-responsive > .table-bordered > thead > tr > th:last-child,

.panel > .table-bordered > tbody > tr > th:last-child,

.panel > .table-responsive > .table-bordered > tbody > tr > th:last-child,

.panel > .table-bordered > tfoot > tr > th:last-child,

.panel > .table-responsive > .table-bordered > tfoot > tr > th:last-child,

.panel > .table-bordered > thead > tr > td:last-child,

.panel > .table-responsive > .table-bordered > thead > tr > td:last-child,

.panel > .table-bordered > tbody > tr > td:last-child,

.panel > .table-responsive > .table-bordered > tbody > tr > td:last-child,

.panel > .table-bordered > tfoot > tr > td:last-child,

.panel > .table-responsive > .table-bordered > tfoot > tr > td:last-child {

border-right: 0;

}



.panel > .table-bordered > thead > tr:last-child > th,

.panel > .table-responsive > .table-bordered > thead > tr:last-child > th,

.panel > .table-bordered > tbody > tr:last-child > th,

.panel > .table-responsive > .table-bordered > tbody > tr:last-child > th,

.panel > .table-bordered > tfoot > tr:last-child > th,

.panel > .table-responsive > .table-bordered > tfoot > tr:last-child > th,

.panel > .table-bordered > thead > tr:last-child > td,

.panel > .table-responsive > .table-bordered > thead > tr:last-child > td,

.panel > .table-bordered > tbody > tr:last-child > td,

.panel > .table-responsive > .table-bordered > tbody > tr:last-child > td,

.panel > .table-bordered > tfoot > tr:last-child > td,

.panel > .table-responsive > .table-bordered > tfoot > tr:last-child > td {

border-bottom: 0;

}


h1, h2, h3 {

line-height: 40px;

}

.hr0{ height:1px;border:none;border-top:1px dashed #0066CC;}

h1 {

font-size: 38.5px;

}



h2 {

font-size: 31.5px;

}



h3 {

font-size: 24.5px;

}



h4 {

font-size: 17.5px;

}



h5 {

font-size: 14px;

}



h6 {

font-size: 11.9px;

}



h1 small {

font-size: 24.5px;

}



h2 small {

font-size: 17.5px;

}



h3 small {

font-size: 14px;

}



h4 small {

font-size: 14px;

}



pre {

display: block;

padding: 9.5px;

margin: 0 0 10px;

font-size: 13px;

line-height: 20px;

word-break: break-all;

word-wrap: break-word;

white-space: pre;

white-space: pre-wrap;

background-color: #f5f5f5;

border: 1px solid #ccc;

border: 1px solid rgba(0,  0,  0,  0.15);

-webkit-border-radius: 4px;

-moz-border-radius: 4px;

border-radius: 4px;

}

pre.prettyprint {

margin-bottom: 20px;

}



pre code {

padding: 0;

color: inherit;

white-space: pre;

white-space: pre-wrap;

background-color: transparent;

border: 0;

}



.pre-scrollable {

max-height: 340px;

overflow-y: scroll;

}



.label, .badge {

display: inline-block;

padding: 2px 4px;

font-size: 11.844px;

font-weight: bold;

line-height: 14px;

color: #ffffff;

vertical-align: baseline;

white-space: nowrap;

text-shadow: 0 -1px 0 rgba(0,  0,  0,  0.25);

background-color: #5cb85c;

}



.label {

-webkit-border-radius: 3px;

-moz-border-radius: 3px;

border-radius: 3px;

}



.badge {

padding-left: 9px;

padding-right: 9px;

-webkit-border-radius: 9px;

-moz-border-radius: 9px;

border-radius: 9px;

}





.btn .label, .btn .badge {

position: relative;

top: -1px;

}



.btn-mini .label, .btn-mini .badge {

top: 0;

}



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



.table caption+thead tr:first-child th, .table caption+thead tr:first-child td, .table colgroup+thead tr:first-child th, .table colgroup+thead tr:first-child td, .table thead:first-child tr:first-child th, .table thead:first-child tr:first-child td {

border-top: 0;

}



.table tbody+tbody {

border-top: 2px solid #dddddd;

}



.table .table {

background-color: #ffffff;

}



.table-condensed th, .table-condensed td {

padding: 4px 5px;

}



.table-bordered {

border: 1px solid #dddddd;

border-collapse: separate;

*border-collapse: collapse;

border-left: 0;

-webkit-border-radius: 4px;

-moz-border-radius: 4px;

border-radius: 4px;

}

.table-bordered th, .table-bordered td {

border-left: 1px solid #dddddd;

}



.table-bordered caption+thead tr:first-child th, .table-bordered caption+tbody tr:first-child th, .table-bordered caption+tbody tr:first-child td, .table-bordered colgroup+thead tr:first-child th, .table-bordered colgroup+tbody tr:first-child th, .table-bordered colgroup+tbody tr:first-child td, .table-bordered thead:first-child tr:first-child th, .table-bordered tbody:first-child tr:first-child th, .table-bordered tbody:first-child tr:first-child td {

border-top: 0;

}



.table-bordered thead:first-child tr:first-child>th:first-child, .table-bordered tbody:first-child tr:first-child>td:first-child, .table-bordered tbody:first-child tr:first-child>th:first-child {

-webkit-border-top-left-radius: 4px;

-moz-border-radius-topleft: 4px;

border-top-left-radius: 4px;

}



.table-bordered thead:first-child tr:first-child>th:last-child, .table-bordered tbody:first-child tr:first-child>td:last-child, .table-bordered tbody:first-child tr:first-child>th:last-child {

-webkit-border-top-right-radius: 4px;

-moz-border-radius-topright: 4px;

border-top-right-radius: 4px;

}



.table-bordered thead:last-child tr:last-child>th:first-child, .table-bordered tbody:last-child tr:last-child>td:first-child, .table-bordered tbody:last-child tr:last-child>th:first-child, .table-bordered tfoot:last-child tr:last-child>td:first-child, .table-bordered tfoot:last-child tr:last-child>th:first-child {

-webkit-border-bottom-left-radius: 4px;

-moz-border-radius-bottomleft: 4px;

border-bottom-left-radius: 4px;

}



.table-bordered thead:last-child tr:last-child>th:last-child, .table-bordered tbody:last-child tr:last-child>td:last-child, .table-bordered tbody:last-child tr:last-child>th:last-child, .table-bordered tfoot:last-child tr:last-child>td:last-child, .table-bordered tfoot:last-child tr:last-child>th:last-child {

-webkit-border-bottom-right-radius: 4px;

-moz-border-radius-bottomright: 4px;

border-bottom-right-radius: 4px;

}



.table-bordered tfoot+tbody:last-child tr:last-child td:first-child {

-webkit-border-bottom-left-radius: 0;

-moz-border-radius-bottomleft: 0;

border-bottom-left-radius: 0;

}



.table-bordered tfoot+tbody:last-child tr:last-child td:last-child {

-webkit-border-bottom-right-radius: 0;

-moz-border-radius-bottomright: 0;

border-bottom-right-radius: 0;

}



.table-bordered caption+thead tr:first-child th:first-child, .table-bordered caption+tbody tr:first-child td:first-child, .table-bordered colgroup+thead tr:first-child th:first-child, .table-bordered colgroup+tbody tr:first-child td:first-child {

-webkit-border-top-left-radius: 4px;

-moz-border-radius-topleft: 4px;

border-top-left-radius: 4px;

}



.table-bordered caption+thead tr:first-child th:last-child, .table-bordered caption+tbody tr:first-child td:last-child, .table-bordered colgroup+thead tr:first-child th:last-child, .table-bordered colgroup+tbody tr:first-child td:last-child {

-webkit-border-top-right-radius: 4px;

-moz-border-radius-topright: 4px;

border-top-right-radius: 4px;

}



.table-striped tbody>tr:nth-child(odd)>td, .table-striped tbody>tr:nth-child(odd)>th {

background-color: #f9f9f9;

}



.table-hover tbody tr:hover>td, .table-hover tbody tr:hover>th {

background-color: #f5f5f5;

}



table td[class*="span"], table th[class*="span"], .row-fluid table td[class*="span"], .row-fluid table th[class*="span"] {

display: table-cell;

float: none;

margin-left: 0;

}



.table td.span1, .table th.span1 {

float: none;

width: 44px;

margin-left: 0;

}



.table td.span2, .table th.span2 {

float: none;

width: 124px;

margin-left: 0;

}



.table td.span3, .table th.span3 {

float: none;

width: 204px;

margin-left: 0;

}



.table td.span4, .table th.span4 {

float: none;

width: 284px;

margin-left: 0;

}



.table td.span5, .table th.span5 {

float: none;

width: 364px;

margin-left: 0;

}



.table td.span6, .table th.span6 {

float: none;

width: 444px;

margin-left: 0;

}



.table td.span7, .table th.span7 {

float: none;

width: 524px;

margin-left: 0;

}



.table td.span8, .table th.span8 {

float: none;

width: 604px;

margin-left: 0;

}



.table td.span9, .table th.span9 {

float: none;

width: 684px;

margin-left: 0;

}



.table td.span10, .table th.span10 {

float: none;

width: 764px;

margin-left: 0;

}



.table td.span11, .table th.span11 {

float: none;

width: 844px;

margin-left: 0;

}



.table td.span12, .table th.span12 {

float: none;

width: 924px;

margin-left: 0;

}



.table tbody tr.success>td {

background-color: #dff0d8;

}

.table tbody tr.error>td {

background-color: #f2dede;

}

.table tbody tr.warning>td {

background-color: #fcf8e3;

}

.table tbody tr.info>td {

background-color: #d9edf7;

}

.table-hover tbody tr.success:hover>td {

background-color: #d0e9c6;

}

.table-hover tbody tr.error:hover>td {

background-color: #ebcccc;

}

.table-hover tbody tr.warning:hover>td {

background-color: #faf2cc;

}



.table-hover tbody tr.info:hover>td {

background-color: #c4e3f3;

}












</style>
<div class="container-fluid">
	<div class="row clearfix">
		<div class="col-md-12 column">
			<h3 class="text-info">
				今天也是美好的一天
            </h3> <span class="label label-primary">更新时间'''+timeupdate+'''</span><br><br>
			
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
                        </th><th>
							概要
                        </th>
                   
                    
				</tr></thead>
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
				</tr></tbody>
			</table>
		</div>
	</div>
</div>





<div class="col-md-12 columnr-fluid">
			<h2>
              百度热搜榜TOP10
			</h2>
			<p>
			点击链接查看详情<br>
			'''+i+''' 
			</p>
		</div>
			</div>









<hr class="hr0" />
<div class="page-header">
<center>
				<h1>
					《'''+tishi+''' 》<small>'''+dynasty+' '+author+'''</small>
				</h1>
				<h3>
				'''+reshi+''' 
				</h3>
</center>
<br>




<hr class="hr0" />
<center>
				<h1>
					END
				</h1>
				<h3>
				👌
				</h3>
</center>
	''')
