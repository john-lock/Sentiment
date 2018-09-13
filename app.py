
import re
from nltk import tokenize
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
            line_list = list(filter(lambda x: len(str(x)) < 400, tokenized))
            # line_list = list(filter(lambda x: len(str(x)) > 20, line_list))  use to give min length

            # Get polarity of each sentence
            for sentence in line_list:
                ss = sid.polarity_scores(sentence)
                data.append(ss)

            # Combine sentances and sentence scores
            for i in range(len(line_list)):
                data[i].update({i: line_list[i]})

            # Get num of +/- compound
            count_pos = list(filter(lambda x: x['compound'] >= 0, data))
            count_neg = list(filter(lambda x: x['compound'] < 0, data))
            count_pos_comp = len(count_pos)
            count_neg_comp = len(count_neg)
            count_total = len(data)

            # Most/Least values
            most_negative = sorted(data, key=lambda x: x['neg'])
            most_neg = most_negative[((len(data) -1))]
            neg_comp_sorted = sorted(data, key=lambda x: x['compound'], reverse=True)
            most_negative_comp_full = dict(neg_comp_sorted[((len(data)-1))])
            most_negative_comp_reduced = dict(neg_comp_sorted[((len(data)-1))])
            for key in ['neg', 'neu', 'pos', 'compound']:
                most_negative_comp_reduced.pop(key)

            most_positive = sorted(data, key=lambda x: x['pos'])
            most_pos = most_positive[((len(data) -1))]
            pos_comp_sorted = sorted(data, key=lambda x: x['compound'])
            most_positive_comp_full = dict(pos_comp_sorted[((len(data)-1))])
            most_positive_comp_reduced = dict(pos_comp_sorted[((len(data)-1))])
            for key in ['neg', 'neu', 'pos', 'compound']:
                most_positive_comp_reduced.pop(key)


    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run()
