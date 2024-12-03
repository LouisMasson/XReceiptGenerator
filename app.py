import os
from flask import Flask, render_template, request, jsonify
import requests
from config import X_API_KEY

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/<username>')
def get_user(username):
    headers = {
        'Authorization': f'Bearer {X_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'https://api.twitter.com/2/users/by/username/{username}',
            headers=headers
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': 'Utilisateur non trouvé ou erreur API'
            }), 404
            
    except Exception as e:
        return jsonify({
            'error': 'Erreur lors de la récupération des données'
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page non trouvée"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Erreur serveur interne"), 500
