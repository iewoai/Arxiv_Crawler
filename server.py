import shutil, os, sys, time
from subprocess import Popen
import subprocess
# cmd = 'magick convert -density 150 F:/py学习/arxiv/data/pdf/1805.11724v3.pdf F:/py学习/arxiv/tmp/thumb.png'

# os.system(cmd)
# pp = Popen(['magick', 'convert', '-density', '150', 'F:/py学习/arxiv/data/pdf/1805.11724v3.pdf', 'F:/py学习/arxiv/tmp/thumb.png'])

# # # Popen('convert -density 150 F:/py学习/arxiv/data/pdf/1805.11724v3.pdf F:/py学习/arxiv/tmp/thumb.png')
# # # result = os.popen(cmd)
# # # print(result.read())
# # # os.system(cmd)
# t0 = time.time()
# while time.time() - t0 < 100: # give it 15 seconds deadline
# 	ret = pp.poll()
# 	if not (ret is None):
# 		# process terminated
# 		break
# 	time.sleep(0.1)
# ret = pp.poll()
# if ret is None:
# 	print("convert command did not terminate in 20 seconds, terminating.")
# 	pp.terminate()
# else:
# 	print('转换成功')
# # os.system('notepad')
# # os.system(r'"D:\CloudMusic\cloudmusic.exe"')
# subprocess.call("magick convert -density 150 F:/py学习/arxiv/data/pdf/1805.11724v3.pdf F:/py学习/arxiv/tmp/thumb.png")
if not os.path.exists(Config.tmp_dir): os.makedirs(Config.tmp_dir)