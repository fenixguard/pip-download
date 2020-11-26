import io
import os
import zipfile
import shutil
from subprocess import Popen
from typing import Optional

import pip
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import FileStorage

from parsers import pip_parser, requirements_parser, download_parser

app = Flask(__name__)
Bootstrap(app)

BASE_DIR = os.getcwd()
PACKAGE_DIR = 'packages'
REQUIREMENTS_DIR = 'requirements'


@app.route('/')
@app.route('/index')
def view_index():
    return render_template('index.html')


@app.route('/requirements')
def view_requirements():
    return render_template('requirements.html')


def create_clear_directories():
    try:
        shutil.rmtree(os.path.join(BASE_DIR, PACKAGE_DIR))
    except Exception as error:
        print(error)
    try:
        shutil.rmtree(os.path.join(BASE_DIR, REQUIREMENTS_DIR))
    except Exception as error:
        print(error)
    try:
        os.mkdir(os.path.join(BASE_DIR, PACKAGE_DIR))
    except Exception as error:
        print(error)
    try:
        os.mkdir(os.path.join(BASE_DIR, REQUIREMENTS_DIR))
    except Exception as error:
        print(error)


def get_zip_stream():
    files = os.listdir(os.path.join(BASE_DIR, PACKAGE_DIR))
    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            with open(os.path.join(BASE_DIR, PACKAGE_DIR, file), mode='rb') as ff:
                zip_file.writestr(file, ff.read())
    memory_zip.seek(0)
    return memory_zip


@app.route('/requirements/post_requirements', methods=['POST'])
def post_requirements():
    args = requirements_parser.parse_args()
    options: str = args['options']
    if 'requirements' not in args:
        return '', 500
    requirements: Optional[FileStorage] = args['requirements']
    create_clear_directories()
    requirements.save(os.path.join(BASE_DIR, REQUIREMENTS_DIR, 'requirements.txt'))
    if requirements and options:
        pip.main(['download',
                  '-d', os.path.join(BASE_DIR, PACKAGE_DIR),
                  '-r', os.path.join(BASE_DIR, REQUIREMENTS_DIR, 'requirements.txt'),
                  options])
        # Popen(f"pip download -d {os.path.join(BASE_DIR, PACKAGE_DIR)} -r {os.path.join(BASE_DIR, REQUIREMENTS_DIR, 'requirements.txt')} {options}").wait()
    elif requirements and not options:
        pip.main(['download',
                  '-d', os.path.join(BASE_DIR, PACKAGE_DIR),
                  '-r', os.path.join(BASE_DIR, REQUIREMENTS_DIR, 'requirements.txt')])
        # Popen(f"pip download -d {os.path.join(BASE_DIR, PACKAGE_DIR)} -r {os.path.join(BASE_DIR, REQUIREMENTS_DIR, 'requirements.txt')}").wait()
    files = os.listdir(os.path.join(BASE_DIR, PACKAGE_DIR))
    if len(files) == 0:
        return '', 500
    return '', 204


@app.route('/requirements/get_requirements', methods=['GET'])
def get_requirements():
    return send_file(get_zip_stream(), as_attachment=True,
                     attachment_filename='requirements_dependencies.zip')


@app.route('/post_dependencies', methods=['POST'])
def post_dependencies():
    args = pip_parser.parse_args()
    package: str = args['package']
    options: str = args['options']
    create_clear_directories()
    if options and package:
        pip.main(['download',
                  '-d', os.path.join(BASE_DIR, PACKAGE_DIR),
                  options,
                  package])
        # Popen(f"pip download -d {os.path.join(BASE_DIR, PACKAGE_DIR)} {options} {package}").wait()
    else:
        pip.main(['download',
                  '-d', os.path.join(BASE_DIR, PACKAGE_DIR),
                  package])
        # Popen(f"pip download -d {os.path.join(BASE_DIR, PACKAGE_DIR)} {package}").wait()
    files = os.listdir(os.path.join(BASE_DIR, PACKAGE_DIR))
    if len(files) == 0:
        return '', 500
    return '', 204


@app.route('/get_dependencies', methods=['GET'])
def get_dependencies():
    args = pip_parser.parse_args()
    package: str = args['package']

    return send_file(get_zip_stream(), as_attachment=True,
                     attachment_filename=f'{package}.zip')


if __name__ == '__main__':
    app.run()
