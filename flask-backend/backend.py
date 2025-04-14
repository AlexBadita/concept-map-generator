# For file and directory operations
import os

# Flask framework for building the backend
from flask import Flask, request, jsonify
# To handle Cross-Origin Resource Sharing (CORS)
from flask_cors import CORS

# Handles processing the text amd extracting (concept -> relation -> concept) pairs
from logic import coreference_resolution, find_concept_link_concept_pairs
# Handles generating the graph layout (the coordinates of the nodes and edges)
from graph import generate_layout
# Handles extracting additional information from the PDF for an improved graph
from ranking import extract_text_from_pdf, rank_abstract_concepts, rank_tokens, filter_concept_map

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS for the app
CORS(app)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Endpoint to handle text and file uploads for generating a concept map
@app.route('/send-data', methods=['POST'])
def receive_data():
    try:
        # Retrieve text and file from the request
        text = request.form.get('text', '')
        file = request.files.get('file', None)

        concept_map = []
        if text:
            # Perform coreference resolution on the input text
            resolved_text = coreference_resolution(text)
            # Extract concept map (concept -> relation -> concept) pairs
            concept_map = find_concept_link_concept_pairs(resolved_text)

        if file:
            # Save the uploaded file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Extract text from the uploaded PDF file
            file_text = extract_text_from_pdf(file_path)
            # Rank tokens extracted from the file text
            ranked_tokens = rank_tokens(file_text)
            # Rank abstract concepts based on the resolved text and ranked tokens
            ranked_abstract_concepts = rank_abstract_concepts(resolved_text, ranked_tokens)
            # Filter the concept map based on the ranked abstract concepts
            concept_map = filter_concept_map(concept_map, ranked_abstract_concepts)

        # Generate a graph layout for the concept map
        graph = generate_layout(concept_map)
        # Return the graph as a JSON response
        return jsonify({"success": True, "graph": graph}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to handle text-only input for generating a concept map
@app.route('/send-text', methods=['POST'])
def receive_text():
    try:
        # Retrieve JSON data from the request
        data = request.json
        text = data.get('text', '')
        # Perform coreference resolution on the input text
        resolved_text = coreference_resolution(text)
        # Extract concept map (concept -> relation -> concept) pairs
        concept_map = find_concept_link_concept_pairs(resolved_text)
        # Generate a graph layout from the concept map
        graph = generate_layout(concept_map)
        # Return the graph as a JSON response
        return jsonify({"success": True, "graph": graph}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

""" TO DO
# Endpoint to handle file-only input for extracting and ranking concepts
@app.route('/send-file', methods=['POST'])
def receive_file():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        # Save the uploaded file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # Extract text from the uploaded PDF file
        text = extract_text_from_pdf(file_path)
        # Rank concepts extracted from the text
        ranked_tokens = rank_concepts(text)
        # Return the ranked tokens as a JSON response
        return jsonify(ranked_tokens)
"""

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)