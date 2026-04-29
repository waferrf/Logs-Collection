"""
Serveur Flask pour collecter et sauvegarder les événements du site web
Format: logs/YYYYMMDD/YYYYMMDDhhmmss.json
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Configuration
LOGS_DIR = Path('logs')
LOGS_DIR.mkdir(exist_ok=True)


def get_log_file_path():
    """
    Génère le chemin du fichier de log selon le format demandé:
    logs/YYYYMMDD/YYYYMMDDhhmmss.json
    """
    now = datetime.now()
    
    # Dossier par jour : YYYYMMDD
    day_folder = now.strftime('%Y%m%d')
    day_path = LOGS_DIR / day_folder
    day_path.mkdir(exist_ok=True)
    
    # Fichier par événement : YYYYMMDDhhmmss.json
    filename = now.strftime('%Y%m%d%H%M%S') + '.json'
    
    # Gérer les collisions (même seconde)
    file_path = day_path / filename
    counter = 1
    while file_path.exists():
        filename = now.strftime('%Y%m%d%H%M%S') + f'_{counter}.json'
        file_path = day_path / filename
        counter += 1
    
    return file_path


@app.route('/')
def index():
    """Page d'accueil du serveur"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Servir les fichiers statiques (HTML, CSS, JS)"""
    return send_from_directory('.', path)


@app.route('/log', methods=['POST'])
def log_event():
    """
    Endpoint pour recevoir et sauvegarder les événements
    """
    try:
        # Récupérer les données JSON
        event_data = request.get_json()
        
        if not event_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Ajouter des métadonnées supplémentaires
        event_data['server_received_at'] = datetime.now().isoformat()
        event_data['client_ip'] = request.remote_addr
        
        # Générer le chemin du fichier
        log_file_path = get_log_file_path()
        
        # Sauvegarder l'événement
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(event_data, f, ensure_ascii=False, indent=2)
        
        # Log dans la console
        event_type = event_data.get('event_type', 'unknown')
        session_id = event_data.get('session_id', 'unknown')[:15]
        print(f"✅ [{event_type}] Session: {session_id}... -> {log_file_path}")
        
        return jsonify({
            'status': 'success',
            'message': 'Event logged successfully',
            'file': str(log_file_path)
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """
    Endpoint pour obtenir des statistiques sur les logs collectés
    """
    try:
        total_events = 0
        days = {}
        
        # Parcourir tous les dossiers de logs
        for day_folder in LOGS_DIR.iterdir():
            if day_folder.is_dir():
                day_name = day_folder.name
                event_files = list(day_folder.glob('*.json'))
                event_count = len(event_files)
                
                days[day_name] = event_count
                total_events += event_count
        
        return jsonify({
            'total_events': total_events,
            'total_days': len(days),
            'events_by_day': days
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/events', methods=['GET'])
def get_events():
    """
    Endpoint pour récupérer les derniers événements
    """
    try:
        limit = int(request.args.get('limit', 10))
        events = []
        
        # Récupérer tous les fichiers de logs
        all_files = []
        for day_folder in LOGS_DIR.iterdir():
            if day_folder.is_dir():
                all_files.extend(day_folder.glob('*.json'))
        
        # Trier par date (plus récent en premier)
        all_files.sort(reverse=True)
        
        # Lire les N derniers événements
        for log_file in all_files[:limit]:
            with open(log_file, 'r', encoding='utf-8') as f:
                event = json.load(f)
                events.append(event)
        
        return jsonify({
            'count': len(events),
            'events': events
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Vérifier que le serveur fonctionne"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'logs_directory': str(LOGS_DIR.absolute())
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("Serveur de collecte de logs demarre")
    print("=" * 60)
    print(f"Dossier des logs: {LOGS_DIR.absolute()}")
    print("Serveur: http://localhost:5000")
    print("Stats: http://localhost:5000/stats")
    print("Evenements recents: http://localhost:5000/events")
    print("Health check: http://localhost:5000/health")
    print("=" * 60)
    print("\nAppuyez sur Ctrl+C pour arreter le serveur\n")
    
    # Lancer le serveur
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
