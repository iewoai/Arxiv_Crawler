from settings import Config
import os, pickle
from urllib.request import urlopen
import shutil, random, time
# shutil用于高级文件操作

# 若不存在pdf目录则新建一个
timeout_secs = 10
if not os.path.exists(Config.pdf_dir): 
	os.makedirs(Config.pdf_dir)

 # 获得所有下载过的pdf文件名
have = set(os.listdir(Config.pdf_dir))

# 打开db.p文件
db = pickle.load(open(Config.db_path, 'rb'))

# 计算下载指标
numok = 0
numtot = 0

# 提取pdf地址
for pid, j in db.items():
	pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
	assert len(pdfs) == 1
	pdf_url = pdfs[0] + '.pdf'
	# print(pdf_url)

	# 提取.pdf
	basename = pdf_url.split('/')[-1]

	# 将pdf名和文件名组合在一块
	fname = os.path.join(Config.pdf_dir, basename)
	numtot += 1
	try:
		if not basename in have:
			print('从 %s 下载到 %s' % (pdf_url, fname))
			req = urlopen(pdf_url, None, timeout_secs)
			with open(fname, 'wb') as fp:
				shutil.copyfileobj(req, fp)
			# random.uniform 随机生成一个实数
			time.sleep(0.05 + random.uniform(0,0.1))
		else:
			print('%s 文件已存在' % (fname, ))
		numok += 1
	except Exception as e:
		print('下载出错，错误原因：')
		print(e)

	print('下载进度：%d/%d。' % (numtot, len(db)))
print('总下载数：%d，下载成功：%d。' % (len(db), numok))


