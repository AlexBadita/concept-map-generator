from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from logic import coreference_resolution, find_concept_link_concept_pairs
from graph import generate_layout
from ranking import extract_text_from_pdf, rank_abstract_concepts, rank_tokens, filter_concept_map

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/send-data', methods=['POST'])
def receive_data():
    text = request.form.get('text', '')
    file = request.files.get('file', None)

    if text:
        resolved_text = coreference_resolution(text)
        concept_map = find_concept_link_concept_pairs(resolved_text)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_text = extract_text_from_pdf(file_path)
            ranked_tokens = rank_tokens(file_text)
            print("Ranked ", ranked_tokens)
            ranked_abstract_concepts = rank_abstract_concepts(resolved_text, ranked_tokens)
            print("Ranked abs ", ranked_abstract_concepts)
            concept_map = filter_concept_map(concept_map, ranked_abstract_concepts)
        print("Ranked map ", concept_map)
        graph = generate_layout(concept_map)
        return jsonify(graph)

@app.route('/send-text', methods=['POST'])
def receive_text():
    data = request.json
    text = data.get('text', '')
    resolved_text = coreference_resolution(text)
    concept_map = find_concept_link_concept_pairs(resolved_text)
    graph = generate_layout(concept_map)
    return jsonify(graph)

@app.route('/send-file', methods=['POST'])
def receive_file():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        text = extract_text_from_pdf(file_path)
        ranked_tokens = rank_concepts(text)
        print("Back ", ranked_tokens)
        return jsonify(ranked_tokens)

if __name__ == '__main__':
    app.run(debug=True)