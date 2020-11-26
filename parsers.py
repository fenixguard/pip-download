from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

pip_parser = reqparse.RequestParser()
pip_parser.add_argument('package', type=str, required=True, help='Package name', location='args')
pip_parser.add_argument('options', type=str, required=False, help='Options for pip', location='args')

requirements_parser = reqparse.RequestParser()
requirements_parser.add_argument('requirements', type=FileStorage, required=False, store_missing=False, help='Requirements file', location='files')
requirements_parser.add_argument('options', type=str, required=False, help='Options for pip', location='form')

download_parser = reqparse.RequestParser()
download_parser.add_argument('package', type=str, required=True, help='Package name', location='args')
