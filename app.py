from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import string, random


app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize MongoDB connection
mongo = PyMongo(app)
db = mongo.db

#Generate short url
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/shorten', methods=['POST'])
def create_short_url():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'Invalid or missing URL'}), 400

        original_url = data['url']
        
        # Check if the URL already exists in the database
        existing_entry = db.urls.find_one({'original_url': original_url})
        if existing_entry:
            return jsonify({
                'short_code': existing_entry['short_code'],
                'url': existing_entry['original_url']
            }), 200
        
        # Generate a new short code if the URL is new
        short_code = generate_short_code()
        db.urls.insert_one({
            'short_code': short_code,
            'original_url': original_url,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'access_count': 0
        })
        return jsonify({
            'short_code': short_code,
            'url': original_url
        }), 201
    
    except DuplicateKeyError:
        # If the URL already exists due to the unique index, return the existing one
        existing_entry = db.urls.find_one({'original_url': original_url})
        return jsonify({
            'short_code': existing_entry['short_code'],
            'url': existing_entry['original_url']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)