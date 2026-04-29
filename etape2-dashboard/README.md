# 📊 Étape 2 : Dashboard Python Analytics

## 📝 Description

Cette étape consiste à créer un **dashboard interactif** pour analyser les données collectées à l'Étape 1. Le dashboard permet de :
- Calculer des KPIs e-commerce (conversion, revenu, panier moyen)
- Visualiser les données avec des graphiques interactifs
- Analyser le comportement des utilisateurs
- Identifier les tendances et opportunités

---

## 🎯 Objectifs

1. ✅ **Charger** tous les fichiers JSON de logs
2. ✅ **Analyser** les données avec Pandas
3. ✅ **Calculer** les métriques clés (KPIs)
4. ✅ **Visualiser** avec des graphiques (Plotly)
5. ✅ **Créer** un dashboard interactif (Streamlit)

---

## 📁 Structure

```
etape2-dashboard/
├── dashboard.py          # Dashboard Streamlit principal
├── analytics.py          # Moteur d'analyse des logs
├── requirements.txt      # Dépendances Python
└── README.md            # Ce fichier
```

---

## 🚀 Installation

### 1. Installer les dépendances

```bash
cd etape2-dashboard
pip install -r requirements.txt
```

**Dépendances installées :**
- `streamlit` : Framework pour créer le dashboard web
- `pandas` : Analyse de données
- `plotly` : Graphiques interactifs
- `numpy` : Calculs numériques
- `python-dateutil` : Manipulation de dates

---

## 🎮 Utilisation

### Lancer le dashboard

```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse :
**http://localhost:8501**

---

## 📊 Fonctionnalités du Dashboard

### 1. **KPIs Principaux** 📈
- Total d'événements collectés
- Nombre de sessions uniques
- Pages vues
- Événements par session

### 2. **Métriques E-commerce** 🛍️
- Ajouts au panier
- Checkouts démarrés
- Nombre de commandes
- **Revenu total**
- **Taux de conversion** (visites → commandes)
- **Panier moyen**
- Taux d'abandon de panier
- Retraits du panier

### 3. **Visualisations Interactives** 📊

#### Onglet "Événements"
- Distribution des types d'événements (barres + camembert)
- Top 10 pages les plus vues
- Tableau détaillé des pages

#### Onglet "Produits"
- Top produits ajoutés au panier
- Top produits achetés
- Comparaison prix vs popularité

#### Onglet "Temporel"
- Événements par heure de la journée
- Événements au fil du temps (intervalle 10 min)
- Temps moyen passé par page

#### Onglet "Conversion"
- **Entonnoir de conversion** (Visites → Vues → Panier → Checkout → Commande)
- Taux de conversion par étape
- Utilisation des codes promo

#### Onglet "Appareils"
- Répartition Desktop/Mobile/Tablet
- Événements par type d'appareil

### 4. **Données Brutes** 📋
- Visualisation complète du DataFrame
- Téléchargement en CSV

### 5. **Parcours Utilisateur** 🗺️
- Sélection d'une session
- Historique complet des actions
- Visualisation du parcours

---

## 🔧 Utilisation de l'Analyseur (analytics.py)

### En ligne de commande

```bash
python analytics.py
```

Affiche un résumé des données :
- Total d'événements
- Sessions uniques
- Top 10 types d'événements
- Métriques e-commerce

### En tant que module

```python
from analytics import LogAnalyzer

# Initialiser
analyzer = LogAnalyzer()

# Charger les logs
df = analyzer.load_all_logs()

# Obtenir des KPIs
print(f"Total événements: {analyzer.get_total_events()}")
print(f"Sessions: {analyzer.get_unique_sessions()}")

# Métriques e-commerce
metrics = analyzer.get_ecommerce_metrics()
print(f"Revenu: {metrics['total_revenue']}€")
print(f"Conversion: {metrics['conversion_rate']:.2f}%")

# Top produits
top_products = analyzer.get_top_products_added(5)
print(top_products)
```

---

## 📈 KPIs Calculés

### 1. **Trafic**
- `Total événements` : Nombre total d'interactions
- `Sessions uniques` : Nombre de visiteurs distincts
- `Pages vues` : Nombre de pages consultées
- `Événements/Session` : Engagement moyen

### 2. **E-commerce**

#### Revenu
```python
revenu_total = sum(commandes['total_amount'])
panier_moyen = revenu_total / nombre_commandes
```

#### Taux de Conversion
```python
taux_conversion = (commandes / sessions_uniques) × 100
```

#### Abandon de Panier
```python
taux_abandon = ((checkouts - commandes) / checkouts) × 100
```

### 3. **Entonnoir de Conversion**

```
100% → Visites
 60% → Vues Produits
 30% → Ajouts au Panier
 15% → Checkouts Démarrés
  5% → Commandes Finalisées
```

---

## 🎨 Graphiques Disponibles

| Type | Bibliothèque | Description |
|------|-------------|-------------|
| **Barres horizontales** | Plotly Express | Top pages, produits, événements |
| **Camembert** | Plotly Express | Répartition événements, appareils |
| **Lignes** | Plotly Express | Événements par heure |
| **Aires** | Plotly Express | Événements au fil du temps |
| **Entonnoir** | Plotly Go | Conversion e-commerce |

---

## 🔍 Filtres Disponibles

### Dans la Sidebar

1. **Période** : Sélection de plage de dates
2. **Types d'événements** : Filtrer par type (multiselect)
3. **Heure de mise à jour** : Affichée en temps réel

---

## 📊 Exemples de Métriques Calculées

### Exemple avec 430 événements

```
📊 Résumé des données:
Total événements: 430
Sessions uniques: 2

Événements par type:
time_on_page                    120
custom_page_hidden               35
custom_page_visible              30
page_view                        25
custom_performance_metrics       20
scroll                           18
mouse_activity                   15
click                            12
custom_add_to_cart               8
page_exit                        7

🛍️ Métriques e-commerce:
total_add_to_cart: 8
total_remove_from_cart: 2
total_checkout_started: 3
total_orders: 1
total_revenue: 2499€
average_order_value: 2499€
conversion_rate: 50.0%
cart_abandonment_rate: 66.7%
```

---

## 🎯 Insights Possibles

### 1. **Pages Populaires**
- Identifier les pages qui attirent le plus de trafic
- Optimiser les pages avec peu de visites

### 2. **Produits Bestsellers**
- Top produits ajoutés au panier
- Top produits achetés
- Produits à promouvoir

### 3. **Taux de Conversion**
- Analyser l'entonnoir de conversion
- Identifier les points de friction
- A/B testing sur les pages critiques

### 4. **Abandon de Panier**
- Si > 70% → problème de paiement ou prix ?
- Mettre en place des emails de relance
- Simplifier le processus de checkout

### 5. **Codes Promo**
- Quels codes sont les plus utilisés ?
- ROI des campagnes promotionnelles

### 6. **Comportement Temporel**
- Heures de pointe (optimiser les serveurs)
- Jours de la semaine les plus actifs
- Temps passé par page (engagement)

---

## 🚀 Améliorations Futures

### Étape 3 : Google Analytics
- Comparer les données custom avec GA4
- Valider la précision du tracking

### Étape 4 : Apache NiFi
- Automatiser le traitement des logs
- Pipeline ETL visuel

### Étape 5 : Marquez
- Traçabilité des données (lineage)
- Gouvernance des données

### Étape 6 : Machine Learning
- Prédiction des achats
- Recommandations de produits
- Détection d'anomalies

---

## 🛠️ Dépannage

### Erreur : "No module named 'streamlit'"
```bash
pip install streamlit
```

### Erreur : "Aucune donnée disponible"
Vérifier que :
- Le dossier `../etape1-website/logs/` existe
- Il contient des fichiers JSON
- Le serveur de l'Étape 1 a collecté des données

### Dashboard ne se charge pas
```bash
# Tester l'analyseur seul
python analytics.py

# Relancer Streamlit
streamlit run dashboard.py --server.port 8501
```

---

## 📚 Ressources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

## ✅ Checklist de Validation

- [ ] Dashboard se lance sans erreur
- [ ] KPIs principaux s'affichent
- [ ] Graphiques se chargent correctement
- [ ] Filtres fonctionnent
- [ ] Données brutes téléchargeables en CSV
- [ ] Entonnoir de conversion visible
- [ ] Parcours utilisateur consultable

---

## 🎓 Ce que vous avez appris

1. **Pandas** : Manipulation de données JSON → DataFrame
2. **Streamlit** : Création de dashboards web interactifs
3. **Plotly** : Visualisations interactives modernes
4. **Analytics** : Calcul de KPIs e-commerce
5. **Data Science** : Analyse exploratoire de données (EDA)

---

**Prêt pour l'Étape 3 : Intégration Google Analytics !** 🚀
