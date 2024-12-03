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
    
    # Define the fields we want to retrieve
    params = {
        'user.fields': 'created_at,public_metrics,username,name'
    }
    
    try:
        response = requests.get(
            f'https://api.twitter.com/2/users/by/username/{username}',
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({
                'error': "L'utilisateur demandé n'existe pas sur X"
            }), 404
        elif response.status_code == 401:
            return jsonify({
                'error': "Erreur d'authentification avec l'API X"
            }), 401
        elif response.status_code == 429:
            return jsonify({
                'error': "Limite de requêtes API dépassée. Veuillez réessayer plus tard"
            }), 429
        else:
            return jsonify({
                'error': f"Erreur inattendue de l'API X (code {response.status_code})"
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': "Impossible de se connecter à l'API X. Veuillez vérifier votre connexion"
        }), 503
    except Exception as e:
        return jsonify({
            'error': "Une erreur interne s'est produite lors de la récupération des données"
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page non trouvée"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Erreur serveur interne"), 500
