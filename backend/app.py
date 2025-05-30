from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.json_util import dumps

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
app = Flask(__name__)

client = MongoClient(mongo_uri)
db = client.sample_mflix
userCollection = db.users

@app.route('/api', methods=['GET'])
def get_users():
    users = userCollection.find()
    return dumps(users), 200, {'Content-Type': 'application/json'}

@app.route('/simple_form_submit', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        userCollection.insert_one({
            'name': name,
            'email': email,
            'password': password
        })
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
