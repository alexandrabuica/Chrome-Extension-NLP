from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize 
np.seterr(divide='ignore', invalid='ignore')


def read_stopwords(file_name):
    txt_file = open(file_name, encoding='utf-8')
    file_content = txt_file.read().splitlines()
    return file_content


def clean_text(article_body):
    sentences = sent_tokenize(article_body)
    cleaned_text = []
    for sent in sentences:
        words = word_tokenize(sent)
        words = [i.lower() for i in words if i.isalpha()]
        sent = ' '.join(words)
        cleaned_text.append(sent)

    return cleaned_text


def build_similarity_matrix(sentences, stop_words):
    # create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def generate_summary(my_text, top_n):
    stop_words = read_stopwords('stopWords.txt') 
    summarize_text_sent = [] 
    # read text and split it in sentences
    sentences = clean_text(my_text)

    # generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # rank sentences in similarity martix
    try:
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank_numpy(sentence_similarity_graph) 
    except nx.exception.NetworkXError:
        print("error trying to summarize")
    # sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    
    for i in range(top_n):
      summarize_text_sent.append("".join(ranked_sentence[i][1]))

    # output the summarize text
    summarized_text = ". ".join(summarize_text_sent)
    return summarized_text
 
