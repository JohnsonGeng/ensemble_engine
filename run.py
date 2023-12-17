# -*- coding: utf=8 -*-
# @Time: 2023/11/7 
# @Author: Johnson Geng
# @FIle: run.py 
# @Description: 检测引擎启动脚本

import argparse
from engine.Engine import *
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 上传样本保存绝对路径
UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload')

parser = argparse.ArgumentParser(
	description='检测引擎启动脚本',
)

parser.add_argument(
	'-e',
	'--engine',
	type=str,
	choices=['Avast', 'ClamAV', 'DrWeb', 'ESET', 'HuoRong', 'Kaspersky', 'Ember', 'MalConv', 'MicroSoft', 'Novel', 'NovelFamily', 'Winner', 'Qihoo'],
	default='Avast',
	help='需要启动的引擎 可选:Avast/ClamAV/DrWeb/ESET/Ember/HuoRong/Kaspersky/MalConv/MircoSoft/Novel/NovelFamily/Winner/Qihoo 默认:Avast',
)

parser.add_argument(
	'-p',
	'--port',
	type=str,
	default='5000',
	help='服务开启的端口号',
)

# 获取命令行参数
args = parser.parse_args()
engine_name = args.engine
port = args.port


# 初始化引擎
if engine_name == 'Avast':
	e = EngineAvast()
elif engine_name == 'ClamAV':
	e = EngineClamAV()
elif engine_name == 'DrWeb':
	e = EngineDrWeb()
elif engine_name == 'ESET':
	e = EngineESET()
elif engine_name == 'Ember':
	e = EngineEmber()
elif engine_name == 'HuoRong':
	e = EngineHuoRong()
elif engine_name == 'Kaspersky':
	e = EngineKaspersky()
elif engine_name == 'MalConv':
	e = EngineMalConv()
elif engine_name == 'MicroSoft':
	e = EngineMicrosoft()
elif engine_name == 'Novel':
	e = EngineNovel()
elif engine_name == 'NovelFamily':
	e = EngineNovelFamily()
elif engine_name == 'Winner':
	e = EngineWinner()
else:
	e = EngineQihoo()


# 检测接口
@app.route('/detect', methods=['GET', 'POST'])
def detect():
	# 获取上传样本并保存
	file = request.files.get('file')
	file_name = secure_filename(file.filename)
	file_name = engine_name + '_' + file_name
	file_path = os.path.join(UPLOAD_PATH, file_name)
	file.save(file_path)

	result = {}

	# 调用引擎查杀
	r = e.scan(file_path)
	result['result'] = r[0]
	result['lab_pro'] = r[1]

	# GJX: 磁盘容量限制, 需要将扫描完的文件删除
	try:
		os.remove(file_path)
		print('已删除文件{}'.format(file_name))
	except OSError:
		print('文件已删除!')

	return jsonify(result)


if __name__ == '__main__':

	app.run(host='0.0.0.0', port=port, threaded=True)