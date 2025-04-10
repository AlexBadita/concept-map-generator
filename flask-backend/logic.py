import string
import spacy
from spacy.matcher import Matcher
import neuralcoref

input_text = "Information used in existing ontology matching solutions are usually grouped into four categories: lexical information, structural information, semantic information, and external information, respectively. By summarizing and analyzing the approaches for utilizing the same kind of information, this paper nds that lexical information is mainly analyzed based on text and dictionary similarity. Similarly, structural information and semantic information are mainly analyzed based on graph structure and reasoner, respectively. The approaches for aggregating information analysis results are discussed. Challenges in the analysis of various types of information for existing ontology matching solutions are also described, and insights into directions for future research are provided."
# load model
nlp = spacy.load('en_core_web_sm')
# add coreference to pipeline
neuralcoref.add_to_pipe(nlp)

def coreference_resolution(text):
    # apply the pipeline
    doc = nlp(text)
    # replacing all expressoms with the main entity's name
    resolved_text = doc._.coref_resolved
    return resolved_text

def remove_punctuation(tokens):
    # the list of punctuation elements
    punctuation = set(string.punctuation)
    return [token for token in tokens if token not in punctuation]

def extract_tokens(text):
    # apply the pipeline
    doc = nlp(text)
    # create a list of sentences, each containing a list of tokens
    tokens = []
    for sentence in doc.sents:
        sentence_tokens = [token.text.lower() for token in sentence]
        sentence_tokens = remove_punctuation(sentence_tokens)
        tokens.append(sentence_tokens)
    return tokens

def tag_part_of_speach(text):
    # apply the pipeline
    doc = nlp(text)
    # extract tokens and their POS tags
    pos_tags = []
    for sentence in doc.sents:
        sentence_pos_tags = [(token.text.lower(), token.pos_) for token in sentence if token.text not in string.punctuation]
        pos_tags.append(sentence_pos_tags)
    return pos_tags

def extract_noun_phrases(text):
    # apply the pipeline
    doc = nlp(text)
    # extract noun phrases
    noun_phrases = []
    for sentence in doc.sents:
        sentence_noun_phrases = [(chunk.start, chunk.end, chunk.text.lower()) for chunk in sentence.noun_chunks]
        noun_phrases.append(sentence_noun_phrases)
    return noun_phrases

def extract_verb_phrases(text):
    # load the pipeline
    doc = nlp(text)
    # initialize the matcher with the vocab of the model
    matcher = Matcher(nlp.vocab)
    # define the pattern <VERB>*<ADV>*<PART>*<VERB>+<PART>*
    pattern = [
        {"POS": "VERB", "OP": "*"},  # Zero or more verbs
        {"POS": "ADV", "OP": "*"},   # Zero or more adverbs
        {"POS": "PART", "OP": "*"},  # Zero or more particles
        {"POS": "VERB", "OP": "+"},  # One or more verbs
        {"POS": "PART", "OP": "*"},  # Zero or more particles
        {"POS": "ADP", "OP": "*"},   # Zero or more prepositions
    ]
    # add the pattern to the matcher
    matcher.add("VerbPhrasePattern", None, pattern)
    
    # Apply the matcher to the doc
    matches = matcher(doc)
    spans = [doc[start:end] for match_id, start, end in matches]

    # Sort spans by start index and then by length (longer spans first)
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
    SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
    OBJECTS = ["dobj", "dative", "attr", "oprd"]
    ADJECTIVES = ["acomp", "advcl", "advmod", "amod", "appos", "nn", "nmod", "ccomp", "complm",
              "hmod", "infmod", "xcomp", "rcmod", "poss"," possessive"]
    COMPOUNDS = ["compound"]
    PREPOSITIONS = ["prep"]
    
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
    resolved_text = coreference_resolution(input_text)
    for concept in find_concept_link_concept_pairs(resolved_text):
        print(concept)
    # pairs = find_concept_link_concept_pairs(resolved_text)
    # print(pairs)