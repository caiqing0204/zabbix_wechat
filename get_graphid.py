#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
itemid = 0
def get_graphid():
    url = "http://lcoalhost/api_jsonrpc.php"
    header = {"Content-Type":"application/json"}
    trigger_data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "trigger.get",

        "params": {
            "output": ["triggerid", "description", "priority"],
            "sortorder": "DESC",
            "sortfield": "lastchange",
            "selectHosts": ["host"],
            "selectLastEvent": "extend",
            "selectItems": ["items"],
            "only_true": 1,
            "monitored": 1,
            "expandDescription": 1,
            "min_severity": 1,
            "limit": 1,
            "filter": {
                "value": 1,
            },
        },
        关于auth 大家自己从官网api中get，这里我就不一一列出
        "auth":"*********************************", # theauth id is what auth script returns, remeber it is string
       "id":0,
    })



    # create request object
    request = urllib2.Request(url,trigger_data)
    for key in header:
        request.add_header(key,header[key])
    # auth and get authid
    try:
        result = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        return "Auth Failed, Please Check Your Name And Password:",e.code
    else:
        response = json.loads(result.read())
        result.close()
        itemid = response["result"][0]["items"][0]["itemid"]
    #print itemid
    graph_data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "graphitem.get",
        "params": {
            "output": ["itemid","graphid"],
            "itemids": itemid,
        },
        "auth":"***************************************", # theauth id is what auth script returns, remeber it is string
       "id":0,
    })
    request = urllib2.Request(url,graph_data)
    for key in header:
        request.add_header(key,header[key])
    # auth and get authid
    try:
        result = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        return "Auth Failed, Please Check Your Name And Password:",e.code
    else:
        response = json.loads(result.read())
        result.close()
        #print itemid
        try:
            return response["result"][0]
        except:
            return []
        #response["result"]