import subprocess
from engine.Engine import Engine_base


# Clamav引擎     
class Engine_clamav(Engine_base):
        
    
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
            
            malware_name = result[left_index+2:right_index]     

            
            return 1, malware_name
     
    
