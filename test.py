'''
黑丸游戏列表爬虫
'''
import requests
import os
import urllib
from urllib import request
from bs4 import BeautifulSoup
from retrying import retry
import xlwt
import lxml

@retry(stop_max_attempt_number=3)
def souping(url):
	global timeouttag
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
		"Referer": "https://www.cnblogs.com"
	}
	try:
		src = requests.get(url, headers=headers,timeout=20).content
		soup=BeautifulSoup(src,"lxml").decode("gbk")
		soup=BeautifulSoup(soup,"lxml")
		return soup
	except:
		print("超时")
		timeouttag=1
		pass
def titling(soup):
	global gamenum
	cgamenum=gamenum
	game_base = soup.find_all(class_="subject hot")
	for gametitles in game_base:
		gametitle = gametitles.find("span")
		try:
			worksheet.write(cgamenum,0,gametitle.text)
			cgamenum = cgamenum + 1
		except:
			pass
def authoring(soup):
	global gamenum
	cgamenum = gamenum
	game_base = soup.find_all(class_="author")
	for gameauthors in game_base:
		t1 = gameauthors.find("cite")
		t2 = gameauthors.find("em")
		try:
			worksheet.write(cgamenum,1,t1.text)
			worksheet.write(cgamenum,2,t2.text)
			cgamenum = cgamenum + 1
		except:
			pass
def nums(soup):
	global gamenum
	cgamenum = gamenum
	game_base = soup.find_all(class_="nums")
	for nums in game_base:
		t1 = nums.find("strong")
		t2 = nums.find("em")
		try:
			worksheet.write(cgamenum, 3, t1.text)
			worksheet.write(cgamenum, 4, t2.text)
			cgamenum=cgamenum+1
		except:
			pass
	gamenum=cgamenum
def crawling(soup):
	global now_pages,url,timeouttag
	if now_pages <= int(required_pages):
		try:
			print("现在正在爬取第" + str(now_pages) + "页，已保存" + str(gamenum) + "个游戏")
			if timeouttag==0:
				titling(soup)
				authoring(soup)
				nums(soup)
			now_pages=now_pages+1
			timeouttag=0
			url="http://www.galgamezd.org/bbs/forumdisplay.php?fid=8&orderby=dateline&page=" + str(now_pages)
			soup=souping(url)
			crawling(soup)
		except:
			print("爬取失败")
			exit()
			pass




if __name__=="__main__":
	now_pages=1
	gamenum=1
	timeouttag=0
	required_pages = input("请输入要爬取的页数：")
	while isinstance(required_pages,int)|int(required_pages)<=0:
		required_pages=input("请输入正整数！请重新输入要爬取的页数")
	print("正在创建excel表格……")
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet("sheet1")
	worksheet.write(0, 0, "游戏名")
	worksheet.write(0, 1, "作者")
	worksheet.write(0, 2, "时间")
	worksheet.write(0, 3, "回复")
	worksheet.write(0, 4, "查看")
	workbook.save("游戏列表.xls")
	url = "http://www.galgamezd.org/bbs/forumdisplay.php?fid=8&orderby=dateline&page=" + str(now_pages)
	soup=souping(url)
	print("开始爬取……")
	crawling(soup)
	workbook.save("游戏列表.xls")
	print("爬取完成～")


