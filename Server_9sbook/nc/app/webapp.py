#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''

from gfirefly.server.globalobject import webserviceHandle,GlobalObject
from flask import request
from man.NCManager import VNodeManger
GlobalObject().webroot.debug = True

@webserviceHandle("/rank")
def nc_rank():
	""" get rank list"""
	result = VNodeManger().callNC("nc_rank")
	return result

@webserviceHandle("/search")
def nc_search():
	""" click search"""
	bookname = request.args.get('bookname')
	author = request.args.get('author')
	if bookname == None:
		bookname = ""
	if author == None:
		author = ""
	result = VNodeManger().callNC("nc_search",bookname,author)
	return result

@webserviceHandle("/intro")
def nc_intro():
	""" click search result to book introduction"""
	l_url = request.args.get('url')
	result = VNodeManger().callNC("nc_intro",l_url)
	return result

@webserviceHandle("/cat")
def nc_catalogue():
	""" click read"""
	l_url = request.args.get('url')
	result = VNodeManger().callNC("nc_catalogue",l_url)
	return result

@webserviceHandle("/content")
def nc_content():
	""" click catalogue"""
	l_url = request.args.get('url')
	result = VNodeManger().callNC("nc_content",l_url)
	return result