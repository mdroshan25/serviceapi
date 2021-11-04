from flask import Flask, jsonify, request, render_template #import objects from the Flask model
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__) # define app using Flask
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'languages.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]


class Language(db.Model):
    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name


class LanguageSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ['name']


language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/lang', methods=['GET'])
def get_all():
    all_languages = Language.query.all()
    return languages_schema.jsonify(all_languages)
    # return jsonify({'languages': languages})


@app.route('/lang/<string:name>', methods=['GET'])
def get_one(name):
    language = Language.query.get(name)
    return language_schema.jsonify(language)


@app.route('/lang', methods=['POST'])
def add_one():
    # retrieve a name from a request body
    name = request.json['name']
    new_language = Language(name)
    db.session.add(new_language)
    db.session.commit()
    return language_schema.jsonify(new_language)


@app.route('/lang/<string:name>', methods=['PUT'])
def edit_one(name):
    new_language = Language.query.get(name)
    name = request.json['name']
    new_language.name = name
    db.session.commit()
    return language_schema.jsonify(new_language)


@app.route('/lang/<string:name>', methods=['DELETE'])
def remove_one(name):
    remove_language = Language.query.get(name)
    db.session.delete(remove_language)
    db.session.commit()
    return language_schema.jsonify(remove_language)


if __name__ == '__main__':
    app.run(debug=True, port=8080) #run app on port 8080 in debug mode
