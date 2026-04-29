# 🛒 TechShop - Site E-commerce avec Analytics

## 📝 Description

**TechShop** est un site e-commerce complet de vente de produits technologiques (smartphones, ordinateurs, tablettes, accessoires) avec un système de tracking avancé qui enregistre tous les événements utilisateurs pour une analyse approfondie.

## 🎯 Objectifs

✅ **Site e-commerce fonctionnel** avec catalogue de produits  
✅ **Système de panier** avec gestion des quantités  
✅ **Processus de checkout** complet  
✅ **Tracking automatique** de tous les événements utilisateurs  
✅ **Stockage des données** pour analyse (Étape 2)  

## 🌐 Pages du Site

### 1. **Page d'accueil** (`index.html`)
- Hero section avec CTA
- 4 catégories principales (Smartphones, Ordinateurs, Accessoires, Tablettes)
- Produits en vedette (meilleurs notes)
- Bannière promotionnelle
- Formulaire newsletter

### 2. **Page Produits** (`products.html`)
- Catalogue complet de 20 produits
- Filtres par catégorie
- Filtres par prix
- Tri (prix, nom)
- Affichage en grille

### 3. **Page Panier** (`cart.html`)
- Liste des articles
- Modification des quantités
- Suppression d'articles
- Résumé de commande (sous-total, TVA, livraison)
- Codes promo
- Modal de checkout complet

### 4. **Page Contact** (`contact.html`)
- Formulaire de contact
- Informations pratiques
- Liens sociaux
- FAQ interactive

## 📦 Produits Disponibles

Le site propose **20 produits** répartis en 4 catégories :

| Catégorie | Produits | Prix |
|-----------|----------|------|
| 📱 Smartphones | iPhone 15 Pro, Samsung Galaxy S24, Google Pixel 8, OnePlus 12 | 699€ - 1 299€ |
| 💻 Ordinateurs | MacBook Pro, Dell XPS, Lenovo ThinkPad, ASUS ROG, HP Pavilion | 899€ - 2 799€ |
| 🎧 Accessoires | AirPods Pro, Sony WH-1000XM5, Logitech MX Master, claviers, batteries, SSD | 45€ - 399€ |
| 📲 Tablettes | iPad Pro, Samsung Galaxy Tab, iPad Air, Surface Pro, Fire HD | 149€ - 1 299€ |

## 🛠️ Fonctionnalités E-commerce

### Gestion du Panier
- Ajout de produits
- Modification des quantités (+/-)
- Suppression d'articles
- Persistance (localStorage)
- Badge de compteur dans la navigation

### Calculs Automatiques
- Sous-total
- TVA (20%)
- Frais de livraison (gratuite dès 50€)
- Total final

### Codes Promo
- `WELCOME10` : 10% de réduction
- `SAVE20` : 20% de réduction
- `TECHSHOP` : 15% de réduction

### Processus de Checkout
1. Clic sur "Passer la commande"
2. Modal avec formulaire complet
3. Informations de livraison (nom, email, adresse, etc.)
4. Choix du mode de paiement (CB, PayPal, Virement)
5. Acceptation des CGV
6. Confirmation de commande

## 📊 Événements Trackés

Le système collecte automatiquement ces événements e-commerce :

| Événement | Description | Données collectées |
|-----------|-------------|-------------------|
| `page_view` | Vue de page | URL, titre, temps de chargement |
| `click` | Clic sur élément | Élément, position, texte |
| `add_to_cart` | Ajout au panier | ID produit, nom, prix, quantité |
| `remove_from_cart` | Retrait du panier | ID produit, nom |
| `product_viewed` | Vue détail produit | ID, nom, catégorie |
| `category_clicked` | Navigation catégorie | Catégorie sélectionnée |
| `products_filtered` | Utilisation filtres | Catégorie, prix, tri, résultats |
| `checkout_started` | Début checkout | Nombre articles, total |
| `order_completed` | Commande finalisée | Données client, montant, paiement |
| `promo_code_applied` | Code promo utilisé | Code, réduction |
| `newsletter_signup` | Inscription newsletter | Domaine email |
| `form_submit` | Formulaire contact | Sujet, longueur message |

## 🚀 Installation et Lancement

### 1. Installer les dépendances

```powershell
cd "c:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website"
pip install -r requirements.txt
```

### 2. Lancer le serveur

```powershell
python server.py
```

### 3. Ouvrir le site

Allez sur : **http://localhost:5000**

## 💳 Scénario d'Utilisation Complet

Pour générer des données riches:

1. **Navigation** : Visitez toutes les pages
2. **Découverte** : Cliquez sur les catégories
3. **Filtrage** : Utilisez les filtres sur la page Produits
4. **Ajout au panier** : Ajoutez 3-5 produits différents
5. **Modification** : Changez les quantités dans le panier
6. **Code promo** : Testez `WELCOME10`
7. **Checkout** : Remplissez le formulaire complet
8. **Confirmation** : Validez la commande
9. **Contact** : Envoyez un message
10. **Newsletter** : Inscrivez-vous

## 📂 Format des Logs

**Exemple de log d'ajout au panier :**

```json
{
  "timestamp": "2026-02-07T15:30:45.123Z",
  "event_type": "add_to_cart",
  "session_id": "session_1707315045123_xyz789",
  "page_url": "/index.html",
  "product_id": 5,
  "product_name": "MacBook Pro 16\"",
  "product_price": 2799,
  "quantity": 1,
  "user_agent": "Mozilla/5.0...",
  "server_received_at": "2026-02-07T15:30:45.456Z"
}
```

## 📈 Métriques E-commerce à Calculer (Étape 2)

Ces données permettront de calculer :

- **Taux de conversion** : Visiteurs → Acheteurs
- **Panier moyen** : Montant moyen par commande
- **Produits populaires** : Plus vus, plus achetés
- **Taux d'abandon de panier** : Paniers créés vs commandes
- **Catégories favorites** : Distribution des ventes
- **Efficacité des promos** : Utilisation codes promo
- **Tunnel de conversion** : Produit → Panier → Checkout → Commande
- **Comportement utilisateur** : Parcours de navigation

## �️ Structure Technique

### Fichiers HTML
- `index.html` - Page d'accueil
- `products.html` - Catalogue produits
- `cart.html` - Panier et checkout
- `contact.html` - Contact et FAQ

### Fichiers JavaScript
- `tracker.js` - Système de tracking (400+ lignes)
- `products-data.js` - Base de données des 20 produits
- `cart.js` - Gestion du panier (classe ShoppingCart)
- `script.js` - Logique e-commerce et interactions

### Fichiers CSS
- `styles.css` - Styles complets du site (responsive)

### Backend Python
- `server.py` - Serveur Flask avec 5 endpoints
- `requirements.txt` - Dépendances

## 🔧 API du Serveur

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Servir le site web |
| `/log` | POST | Recevoir et sauvegarder un événement |
| `/stats` | GET | Statistiques globales des logs |
| `/events` | GET | Derniers événements (param: limit) |
| `/health` | GET | État du serveur |

## 📊 Utilisation de l'API

```powershell
# Statistiques
Invoke-WebRequest http://localhost:5000/stats

# 10 derniers événements
Invoke-WebRequest http://localhost:5000/events?limit=10

# Santé du serveur
Invoke-WebRequest http://localhost:5000/health
```

## 💡 Conseils pour Générer des Données

### Simulation de Clients Différents

**Client 1 - Acheteur décisif :**
1. Aller directement sur Produits
2. Filtrer par catégorie "Smartphones"
3. Ajouter iPhone 15 Pro au panier
4. Aller au panier immédiatement
5. Valider la commande

**Client 2 - Comparateur :**
1. Visiter plusieurs catégories
2. Consulter 5-10 produits
3. Ajouter 3 produits au panier
4. Modifier les quantités
5. Supprimer un produit
6. Appliquer un code promo
7. Finaliser ou abandonner

**Client 3 - Hésitant :**
1. Parcourir toutes les pages
2. Lire la FAQ
3. Ajouter 1-2 produits au panier
4. Sortir sans acheter (abandon de panier)

### Différentes Sessions
- Utilisez plusieurs navigateurs
- Mode navigation privée
- Différents appareils (si possible)

## 🐛 Dépannage

### Le serveur ne démarre pas
```powershell
pip install -r requirements.txt --force-reinstall
```

### Les produits ne s'affichent pas
- Vérifier la console du navigateur (F12)
- S'assurer que `products-data.js` et `cart.js` sont chargés

### Le panier ne fonctionne pas
- Vérifier le localStorage du navigateur
- Consulter la console pour les erreurs JavaScript

### Port 5000 occupé
Modifier dans `server.py` :
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📈 Indicateurs Clés de Performance (KPIs)

Ces métriques pourront être calculées à l'Étape 2 :

### Conversion
- Taux de visite → ajout panier
- Taux de visite → commande
- Taux de panier → commande (checkout)

### Engagement
- Temps moyen par session
- Pages par visite
- Produits consultés par visite
- Interactions par session

### Produits
- Top 5 produits vus
- Top 5 produits achetés
- Catégorie la plus populaire
- Prix moyen du panier

### Comportement
- Taux d'abandon de panier
- Utilisation des filtres
- Codes promo utilisés
- Parcours de navigation

## ➡️ Prochaines Étapes

### Étape 2 : Dashboard Python Analytics
Une fois que vous avez généré suffisamment de données (50+ événements recommandés), passez à l'Étape 2 pour :

- Lire et analyser tous les logs
- Calculer les métriques e-commerce
- Créer des graphiques de vente
- Visualiser les tunnels de conversion
- Identifier les produits stars
- Analyser le comportement utilisateur

### Étape 3 : Google Analytics
Comparer vos métriques avec Google Analytics

### Étape 6 : Machine Learning
Utiliser les données pour :
- Prédire la probabilité d'achat
- Recommander des produits
- Détecter les abandons de panier
- Segmenter les clients

## ✅ Checklist de Validation

Votre site e-commerce est complet si :

- [x] Le serveur démarre sans erreur
- [x] Les 4 pages s'affichent correctement
- [x] Les 20 produits sont visibles
- [x] Les filtres fonctionnent
- [x] On peut ajouter au panier
- [x] Le badge du panier se met à jour
- [x] On peut modifier les quantités
- [x] Le checkout s'ouvre
- [x] La commande peut être validée
- [x] Les événements sont loggés (console F12)
- [x] Les fichiers JSON sont créés dans `logs/`

## 🎓 Apprentissages

Ce projet vous permet de maîtriser :

✅ **E-commerce** : Panier, checkout, gestion produits  
✅ **JavaScript** : Manipulation DOM, événements, localStorage  
✅ **Data Tracking** : Collecte événements, analytics  
✅ **Python/Flask** : API REST, sauvegarde fichiers  
✅ **UX/UI** : Design responsive, interactions  

---

**🎉 Bravo ! Vous avez un site e-commerce complet avec analytics ! 🎉**

📊 **Passez à l'Étape 2 pour analyser toutes ces données !**

## 🚀 Installation et Lancement

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

1. **Installer les dépendances Python**

```powershell
cd "c:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website"
pip install -r requirements.txt
```

2. **Lancer le serveur**

```powershell
python server.py
```

3. **Ouvrir le site web**

Ouvrez votre navigateur et allez sur :
```
http://localhost:5000
```

Le serveur sera accessible avec les endpoints suivants :
- `http://localhost:5000` - Site web
- `http://localhost:5000/stats` - Statistiques des logs
- `http://localhost:5000/events` - Derniers événements
- `http://localhost:5000/health` - Vérification du serveur

## 📊 Types d'événements trackés

Le système collecte **automatiquement** les événements suivants :

### 1. **Page View** (`page_view`)
- Chargement de chaque page
- URL, titre, referrer
- Temps de chargement

### 2. **Clics** (`click`)
- Tous les clics sur la page
- Élément cliqué (tag, id, classe)
- Position du clic (x, y)
- Texte de l'élément

### 3. **Scroll** (`scroll`)
- Défilement de la page
- Position verticale
- Pourcentage de scroll
- Profondeur maximale atteinte

### 4. **Temps sur la page** (`time_on_page`)
- Durée passée sur la page
- Mis à jour toutes les 30 secondes

### 5. **Soumission de formulaires** (`form_submit`)
- Formulaires newsletter et contact
- Nombre de champs
- Noms des champs (sans les valeurs)

### 6. **Focus sur les champs** (`form_field_focus`)
- Interaction avec les formulaires
- Type de champ
- ID et nom du champ

### 7. **Activité de la souris** (`mouse_activity`)
- Résumé des mouvements
- Position de la dernière interaction

### 8. **Sortie de page** (`page_exit`)
- Temps total passé
- Avant la fermeture/navigation

### 9. **Événements personnalisés** (`custom_*`)
- Interactions spécifiques (like, share, etc.)
- Événements métiers

### 10. **Métriques de performance** (`performance_metrics`)
- Temps de chargement de la page
- Temps DNS, TCP, etc.

## 📂 Format des logs

Les logs sont sauvegardés dans le format suivant :

**Chemin** : `logs/YYYYMMDD/YYYYMMDDhhmmss.json`

**Exemple** : `logs/20260207/20260207143052.json`

**Contenu du fichier JSON** :

```json
{
  "timestamp": "2026-02-07T14:30:52.123Z",
  "event_type": "click",
  "session_id": "session_1707314652123_abc123def",
  "page_url": "/index.html",
  "page_title": "Accueil - Mon Site Analytics",
  "referrer": "",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
  "screen_width": 1920,
  "screen_height": 1080,
  "viewport_width": 1200,
  "viewport_height": 900,
  "element_tag": "BUTTON",
  "element_id": "btn-hero-cta",
  "element_class": "btn btn-primary",
  "element_text": "Commencer",
  "x_position": 450,
  "y_position": 320,
  "page_x": 450,
  "page_y": 650,
  "server_received_at": "2026-02-07T14:30:52.456Z",
  "client_ip": "127.0.0.1"
}
```

## 🎮 Utilisation du site

### Page d'accueil (`index.html`)
- **Section Hero** : Bouton CTA principal
- **Features** : 3 cartes avec boutons d'information
- **Zone interactive** : 4 boutons (Like, Share, Save, Download)
- **Compteur de clics** : Affiche le nombre total de clics
- **Newsletter** : Formulaire d'inscription

### Page À propos (`about.html`)
- Timeline du projet
- Statistiques
- Technologies utilisées

### Page Contact (`contact.html`)
- Formulaire de contact complet
- Informations de contact
- Boutons sociaux
- Section FAQ interactive

## 🛠️ Fonctionnalités techniques

### Tracker.js

**Classe `EventTracker`** :
- Génération d'ID de session unique
- Envoi automatique des événements au serveur
- Fallback localStorage si le serveur est indisponible
- Méthodes de tracking pour chaque type d'événement

**Fonctions globales** :
```javascript
// Tracker un événement personnalisé
trackEvent('button_clicked', { button_name: 'test' });

// Obtenir les stats de la session
const stats = getSessionStats();
console.log(stats);
```

### Server.py

**Endpoints disponibles** :

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Servir le site web |
| `/log` | POST | Recevoir et sauvegarder un événement |
| `/stats` | GET | Statistiques globales des logs |
| `/events` | GET | Derniers événements (query param: `limit`) |
| `/health` | GET | Vérifier l'état du serveur |

**Exemple d'utilisation** :

```powershell
# Obtenir les stats
curl http://localhost:5000/stats

# Obtenir les 20 derniers événements
curl http://localhost:5000/events?limit=20

# Vérifier la santé du serveur
curl http://localhost:5000/health
```

## 📈 Statistiques collectées

Une fois le site utilisé, vous pouvez voir les statistiques :

```powershell
# Dans PowerShell
Invoke-WebRequest http://localhost:5000/stats | Select-Object -ExpandProperty Content
```

Exemple de résultat :
```json
{
  "total_events": 147,
  "total_days": 3,
  "events_by_day": {
    "20260207": 89,
    "20260206": 42,
    "20260205": 16
  }
}
```

## 🔍 Détails techniques

### Session Management
- **ID de session** : Unique par navigateur/onglet
- **Stockage** : `sessionStorage` (perdu à la fermeture)
- **Format** : `session_TIMESTAMP_RANDOM`

### Performance
- Envoi asynchrone (ne bloque pas l'interface)
- Debouncing pour les événements fréquents (scroll, souris)
- Fallback localStorage si serveur indisponible

### Confidentialité
- ❌ Pas de collecte des valeurs des formulaires
- ✅ Seulement les métadonnées (nombre de caractères, noms de champs)
- ✅ Anonymisation possible via l'ID de session

## 🐛 Dépannage

### Le serveur ne démarre pas

```powershell
# Vérifier que les dépendances sont installées
pip list | Select-String "flask"

# Réinstaller si nécessaire
pip install -r requirements.txt --force-reinstall
```

### Les événements ne sont pas enregistrés

1. Vérifier que le serveur est bien lancé
2. Ouvrir la console du navigateur (F12)
3. Vérifier les messages de tracking
4. Vérifier le dossier `logs/` :

```powershell
Get-ChildItem -Path logs -Recurse -Filter *.json | Measure-Object
```

### Port 5000 déjà utilisé

Modifier le port dans `server.py` :
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

Et dans `tracker.js` :
```javascript
this.serverUrl = 'http://localhost:5001/log';
```

## 📖 Prochaines étapes

Une fois que vous avez collecté suffisamment de données (quelques dizaines d'événements minimum), vous pouvez passer à l'**Étape 2** :

➡️ **Dashboard Python** pour analyser ces logs et créer des visualisations

Les logs générés ici seront utilisés pour :
- Calculer des métriques (visites, clics, etc.)
- Créer des graphiques
- Identifier les comportements utilisateurs
- Entraîner des modèles de machine learning (Étape 6)

## 💡 Conseils

### Pour générer plus de données
1. Naviguez sur les 3 pages
2. Cliquez sur tous les boutons
3. Remplissez les formulaires
4. Scrollez sur les pages
5. Revenez plusieurs fois

### Pour tester différents scénarios
- Utilisez plusieurs navigateurs (Chrome, Firefox, Edge)
- Testez en mode navigation privée (nouvelles sessions)
- Variez les heures de visite
- Testez sur mobile (responsive)

## ✅ Vérification de l'étape

Votre Étape 1 est réussie si :

- [x] Le serveur démarre sans erreur
- [x] Le site web s'affiche correctement
- [x] Les 3 pages sont accessibles
- [x] Les événements sont loggés dans la console
- [x] Les fichiers JSON sont créés dans `logs/YYYYMMDD/`
- [x] Les formulaires fonctionnent
- [x] L'endpoint `/stats` retourne des données

---

**Bravo ! Vous avez complété l'Étape 1 ! 🎉**

Passez maintenant à l'**Étape 2** pour analyser ces données.
