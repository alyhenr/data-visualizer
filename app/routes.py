from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from .utils import convertToTxt
from .dataModel import DataModel

routes_bp = Blueprint('routes_bp', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'txt'}
UPLOAD_FOLDER = 'static/uploads'

# Check for allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file is allowed (txt)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Instantiate the DataModel class with the uploaded file
            data_model = DataModel(file_path)

            # Store the labels and data to be used in the next step
            labels = data_model.labels
            return render_template('plot_options.html', labels=labels, filename=filename)

    return render_template('upload.html')

@routes_bp.route('/plot', methods=['POST'])
def plot_data():
    column_name = request.form['column_name']
    plot_type = request.form['plot_type']
    filename = request.form['filename']

    # Recreate the DataModel instance using the filename
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    data_model = DataModel(file_path)

    # Generate the plot as a base64-encoded image
    plot_image = data_model.plot_column(column_name, plot_type)
    
    if plot_image:
        return render_template('plot_options.html', labels=data_model.labels, filename=filename, plot_image=plot_image)
    else:
        return render_template('plot_options.html', labels=data_model.labels, filename=filename, error="Unsupported type of plot for the data provided")


@routes_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')
