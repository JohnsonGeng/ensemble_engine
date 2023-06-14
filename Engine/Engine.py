# 引擎基类
class Engine_base:

    def __init__(self):
    
        print('Start Engine:{}'.format(self.__class__.__name__))

    # 扫描
    def scan(self, file_path):

        pass

    # 解析
    def __parse(self, result=''):

        pass
 