import sys
from flask import Flask, request, Response, jsonify
import random, json 
from flask_cors import CORS
from summarizer import generate_summary 
from recommender import get_recomm
from flask_cors import CORS
import joblib
from sentimentClassifier import load_cls 

app = Flask(__name__)
CORS(app) 
sentiment_classifier = load_cls()

@app.route('/data', methods = ['POST', 'GET'])
def recommend_news(): 
    titles = []
    msg="none"
    try:
        text_data = request.get_json()
        article_body = text_data['information'] 
        title = text_data['title']  
        titles = get_recomm(article_body, title, sentiment_classifier) 
        return jsonify(titles)
    except:
        return(jsonify((msg))) 

if __name__ == '__main__': 
    app.run()