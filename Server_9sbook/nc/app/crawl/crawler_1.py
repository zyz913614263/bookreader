#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''
from pyquery import PyQuery as pq
import urllib,sys

class Crawler_1:
	""" 
		代码中涉及到的地址仅开发测试案例使用，请下载后立即更换
		http://www.huaixiu.net/modules/article/search.php?searchkey=%BE%F8%CA%C0%CC%C6%C3%C5&searchtype=articlename&searchbuttom=%CB%D1+%CB%F7
		http://www.huaixiu.net/modules/article/search.php?searchkey=%BE%F8%CA%C0&searchtype=articlename&searchbuttom=%CB%D1+%CB%F7
		http://www.huaixiu.net/modules/article/search.php?searchkey=%CC%C6%BC%D2%C8%FD%C9%D9&searchtype=author&searchbuttom=%CB%D1+%CB%F7
	"""
	nc_url = "http://www.huaixiu.net"
	nc_article="&searchtype=articlename&searchbuttom=%CB%D1+%CB%F7"
	nc_author="&searchtype=author&searchbuttom=%CB%D1+%CB%F7"
	nc_title = "沸腾文学"
	search_url = ""
	
	# 搜索返回列表最大数量限制
	SEARCH_LIST_LEN_LIMT = 99
	
	def get_escape_str(self,p_str):
# 		l_str = urllib.quote(p_str.decode(sys.stdin.encoding).encode('gbk'))
		l_str = urllib.quote(p_str.decode(sys.getdefaultencoding()).encode('gbk'))
		return l_str
	
	def search(self,p_bookname="",p_author=""):
		l_param = "/modules/article/search.php?searchkey="
		if p_bookname != "":
			p_bookname = self.get_escape_str(p_bookname)
			l_param += p_bookname+self.nc_article
		elif p_author != "":
			p_author = self.get_escape_str(p_author)
			l_param += p_author+self.nc_author

		self.search_url = self.nc_url+l_param
		l_d = pq(url = self.search_url)
		
		l_error = l_d("div").filter(".b_title")
		if l_error:
			return [{}]
		
		if l_d("table").filter(".grid"):
			return self.search_dim(l_d)
		else:
			return self.search_exact(l_d)
	
	def search_exact(self,p_d):
		l_content = p_d("div").filter(lambda i, this:pq(this).attr('id') == 'content')
		l_ul = l_content("ul").filter(".ulrow")
		l_td_img = l_content("td").filter(lambda i, this:pq(this).attr('width') == '80%').eq(1)
		# 图书信息链接
		book_intro_url = self.search_url
		# 图书目录链接
		book_cat_url = self.nc_url + l_ul.eq(0)("a").attr("href")
		# 封面图片链接
		book_img_url = l_td_img("img").attr("src")
		# 图书标题
		book_name = l_content("span").filter(lambda i, this:pq(this).attr('style') == 'font-size:18px; font-weight: bold; line-height: 200%').text().strip()
		# 最新章节
		book_latest_chapter = l_td_img("a").eq(1).text().strip()
		# 作者
		book_author = l_content("td").filter(lambda i, this:pq(this).attr('width') == '25%').eq(1).text().strip()
		book_author = book_author.replace("作    者：","")
		# 字数
		book_words = l_content("td").filter(lambda i, this:pq(this).attr('width') == '25%').eq(3).text().strip()
		book_words = book_words.replace("全文长度：","")
		# 更新时间
		book_update_date = l_content("table").eq(0)("tr").eq(2)("td").eq(0).text().strip()
		book_update_date = book_update_date.replace("最后更新：","")
		# 来源网站名
		book_source_site = self.nc_title
		# 章节
		book_chapter = l_td_img("a").eq(1).text().strip()
		l_td_img.remove("a")
		l_td_img.remove("span")
		# 内容简介
		book_intro = l_td_img.text()
		l_intro_list = []
		result = {"intro_url":book_intro_url,"cat_url":book_cat_url,"img_url":book_img_url,"book_name":book_name,"latest_chapter":book_latest_chapter,"book_author":book_author,"book_words":book_words,"update_date":book_update_date,"book_source_site":book_source_site,"book_chapter":book_chapter,"book_intro":book_intro}
		l_intro_list.append(result)
		return l_intro_list
	
	def search_dim(self,p_d):
		l_pages = int(p_d("a").filter(".last").text().strip())
		
		l_intro_list = []
		for i in range(1,l_pages+1):
			l_url = self.search_url+"&page="+str(i)
			l_d = pq(url = l_url)
			l_content = l_d("table").filter(".grid")("tr")
			del l_content[0]
			for item in l_content.items():
				# 列表长度为100
				result_len = len(l_intro_list)
				if result_len > self.SEARCH_LIST_LEN_LIMT:
					break
# 				l_intro_url = item.eq(0)("a").attr("href")
# 				l_intro_d = pq(url = l_intro_url)
# 				l_intro_list += self.search_exact(l_intro_d)
				item = item("td")
				# 图书信息链接
				book_intro_url = item.eq(0)("a").attr("href")
				# 图书目录链接
				book_cat_url = item.eq(1)("a").attr("href")
				# 封面图片链接
				book_img_url = ""
				# 图书标题
				book_name = item.eq(0)("a").text().strip()
				# 最新章节
				book_latest_chapter = item.eq(1)("a").text().strip()
				# 作者
				book_author = item.eq(2).text().strip()
				# 字数
				book_words = item.eq(3).text().strip()
				# 更新时间
				book_update_date = item.eq(4).text().strip()
				# 来源网站名
				book_source_site = self.nc_title
				# 章节
				book_chapter = item.eq(1).text().strip()
				# 内容简介
				book_intro = item.eq(5).text().strip()
				
				result = {"intro_url":book_intro_url,"cat_url":book_cat_url,"img_url":book_img_url,"book_name":book_name,"latest_chapter":book_latest_chapter,"book_author":book_author,"book_words":book_words,"update_date":book_update_date,"book_source_site":book_source_site,"book_chapter":book_chapter,"book_intro":book_intro}
				
				l_intro_list.append(result)
				
		return l_intro_list
	
	def intro(self,p_url):
		l_d = pq(url = p_url)
		l_content = l_d("div").filter(lambda i, this:pq(this).attr('id') == 'content')
		l_ul = l_content("ul").filter(".ulrow")
		l_td_img = l_content("td").filter(lambda i, this:pq(this).attr('width') == '80%').eq(1)
		# 阅读链接
		book_cat_url = self.nc_url + l_ul.eq(0)("a").attr("href")
		# 封面图片链接
		book_img_url = l_td_img("img").attr("src")
		# 图书标题
		book_name = l_content("span").filter(lambda i, this:pq(this).attr('style') == 'font-size:18px; font-weight: bold; line-height: 200%').text().strip()
		# 最新章节
		book_latest_chapter = l_td_img("a").eq(1).text().strip()
		# 作者
		book_author = l_content("td").filter(lambda i, this:pq(this).attr('width') == '25%').eq(1).text().strip()
		book_author = book_author.replace("作    者：","")
		# 字数
		book_words = l_content("td").filter(lambda i, this:pq(this).attr('width') == '25%').eq(3).text().strip()
		book_words = book_words.replace("全文长度：","")
		# 更新时间
		book_update_date = l_content("table").eq(0)("tr").eq(2)("td").eq(0).text().strip()
		book_update_date = book_update_date.replace("最后更新：","")
		# 来源网站名
		book_source_site = self.nc_title
		# 章节
		book_chapter = l_td_img("a").eq(1).text().strip()
		l_td_img.remove("a")
		l_td_img.remove("span")
		# 内容简介
		book_intro = l_td_img.text()
		l_intro_list = []
		result = {"cat_url":book_cat_url,"img_url":book_img_url,"book_name":book_name,"latest_chapter":book_latest_chapter,"book_author":book_author,"book_words":book_words,"update_date":book_update_date,"book_source_site":book_source_site,"book_chapter":book_chapter,"book_intro":book_intro}
		l_intro_list.append(result)
		return l_intro_list
	
	def catalogue(self,p_url):
		l_url = p_url
		l_d = pq(url = l_url)
		l_table = l_d("table")
		l_items = l_table("a")
		
		chapter_list = []
		for item in l_items.items():
			chapter_name = item.text().strip()
			chapter_url = p_url+item.attr("href").strip()
			chapter_obj = {"chapter_name":chapter_name,"chapter_url":chapter_url}
			chapter_list.append(chapter_obj)
		return chapter_list

	def content(self,p_url):
		l_url = p_url
		l_d = pq(url = l_url)
		content_text = l_d("div").filter(lambda i, this:pq(this).attr('id') == 'content').html()
		content_text = str(content_text)
		content_text = content_text.replace("<br /><br />", "\n")
		content_text = content_text.replace("<br />", "\n")
		content_text = content_text.replace("    ","　　")
		result = {"content_text":content_text,"img_url":""}
		return result
