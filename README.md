# Projet Python Avancé - Analytics et Data Pipeline

## 📋 Vue d'ensemble

Ce projet est un **système complet d'analyse de données web** qui illustre le cycle de vie complet des données : de la collecte à l'exploitation par du machine learning, en passant par le traitement, la visualisation et la gouvernance.

### 🎯 Objectif pédagogique
Comprendre et maîtriser l'ensemble de la chaîne de traitement des données :
- **Collecte** : Capturer les interactions utilisateurs
- **Stockage** : Organiser les données de manière structurée
- **Traitement** : Transformer et agréger les données brutes
- **Visualisation** : Créer des dashboards analytiques
- **Gouvernance** : Tracer la provenance des données (Data Lineage)
- **Intelligence** : Extraire de la valeur avec le Machine Learning

### 🏗️ Architecture globale

Le projet simule une plateforme d'analytics moderne en 6 étapes progressives, chacune ajoutant une couche de complexité et de fonctionnalités.

```
┌─────────────────┐
│  Site Web       │  ← Étape 1 : Collecte des événements
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │ Événements (clics, navigation...)
         ↓
┌─────────────────┐
│  Logs JSON      │  ← Stockage structuré par date/heure
│  YYYYMMDD/...   │     (ex: 20240115/20240115143052.json)
└────────┬────────┘
         │
         ├─→ Étape 2 : Dashboard Python (Streamlit/Dash)
         │   ↳ Métriques personnalisées
         │
         ├─→ Étape 3 : Google Analytics
         │   ↳ Comparaison avec solution industrielle
         │
         ├─→ Étape 4 : Apache NiFi
         │   ↳ Pipeline de transformation
         │   └─→ Output/
         │
         ├─→ Étape 5 : Marquez
         │   ↳ Lineage & Gouvernance
         │
         └─→ Étape 6 : Machine Learning
             ↳ Prédictions & Intelligence
```

## 📁 Structure du projet

```
projet-python-avancer/
├── etape1-website/          # Site web avec collecte de logs
│   ├── index.html           # Page principale
│   ├── styles.css           # Styles CSS
│   ├── script.js            # Tracking JavaScript
│   ├── server.py            # Serveur Python pour recevoir logs
│   └── logs/                # Stockage des événements
│       └── YYYYMMDD/        # Dossier par jour
│           └── YYYYMMDDhhmmss.json  # Fichier par événement
│
├── etape2-dashboard/        # Dashboard d'analyse Python
│   ├── app.py               # Application Streamlit/Dash
│   ├── metrics.py           # Calcul des métriques
│   ├── visualizations.py    # Graphiques et charts
│   └── requirements.txt     # Dépendances Python
│
├── etape3-google-analytics/ # Intégration Google Analytics
│   ├── ga_integration.py    # API Google Analytics
│   ├── comparison.py        # Comparaison métriques
│   └── credentials/         # Clés API
│       └── ga_credentials.json
│
├── etape4-nifi/            # Pipeline Apache NiFi
│   ├── templates/          # Templates de flux NiFi
│   ├── processors/         # Processeurs personnalisés
│   └── output/             # Données transformées
│
├── etape5-marquez/         # Lineage des données
│   ├── config/             # Configuration Marquez
│   └── lineage_viz.py      # Visualisation du lineage
│
├── etape6-ml/              # Machine Learning
│   ├── model.py            # Architecture du modèle
│   ├── train.py            # Entraînement
│   ├── predictions.py      # Inférence
│   ├── features.py         # Feature engineering
│   └── evaluation.py       # Métriques de performance
│
└── README.md               # Ce fichier
```

---

## 📚 Détail des étapes

### 🌐 Étape 1 : Site web avec collecte de logs

**Objectif** : Créer un site web qui enregistre automatiquement tous les événements utilisateurs.

#### Fonctionnalités
- **Site web interactif** : Pages HTML avec boutons, formulaires, navigation
- **Tracking d'événements** :
  - Clics sur boutons
  - Navigation entre pages
  - Temps passé sur la page
  - Défilement (scroll)
  - Soumission de formulaires
  
#### Système de stockage
- **Format de dossiers** : `YYYYMMDD/` (ex: `20240115/`)
- **Format de fichiers** : `YYYYMMDDhhmmss.json` (ex: `20240115143052.json`)
- **Contenu JSON** :
```json
{
  "timestamp": "2024-01-15T14:30:52.123Z",
  "event_type": "click",
  "element_id": "btn-submit",
  "page_url": "/index.html",
  "user_agent": "Mozilla/5.0...",
  "session_id": "abc123...",
  "metadata": {
    "x": 450,
    "y": 320
  }
}
```

#### Technologies
- **Frontend** : HTML5, CSS3, JavaScript vanilla
- **Backend** : Serveur Python (Flask/FastAPI) pour recevoir les logs
- **Stockage** : Système de fichiers local

#### Livrables
- Site web fonctionnel avec au moins 3 pages
- Script JavaScript de tracking
- Serveur Python pour sauvegarder les logs
- Au moins 5 types d'événements trackés

---

### 📊 Étape 2 : Dashboard Python d'analyse

**Objectif** : Analyser les logs collectés et créer un tableau de bord visuel pour comprendre le comportement des utilisateurs.

#### Métriques à calculer
1. **Métriques de trafic** :
   - Nombre total de visites
   - Visites par jour/heure
   - Pages les plus visitées
   - Durée moyenne des sessions

2. **Métriques d'engagement** :
   - Taux de rebond (bounce rate)
   - Événements par session
   - Chemins de navigation populaires
   - Heatmap des clics

3. **Métriques temporelles** :
   - Distribution horaire du trafic
   - Jours les plus actifs
   - Tendances sur la période

#### Visualisations
- **Graphiques temporels** : Courbes d'évolution du trafic
- **Graphiques en barres** : Événements par type
- **Camemberts** : Distribution des sources de trafic
- **Heatmaps** : Visualisation de l'activité

#### Technologies suggérées
- **Streamlit** : Simple, rapide, interactif
- **Dash (Plotly)** : Plus de contrôle, graphiques avancés
- **Pandas** : Manipulation des données
- **Plotly/Matplotlib** : Visualisations

#### Fonctionnalités du dashboard
- Filtres par date
- Sélection de métriques
- Export des données
- Actualisation en temps réel

---

### 📈 Étape 3 : Intégration Google Analytics

**Objectif** : Comparer vos métriques maison avec celles de Google Analytics, un outil professionnel.

#### Tâches
1. **Intégration dans le site web** :
   - Créer un compte Google Analytics
   - Ajouter le code de tracking (gtag.js)
   - Configurer les événements personnalisés

2. **Récupération des données** :
   - Utiliser l'API Google Analytics 4 (GA4)
   - Authentification OAuth 2.0
   - Requêtes pour extraire les métriques

3. **Comparaison** :
   - Afficher les deux sources côte à côte
   - Calculer les écarts
   - Analyser les différences

#### Exemples de comparaison
| Métrique | Vos logs | Google Analytics | Écart |
|----------|----------|------------------|-------|
| Visites | 1,234 | 1,198 | +3% |
| Pages vues | 3,456 | 3,402 | +1.6% |
| Taux de rebond | 42% | 45% | -3% |

#### Apprentissages
- Comprendre pourquoi les chiffres peuvent différer
- Découvrir les fonctionnalités avancées de GA
- Apprendre l'API Google Analytics

---

### ⚙️ Étape 4 : Pipeline Apache NiFi

**Objectif** : Remplacer le script Python d'analyse par un pipeline de traitement de données professionnel et visuel.

#### Qu'est-ce qu'Apache NiFi ?
Apache NiFi est un outil de pipeline de données qui permet de :
- **Collecter** des données de multiples sources
- **Transformer** les données (filtrage, enrichissement, agrégation)
- **Router** les données selon des règles
- **Livrer** les données à des destinations variées

#### Architecture du flux NiFi

```
┌──────────────┐
│ GetFile      │ ← Lire les fichiers JSON du dossier logs/
└──────┬───────┘
       │
┌──────▼───────┐
│ EvaluateJson │ ← Extraire les champs JSON
└──────┬───────┘
       │
┌──────▼───────┐
│ RouteOnAttr  │ ← Router par type d'événement
└──┬────┬────┬─┘
   │    │    │
   │    │    └─→ Événements de clic
   │    └──────→ Événements de navigation
   └───────────→ Autres événements
       │
┌──────▼────────┐
│ AggregateBy   │ ← Agréger par heure/jour
│ TimeWindow    │
└──────┬────────┘
       │
┌──────▼────────┐
│ PutFile       │ ← Écrire dans output/
└───────────────┘
```

#### Transformations à implémenter
1. **Filtrage** : Éliminer les événements invalides
2. **Enrichissement** : Ajouter des métadonnées (géolocalisation, device type)
3. **Agrégation** : Calculer les métriques par fenêtre de temps
4. **Formatage** : Générer des fichiers CSV/JSON pour le dashboard

#### Intégration avec le dashboard
- Le dashboard lit maintenant les fichiers du dossier `output/`
- Mise à jour automatique quand NiFi génère de nouvelles données
- NiFi devient la source de vérité pour les analyses

---

### 🔍 Étape 5 : Lineage avec Marquez

**Objectif** : Tracer la provenance des données (d'où viennent-elles, comment sont-elles transformées, où vont-elles).

#### Qu'est-ce que le Data Lineage ?
Le lineage des données permet de :
- **Tracer** l'origine de chaque donnée
- **Documenter** les transformations appliquées
- **Auditer** le flux de données
- **Déboguer** les problèmes de qualité
- **Conformité** réglementaire (RGPD, etc.)

#### Architecture avec Marquez

```
┌─────────────────────────────────────────────┐
│             Marquez Server                  │
│  (Collecte et stocke le lineage)           │
└────────────▲────────────────────────────────┘
             │
             │ OpenLineage events
             │
┌────────────┴────────────────────────────────┐
│          Apache NiFi                        │
│  (avec OpenLineage integration)            │
└─────────────────────────────────────────────┘
```

#### Visualisation du lineage

```
Site Web (logs/)
    │
    │ event_type, timestamp, user_id...
    ↓
[GetFile] → [ValidateJSON] → [FilterInvalid]
                                    │
                                    ├─ validated_events
                                    ↓
                            [EnrichWithGeo]
                                    │
                                    ├─ enriched_events
                                    ↓
                            [AggregateByHour]
                                    │
                                    ├─ hourly_metrics
                                    ↓
                            output/metrics.json
                                    │
                                    ↓
                            Dashboard Python
```

#### Informations capturées
- **Datasets** : Fichiers sources et destinations
- **Jobs** : Processeurs NiFi
- **Runs** : Exécutions avec statut (succès/échec)
- **Schema** : Structure des données à chaque étape
- **Transformations** : Opérations appliquées

#### Cas d'usage
- "Cette métrique vient de quelles données sources ?"
- "Quelles transformations ont été appliquées ?"
- "Qui consomme ces données ?"
- "Quelle est la fraîcheur des données ?"

---

### 🤖 Étape 6 : Machine Learning

**Objectif** : Utiliser les données collectées pour entraîner un modèle d'apprentissage automatique qui apporte de la valeur business.

#### Cas d'usage possibles

1. **Prédiction du comportement utilisateur**
   - Prédire si un utilisateur va convertir (acheter, s'inscrire)
   - Identifier les utilisateurs à risque de churn
   - Recommander la prochaine page à visiter

2. **Détection d'anomalies**
   - Identifier les comportements suspects (fraude, bots)
   - Détecter les bugs du site (erreurs fréquentes)
   - Alerter sur des baisses de trafic inhabituelles

3. **Segmentation des utilisateurs**
   - Clustering par comportement
   - Personnalisation de l'expérience
   - Ciblage marketing

4. **Prédiction du taux de rebond**
   - Prédire si un utilisateur va quitter après la première page
   - Identifier les facteurs de rebond
   - Optimiser les landing pages

#### Pipeline ML

```
1. Collecte des données
   ↓
2. Feature Engineering
   - Durée de session
   - Nombre de pages vues
   - Type d'appareil
   - Heure de visite
   - Jour de la semaine
   - Séquence de navigation
   ↓
3. Préparation
   - Nettoyage
   - Normalisation
   - Train/Test split
   ↓
4. Entraînement
   - Choix de l'algorithme
   - Optimisation des hyperparamètres
   - Cross-validation
   ↓
5. Évaluation
   - Accuracy, Precision, Recall
   - Courbe ROC, AUC
   - Matrice de confusion
   ↓
6. Déploiement
   - API de prédiction
   - Intégration au dashboard
   - Monitoring des performances
```

#### Technologies
- **scikit-learn** : Modèles classiques (Random Forest, SVM, etc.)
- **TensorFlow/Keras** : Deep Learning
- **PyTorch** : Réseaux de neurones avancés
- **XGBoost/LightGBM** : Gradient Boosting performant

#### Exemple : Prédiction de conversion

**Features** :
- `time_on_site` : Temps passé (secondes)
- `num_pages_viewed` : Nombre de pages vues
- `num_clicks` : Nombre de clics
- `device_type` : Mobile/Desktop/Tablet
- `hour_of_day` : Heure de la visite
- `referrer_type` : Organique/Direct/Social

**Target** :
- `converted` : 0 ou 1 (conversion oui/non)

**Modèle** : Random Forest Classifier

**Résultats attendus** :
- Accuracy : ~85%
- Feature importance : identifier les facteurs clés
- Prédictions en temps réel

#### Intégration au dashboard
- Section "Prédictions ML"
- Score de conversion pour chaque session
- Recommandations d'optimisation
- Alertes automatiques

---

## 🚀 Installation et lancement

### Prérequis
- Python 3.9+
- Node.js (pour certains outils)
- Java 8+ (pour Apache NiFi)
- Docker (optionnel, pour Marquez)

### Installation rapide

```bash
# Cloner le projet
cd "C:\Users\Administrateur\Desktop\Logs-Collection"

# Installer les dépendances Python
pip install -r requirements.txt

# Lancer le site web (Étape 1)
cd etape1-website
python server.py

# Lancer le dashboard (Étape 2)
cd ../etape2-dashboard
streamlit run app.py
```

### Installation détaillée
Voir les fichiers README dans chaque sous-dossier d'étape.

---

## 📖 Apprentissages clés

Ce projet vous permettra de maîtriser :

1. **Développement Web** : HTML/CSS/JavaScript, tracking d'événements
2. **Backend Python** : APIs, traitement de fichiers, serveurs
3. **Data Engineering** : ETL, pipelines de données, Apache NiFi
4. **Data Visualization** : Dashboards interactifs, graphiques
5. **APIs tierces** : Google Analytics API, authentification OAuth
6. **Data Governance** : Lineage, traçabilité, conformité
7. **Machine Learning** : Feature engineering, entraînement, évaluation
8. **Architecture de données** : Design de systèmes, bonnes pratiques

---

## 🎓 Progression recommandée

1. **Semaine 1-2** : Étapes 1 et 2 (Site + Dashboard basique)
2. **Semaine 3** : Étape 3 (Google Analytics)
3. **Semaine 4-5** : Étape 4 (Apache NiFi)
4. **Semaine 6** : Étape 5 (Marquez)
5. **Semaine 7-8** : Étape 6 (Machine Learning)

---

## 📝 Ressources

- [Documentation Apache NiFi](https://nifi.apache.org/docs.html)
- [Google Analytics 4 API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Marquez Documentation](https://marquezproject.github.io/marquez/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/index.html)

---

## 🤝 Contribution

Ce projet est évolutif. N'hésitez pas à :
- Ajouter de nouvelles métriques
- Implémenter d'autres cas d'usage ML
- Améliorer les visualisations
- Optimiser les pipelines

---

## 📄 Licence

Projet éducatif - Libre d'utilisation et de modification.

---

**Bon courage pour votre projet ! 🚀**
