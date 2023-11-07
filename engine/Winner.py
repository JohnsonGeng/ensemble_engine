# -*- coding: utf=8 -*-
# @Time: 2023/10/21 
# @Author: Johnson Geng
# @FIle: Winner.py 
# @Description: ...

import os
import sys
import numpy as np
import xgboost as xgb
from engine.ember_src import EmberModel
from engine.Engine import Engine_base


# 获取脚本根目录
MODULE_PATH = os.path.split(os.path.abspath(sys.modules[__name__].__file__))[0]
MODEL_PATH = os.path.join(MODULE_PATH, 'model')

# Winner引擎
class Engine_winner(Engine_base):

	def __init__(self):

		loaded_model = xgb.Booster()
		loaded_model.load_model(os.path.join(MODEL_PATH, 'winner.model'))
		print(loaded_model)
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