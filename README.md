
# 🚀  URL Shortening Service
A URL Shortening Service built using Flask and MongoDB. This service allows you to shorten long URLs, retrieve original URLs, update and delete shortened URLs, and view usage statistics.

## 📥 Setup Instructions
Follow these steps to set up and run the project:

#### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/url-shortening-service.git
cd url-shortening-service
```
#### 2. Create a Virtual Environment
```sh
python -m venv venv
```
#### 3. Activate the Virtual Environment
Windows:

```sh
.\venv\Scripts\activate
```
Linux/MacOS:

```bash

source venv/bin/activate
```
#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
#### 5. Install MongoDB
Download and install MongoDB from https://www.mongodb.com
#### 6. Start MongoDB service
```bash
mongod
```
#### 7. Connect to MongoDB using mongosh
```bash
mongosh
```
#### 8. Create Database and Collection
```javascript
use url_shortener
db.createCollection('urls')
```
#### 9. Run Flask Application
```bash
python app.py
```

## 🌐 Endpoints
Below are the endpoints available in the Flask app:

#### 1. Create a Shortened URL
Endpoint: POST /shorten
Description: Shortens a given URL.

Curl Command:

```bash
curl -X POST "http://127.0.0.1:5000/shorten" -H "Content-Type: application/json" -d "{\"url\": \"https://github.com/EmanZahid123/\"}"
```

#### 2. Retrieve Original URL
Endpoint: GET /shorten/<short_code>
Description: Redirects to the original URL using the short code.

Curl Command:

```bash
curl -X GET http://127.0.0.1:5000/shorten/7R8Nct
```
#### 3. Update Shortened URL
Endpoint: PUT /shorten/<short_code>
Description: Updates the original URL for a given short code.

Curl Command:

```bash
curl -X PUT "http://127.0.0.1:5000/shorten/ZSuPba" -H "Content-Type: application/json" -d "{\"url\": \"https://www.updated.com\"}"
```

#### 4. Delete Shortened URL
Endpoint: DELETE /shorten/<short_code>
Description: Deletes a shortened URL.

Curl Command:

```bash
curl -X DELETE http://127.0.0.1:5000/shorten/RowBR1
```
#### 5. Get URL Statistics
Endpoint: GET /shorten/<short_code>/stats
Description: Fetches statistics about a shortened URL (like access count and timestamps).

Curl Command:

```bash
curl -X GET http://127.0.0.1:5000/shorten/7R8Nct/stats
```

![ Curl](images/curl_response.png)  

## 🖥️ Frontend Overview
The frontend is built using HTML and Bootstrap for styling.

File: index.html
Description:

A simple form to submit a URL for shortening.
Displays shortened URLs with options to redirect, update, or delete.

![ UI](images/url_shortener.png)  


## 💡 Additional Notes
The short code is a 6-character alphanumeric string.
If a URL is already shortened, the existing short code will be returned.
If an invalid short code is provided, an appropriate error message will be shown.
