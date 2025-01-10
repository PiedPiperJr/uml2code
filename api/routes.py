import io
import os
import sys
import uuid
from .services.file_processor import process_file
from flask import Blueprint, request, send_file, jsonify, after_this_request

bp = Blueprint('routes', __name__)

@bp.route('/process', methods=['POST'])
def process_drawio_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    gen_path = str(uuid.uuid4())
    tmp_path = os.path.join(os.getcwd(), 'api', f'{gen_path}')
    os.makedirs(tmp_path, exist_ok=True)
    file_path = os.path.join(tmp_path, f"{file.filename}")
    file.save(file_path)
    file.close()

    try:
        # generate java classes and build a zip
        zip_path = process_file(file_path, tmp_path, gen_path)

        # @after_this_request decorator doesn't works on windows cause the delete_file() method is called before the file is sent. 
        if sys.platform == "win32":
            # load zip file in memory, delete the file, and return stored data(maybe there's a better alternative ?)
            return_data = io.BytesIO()
            with open(zip_path, 'rb') as fp:
                return_data.write(fp.read())
            return_data.seek(0)
            os.remove(zip_path)
            return send_file(return_data, download_name="generated_classes.zip", max_age=0)

        elif sys.platform == "linux":
            @after_this_request
            def remove_zip(response):
                try:
                    os.remove(zip_path)
                    return response
                except Exception as e:
                    return jsonify({"error": str(e)}), 400
            return send_file(zip_path, download_name="generated_classes.zip", max_age=0)
        else:
            print("bad server platform")
            return jsonify({"internal error": {}}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400