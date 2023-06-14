import subprocess
from Engine.Engine import Engine_base


# 卡巴斯基引擎 
class Engine_kaspersky(Engine_base):

    def __init__(self):
        
        # 引擎路径和查杀结果保存路径
        self.detector_path = 'C:\\Program Files (x86)\\Kaspersky Lab\\Kaspersky Total Security 21.3'
       

    def scan(self, file_path):
        
        # 调用查杀命令
        command = '"' + self.detector_path + '\\avp.com" scan /i0 ' + '"' + file_path + '"'
        result = subprocess.getoutput(command)
        return self.__parse(result)
        
                
                
    def __parse(self, result=''):
    
        # 读取查杀结果并解析
        if 'Total detected:	1' in result:
            
            # 检测结果有两种形式, 分别'suspicion xxxx'和'detected xxxx'
            if 'suspicion' in result:
                
                left_index = result.find('suspicion')
                result = result[left_index+len('suspicion'):].split('\n')[0].strip()
                
            else:
            
                left_index = result.find('detected')
                result = result[left_index+len('detected'):].split('\n')[0].strip()
          
            
            return 1, result
            
        else:
        
            return 0, 'Undetected'
         
          
        
if __name__ == '__main__':

    
    # 调用测试
    e_kas = Engine_kaspersky()
    file_path = 'd:\\setup.exe'
    print(e_kas.scan(file_path))
    
    
    
    
