import os
import operator
import re
import nltk
import re
from nltk import tokenize
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def scrape():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form['urlInput']
            r = requests.get(url)
        except:
            errors.append("Unable to reach URL, please try again")
            return render_template('index.html', errors=errors)
        if r:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup(['style', 'script', 'head', 'header', 'title', 'meta', 'footer']):
                element.extract()
            raw_result_text = soup.get_text()
            raw_result_text = re.sub("\n", " ", str(raw_result_text))

            # NLP
            tokenized = tokenize.sent_tokenize(raw_result_text)
            sid = SentimentIntensityAnalyzer()
            data = []

            # Remove too lengthy sentences (understood to be errors)
            line_list = filter(lambda x: len(str(x)) < 10, tokenized)

            # Get polarity of each sentence
            for sentence in line_list:
                ss = sid.polarity_scores(sentence)
                data.append(ss)

            # Combine sentances and sentence scores
            for i in range(len(line_list)):
                data[i].update({i: line_list[i]})

            # Get num of +/- compound



            # Most/Least values
            most_negative = sorted(data, key=lambda x: x['neg'])
            most_neg = most_negative[((len(data) -1))]
            neg_comp_sorted = sorted(data, key=lambda x: x['compound'])
            most_negative_comp = neg_comp_sorted[0]
            most_positive = sorted(data, key=lambda x: x['pos'])
            most_pos = most_positive[((len(data)-1))]
            pos_comp_sorted = sorted(data, key=lambda x: x['compound'])
            most_positive_comp = pos_comp_sorted[((len(data)-1))]

            # Return most positive, most negative
    return render_template('index.html', **locals())
                #for k in sorted(ss):

                    # print('{0}: {1}, '.format(k, ss[k]), end='')

"""
            def word_feats(raw_result_text):
                return dict([(word, True) for word in raw_result_text])

           """

if __name__ == '__main__':
    app.run()
