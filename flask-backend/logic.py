# For handling punctuation
import string
# For natural language processing
import spacy
# For pattern matching in text
from spacy.matcher import Matcher
# For coreference resolution
import neuralcoref

# Sample input text for testing
input_text = "Information used in existing ontology matching solutions are usually grouped into four categories: lexical information, structural information, semantic information, and external information, respectively. By summarizing and analyzing the approaches for utilizing the same kind of information, this paper nds that lexical information is mainly analyzed based on text and dictionary similarity. Similarly, structural information and semantic information are mainly analyzed based on graph structure and reasoner, respectively. The approaches for aggregating information analysis results are discussed. Challenges in the analysis of various types of information for existing ontology matching solutions are also described, and insights into directions for future research are provided."

# Load the spacy language model
nlp = spacy.load('en_core_web_sm')

# Add neuralcoref to the spacy pipeline for coreference resolution
neuralcoref.add_to_pipe(nlp)

def coreference_resolution(text):
    """
    Resolve coreferences in the input text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with coreferences resolved.
    """
    # Apply the NLP pipeline
    doc = nlp(text)
    # Replace references with main entities
    resolved_text = doc._.coref_resolved
    return resolved_text

def remove_punctuation(tokens):
    """
    Remove punctuation from a list of tokens.

    Args:
        tokens (list): List of tokens.

    Returns:
        list: List of tokens without punctuation.
    """
    # Set of punctuation characters
    punctuation = set(string.punctuation)
    return [token for token in tokens if token not in punctuation]

def extract_tokens(text):
    """
    Extract tokens from the input text, grouped by sentences.

    Args:
        text (str): The input text.

    Returns:
        list: A list of sentences, each containing a list of tokens.
    """
    # Apply the NLP pipeline
    doc = nlp(text)
    
    tokens = []
    for sentence in doc.sents:
        sentence_tokens = [token.text.lower() for token in sentence]
        sentence_tokens = remove_punctuation(sentence_tokens)
        tokens.append(sentence_tokens)
    return tokens

def tag_part_of_speach(text):
    """
    Tag tokens in the text with their part-of-speech (POS).

    Args:
        text (str): The input text.

    Returns:
        list: A list of sentences, each containing tokens with their POS tags.
    """
    # Apply the NLP pipeline
    doc = nlp(text)
   
    pos_tags = []
    for sentence in doc.sents:
        sentence_pos_tags = [(token.text.lower(), token.pos_) for token in sentence if token.text not in string.punctuation]
        pos_tags.append(sentence_pos_tags)
    return pos_tags

def extract_noun_phrases(text):
    """
    Extract noun phrases from the input text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of sentences, each containing noun phrases with their start and end indices.
    """
    # Apply the NLP pipeline
    doc = nlp(text)
    
    noun_phrases = []
    for sentence in doc.sents:
        sentence_noun_phrases = [(chunk.start, chunk.end, chunk.text.lower()) for chunk in sentence.noun_chunks]
        noun_phrases.append(sentence_noun_phrases)
    return noun_phrases

def extract_verb_phrases(text):
    """
    Extract verb phrases from the input text using pattern matching.

    Args:
        text (str): The input text.

    Returns:
        list: A list of sentences, each containing verb phrases with their start and end indices.
    """
    # Apply the NLP pipeline
    doc = nlp(text)
    # Initialize the matcher
    matcher = Matcher(nlp.vocab)

    # Define the pattern for verb phrases 
    # <VERB>*<ADV>*<PART>*<VERB>+<PART>*
    pattern = [
        {"POS": "VERB", "OP": "*"},  # Zero or more verbs
        {"POS": "ADV", "OP": "*"},   # Zero or more adverbs
        {"POS": "PART", "OP": "*"},  # Zero or more particles
        {"POS": "VERB", "OP": "+"},  # One or more verbs
        {"POS": "PART", "OP": "*"},  # Zero or more particles
        {"POS": "ADP", "OP": "*"},   # Zero or more prepositions
    ]
    # Add the pattern to the matcher
    matcher.add("VerbPhrasePattern", None, pattern)
    
    # Apply the matcher to the document
    matches = matcher(doc)
    spans = [doc[start:end] for match_id, start, end in matches]

    # Filter overlapping spans
    spans = sorted(spans, key=lambda span: (span.start, -(span.end - span.start)))
    
    filtered_spans = []
    for span in spans:
        # Check if span overlaps with any already accepted span
        if not any(span.start < accepted_span.end and span.end > accepted_span.start for accepted_span in filtered_spans):
            filtered_spans.append(span)
    
    verb_phrases = []
    for sentence in doc.sents:
        sentence_verb_phrases = []
        for span in filtered_spans:
            start, end = span.start, span.end
            if start >= sentence.start and end <= sentence.end:
                sentence_verb_phrases.append((start, end, doc[start:end].text))
        verb_phrases.append(sentence_verb_phrases)

    return verb_phrases

def find_possible_relations(concepts, links):
    """
    Find possible relations between concepts based on links.

    Args:
        concepts (list): List of concepts grouped by sentences.
        links (list): List of links grouped by sentences.

    Returns:
        list: A list of relations between concepts.
    """
    relations = []
    for sentence_concepts, sentence_links in zip(concepts, links):
        sentence_relations = []
        for i in range(len(sentence_concepts) - 1):
            for j in range(i + 1, len(sentence_concepts)):
                start1, end1, concept1 = sentence_concepts[i]
                start2, end2, concept2 = sentence_concepts[j]
                links = [link[2] for link in sentence_links if end1 <= link[0] and start2 >= link[1]]
                if links:
                    sentence_relations.append((concept1, concept2, links))
        relations.append(sentence_relations)
    return relations

def find_concept_link_concept_pairs(text):
    """
    Extract concept-relation-concept pairs from the input text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of tuples representing concept-relation-concept pairs.
    """
    SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
    OBJECTS = ["dobj", "dative", "attr", "oprd"]
    # ADJECTIVES = ["acomp", "advcl", "advmod", "amod", "appos", "nn", "nmod", "ccomp", "complm",
    #           "hmod", "infmod", "xcomp", "rcmod", "poss"," possessive"]
    # COMPOUNDS = ["compound"]
    PREPOSITIONS = ["prep"]
    
    # Apply the NLP pipeline
    doc = nlp(text)
    noun_phrases = extract_noun_phrases(text)
    verb_phrases = extract_verb_phrases(text)
    possible_links = find_possible_relations(noun_phrases, verb_phrases)
    
    pairs = []
    
    for sentence_verb_phrases, sentence_noun_phrases, sentence_possible_links in zip(verb_phrases, noun_phrases, possible_links):
        for subj, obj, links in sentence_possible_links:
            if len(links) == 1:
                pairs.append((subj, links[0], obj))
            elif len(links) > 1:
                for start, end, verb_phrase in sentence_verb_phrases:
                    subject = None
                    object_ = None
                    if verb_phrase in links:
                        verb_token = doc[start:end].root
                        
                        for child in verb_token.children:
                            if child.dep_ in SUBJECTS and child.text in subj:
                                    subject = child
                            elif child.dep_ in OBJECTS and child.text in obj:
                                    object_ = child
                            elif child.dep_ in PREPOSITIONS:
                                for pobj in child.children:
                                    if pobj.dep_ == 'pobj' and pobj.text in obj:
                                        object_ = pobj

                    if subject and object_:
                        pairs.append((subj, verb_phrase, obj))
    return pairs

if __name__ == '__main__':
    # Test the coreference resolution and concept extraction
    resolved_text = coreference_resolution(input_text)
    for concept in find_concept_link_concept_pairs(resolved_text):
        print(concept)
    # pairs = find_concept_link_concept_pairs(resolved_text)
    # print(pairs)