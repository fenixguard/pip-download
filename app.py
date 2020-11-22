import io
import os
import zipfile

import pip
import tempfile
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap

from parsers import pip_parser, download_parser

app = Flask(__name__)
Bootstrap(app)

BASE_DIR = os.getcwd()


@app.route('/')
@app.route('/index')
def view_index():
    return render_template('index.html')


@app.route('/get_dependencies', methods=['POST', 'GET'])
def get_dependencies():
    args = pip_parser.parse_args()
    package = args['package']
    options = args['options']
    with tempfile.TemporaryDirectory() as temp:
        if options:
            pip.main(['download', '-d', os.path.join(temp, 'packages'), options, package])
        else:
            pip.main(['download', '-d', os.path.join(temp, 'packages'), package])

        files = os.listdir(os.path.join(temp, 'packages'))
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:

            for file in files:
                with open(os.path.join(temp, 'packages', file), mode='rb') as ff:
                    zip_file.writestr(file, ff.read())
        memory_zip.seek(0)

        return send_file(memory_zip, as_attachment=True, attachment_filename=f'{package}.zip')   # return b64encode(bytes(memory_zip.getvalue())), 200


if __name__ == '__main__':
    app.run()
