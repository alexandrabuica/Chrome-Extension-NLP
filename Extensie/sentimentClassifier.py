import pandas as pd
import glob, string, re, pickle
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score 
import simplemma

langdata = simplemma.load_data('ro')

def map_first_lines(file_list):
    for file in file_list:
        with open(file, 'r', encoding='utf-8-sig', errors='ignore') as fd:
            yield fd.read()

def load_cls():
    clsf =joblib.load('nb_model.pickle') 
    print('sklearn clsf loaded!')
    return clsf

def read_stopwords(file_name):
    txt_file = open(file_name, encoding='utf-8')
    file_content = txt_file.read().splitlines()
    return file_content

def remove_stopwords_punctuations(text):
    punctuations = string.punctuation
    cleaned_words = []
    cleaned_text = ''
    stopwords = read_stopwords('stopWords.txt')
    for word in word_tokenize(text):
        if (word not in stopwords and word not in punctuations):
            cleaned_words.append(word)
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

def create_dataframe(list1, list2):
    df1 = pd.DataFrame(list1, columns=['Text'])
    df1['Sentiment'] = 'positive'
    df2 = pd.DataFrame(list2, columns=['Text'])
    df2['Sentiment'] = 'negative'
    dataset = pd.concat([df1, df2])
    return dataset

pos_f = glob.glob("positive/*.txt")
pos_n = glob.glob("negative/*.txt")

pos_read = map_first_lines(pos_f)
neg_read = map_first_lines(pos_n)

POSITIVE_REVIEWS = [line for line in pos_read if line]
NEGATIVE_REVIEWS = [line for line in neg_read if line]

data_set =create_dataframe(POSITIVE_REVIEWS, NEGATIVE_REVIEWS) 

# sns.countplot(data_set.Sentiment)
# plt.title('Distributia numarului de review-uri pozitive si negative')
# plt.show()
data_set['word_count'] = data_set['Text'].str.split().str.len()
print(data_set.groupby('Sentiment')['word_count'].mean())
# sns.distplot(data_set[data_set['Sentiment']=='positive']['word_count'], label='Pozitiv')
# sns.distplot(data_set[data_set['Sentiment']=='negative']['word_count'], label='Negativ')
# plt.legend()
# plt.show()

data_set['Sentiment_ec'] = data_set['Sentiment'].map({'positive': 1, 'negative': 0}).astype(int)

def clean_text(raw_text):
    stop_words = read_stopwords('stopWords.txt')
    cleaned_text = re.sub("[^A-Za-z]", " ", str(raw_text))
    cleaned_text = cleaned_text.lower()
    cleaned_text = word_tokenize(cleaned_text)
    cleaned_text = [simplemma.lemmatize(text, langdata) for text in cleaned_text if text not in stop_words and text not in string.punctuation]
    cleaned_text = " ".join(cleaned_text)
    return cleaned_text

corpus = [] 

for i in range(0, len(data_set)):
    cleaned_text = clean_text(data_set['Text'].iloc[i])
    corpus.append(cleaned_text)
 
data_set_new = pd.DataFrame({'Sentiment_ec':data_set['Sentiment_ec'], 'Text': corpus}) 

tf_id = TfidfVectorizer()
X_tf = tf_id.fit_transform(corpus)

y = data_set_new['Sentiment_ec']
X_train, X_test, y_train, y_test = train_test_split(X_tf, y, test_size = 0.2, random_state = 0)

sentiment_classifier = MultinomialNB().fit(X_train, y_train)
y_pred=sentiment_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print()
report = classification_report(y_test, y_pred)
print(report)

print("Accuracy : ", accuracy)

print("confusion_matrix:")
print(cm)
# sns.heatmap(cm, annot=True, fmt="d")
# plt.show()
pickle.dump(tf_id, open("tfidf_vectorizer.pickle", "wb"))
pickle.dump(sentiment_classifier, open("nb_model.pickle", "wb"))

 