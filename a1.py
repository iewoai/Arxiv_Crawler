import urllib.request
import pickle
import feedparser
import time
from settings import Config, safe_pickle_dump
import random

# 将feedparser.FeedParserDict转换为python dict变量
def encode_feedparser_dict(d):
	if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
		j = {}
		for k in d.keys():
			j[k] = encode_feedparser_dict(d[k])
		return j
	elif isinstance(d, list):
		l = []
		for k in d:
			l.append(encode_feedparser_dict(k))
		return l
	else:
		return d

# 提取论文id 和版本 v
def parse_arxiv_url(url):
	ix = url.rfind('/')
	idversion = url[ix+1:]
	parts = idversion.split('v')
	assert len(parts) == 2, 'error parsing url ' + url
	# assert断言语句，若bool不为真则输出报错，程序终止
	return parts[0], int(parts[1])

def print_all(db):
	print("正在逐一打印爬取的论文信息：")
	for i,paper in enumerate(db):
		#print(db[p])
		p = db[paper]
		print(p['link'])
		print(p['title'].replace('\n','').replace('  ',' '))
		print(p['updated'])
		print(p['published'])
		print(p['title'])
		print(p['summary'].replace('\n',''))
		name = []
		for author in p['authors']:
			name.append(author['name'])
		names = " ".join(name)
		print(names)
		pdfs = [x['href'] for x in p['links'] if x['type'] == 'application/pdf']
		print(pdfs[0])
		print(p['arxiv_primary_category']['term'])
		tag_name = []
		for tag in p['tags']:
			tag_name.append(tag['term'])
		tags = " ".join(tag_name)
		print(tags)
		print(p['_rawid'])
		print(p['_version'])
		if p.get('arxiv_comment'):
			print(p['arxiv_comment'])
		if p.get('arxiv_doi'):
			print(p['arxiv_doi'].replace('\n',''))

if __name__ == "__main__":
	# url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=descending'
	print('正在爬取arxiv，关键词： %s' % (Config.search_query))
	try:
		db = pickle.load(open(Config.db_path, 'rb'))
	except Exception as e:
		print('打开数据储存文件失败：')
		print(e)
		print('开始创建新的空数据储存！')
		db = {}
	print('数据储存文件最初有 %d 篇论文' % (len(db)))
	num_added_total = 0
	for i in range(Config.start_index, Config.max_index, Config.max_results):
		query = 'search_query=%s&start=%i&max_results=%i&sortBy=%s&sortOrder=%s' % (Config.search_query, i, Config.max_results, Config.sortBy, Config.sortOrder)
		url = Config.api_url + query
		data = urllib.request.urlopen(url).read()
		feed = feedparser.parse(data)
		#print (type(feed))
		num_added = 0
		num_skipped = 0
		for e in feed.entries:

			j = encode_feedparser_dict(e)
			# 提取每篇entry的id和v
			rawid, version = parse_arxiv_url(j['id'])
			j['_rawid'] = rawid
			j['_version'] = version

			# 当数据库没有此论文和只有旧版时，加入数据库
			if not rawid in db or j['_version'] > db[rawid]['_version']:
				db[rawid] = j
				print('更新于 %s ，增加论文： %s' % (j['updated'], j['title']))
				num_added += 1
				num_added_total += 1
			else:
				num_skipped += 1

		# 打印出
		print('增加 %d 篇论文, 重复存在 %d篇.' % (num_added, num_skipped))

		if len(feed.entries) == 0:
			print('没有爬取到论文，请检查参数设置或限制情况。')
			print(response)
			break

		if num_added == 0 and Config.break_on_no_added == 1:
			print('没有新的论文，爬取结束！')
			break

		print('休息 %i 秒...' % (Config.wait_time , ))
		time.sleep(Config.wait_time + random.uniform(0, 3))

	# save the database before we quit, if we found anything new
	if num_added_total > 0:
		print("本次共爬取了 %i 篇论文。" %(num_added_total))
		# print('Saving database with %d papers to %s' % (len(db), Config.db_path))
		# safe_pickle_dump(db, Config.db_path)
		# print(db)
		print_all(db)
		safe_pickle_dump(db, Config.db_path)
