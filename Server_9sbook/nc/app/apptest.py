#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''

from gfirefly.server.globalobject import netserviceHandle

@netserviceHandle
def echo_1(_conn,data):
    return data

    


