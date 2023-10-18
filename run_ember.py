import os
from Engine.Ember import Engine_ember
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 上传样本保存绝对路径
UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload')

# 初始化引擎构建引擎列表
e_ember = Engine_ember()
   
    
# 检测接口
@app.route('/detect', methods=['GET', 'POST'])
def detect():
    
    # 获取上传样本并保存
    file = request.files.get('file')
    file_name = secure_filename(file.filename)
    file_name = 'Ember_' + file_name
    file.save(os.path.join(UPLOAD_PATH, file_name))

    result = {}
    file_path = os.path.join(UPLOAD_PATH, file_name)

    # 调用引擎查杀
    r = e_ember.scan(file_path)    
    result['result'] = r[0]
    result['lab_pro'] = r[1]

    # GJX: 磁盘容量限制, 需要将扫描完的文件删除
    try:
        os.remove(file_path)
        print('已删除文件{}'.format(file_name))
    except:
        print('文件已删除!')
    
    return jsonify(result)

    
if __name__ == '__main__':

    app.run('0.0.0.0', port=5002, threaded=True)

