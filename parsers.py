from flask_restplus import reqparse

pip_parser = reqparse.RequestParser()
pip_parser.add_argument('package', type=str, required=True, help='Package name', location='args')
pip_parser.add_argument('options', type=str, required=False, help='Options for pip', location='args')

archive_parser = reqparse.RequestParser()
archive_parser.add_argument('package', type=str, required=True, help='Package name', location='args')
