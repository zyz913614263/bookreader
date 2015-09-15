#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''
from pyquery import PyQuery as pq

class Rank:
    ''' get rank list '''
    
    rank_url = "http://www.huaixiu.net/files/article/topweekvisit/0/1.htm"
    nc_title = "沸腾文学"
    
    def get_rank(self):
        l_d = pq(url = self.rank_url)
        l_content = l_d("table").filter(".grid")("tr")
        del l_content[0]
        l_rank_list = []
        for item in l_content.items():
            item = item("td")
            # 图书信息链接
            book_intro_url = item.eq(0)("a").attr("href")
            # 图书目录链接
            book_cat_url = item.eq(2)("a").attr("href")
            # 封面图片链接
            book_img_url = ""
            # 图书标题
            book_name = item.eq(0)("a").text().strip()
            # 最新章节
            book_latest_chapter = item.eq(1)("a").text().strip()
            # 作者
            book_author = item.eq(3).text().strip()
            # 字数
            book_words = item.eq(4).text().strip()
            # 更新时间
            book_update_date = item.eq(5).text().strip()
            # 来源网站名
            book_source_site = self.nc_title
            # 内容简介
            book_intro = item.eq(6).text().strip()
            
            result = {"intro_url":book_intro_url,"cat_url":book_cat_url,"img_url":book_img_url,"book_name":book_name,"latest_chapter":book_latest_chapter,"book_author":book_author,"book_words":book_words,"update_date":book_update_date,"book_source_site":book_source_site,"book_intro":book_intro}
            l_rank_list.append(result)
        return l_rank_list

        