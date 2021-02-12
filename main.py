import requests
import json
from prettytable import PrettyTable
import time
import configparser
import re

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0(0x18000029) NetType/WIFI Language/zh_CN'
def getUser(openid):
	global referer
	#获取member_id
	headers = {
	'referer': referer,
	'imprint': openid,
	'user-agent': user_agent,
	}
	data = {
	'openid': openid
	}
	url = 'https://a.welife001.com/getUser'
	response = requests.post(url,headers = headers,data = data)
	#print(response.text)
	json_response = json.loads(response.text)
	class_list = json_response['currentUser']['child_class_list']
	member_id_list = []
	for x in class_list:
		member_id_list.append(x['member_id'])
	#print(member_id_list)
	getParent(openid,member_id_list)
def getParent(openid,member_id_list):
	global referer
	#通过member_id获取未提交的作业
	member_id = "%3A".join(member_id_list)
	url = 'https://a.welife001.com/info/getParent?type=-1&members=' + member_id + '&page=0&size=10&date=-1&hasMore=true&isRecent=true'
	headers = {
	'referer': referer,
	'imprint': openid,
	'user-agent': user_agent,
	}
	response = requests.get(url,headers = headers)
	#print(response.text)
	json_response = json.loads(response.text)
	data = json_response['data']
	homework = []
	for x in data:
		mydict = {}
		mydict['_id'] = x['_id']
		mydict['cid'] = x['cls']
		mydict['title'] = x['title']
		mydict['text_content'] = x['text_content']
		homework.append(mydict)
	table = PrettyTable(['title','text_content'])
	a = 0
	for y in homework:
		table.add_row([str(a) + '--' + y['title'],y['text_content']])
		a = a+1
	print(table)
	number = input('Enter the number:')
	checkNew2Parent(homework[int(number)]['cid'],homework[int(number)]['_id'],openid)
def checkNew2Parent(cls,_id,openid):
	global referer
	url = 'https://a.welife001.com/applet/notify/checkNew2Parent'
	headers = {
		'referer': referer,
		'imprint': openid,
		'user-agent': user_agent,
		'accept-language':'zh-cn',
	}
	data = {
		"extra": 1,
		"cid": cls,
		"cls_ts": int(round(time.time() * 1000)),
		"daka_day": "",
		"member_id": _id,
		"_id": _id,
		"page": 0,
		"size": 10
	}
	response = requests.post(url,headers = headers,data = data)
	json_response = json.loads(response.text)
	json_data = json_response['data']
	if 'datika' in json_data:
		#print('true')
		subjects = json_data['datika']['subjects']
		
		number = 1
		for x in subjects:
			#print(x['detailArrays'])
			answer = []
			for y in x['detailArrays']:
				answer.append(y['rightval'])
			print(str(number) + '：' + '[' + ','.join(answer) + ']')
			number = number + 1
		print('Finished by Snow Total:' + str(len(subjects)))
		input("Please Enter")
	else:
		print("Not find 'datika'")
		input("Please Enter")
def get_referer():
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
	}
	url = 'https://docpub1.docs.qq.com/DYVZJSUp4U2xjR3NG.doc1'
	response = requests.get(url,headers = headers)
	version = re.findall('wx23d8d7ea22039466/(.*?)/page-frame.html',response.text,re.S)[0]
	referer = 'https://servicewechat.com/wx23d8d7ea22039466/' + version + '/page-frame.html'
	return referer
if __name__ == '__main__':
	referer = get_referer()
	config = configparser.ConfigParser()
	config.read('config.ini')
	openid = config.get('User','openid')
	print('By Snow')
	getUser(openid)


	
