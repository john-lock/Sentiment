import os
import operator
import re
import nltk
#from stop_words import stops
#from collections import Counter
import re


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
            for element in soup(['style', 'script', 'head','header', 'title', 'meta', 'footer']):
                element.extract()
            results = soup.get_text()

    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()
