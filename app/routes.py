from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from .handlers import hello

routes_bp = Blueprint('routes_bp', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@routes_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # flash('No file part')
        return redirect(url_for('routes_bp.home'))
    file = request.files['file']
    if file.filename == '':
        # flash('No selected file')
        return redirect(url_for('routes_bp.home'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # flash('File successfully uploaded')
        return redirect(url_for('routes_bp.home'))
    # flash('Invalid file type')
    return redirect(url_for('routes_bp.home'))
