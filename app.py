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
    

# Retrieve original URL
@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    record = db.urls.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404
    
    # Increment access count
    db.urls.update_one(
        {'short_code': short_code},
        {'$inc': {'access_count': 1}}
    )
    return redirect(record['original_url'])

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    try:
        data = request.get_json()
        new_url = data.get('url')
        if not new_url:
            return jsonify({'error': 'Invalid URL'}), 400

        # Try updating the record
        result = db.urls.update_one(
            {'short_code': short_code},
            {'$set': {'original_url': new_url, 'updated_at': datetime.utcnow()}}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Short URL not found'}), 404
        
        return jsonify({'message': 'URL updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    result = db.urls.delete_one({'short_code': short_code})
    if result.deleted_count == 0:
        return jsonify({'error': 'Short URL not found'}), 404
    return '', 204


@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    record = db.urls.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404
    
    stats = {
        'short_code': record['short_code'],
        'original_url': record['original_url'],
        'created_at': record['created_at'],
        'updated_at': record['updated_at'],
        'access_count': record['access_count']
    }
    return jsonify(stats), 200




if __name__ == '__main__':
    app.run(debug=True)
