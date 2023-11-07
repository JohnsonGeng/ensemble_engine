import subprocess
from engine.Engine import Engine_base
     
 
# Sophos引擎   
class Engine_sophos(Engine_base):
        
        
    def scan(self, file_path):
        
        command = 'savscan ' + file_path + ' -remove'
        result = subprocess.getoutput(command)
        
        return self.__parse(result)
        
        
    def __parse(self, result):
    
        
        if 'No viruses were discovered' in result:
            
            return 0
            
        else:
        
            return 1 
    
