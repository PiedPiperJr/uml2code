import os
import json
import time
import uuid
import shutil
import tempfile
from werkzeug.utils import secure_filename

from services.network import download_file
from services.file_processor import process_file, copy_tree
from services.project_builder import create_spring_boot_project
from flask import Blueprint, request, send_file, jsonify, after_this_request


bp = Blueprint('routes', __name__)

@bp.route('/process', methods=['POST'])
def process_drawio_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Récupération des données JSON sous forme de texte
    data_raw = request.form.get('data')
    if not data_raw:
        return jsonify({"error": "Missing 'data' field"}), 400

    try:
        data = json.loads(data_raw)  # Parse en JSON
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in 'data'"}), 400
                
    temp_dir = tempfile.mkdtemp()
    filename = secure_filename(file.filename)
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)
    
    # Prepare output directory
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    zip_name = f"generated_{uuid.uuid4().hex[:8]}"
    
    if data['type'] == 'springboot':
        # create spring boot project
        print(output_dir)
        create_spring_boot_project(data['spring_data'], output_dir)
        
        # download and replace the pom.xml file with the request provided data
        download_file(data['pomxml_url'], output_dir)
        
        classes_path = os.path.join(output_dir, 'src', 'main', 'java', *(data['spring_data']['groupId'].split('.')), data['spring_data']['name'])
        package_name = data['spring_data']['packageName']
        zip_path = process_file(
            diagram_path=file_path,
            ouput_dir=classes_path,
            zip_name=zip_name,
            folder_to_zip=output_dir,
            language='springboot',
            package_name=package_name
        )
        print('zip path = ', zip_path)
        
    elif data['type'] == 'laravel':
        # copy laravel project structure to the tmp folder
        copy_tree('./build/laravel', output_dir)
        zip_path = process_file(
            diagram_path=file_path,
            ouput_dir=output_dir,
            zip_name=zip_name,
            language='laravel'
        )
    else:
        return jsonify({"error": f"Unsupported framework type: {data['type']}"}), 400
    
    @after_this_request
    def cleanup(response):
        try:
            # os.remove(file_path)
            os.remove(zip_path)
            # os.rmdir(output_dir)
            # os.rmdir(temp_dir)
        except Exception as e:
            print(f"Error during cleanup: {e}")
        return response
    
    # Send the zip file
    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{zip_name}.zip"
    )
        
    # except ValueError as e:
    #     return jsonify({"error": str(e)}), 400
    
    # except Exception as e:
    #     return jsonify({"error": f"Processing failed: {str(e)}"}), 500