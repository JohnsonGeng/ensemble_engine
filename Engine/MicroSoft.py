import subprocess
from Engine.Engine import Engine_base
 
# WindowsDefender引擎 
class Engine_microsoft(Engine_base):

    def __init__(self):
   
        # 引擎路径与扫描结果输出路径
        self.detector_path = 'C:\\Program Files\\Windows Defender'
        
        
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
            
            
            return 1, result[left_index+len('Threat                  :'):right_index].strip()


    
    
    
