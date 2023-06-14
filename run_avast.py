import os
from Engine.Avast import Engine_avast
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 上传样本保存绝对路径
UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'avast_upload')

# 初始化引擎
e_avast = Engine_avast()
    
    
# 检测接口
@app.route('/detect', methods=['GET', 'POST'])
def detect():
    
    # 获取上传样本并保存
    file = request.files.get('file')
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_PATH, filename))
    
    result = {}
    file_path = UPLOAD_PATH+'\\'+filename

    
    # 调用引擎查杀
    r = e_avast.scan(file_path)
    result['result'] = r[0]
    result['lab_pro'] = r[1]
    
    try:
        os.remove(file_path)
        print('已删除文件{}'.format(filename))
    except:
        print('文件已删除!')
    
    return jsonify(result)
    
    
    
if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True)