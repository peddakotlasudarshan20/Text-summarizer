from flask import Flask, render_template, request
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist

app = Flask(__name__)

def text_summarizer(text, num_sentences=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    fdist = FreqDist(filtered_words)
    sentence_scores = [sum(fdist[word] for word in word_tokenize(sentence.lower()) if word in fdist)
                       for sentence in sentences]
    sentence_scores = list(enumerate(sentence_scores))

    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

    random_sentences = random.sample(sorted_sentences, min(num_sentences, len(sorted_sentences)))

    summary_sentences = sorted(random_sentences, key=lambda x: x[0])

    summary = ' '.join([sentences[i] for i, _ in summary_sentences])

    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        text = request.form['text']
        num_sentences = int(request.form['num_sentences'])
        summary = text_summarizer(text, num_sentences)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
