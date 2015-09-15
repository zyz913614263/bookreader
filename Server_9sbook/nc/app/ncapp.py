#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''

from gfirefly.server.globalobject import remoteserviceHandle
from gfirefly.utils import services
import crawl,json
from crawl.rank import Rank

ss_service = services.Service("nc")

URL_1 = "huaixiu.net"
URL_2 = "XXX.net"
NC_SITE_COUNT = 2

@remoteserviceHandle("web")
def nc_rank():
	result = get_rank()
	return result

@remoteserviceHandle("web")
def nc_search(p_bookname="",p_author=""):
	result = get_search(p_bookname,p_author)
	return result

@remoteserviceHandle("web")
def nc_intro(p_url):
	result = get_intro(p_url)
	return result

@remoteserviceHandle("web")
def nc_catalogue(p_url):
	result = get_catalogue(p_url)
	return result

@remoteserviceHandle("web")
def nc_content(p_url):
	result = get_content(p_url)
	return result

# ==========================================================================
# will crawl for novel
# ==========================================================================

def handel(func):
	ss_service.mapTarget(func)

def get_rank():
	l_rank = Rank()
	l_rank_list = l_rank.get_rank()
	result = json.dumps(l_rank_list)
	return result

def get_search(p_bookname="",p_author=""):
	l_type = 1
	book_list = []
	for i in range(1,NC_SITE_COUNT):
		l_type = i
		l_moudle = getattr(crawl,"crawler_%s"%l_type)
		l_class = getattr(l_moudle,"Crawler_%s"%l_type)
		craw = l_class()
		l_intro_list = craw.search(p_bookname, p_author)
		book_list += l_intro_list
	result = json.dumps(book_list)
	return result

def get_intro(p_url):
	l_type = get_craw_type(p_url)
	l_moudle = getattr(crawl,"crawler_%s"%l_type)
	l_class = getattr(l_moudle,"Crawler_%s"%l_type)
	craw = l_class()
	result_list = craw.intro(p_url)
	result = json.dumps(result_list)
	return result

def get_catalogue(p_url):
	l_type = get_craw_type(p_url)
	l_moudle = getattr(crawl,"crawler_%s"%l_type)
	l_class = getattr(l_moudle,"Crawler_%s"%l_type)
	craw = l_class()
	result_list = craw.catalogue(p_url)
	result = json.dumps(result_list)
	return result

def get_content(p_url):
	l_type = get_craw_type(p_url)
	l_moudle = getattr(crawl,"crawler_%s"%l_type)
	l_class = getattr(l_moudle,"Crawler_%s"%l_type)
	craw = l_class()
	result_content = craw.content(p_url)
	result = json.dumps(result_content)
	return result

# =======================================================
# get url type ,to find match moudle, and get content
# =======================================================
def get_craw_type(p_url):
	if p_url.find(URL_1) != -1:
		return 1
	elif p_url.find(URL_2) != -1:
		return 2
	else:
		return 999
