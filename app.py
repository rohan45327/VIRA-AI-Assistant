from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
from vira import web_command,get_summary
app = Flask(__name__,static_folder='static')
CORS(app)
@app.route('/')
def serve():
    print("Vira Backend is running! Send commands to /command")
    return send_from_directory(app.static_folder,'vira.html')
@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({"response": "No command provided."}),400
    print(f"Received command from web: {command}")
    jarvis_response = web_command(command)
    print(f"Vira response: {jarvis_response}")
    return jsonify({"response": jarvis_response})
@app.route('/upload',methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded."}),400
    file=request.files['file']
    inst = request.form.get('comd', '') 
    file_type=file.content_type
    if file_type=='application/pdf'or file.filename.lower().endswith('.pdf'):
        response_text=get_summary(inst,file)
    else:
        response_text=f"Sorry you provided {file.filename}. But I only Support PDF files"
    return jsonify({"response" : response_text})
if __name__ == '__main__':
    app.run(debug=True, port=5000)