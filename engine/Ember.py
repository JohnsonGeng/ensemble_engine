from engine.ember_src import EmberModel
from engine.Engine import Engine_base

# Ember引擎
class Engine_ember(Engine_base):

    def __init__(self):

        # 初始化模型
        self.detector = EmberModel(name='Ember')

    def scan(self, file_path):

        # 以二进制方式读取文件
        with open(file_path, 'rb') as f:
            bytez = f.read()

        # 提取特征并检测
        feature = self.detector.extract(bytez)
        result = self.detector.predict(feature)

        return self.__parse(result)


    def __parse(self, result):

        if result > self.detector.threshold:
            
            result = 'Confidence:'+str(round(result*100,2))+'%'        
    
            return 1, result
        else:
            return 0, 'Undetected'

    
    
    
    
