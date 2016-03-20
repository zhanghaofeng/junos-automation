#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import urllib2
import urllib
import json
import httplib
import re
import datetime
import sys
import os
import time

def getDatetimeFromStr(s):
	format = '%Y-%m-%d %H:%M:%S'
	return datetime.datetime.strptime(s, format)

def previous_hour():
	dt = datetime.datetime.now()
	dt2 = dt.strftime('%Y-%m-%d %H')+":00:00"
	return getDatetimeFromStr(dt2)-datetime.timedelta(hours=1)

def wechat_send(token, wechat_msg, users):
	data={
		"touser":users,
		"msgtype":"text",
		"agentid":"0",
		"text":{
			"content":wechat_msg,
		},
	}
	data=json.dumps(data,ensure_ascii=False)
	msm_post='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'%token
	f=urllib2.urlopen(msm_post,data)
	content =f.read()
	f.close
	print content

if __name__ == '__main__':
	
	reload(sys)
	sys.setdefaultencoding('utf8')
	# argv[1] is the alarm file generated by perl
	# argv[2] is the wechat receiver
	inputfile = sys.argv[1]
	receiver = sys.argv[2]
	skype_call_enable = 0

	#we get token from wechat first. It should last 7200 seconds
	corpid='wx1692320648865972'
	corpsecret='RilwFUtsR1mo9Ca9NoCw0O1bdBJXw3WrEp0u0RL-fu11k_OUHvqSRY4elmpO5UZ-'
	get_token='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(corpid,corpsecret)
	f=urllib2.urlopen(get_token)
	s=f.read()
	f.close()
	j=json.loads(s)
	token=j['access_token']

	#Process alarms
	alarmfile = open(inputfile)
	msg = ""

	for line in alarmfile:
	#check all Major and Minor alarms
		if re.search(r"Major|Minor", line):
			dt = re.search(r"(\d+-\d+-\d+ \d+:\d+:\d+)", line).group(1)
			if getDatetimeFromStr(dt) >= previous_hour():
				msg = msg + line + "\n"
		#check Fabric drops
		if "Fabric drop counter" in line:
			#enable skype_call flag. set to 1 if needs to call everybody
			skype_call_enable = 1
			routername = line.split(',')[0]
			counter = line.split(',')[-1].replace(' delta: ','')
			pps = int(counter)/3600
			msg = routername + " Fabric Drop Average PPS: " + str(pps) + "\n\n"
			#call Wilson
			skype_call_msg = "Fabric丢包，呼叫张靖电话中..."
			wechat_send(token, skype_call_msg, "wilson|Tim|Haofeng")
			os.system('python /home/hfzhang/skype-call.py +8613716045359')
			#os.system('python /home/hfzhang/skype-call.py +8618601355602')
			
	#alarmfile all processed.
	alarmfile.close()
	
	#Send wechat messages.
	#if len(msg) != 0 and len(msg) <= 2000:
	#	wechat_send(token, msg, receiver)
	#else:
	loop = len(msg) // 2000
	for i in range(loop+1):
		wechat_send(token, msg[i*2000:(i+1)*2000], receiver)

	#sleep 5 minutes to make sure somebody picked up phone. Then call again.
	print "Check whether need to call other guys"
	if (skype_call_enable == 1):
		print "Call flag enabled. need to call haofeng and Tim."
		time.sleep(300)
		#call hfzhang
		skype_call_msg = "Fabric丢包，呼叫张浩锋电话中..."
		wechat_send(token, skype_call_msg, "wilson|Tim|Haofeng")	
		os.system('python /home/hfzhang/skype-call.py +8618601355602')
		time.sleep(300)
		#call Tim
		skype_call_msg = "Fabric丢包，呼叫Tim电话中..."
		wechat_send(token, skype_call_msg, "wilson|Tim|Haofeng")		
		os.system('python /home/hfzhang/skype-call.py +8613810090097')
		#os.system('python /home/hfzhang/skype-call.py +8618601355602')
		skype_call_enable = 0
		sys.exit(0)
	else:
		print "Call flag not enabled; no call placed"