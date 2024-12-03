import os
from flask import Flask, render_template, request, jsonify
import requests
from flask_caching import Cache
from config import X_API_KEY

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Flask-Caching
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 900,  # 15 minutes en secondes
    'CACHE_THRESHOLD': 100  # Nombre maximum d'éléments dans le cache
})
cache.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/<username>')
def get_user(username):
    # Vérifier le cache d'abord
    cache_key = f'user_{username}'
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        return jsonify(cached_response)

    headers = {
        'Authorization': f'Bearer {X_API_KEY}',
        'User-Agent': 'XReceiptGenerator/1.0',
        'Accept': 'application/json'
    }
    
    # Define the fields we want to retrieve
    params = {
        'user.fields': 'description,created_at,public_metrics,profile_image_url,url,username,name,verified'
    }
    
    try:
        response = requests.get(
            f'https://api.twitter.com/2/users/by/username/{username}',
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            # Stocker dans le cache avant de retourner
            response_data = response.json()
            cache.set(cache_key, response_data)
            return jsonify(response_data)
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
