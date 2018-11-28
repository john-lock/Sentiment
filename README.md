
# Overview
Analyse the sentiment of each sentence on a page. This application takes any URL and scrapes the text using Beautiful Soup. Text in areas which are not visible to the user, eg within Meta tags, are removed as to not include hidden text in the analysis. 

The resulting text is then broken down into sentences, known as Tokenizing, and passed to Natural Language ToolKit (NLTK) which returns a score for each with the 'Sentiment Intensity Analyzer' it provides. Each sentence score has a positive, neutral and negative component based on each word in the sentence. To give the user a quick insight into the results the sentence with the highest positive score is shown and the same for the negative. A compound score is also returned which is a weighted score based on the positive, neutral and negative composition.

# Setup & Installation
To setup this for yourself:
- Git clone https://github.com/john-lock/Sentiment.git
- Setup virtualenv with 'virtualenv venv' then activate with 'source venv/bin/activate'
- Install the requirements with 'pip install -r requirements.txt'
- Add NLTK Corpus, via a python shell
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('vader_lexicon')
- Run the application with 'flask run'



# TODO
- Update tests to Pytest
- Add document upload function


