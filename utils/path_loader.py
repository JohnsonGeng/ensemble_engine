# -*- coding: utf=8 -*-
# @Time: 2023/11/7 
# @Author: Johnson Geng
# @FIle: path_loader.py 
# @Description: 项目路径配置


import os
import sys
import configparser

# 当前脚本路径
MODULE_PATH = os.path.split(os.path.abspath(sys.modules[__name__].__file__))[0]
# 项目路径
PROJECT_PATH = os.path.split(MODULE_PATH)[0]

# 读取配置文件
config = configparser.ConfigParser()
config.optionxform = str
config.read(os.path.join(PROJECT_PATH, 'config.ini'))


MODEL_PATH = os.path.join(os.path.join(PROJECT_PATH, 'engine'), 'model')
# Avast路径
AVAST_PATH = config['PATH']['avast_path']
# DrWeb路径
DRWEB_PATH = config['PATH']['drweb_path']
# ESET路径
ESET_PATH = config['PATH']['eset_path']
# HuoRong路径
HUORONG_PATH = config['PATH']['huorong_path']
# HuoRong32位DLL路径
HUORONG_DLL32_PATH = config['PATH']['huorong_dll32_path']
# HuoRong64位DLL路径
HUORONG_DLL64_PATH = config['PATH']['huorong_dll64_path']
# HuoRong数据库路径
HUORONG_DATABASE_PATH = config['PATH']['huorong_sql_path']
# Kaspersky路径
KASPERSKY_PATH = config['PATH']['kaspersky_path']
# MicroSoft路径
MICROSOFT_PATH = config['PATH']['microsoft_path']
# Winner路径
WINNER_PATH = os.path.join(MODEL_PATH, 'winner.model')
# 360路径
QIHOO_PATH = config['PATH']['qihoo_path']
# 360日志路径
QIHOO_LOG_PATH = config['PATH']['qihoo_log_path']