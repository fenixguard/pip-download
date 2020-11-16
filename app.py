import io
import os
import zipfile

import pip
import tempfile
from base64 import b64encode
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from parsers import pip_parser

app = Flask(__name__)
Bootstrap(app)


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
        return b64encode(bytes(memory_zip.getvalue())), 200


if __name__ == '__main__':
    app.run()
