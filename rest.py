from flask import Flask, jsonify, request
from DBCon import DBCon

app = Flask(__name__)
db = DBCon()
@app.route('/api', methods=['GET'])
def get_():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/starships', methods=['GET'])
def get_startships():
    return jsonify(db.get_starship_pilots_and_homeworlds())

if __name__ == '__main__':
    pw = "postgres_password"
    db.open(pw)
    app.run(debug=True)