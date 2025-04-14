# For extracting text from PDF files
import fitz
# For handling punctuation
import string
# For regular expressions
import re
# For natural language processing
import spacy
# For removing stopwords
from nltk.corpus import stopwords
# For lemmatizing words
from nltk.stem import WordNetLemmatizer
# For calculating TF-IDF scores
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_noun_phrases(text):
    """
    Extract noun phrases from the input text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of noun phrases.
    """
    # Load the spacy model
    nlp = spacy.load('en_core_web_sm')
    # Apply the NLP pipeline
    doc = nlp(text)
    # Extract noun phrases
    noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
    return noun_phrases

def clean_noun_phrases(noun_phrases):
    """
    Clean noun phrases by removing punctuation, numbers, and newlines.

    Args:
        noun_phrases (list): List of noun phrases.

    Returns:
        list: Cleaned noun phrases.
    """
    cleaned_noun_phrases = []
    for noun_phrase in noun_phrases:
        noun_phrase = noun_phrase.replace('\n', '') # Remove newlines
        noun_phrase = re.sub(r'\d+', '', noun_phrase) # Remove numbers
        noun_phrase = noun_phrase.translate(str.maketrans('', '', string.punctuation)) # Remove punctuation
        if(len(noun_phrase) > 1):  # Exclude very short phrases
            cleaned_noun_phrases.append(noun_phrase)
    return cleaned_noun_phrases

def preprocess_noun_phrases(noun_phrases):
    """
    Preprocess noun phrases by removing stopwords and lemmatizing words.

    Args:
        noun_phrases (list): List of noun phrases.

    Returns:
        list: Preprocessed noun phrases.
    """
    # Load English stopwords
    stop_words = set(stopwords.words('english'))
    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()
    processed_phrases = []
    for phrase in noun_phrases:
        # Split the phrase into words
        words = phrase.split()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        if lemmatized_words:  # Exclude empty phrases
            processed_phrases.append(' '.join(lemmatized_words))
    return processed_phrases

def rank_words_tfidf(noun_phrases):
    """
    Rank words using TF-IDF scores.

    Args:
        noun_phrases (list): List of noun phrases.

    Returns:
        dict: Dictionary of words and their TF-IDF scores.
    """
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Compute the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(noun_phrases)
     # Get the feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    # Sum the TF-IDF scores for each word
    scores = tfidf_matrix.sum(axis=0).A1
    # Create a dictionary of words and their scores
    tfidf_scores = dict(zip(feature_names, scores))
    # top_concepts = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    return tfidf_scores

def rank_tokens(text):
    """
    Rank tokens in the text based on their TF-IDF scores.

    Args:
        text (str): The input text.

    Returns:
        dict: Dictionary of tokens and their TF-IDF scores.
    """
    # Extract noun phrases
    noun_phrases = extract_noun_phrases(text)
    # Clean the noun phrases
    cleaned_noun_phrases = clean_noun_phrases(noun_phrases)
    # Preprocess the noun phrases
    processed_noun_phrases = preprocess_noun_phrases(cleaned_noun_phrases)
     # Rank the words using TF-IDF
    tfidf_scores = rank_words_tfidf(processed_noun_phrases)
    return tfidf_scores

def rank_abstract_concepts(text, ranked_tokens):
    """
    Rank abstract concepts based on their relevance to the text.

    Args:
        text (str): The input text.
        ranked_tokens (dict): Dictionary of tokens and their TF-IDF scores.

    Returns:
        list: Ranked abstract concepts with their scores.
    """
    # Extract noun phrases
    noun_phrases = extract_noun_phrases(text)
    # Preprocess the noun phrases
    preprocessed_noun_phrases = preprocess_noun_phrases(noun_phrases)
    concept_scores = {}
    for i in range(len(preprocessed_noun_phrases)):
        # Compute the score for each concept
        score = compute_concept_score(preprocessed_noun_phrases[i].split(), ranked_tokens)
        concept_scores[noun_phrases[i]] = score
    # Sort concepts by score
    ranked_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_concepts

def compute_concept_score(tokens, tfidf_scores):
    """
    Compute the score of a concept based on its tokens' TF-IDF scores.

    Args:
        tokens (list): List of tokens in the concept.
        tfidf_scores (dict): Dictionary of tokens and their TF-IDF scores.

    Returns:
        float: The highest TF-IDF score among the tokens.
    """
    max = 0
    for token in tokens:
        try:
            # Get the TF-IDF score for the token
            score = tfidf_scores[token]
            if score > max:
                # Update the maximum score
                max = score
        except:
            pass # Ignore tokens not in the TF-IDF dictionary
    return max

def filter_concept_map(concept_map, ranked_concepts, top_n=15):
    """
    Filter the concept map to include only the top-ranked concepts.

    Args:
        concept_map (list): List of concept-relation-concept tuples.
        ranked_concepts (list): List of ranked concepts with their scores.
        top_n (int): Number of top concepts to include.

    Returns:
        list: Filtered concept map.
    """
    new_map = []
    # Get the top N concepts
    top_concepts = [concept[0] for concept in ranked_concepts][:top_n]
    # top_concepts = ranked_concepts[:top_n]
    print(top_concepts)
    for concept1, link, concept2 in concept_map:
        if concept1 in top_concepts and concept2 in top_concepts: # Include only top-ranked concepts
            new_map.append((concept1, link, concept2))
    return new_map