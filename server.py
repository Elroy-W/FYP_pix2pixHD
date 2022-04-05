
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import shutil
import json

UPLOAD_FOLDER = './test_data/test_A'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Hello World!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
        os.mkdir(app.config['UPLOAD_FOLDER'])
        shutil.rmtree('./test_data/result')
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.system(
                'python new_test.py --name fyp-wer --dataroot ./test_data --label_nc 0 --how_many 1 --no_instance --resize_or_crop none --results_dir ./test_data/result')
            result = {"result": [{
                "original": "../test_data/result/fyp-wer/test_latest/images/"+filename.rsplit('.', 1)[0] + "_input_label.png",
                "retouched": "../test_data/result/fyp-wer/test_latest/images/"+filename.rsplit('.', 1)[0] + "_synthesized_image.png"
            }
            ]}

            with open('./web/asset/Json/template.json', 'w') as result_file:
                result_file.write(json.dumps(result))
                result_file.close()
            return redirect('http://localhost:5500/web/result.html')

    return redirect('http://localhost:5500/web/home.html')


if __name__ == '__main__':
    # for debugging
    app.debug = True
    app.run()
