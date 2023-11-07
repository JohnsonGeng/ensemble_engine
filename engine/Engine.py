import os
import time
import json
import ctypes
import sqlite3
import subprocess
import numpy as np
import xgboost as xgb
from utils.path_loader import *
from engine.ember_src import EmberModel
from engine.malconv_src import MalConvModel


# 引擎基类
class EngineBase:

	def __init__(self):
		print('Start engine:{}'.format(self.__class__.__name__))

	# 扫描
	def scan(self, file_path):
		pass

	# 解析
	def __parse(self, *args, **kwargs):
		pass


# Avast引擎
class EngineAvast(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径与扫描结果输出路径
		self.detector_path = AVAST_PATH

	def scan(self, file_path):

		# 调用查杀命令: /_ 表示输出到命令行
		command = '"' + self.detector_path + '\\ashCmd.exe" ' + '"' + file_path + '" /_ /p'
		result = subprocess.getoutput(command)

		return self.__parse(result)

	def __parse(self, result):

		# 读取查杀结果并解析
		infected_count = result[result.rfind('感染文件个数: ') + len('感染文件个数: ')]

		# 读取查杀结果并解析

		if infected_count == '0':

			return 0, 'Undetected'

		else:

			content_list = result.split('\n')

			# 一个样本可能会被识别出多个威胁
			for line in content_list:

				line_list = line.split('\t')

				if line_list[-1] == 'OK':

					continue

				else:

					lab = line_list[-1]
					break

			return 1, lab


# ClamAV引擎
class EngineClamAV(EngineBase):

	def scan(self, file_path):

		command = 'clamdscan ' + file_path
		result = subprocess.getoutput(command)

		return self.__parse(result)

	def __parse(self, result):

		# 读取查杀结果并解析

		if result[result.rfind('Infected files:') + 16] == '0':

			return 0, 'Undetected'

		else:

			left_index = result.find(': ')
			right_index = result.find(' FOUND')

			malware_name = result[left_index + 2:right_index]

			return 1, malware_name


# DrWeb引擎
class EngineDrWeb(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径和查杀结果保存路径
		self.detector_path = DRWEB_PATH
		self.output_path = os.path.join(os.path.join(PROJECT_PATH, 'result'), 'drweb_result.txt')

	def scan(self, file_path):

		# 调用查杀命令
		command = '"' + self.detector_path + '\\dwscancl.exe" ' + '"' + file_path + '" /RP:' + '"' + self.output_path + '"'
		subprocess.call(command)
		return self.__parse()

	def __parse(self, result=''):

		# 读取查杀结果并解析
		with open(self.output_path, 'r+') as f:

			result = f.read()

			# 解析文件出错了
			if 'raised error condition' in result:

				return 0, 'Error'

			elif result[result.rfind('infected') - 2] == 'o':

				return 0, 'Undetected'

			else:

				left_index = result.rfind('The mask was translated to "" filter')
				right_index = result.rfind('WARNING! Restore points directories have not been scanned')
				detail = result[left_index + len('The mask was translated to "" filter'):right_index].strip().split(
					'\n')

				for line in detail:
					lab = line[:line.rfind(' - infected')].split(' ')[-1]

					break

				return 1, lab.strip()


# Ember引擎
class EngineEmber(EngineBase):

	def __init__(self):

		super().__init__()
		# 初始化模型
		self.detector = EmberModel(name='Ember')

	def scan(self, file_path):

		# 以二进制方式读取文件
		with open(file_path, 'rb') as f:
			bytez = f.read()

		# 提取特征并检测
		feature = self.detector.extract(bytez)
		result = self.detector.predict(feature)

		return self.__parse(result)

	def __parse(self, result):

		if result > self.detector.threshold:

			result = 'Confidence:' + str(round(result * 100, 2)) + '%'

			return 1, result
		else:
			return 0, 'Undetected'


# ESET引擎
class EngineESET(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径
		self.detector_path = ESET_PATH

	def scan(self, file_path):

		# 调用查杀命令
		command = '"' + self.detector_path + '\\ecls.exe" /files ' + '"' + file_path + '"'
		result = subprocess.getoutput(command)

		return self.__parse(result)

	def __parse(self, result=''):

		# 读取查杀结果并解析
		if result[result.rfind('检测到:') + 20] != '0':
			left_index = result.find('结果=“')
			right_index = result.find('”，操作=')

			return 1, result[left_index + len('结果=“'):right_index].strip(' 的变量')
		else:
			return 0, 'Undetected'


# 火绒引擎
class EngineHuoRong(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径
		self.detector_path = HUORONG_PATH

		# 加载窗口处理dll
		pDLL = None
		try:
			pDLL = ctypes.WinDLL(HUORONG_DLL32_PATH)
		except:
			try:
				pDLL = ctypes.WinDLL(HUORONG_DLL64_PATH)
			except:
				print("Load Native Library Error.")
		self.getHandle = pDLL.getHandle
		self.click = pDLL.click

	def scan(self, file_path):
		class LogDB:
			def __init__(self):
				self.db = sqlite3.connect(HUORONG_DATABASE_PATH)

			def get_current_id(self):
				return self.db.execute("select max(id) from HrLogV3 where fname='scan'").fetchone()[0]

			def get_detail_by_id(self, id):
				return self.db.execute("select detail from HrLogV3 where id = {}".format(id)).fetchone()[0]

		try:
			self.log_db = LogDB()
			current_id = self.log_db.get_current_id()
			command = '"' + self.detector_path + '\\HipsMain.exe" -s ' + '"' + file_path + '"'
			subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			while True:
				handle = self.getHandle()
				if handle != -1:
					break
			while True:
				self.click(handle, 655, 40)
				next_id = self.log_db.get_current_id()
				if next_id != current_id:
					break
				time.sleep(0.5)
			result = self.log_db.get_detail_by_id(next_id)
			return self.__parse(result)
		except:
			return "检测失败"

	def __parse(self, result):

		if json.loads(result)['detail']['threats'] == 0:

			return 0, 'Undetected'

		else:

			return 1, json.loads(result)['detail']['threat_list'][0]['det']


# 卡巴斯基引擎
class EngineKaspersky(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径和查杀结果保存路径
		self.detector_path = KASPERSKY_PATH

	def scan(self, file_path):

		# 调用查杀命令
		command = '"' + self.detector_path + '\\avp.com" scan /i0 ' + '"' + file_path + '"'
		output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		result = output.stdout.read().decode('utf-8')
		return self.__parse(result)

	def __parse(self, result=''):

		# 读取查杀结果并解析
		if 'Total detected:	1' in result:

			# 检测结果有两种形式, 分别'suspicion xxxx'和'detected xxxx'
			if 'suspicion' in result:

				left_index = result.find('suspicion')
				result = result[left_index + len('suspicion'):].split('\n')[0].strip()

			else:

				left_index = result.find('detected')
				result = result[left_index + len('detected'):].split('\n')[0].strip()

			return 1, result

		else:

			return 0, 'Undetected'


# MalConv引擎
class EngineMalConv(EngineBase):

	def __init__(self):

		super().__init__()
		# 初始化模型
		self.detector = MalConvModel()

	def scan(self, file_path):

		# 以二进制方式读取文件
		with open(file_path, 'rb') as f:
			bytez = f.read()

		# 提取特征并检测
		result = self.detector.predict(bytez)

		return self.__parse(result)

	def __parse(self, result):

		if result > self.detector.threshold:

			result = 'Confidence:' + str(round(result * 100, 2)) + '%'

			return 1, result
		else:
			return 0, 'Undetected'


# MicroSoft引擎
class EngineMicrosoft(EngineBase):

	def __init__(self):

		# 引擎路径与扫描结果输出路径
		super().__init__()
		self.detector_path = MICROSOFT_PATH

	def scan(self, file_path):

		# 调用查杀命令: /_ 表示输出到命令行
		command = '"' + self.detector_path + '\\MpCmdRun.exe" -Scan -ScanType 3 -File ' + file_path + ' -DisableRemediation'
		result = subprocess.getoutput(command)
		return self.__parse(result)

	def __parse(self, result):

		# 读取查杀结果并解析

		if 'found no threats' in result:

			return 0, 'Undetected'

		else:

			# 获取检测类别
			left_index = result.find('Threat                  :')
			right_index = result.find('Resources')

			return 1, result[left_index + len('Threat                  :'):right_index].strip()


# Novel引擎
class EngineNovel(EngineBase):

	def __init__(self):

		super().__init__()
		# 初始化模型
		self.detector = EmberModel(name='Novel')

	def scan(self, file_path):

		# 以二进制方式读取文件
		with open(file_path, 'rb') as f:
			bytez = f.read()

		# 提取特征并检测
		feature = self.detector.extract(bytez)
		result = self.detector.predict(feature)

		return self.__parse(result)

	def __parse(self, result):

		if result > self.detector.threshold:

			result = 'Confidence:' + str(round(result * 100, 2)) + '%'

			return 1, result
		else:
			return 0, 'Undetected'


# Winner引擎
class EngineWinner(EngineBase):

	def __init__(self):

		super().__init__()
		loaded_model = xgb.Booster()
		loaded_model.load_model(WINNER_PATH)
		# 初始化模型和特征提取器
		self.model = loaded_model
		self.extractor = EmberModel().extractor

	def scan(self, file_path):

		# 以二进制方式读取文件
		with open(file_path, 'rb') as f:
			bytez = f.read()

		# 提取特征并检测
		feature = np.array(self.extractor.feature_vector(bytez), dtype=np.float32)
		feature = feature.reshape(1, 2381)
		dtest = xgb.DMatrix(feature)
		result = self.model.predict(dtest)[0]

		return self.__parse(result)

	def __parse(self, result):

		if result > 0.5:

			result = 'Confidence:' + str(round(result * 100, 2)) + '%'

			return 1, result
		else:
			return 0, 'Undetected'


# 360杀毒引擎
class EngineQihoo(EngineBase):

	def __init__(self):

		super().__init__()
		# 引擎路径和扫描结果输出路径
		self.detector_path = QIHOO_PATH
		self.output_path = QIHOO_LOG_PATH

	def scan(self, file_path):

		# 获取扫描的时间
		scan_time = time.localtime(time.time())
		scan_time = time.strftime('%Y%m%d%H%M%S', scan_time)

		# 调用查杀命令
		command = '"' + self.detector_path + '\\360sd.exe" ' + '"' + file_path + '"'
		subprocess.call(command)

		return self.__parse(scan_time)

	def __parse(self, scan_time):

		# 读取查杀结果并解析

		while True:

			log_list = os.listdir(self.output_path)
			last_log_time = log_list[-1][:-4]

			if last_log_time < scan_time:

				continue

			else:
				# 360杀毒可能没有释放文件句柄，会抛出Permission Denied异常
				try:
					with open(self.output_path + '\\' + log_list[-1], 'r+') as f:

						content = f.read()
					break

				# 出错了一直读，直到读取成功为止
				except:

					continue

		if '未发现威胁文件' in content:

			return 0, 'Class'

		else:

			return 1, 'Class'
