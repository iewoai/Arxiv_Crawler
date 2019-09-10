import os, re
import time, sys
import shutil
from subprocess import Popen
# 控制命令行

from settings import Config

 # 判断imagemagic有没有安装
if not shutil.which('convert'):
	print("没有安装 imagemagick！")
	sys.exit()

pdf_dir = Config.pdf_dir
if not os.path.exists(Config.thumbs_dir): os.makedirs(Config.thumbs_dir)

t = time.time()
files_in_pdf_dir = os.listdir(pdf_dir)
pdf_files = [x for x in files_in_pdf_dir if x.endswith('.pdf')]
# print(pdf_files)
for i,p in enumerate(pdf_files):
	# tmp为中转文件，用来暂存透明底图片
	if not os.path.exists(Config.tmp_dir): 
		os.makedirs(Config.tmp_dir)
	pdf_path = os.path.join(pdf_dir, p)
	pattern = re.compile(r"(.*?).pdf")
	m = pattern.match(p)
	pdf_id = m.group(1)
	thumb_path = os.path.join(Config.thumbs_dir, pdf_id)
	# print(thumb_path)
	if os.path.isfile(thumb_path): 
		print("跳过 %s， pdf缩略图已经存在。" % (pdf_path, ))
		continue
	print("进度：%d/%d 正在转换： %s" % (i, len(pdf_files), p))
	a_thumb_path = os.path.join(os.getcwd(), thumb_path)
	a_pdf_path = os.path.join(os.getcwd(), pdf_path)
	a_tmp_path = os.path.join(os.getcwd(), Config.tmp_dir)
	# print(a_thumb_path)
	# print(a_pdf_path)
	# print(a_tmp_path)
	# # 直接转换成jpg格式时会出现黑快，所以直接转化为透明格式png，然后再转化为白色背景png
	# cmd = 'magick convert -density 150 %s %s' % (a_pdf_path, os.path.join(a_tmp_path, 'thumb.png'))
	print(a_pdf_path, os.path.join(a_tmp_path, 'thumb.png'))
	pp = Popen(['magick', 'convert', '-density', '150', '%s' % (a_pdf_path, ), os.path.join(a_tmp_path, 'thumb.png')])
	t0 = time.time()
	while time.time()-t0 < 100:
		ret = pp.poll()
		if not (ret is None):
			break
		time.sleep(0.1)
	ret = pp.poll()
	if ret is None:
		print('转换失败，强行终止')
		pp.terminate()
	else:
		print('转换成功，所需时间： %ds' % (time.time()-t0))

		# 转换20秒内未成功，终止
	if not os.path.exists(a_thumb_path):
		os.makedirs(a_thumb_path)

	# 转化为白色背景png
	t1 = time.time()
	if os.path.isfile(os.path.join(Config.tmp_dir, 'thumb-0.png')):
		cmd = "magick mogrify -path %s -background white -flatten %s" % (a_thumb_path, os.path.join(a_tmp_path, '*.png'))
		print('正在转化白色背景缩略图')
		os.system(cmd)
		print('转换成功，所需时间： %ds' % (time.time()-t1))
		shutil.rmtree(a_tmp_path)
	time.sleep(0.01)
print('全部转换成功，所需时间： %ds' % (time.time()-t))


	# if os.path.isfile(os.path.join(Config.tmp_dir, 'thumb-0.png')):
	# 	for i in range(8):
	# 		f = os.path.join(Config.tmp_dir, 'thumb-%d.png' % (i,))
	# 		f2= os.path.join(Config.tmp_dir, 'thumbbuf-%d.png' % (i,))
	# 		if os.path.isfile(f):
	# 			cmd = 'mv %s %s' % (f, f2)
	# 		# mv移动文件
	# 			os.system(cmd)
 #        # okay originally I was going to issue an rm call, but I am too terrified of
 #        # running scripted rm queries, so what we will do is instead issue a "mv" call
 #        # to rename the files. That's a bit safer, right? We have to do this because if
 #        # some papers are shorter than 8 pages, then results from previous paper will
 #        # "leek" over to this result, through the intermediate files.

	# # spawn async. convert can unfortunately enter an infinite loop, have to handle this.
	# # this command will generate 8 independent images thumb-0.png ... thumb-7.png of the thumbnails
	# # print(pdf_path)
	# pp = Popen(['magick', 'convert', '%s[0-7]' % (pdf_path, ), '-thumbnail', 'x156', os.path.join(Config.tmp_dir, 'thumb.png')])
	# t0 = time.time()
	# while time.time() - t0 < 20: # give it 15 seconds deadline
	# 	ret = pp.poll()
	# 	if not (ret is None):
	# 		# process terminated
	# 		break
	# 	time.sleep(0.1)
	# ret = pp.poll()
	# if ret is None:
	# 	print("convert command did not terminate in 20 seconds, terminating.")
	# 	pp.terminate() # give up

	# if not os.path.isfile(os.path.join(Config.tmp_dir, 'thumb-0.png')):
	# # failed to render pdf, replace with missing image
	# 	missing_thumb_path = os.path.join('data', 'missing.jpg')
	# 	os.system('cp %s %s' % (missing_thumb_path, thumb_path))
	# 	print("could not render pdf, creating a missing image placeholder")
	# else:
	# 	cmd = "montage -mode concatenate -quality 80 -tile x1 %s %s" % (os.path.join(Config.tmp_dir, 'thumb-*.png'), thumb_path)
	# 	print(cmd)
	# 	os.system(cmd)

	# time.sleep(0.01)