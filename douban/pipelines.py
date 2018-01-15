# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload (sys)
sys.setdefaultencoding('utf-8')
import json
import MySQLdb

class DoubanPipeline(object):
	def __init__(self):
		self.f = open('movie.json','w')
		self.f.write('[')

	def process_item(self, item, spider):
		for value in item['subjects']:
			content = ','+json.dumps(dict(value),ensure_ascii=False)
			#content = unicode.encode(str,'utf-8');
			self.f.write(content)
		return item

	def close_spider(self,spider):
		self.f.write(']')
		self.f.close()	        

class DoubanPipeline2(object):
	"""docstring for DoubanPipeline2"""
	def __init__(self):
		#passwd='123456'这里就不写
		self.con = MySQLdb.connect(host='127.0.0.1',port = 3306,user='root',db='test')
		# 使用cursor()方法获取操作游标 
		self.cur = self.con.cursor()

	def process_item(self,item,spider):
		for value in item['subjects']:
			sql= 'insert into doubanm1 (id,title,rate) values ({},{},{})'.format(value['id'],value['title'],value['rate'])
			try:
				self.cur.execute(sql) 
				self.con.commit()
			except:
				self.con.rollback()	
		return item	

	def close_spider(self,spider):
		self.cur.close()
		self.con.close()
		