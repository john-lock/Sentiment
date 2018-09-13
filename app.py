from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def scrape():
    errors = []
    results = {}
    
    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()