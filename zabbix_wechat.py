#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib,urllib2,json,cookielib
import sys
import commands,time
import os
import requests
from get_graphid import get_graphid
reload(sys)
sys.setdefaultencoding( "utf-8" )

STime=int(time.time())
zabbix_user='username'
zabbix_pass='.password'
login_url = 'http://localhost/index.php'
zabbix_url = "http://localhost/api_jsonrpc.php"
graph_url = 'http://localhost/chart2.php'
zabbix_header = {"Content-Type":"application/json"}
pic_save_path_dir = '/data/images'
auth_data = json.dumps({
    "jsonrpc":"2.0",
    "method":"user.login",
    "params":
            {
            "user":zabbix_user,
            "password":zabbix_pass
            },
    "id":0
    })
login_data = urllib.urlencode({
                        "name": zabbix_user,
                        "password": zabbix_pass,
                        "autologin": 1,
                        "enter": "Sign in"})


#登录zabbix，设置一个cookie处理器，负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
opener.open(login_url,login_data)#.read()

request = urllib2.Request(zabbix_url,auth_data)
for key in zabbix_header:
    request.add_header(key,zabbix_header[key])
try:
    result = urllib2.urlopen(request)
except urllib2.HTTPError, e:
    print 'The server couldn\'t fulfill the request, Error code: ', e.code
except urllib2.URLError, e:
    print 'We failed to reach a server.Reason: ', e.reason
else:
    response=json.loads(result.read())
    #print response
    result.close()

def pic_save(graphid):
    graph_args = urllib.urlencode({
                            "graphid":graphid,
                            "width":'720',
                            "height":'200',
                            "stime":STime,
                            "period":'86400'})

    data = opener.open(graph_url,graph_args).read()
    image_path = "/data/images/weixin-%s.png" % a.get_graphid()
    pic_save_path = os.path.join(pic_save_path_dir,image_path)
    file=open(pic_save_path,'wb')
    file.write(data)
    #file.flush()
    file.close()


class WeChat(object):
        __token_id = ''
        # init attribute
        def __init__(self,url):
                self.__url = url.rstrip('/')
                self.__corpid = '**********'   ###微信号的ID
                self.__secret = '********************'  ###微信号secret

        # Get TokenID
        def authID(self):
                params = {'corpid':self.__corpid, 'corpsecret':self.__secret}
                data = urllib.urlencode(params)

                content = self.getToken(data)

                try:
                        self.__token_id = content['access_token']
                        # print content['access_token']
                except KeyError:
                        raise KeyError

        # Establish a connection
        def getToken(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'gettoken?'
                try:
                        response = urllib2.Request(url + data)
                except KeyError:
                        raise KeyError
                result = urllib2.urlopen(response)
                content = json.loads(result.read())
                return content

        # Get sendmessage url
        def postData(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'message/send?access_token=%s' % self.__token_id
                request = urllib2.Request(url,data)
                try:
                        result = urllib2.urlopen(request)
                except urllib2.HTTPError as e:
                        if hasattr(e,'reason'):
                                print 'reason',e.reason
                        elif hasattr(e,'code'):
                                print 'code',e.code
                        return 0
                else:
                        content = json.loads(result.read())
                        result.close()
                return content
        # get graphid
        def get_graphid(self):
                if get_graphid():

                        return get_graphid()["graphid"]
                else:
                        return False
        # get media_id
        def get_media_id(self):
                self.authID()
                pic_save(self.get_graphid())
                img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={0}&type=image".format(self.__token_id)
                files = {'image': open("/data/images/weixin-%s.png" % a.get_graphid(), 'rb')}
                r = requests.post(url=img_url, files=files)
                re = json.loads(r.text)
                return re["media_id"]
        # send message
        def sendMessage1(self,touser,title,message,):
                self.authID()
                data = json.dumps({
                        'touser':touser,
                        'toparty':"1",        ###部门ID
                        'msgtype':"text",
                        'agentid':"1000002",        ###应用ID  应用中心查看
                        'text':{

                                'content':title+"\n"+message
                        },

                        'safe':"0",
                },ensure_ascii=False)

                response = self.postData(data)
                print str(response).strip("+")

                if self.get_graphid() and "故障" in sys.argv[2]:
                        data1 = json.dumps({
                                'touser': touser,
                                'toparty': "1",  ###部门ID
                                'msgtype': "image",
                                'agentid': "1000002",  ###应用ID  应用中心查看
                                'image': {

                                        "media_id": self.get_media_id()
                                                               #'content':title
                                },
                                'safe': "0"

                        }, ensure_ascii=False)
                        response1 = self.postData(data1)
                        print str(response1).strip("+")

if __name__ == '__main__':
        a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
        a.sendMessage1(sys.argv[1],sys.argv[2],sys.argv[3])
