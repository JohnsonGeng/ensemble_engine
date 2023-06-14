import subprocess
from Engine.Engine import Engine_base

        
# ESET引擎
class Engine_eset(Engine_base):

    def __init__(self):
    
        # 引擎路径
        self.detector_path = 'C:\\Program Files\\ESET\\ESET Security'


    def scan(self, file_path):
        
        # 调用查杀命令
        command = '"' + self.detector_path + '\\ecls.exe" /files ' + '"' + file_path + '"'
        result = subprocess.getoutput(command)
        
        return self.__parse(result)


    def __parse(self, result=''):
    
        print(result)
        
        # 读取查杀结果并解析
        if result[result.rfind('被感染') + 13] == '0':
            return 0, 'Undeteced'
        else:
        
            left_index = result.find('威胁="')
            right_index = result.find('"，操作')
            
            return 1, result[left_index+len('威胁="'):right_index].strip(' 的变量')
            