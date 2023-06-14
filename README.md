# 集成检测环境

## 概述

在虚拟机上安装杀毒软件以及机器学习检测模型，通过分发服务器下发样本至各虚拟机，利用杀毒引擎的命令行实现病毒查杀。
支持的杀毒引擎包括:
```
ClamAV
DrWeb
ESET
Kaspersky
MicroSoft
Avast
HuoRong
```
支持的机器学习模型包括:
```
Ember
Malconv
```
后续可继续扩充

## 文件结构
```
-- Engine
    -- lib 火绒安全屏蔽界面所需的动态链接库
    -- model 机器学习模型
    -- Engine.py 引擎基类
    -- DrWeb.py 继承引擎基类的某个引擎
    ...
-- result 引擎查杀的中间结果保存
-- upload 待测样本的临时保存路径
-- run_xxx.sh/run_xxx.bat 运行Flask服务的批处理命令
-- run_xxx.py Flask服务运行脚本
```

## 使用

以使用虚拟机的DrWeb杀毒引擎为例 
1. 在虚拟机上安装DrWeb杀毒软件
2. 安装Python解释器或者Conda环境, 后使用pip install flask安装flask库
3. 检查Engine包中的DrWeb.py中Engine_drweb的detector_path路径是否与安装路径一致(版本号可能会有一定区别)
4. 点击对应的run_xxx.bat/run_xxx.sh批处理脚本, 服务启动