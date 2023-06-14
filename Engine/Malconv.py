from Engine.Engine import Engine_base
from Engine.malconv_src import MalConvModel

# Malconv引擎
class Engine_malconv(Engine_base):

    def __init__(self):

        # 初始化模型
        self.detector = MalConvModel()



    def scan(self, file_path):

        # 以二进制方式读取文件
        with open(file_path, 'rb') as f:
            bytez = f.read()

        # 提取特征并检测
        result = self.detector.predict(bytez)

        return self.__parse(result)

    def __parse(self, result):

        if result > self.detector.threshold:
            
            result = 'Confidence:'+str(round(result*100,2))+'%'
            
            return 1, result
        else:
            return 0, 'Undetected'

    
    
    
