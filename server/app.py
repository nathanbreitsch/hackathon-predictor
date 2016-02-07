#!flask/bin/python
from flask import Flask, jsonify, send_from_directory, request
import pickle
import string
from sklearn.decomposition import TruncatedSVD
import json
import pandas as pd

class PassageVectorizer():
    def __init__(self):
        with open('./scrape_data/projects.json','r') as f:
            projects = json.load(f)

        word_count_dict = {}
        for project in projects:
            desc = self.transform_blob(project['description'])
            words = desc.split(' ')
            for word in words:
                if word in word_count_dict:
                    word_count_dict[word] += 1
                else:
                    word_count_dict[word] = 1
        word_order_dict = {}
        words_counted = [word for word in word_count_dict.keys() if word_count_dict[word] > 10]
        words_counted = sorted(words_counted)
        self.num_words = len(words_counted)
        for i in range(0, len(words_counted)):
            word_order_dict[words_counted[i]] = i

        self.word_order_dict = word_order_dict

    def transform_blob(self, blob):
        exclude = set(string.punctuation)
        t_blob = ''.join(ch for ch in blob if ch not in exclude)
        t_blob = t_blob.replace('\n','')
        t_blob = t_blob.replace('  ',' ')
        t_blob = t_blob.upper()
        return t_blob

    def transform_winner(self, winner):
        if(winner):
            return 1
        else:
            return 0

    def vectorize_passage(self, passage):
        data_output = []
        word_vec = [0] * self.num_words
        words = self.transform_blob(passage).split(' ')
        for word in words:
            if word in self.word_order_dict:
                word_vec[self.word_order_dict[word]] += 1

        return word_vec




with open('./passage_vectorizer.pkl','rb') as f:
    pv = pickle.load(f)

with open('./pca_transform.pkl','rb') as f:
    pca = pickle.load(f)

with open('./svm_classifier.pkl','rb') as f:
    clf = pickle.load(f)

#with open('./data_output.json', 'r') as f:
#    projects = json.load(f)

with open('./2d_pca_transform.pkl', 'rb') as f:
    pca2d = pickle.load(f)

with open('./scatter_data.json', 'r') as f:
    scatter_out = json.load(f)

#scatter_data = pd.DataFrame(projects)
#coordinates = pca2d.transform(scatter_data.word_vec.tolist()).tolist()
#wins = scatter_data.winner.tolist()
#combined = zip(coordinates, wins)
#scatter_out = [{'x': float(c[0][0]), 'y': float(c[0][1]), 'w': int(c[1])} for c in combined]

app = Flask(__name__)


@app.route('/scatter/', methods=['GET'])
def get_scatter():
    return jsonify({"data": scatter_out})


@app.route('/judge/', methods=['POST'])
def get_tasks():
    data = request.get_json(force=True)
    word_vec = pv.vectorize_passage(data['description'])
    print(len(word_vec))
    pc = pca.transform(word_vec)
    result = clf.predict(pc).tolist()[0]

    return jsonify({'result': result})

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return send_from_directory('static','index.html')

if __name__ == '__main__':
    app.run(debug=True)
