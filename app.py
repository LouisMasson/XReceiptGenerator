import os
from flask import Flask, render_template, request, jsonify
import requests
from flask_caching import Cache
from config import X_API_KEY
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Structure: {username: {'count': 0, 'last_reset': datetime}}
request_counters = defaultdict(lambda: {'count': 0, 'last_reset': datetime.now()})

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
    # Vérifier et mettre à jour le compteur
    counter = request_counters[username]
    now = datetime.now()
    
    # Réinitialiser le compteur si c'est un nouveau jour
    if (now - counter['last_reset']).days >= 1:
        counter['count'] = 0
        counter['last_reset'] = now
    
    # Vérifier la limite
    if counter['count'] >= 3:
        return jsonify({
            'error': "Limite de 3 requêtes par jour atteinte pour cet utilisateur. Réessayez demain."
        }), 429
    
    # Incrémenter le compteur
    counter['count'] += 1

    # Calculer les requêtes restantes
    remaining_requests = 3 - counter['count']
    next_reset = counter['last_reset'] + timedelta(days=1)
    reset_time = next_reset.strftime('%H:%M')
    reset_date = next_reset.strftime('%d/%m/%Y')

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
            # Ajouter les informations du compteur dans data
            response_data['data']['requests_info'] = {
                'remaining': remaining_requests,
                'reset_time': reset_time,
                'reset_date': reset_date
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
