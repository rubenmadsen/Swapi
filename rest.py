from flask import Flask, jsonify, request
from DBCon import DBCon

app = Flask(__name__)
db = DBCon()
@app.route('/api', methods=['GET'])
def get_():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/characters', methods=['GET'])
def get_startships():
    return db.get_characters_and_homeworlds().to_json(orient='records')

if __name__ == '__main__':
    pw = "postgres_password"
    db.open(pw)
    app.run(debug=True, port=4200)