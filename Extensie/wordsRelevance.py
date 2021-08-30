from nltk.tokenize import word_tokenize, sent_tokenize 
import math

def read_stopwords(file_name):
    txt_file = open(file_name, encoding='utf-8')
    file_content = txt_file.read().splitlines()
    return file_content


def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))


def clean_text(words):
    stop_words = read_stopwords('stopWords.txt')
    words = [i for i in words if i.isalnum() or i.isalpha()]
    words = [i for i in words if i not in stop_words]
    return words


def tokenize_text(article_body):
    metrics = {}
    total_sentences = sent_tokenize(article_body)
    total_words = word_tokenize(article_body)
    total_words = clean_text(total_words)
    metrics["all_sentences"] = total_sentences
    metrics["all_words"] = total_words
    metrics["sent_length"] = len(total_sentences)
    metrics["words_length"] = len(total_words)
    return metrics


def calculate_tf_score(all_words, words_length):
    score = {}
    for each_word in all_words:
        if each_word in score:
            score[each_word] += 1
        else:
            score[each_word] = 1
    score.update((x, y / int(words_length)) for x, y in score.items())
    return score


def calculate_idf_score(all_words, all_sentences, sent_length):
    score = {}
    for each_word in all_words:
        if each_word in score:
            score[each_word] = check_sent(each_word, all_sentences)
        else:
            score[each_word] = 1
    score.update((x, math.log(int(sent_length) / y)) for x, y in score.items())
    return score


def get_most_relevant_words(article_body):
    text_metrics = tokenize_text(article_body)
    tf_score = calculate_tf_score(text_metrics["all_words"], text_metrics["words_length"])
    idf_score = calculate_idf_score(text_metrics["all_words"], text_metrics["all_sentences"],
                                    text_metrics["sent_length"])
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    return (list(tf_idf_score)[:5])
