from flask import Flask, render_template, request, jsonify
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)

# Read and preprocess the document
with open('data1.txt', 'r', errors='ignore') as f:
    raw_doc = f.read().lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)
    return None

def response(user_response):
    robo1_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo1_response = "I am sorry! I don't understand "
    else:
        robo1_response = sent_tokens[idx]
    return robo1_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_response = request.form["message"].lower()
    if user_response != 'bye':
        if user_response in ['thanks', 'thank you']:
            return jsonify(response="You are welcome..")
        elif greet(user_response) is not None:
            return jsonify(response=greet(user_response))
        else:
            sent_tokens.append(user_response)
            word_tokens.extend(nltk.word_tokenize(user_response))
            final_words = list(set(word_tokens))
            bot_response = response(user_response)
            sent_tokens.remove(user_response)
            return jsonify(response=bot_response)
    else:
        return jsonify(response="Goodbye!")

if __name__ == "__main__":
    app.run(debug=True)
