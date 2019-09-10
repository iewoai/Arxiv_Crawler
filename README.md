# Arxiv_Crawler
用于下载arxiv上的论文，并将.pdf转化为缩略图片

一、文件含义
	 
	 1.data文件用来存放pdf文件和论文缩略图文件
	 
	 2.a1.py为下载论文主程序，用于提取论文信息
	 
	 3.db.p用来存储爬取的论文信息
	 
	 4.download_pdf.py下载论文
	 
	 5.thumb_pdf.py将论文.pdf文件转化为u缩略图
	 
	 6.settings.py环境配置文件
	 
二、程序说明
	
	1.爬取论文信息和下载论文pdf用了urllib.request库
	
	2.pdf转图片则用了magick工具
	
