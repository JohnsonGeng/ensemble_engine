import os
import subprocess
from engine.Engine import Engine_base

        
# Drweb引擎 
class Engine_drweb(Engine_base):

    def __init__(self):
        
        # 引擎路径和查杀结果保存路径
        self.detector_path = 'C:\\Program Files\\DrWeb'
        self.output_path = os.path.join(os.path.dirname(__file__), '..\\result') + '\\drweb_result.txt'

    def scan(self, file_path):
        
        # 调用查杀命令
        command = '"' + self.detector_path + '\\dwscancl.exe" ' + '"' + file_path + '" /RP:' + '"'+ self.output_path + '"'
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
                detail = result[left_index+len('The mask was translated to "" filter'):right_index].strip().split('\n')
                
                for line in detail:
                    
                    lab = line[:line.rfind(' - infected')].split(' ')[-1]
                    
                    break

                return 1, lab.strip()