import re
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def analysis():
    """
    Returns a sentiment score for page, and scores for each sentence visible.
    """
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form["urlInput"]
            r = requests.get(url)
        except requests.exceptions.MissingSchema as e:
            url = "http://" + request.form["urlInput"]
            r = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            errors.append("Unable to reach URL, please try again")
            errors.append("URL attempted:" + url)
            errors_str = "\n".join(errors)
            return render_template("index.html", errors=errors, url=url)

        if r:
            # Remove elements that are not visible on page as rendered to user
            soup = BeautifulSoup(r.text, "html.parser")
            for element in soup(
                ["style", "script", "head", "header", "title", "meta", "footer"]
            ):
                element.extract()
            raw_result_text = soup.get_text()
            raw_result_text = re.sub("\n", " ", str(raw_result_text))

            tokenized = tokenize.sent_tokenize(raw_result_text)
            sid = SentimentIntensityAnalyzer()

            # Remove too lengthy sentences (understood to be errors)
            line_list = list(filter(lambda x: len(str(x)) < 400, tokenized))

            data = []

            # Get polarity of each sentence
            for sentence in line_list:
                ss = sid.polarity_scores(sentence)
                data.append(ss)

            # Add sentence id and sentence
            for i in range(len(line_list)):
                data[i].update({"id": i})
                data[i].update({"text": line_list[i]})

            # Get most positive/negative sentences
            try:
                most_neg_sorted = sorted(data, key=lambda x: x["neg"])
                most_neg_txt = most_neg_sorted[((len(data) - 1))]["text"]
                most_neg_id = int(most_neg_sorted[((len(data) - 1))]["id"])
                most_pos_sorted = sorted(data, key=lambda x: x["pos"])
                most_pos_txt = most_pos_sorted[((len(data) - 1))]["text"]
                most_pos_id = int(most_pos_sorted[((len(data) - 1))]["id"])

            except IndexError as e:
                errors.append(
                    "Did not find visible text on page, please try a different page"
                )
                return render_template("index.html", errors=errors, url=url)

            # Get number of +/- of compound rating
            count_pos = list(filter(lambda x: x["compound"] >= 0.2, data))
            count_neut = list(
                filter(lambda x: x["compound"] > -0.2 and x["compound"] < 0.2, data)
            )
            count_neg = list(filter(lambda x: x["compound"] <= -0.2, data))
            count_pos_comp = len(count_pos)
            count_neut_comp = len(count_neut)
            count_neg_comp = len(count_neg)
            count_total = len(data)
            if count_total > 0:
                count_pos_perc = round(count_pos_comp / count_total * 100, 2)
                count_neut_perc = round(count_neut_comp / count_total * 100, 2)
                count_neg_perc = round(count_neg_comp / count_total * 100, 2)

            # Scores of most neg & pos sentences
            most_neg_score = data[(most_neg_id)]["compound"]
            most_pos_score = data[(most_pos_id)]["compound"]

    return render_template("index.html", **locals())


@app.route("/testpage")
def test():
    """
    A static page to test against for consistency
    """
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=False)
