import os
import time
import subprocess
from engine.Engine import Engine_base

        
# 360引擎
# 注:需要将360杀毒安装路径（一般是C:\Program Files\360\360sd）下的Log\VirusScanLog文件夹读取权限打开
class Engine_360(Engine_base):

    def __init__(self):
        
        # 引擎路径和扫描结果输出路径
        self.detector_path = 'C:\\Program Files\\360\\360sd'
        self.output_path =  self.detector_path+'\\Log\\VirusScanLog'

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
        
            return 0
            
        else:
        
            return 1
   
      
    
    
