import fitz
import string
import re
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_noun_phrases(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
    return noun_phrases

def clean_noun_phrases(noun_phrases):
    cleaned_noun_phrases = []
    for noun_phrase in noun_phrases:
        noun_phrase = noun_phrase.replace('\n', '')
        noun_phrase = re.sub(r'\d+', '', noun_phrase)
        noun_phrase = noun_phrase.translate(str.maketrans('', '', string.punctuation))
        if(len(noun_phrase) > 1):
            cleaned_noun_phrases.append(noun_phrase)
    return cleaned_noun_phrases

def preprocess_noun_phrases(noun_phrases):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    processed_phrases = []
    for phrase in noun_phrases:
        words = phrase.split()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        if lemmatized_words:
            processed_phrases.append(' '.join(lemmatized_words))
    return processed_phrases

def rank_words_tfidf(noun_phrases):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(noun_phrases)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    tfidf_scores = dict(zip(feature_names, scores))
    # top_concepts = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    return tfidf_scores

def rank_tokens(text):
    noun_phrases = extract_noun_phrases(text)
    cleaned_noun_phrases = clean_noun_phrases(noun_phrases)
    processed_noun_phrases = preprocess_noun_phrases(cleaned_noun_phrases)
    tfidf_scores = rank_words_tfidf(processed_noun_phrases)
    return tfidf_scores

def rank_abstract_concepts(text, ranked_tokens):
    noun_phrases = extract_noun_phrases(text)
    preprocessed_noun_phrases = preprocess_noun_phrases(noun_phrases)
    concept_scores = {}
    for i in range(len(preprocessed_noun_phrases)):
        score = compute_concept_score(preprocessed_noun_phrases[i].split(), ranked_tokens)
        concept_scores[noun_phrases[i]] = score
    ranked_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_concepts

def compute_concept_score(tokens, tfidf_scores):
    max = 0
    for token in tokens:
        try:
            score = tfidf_scores[token]
            if score > max:
                max = score
        except:
            pass
    # return max(tfidf_scores[token] for token in tokens)
    return max

def filter_concept_map(concept_map, ranked_concepts, top_n=15):
    new_map = []
    top_concepts = [concept[0] for concept in ranked_concepts][:top_n]
    # top_concepts = ranked_concepts[:top_n]
    print(top_concepts)
    for concept1, link, concept2 in concept_map:
        if concept1 in top_concepts and concept2 in top_concepts:
            new_map.append((concept1, link, concept2))
    return new_map