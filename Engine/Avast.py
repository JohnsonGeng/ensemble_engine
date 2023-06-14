import subprocess
from Engine.Engine import Engine_base

 
# Avast引擎 
class Engine_avast(Engine_base):

    def __init__(self):
   
        # 引擎路径与扫描结果输出路径
        self.detector_path = 'C:\\Program Files\\Avast Software\\Avast'
        
        
    def scan(self, file_path):
   
        
        # 调用查杀命令: /_ 表示输出到命令行
        command = '"' + self.detector_path + '\\ashCmd.exe" ' + '"' + file_path + '" /_ /p'
        result = subprocess.getoutput(command)
        
        
        return self.__parse(result, file_path)
        
        
    def __parse(self, result, file_path):
        
         # 读取查杀结果并解析
        infected_count = result[result.rfind('感染文件个数: ')+len('感染文件个数: ')]
        
        
        # 读取查杀结果并解析
        
        if infected_count == '0':
            
            return 0, 'Undetected'
            
        else:

            content_list = result.split('\n')       
            
            
            # 一个样本可能会被识别出多个威胁
            for line in content_list:
                
                line_list = line.split('\t')
                
                if line_list[-1] == 'OK':
                    
                    continue
                
                else:
                
                    lab = line_list[-1]
                    break
        
            return 1, lab

        
if __name__ == '__main__':

    
    # 调用测试
    e_avast = Engine_avast()
    e_huorong = Engine_huorong()
    file_path = 'd:\\setup.exe'
    
    print(e_avast.scan(file_path))
    print(e_huorong.scan(file_path))
    
    
    
    
