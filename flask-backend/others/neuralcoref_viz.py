import spacy
import neuralcoref

# Download the en_core_web_sm model (if not already installed)
try:
    spacy.load('en_core_web_sm')
except OSError:
    print("Downloading en_core_web_sm model...")
    # Download the model if it's not installed
    from spacy.cli import download
    download('en_core_web_sm')

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

# Add NeuralCoref to SpaCy's pipeline
neuralcoref.add_to_pipe(nlp)

# Your text
text = "The quick brown fox jumps over the lazy dog. It is very quick."

# Process the text
doc = nlp(text)

# Print coreferences
for cluster in doc._.coref_clusters:
    print(cluster)

# Visualization part
from spacy import displacy
displacy.serve(doc, style='dep')