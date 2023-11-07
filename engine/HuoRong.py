import os
import sys
import time
import json
import ctypes
import sqlite3
import subprocess
from engine.Engine import Engine_base



# 火绒引擎
class Engine_huorong(Engine_base):

    def __init__(self):
    
        # 引擎路径
        self.detector_path = 'C:\\Program Files (x86)\\Huorong\\Sysdiag\\bin\\'
    
        # 加载窗口处理dll
        pDLL = None
        try:
            pDLL = ctypes.WinDLL("C:\\Users\\huaxi-lab\\Desktop\\ensemble_engine\\engine\\lib\\huorong.dll")
        except:
            try:
                pDLL = ctypes.WinDLL("C:\\Users\\huaxi-lab\\Desktop\\ensemble_engine\\engine\\lib\\huorong_64.dll")
            except:
                print("Load Native Library Error.")
        self.getHandle = pDLL.getHandle
        self.click = pDLL.click
       

    def scan(self, file_path):
        class LogDB:
            def __init__(self):
                self.db = sqlite3.connect(r"C:\ProgramData\Huorong\Sysdiag\log.db")

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

        
if __name__ == '__main__':

    
    # 调用测试
    e_avast = Engine_avast()
    e_huorong = Engine_huorong()
    file_path = 'd:\\setup.exe'
    
    print(e_avast.scan(file_path))
    print(e_huorong.scan(file_path))
    
    
    
    
