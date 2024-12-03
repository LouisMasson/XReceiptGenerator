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
    
    # Define the fields we want to retrieve from v1.1 API
    try:
        response = requests.get(
            f'https://api.twitter.com/1.1/users/show.json?screen_name={username}',
            headers=headers
        )
        
        if response.status_code == 200:
            # Transform v1.1 API response to match our frontend expectations
            raw_data = response.json()
            response_data = {
                'data': {
                    'id': raw_data['id_str'],
                    'name': raw_data['name'],
                    'username': raw_data['screen_name'],
                    'description': raw_data['description'],
                    'created_at': raw_data['created_at'],
                    'profile_image_url': raw_data['profile_image_url_https'].replace('_normal', ''),
                    'url': raw_data['url'],
                    'verified': raw_data['verified'],
                    'location': raw_data['location'],
                    'public_metrics': {
                        'followers_count': raw_data['followers_count'],
                        'following_count': raw_data['friends_count'],
                        'tweet_count': raw_data['statuses_count'],
                        'like_count': raw_data['favourites_count'],
                        'listed_count': raw_data['listed_count']
                    }
                }
            }
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
