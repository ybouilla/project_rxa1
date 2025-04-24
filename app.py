# app.py

import tempfile
from typing import Dict
from flask import Flask, jsonify, request, redirect, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

from process_ecg import process_ecg

ACTIVATE_CORS = True
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}
BUILD_DIR = os.path.join('frontend', 'build')
app = Flask(__name__, static_folder=BUILD_DIR, static_url_path='/')

if ACTIVATE_CORS:
	CORS(app)  # handling Cross Origin Resource Sharing, making AJAX possible


app.config.from_prefixed_env()
app.static_folder = app.config.get('FRONTEND_PATH', BUILD_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
	"""Checks if filename has a csv extension
	"""
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file() -> Dict[Response, int]:

	# check if the post request has the file part
	if 'file' not in request.files:

		return redirect(request.url)
	file = request.files['file']

	# If the user does not select a file, the browser submits an
	# empty file without a filename.
	if file.filename == '':

		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)


		if not os.path.exists(app.config['UPLOAD_FOLDER']):
			os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
		with tempfile.TemporaryDirectory(dir=app.config['UPLOAD_FOLDER']) as dir:

			file.save(os.path.join(dir, filename))
			mean_cycle, min_cycle, max_cycle = process_ecg(os.path.join(dir, filename))

		resp = {
			'message': 'ok',
			'mean_cycle': float(mean_cycle),
			'min_cycle': min_cycle,
			'max_cycle': max_cycle
		}

		return jsonify(resp), 201
	resp = {
		'message': 'bad file format'
	}
	return jsonify(resp), 422


@app.route('/')
def index() -> Response:
    return app.send_static_file('index.html')


if __name__ == '__main__':
	app.run()
