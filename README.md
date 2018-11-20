Analyse the sentiment of each sentence on a page. This application takes any URL and scrapes the text using Beautiful Soup. Text in areas which are not visible to the user, eg within Meta tags, are removed as to not include hidden text in the analysis. 

The resulting text is then broken down into sentences, known as Tokenizing, and passed to Natural Language ToolKit (NLTK) which returns a score for each with the 'Sentiment Intensity Analyzer' it provides. Each sentence score has a positive, neutral and negative component based on each word in the sentence. To give the user a quick insight into the results the sentence with the highest positive score is shown and the same for the negative. A compound score is also returned which is a weighted score based on the positive, neutral and negative composition - developments for this application would be right to utilise this. 

The testing strategy for this application includes using a static page (test.html) to feed into NLPK via the application to ensure results are as expected.

