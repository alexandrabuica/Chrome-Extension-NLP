from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import mysql.connector
from summarizer import generate_summary, read_stopwords
from nltk.tokenize import word_tokenize 
from wordsRelevance import get_most_relevant_words  
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  
from sentimentClassifier import clean_text
import numpy as np

def connect_to_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='Extensie')
    return connection


def convert_tuple_to_string(main_record):
    records = [''.join(row) for row in main_record]
    text = ''
    for word in records:
        text += word
    return text


def get_data(db_data):
    conn = connect_to_database()
    cursor0 = conn.cursor()
    cursor0.execute("SELECT COUNT(*) FROM extensie.articole")
    rowcount = cursor0.fetchone()[0]
    cursor1 = conn.cursor()
    cursor1.execute('SELECT rezumat FROM extensie.articole WHERE id<='+str(rowcount))
    records = cursor1.fetchall()
    for row in records:
        row = convert_tuple_to_string(row) 
        db_data.append(clean_text(row))
    conn.commit()
    conn.close()
    return db_data


def check_already_in_db(title, indices):
    conn = connect_to_database()
    cursor = conn.cursor(buffered=True)
    for i in indices: 
        cursor.execute('SELECT titlu FROM extensie.articole WHERE id =' + str(i)) 
        records = cursor.fetchall()
        for row in records:
            row = convert_tuple_to_string(row)  
            title = title.replace('\n','')
            title = title.replace('\t','')
            title = title.replace("&nbsp;", "")
            row = row.replace('\n','')
            row = row.replace('\t','')
            print('-------')
            print(title.strip())
            print(row.strip())
            if (row.strip()==title.strip()): 
                print("validare")
                indices = np.delete(indices, np.where(indices == i))
            else:
                print("nu s-a gasit nimic la fel") 
    return indices
                

def get_recomm(input, title, classifier):
    articles_data = [generate_summary(input,2)]
    news_articles = get_data(articles_data) 
    print(len(news_articles))
    tfidf_matrix = TfidfVectorizer().fit_transform(news_articles) 
    eucld_distances = euclidean_distances(tfidf_matrix[0:1], tfidf_matrix).flatten() 
    related_docs_indices = eucld_distances.argsort()[1:4] 
    print(related_docs_indices)
    related_docs_indices = check_already_in_db(title, related_docs_indices)
    print(related_docs_indices)
    print(eucld_distances[related_docs_indices])
    conn = connect_to_database()
    cursor = conn.cursor(buffered=True) 
    titles = []
    rec_dict = {}
    recommendations = []
        
    for title in related_docs_indices:
        cursor.execute('SELECT titlu, sursa, corp, imagine, rezumat FROM extensie.articole WHERE id =' + str(title)) 
        record = cursor.fetchall() 
        for a_tuple in record: 
            image = a_tuple[3]
            relevant_words = get_most_relevant_words(a_tuple[4])
            vectorizer = joblib.load('tfidf_vectorizer.pickle') 
            to_predict = vectorizer.transform([a_tuple[2]])
            label = "".join(str(x) for x in classifier.predict(to_predict)) 
            rec_dict = {"title":a_tuple[0], "source": a_tuple[1],
                        "image":image, "label": label, "relevant_words":relevant_words}
            recommendations.append(rec_dict)
    conn.commit()
    conn.close()
    return recommendations
