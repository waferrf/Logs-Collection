# 🚀 Guide de Démarrage Rapide - Étape 2

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

Ouvrez PowerShell et exécutez :

```powershell
cd "c:\Users\wafae\OneDrive\Bureau\projet python avancer\etape2-dashboard"
pip install streamlit pandas plotly numpy python-dateutil
```

**OU** si vous avez des erreurs de permissions :

```powershell
python -m pip install --user streamlit pandas plotly numpy python-dateutil
```

---

### 2️⃣ Tester l'analyseur

Vérifiez que les données sont bien chargées :

```powershell
python test_analytics.py
```

Vous devriez voir :
```
📊 TEST DE L'ANALYSEUR DE LOGS
✅ 430 événements chargés

📈 KPIs PRINCIPAUX
📌 Total événements: 430
👥 Sessions uniques: 2

🛍️ MÉTRIQUES E-COMMERCE
🛒 Ajouts au panier: 8
✅ Commandes finalisées: 1
💰 Revenu total: 2,499€
```

---

### 3️⃣ Lancer le dashboard

```powershell
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à :
**http://localhost:8501**

---

## 🎨 Aperçu du Dashboard

Le dashboard contient **5 onglets** :

### 📈 Onglet "Événements"
- Distribution des types d'événements (graphique en barres + camembert)
- Top 10 pages les plus vues

### 🛍️ Onglet "Produits"
- Top produits ajoutés au panier
- Top produits achetés (avec revenu)

### ⏰ Onglet "Temporel"
- Événements par heure de la journée
- Timeline des événements (intervalle 10 min)
- Temps moyen par page

### 🎯 Onglet "Conversion"
- **Entonnoir de conversion** (Visites → Panier → Checkout → Commande)
- Taux de conversion par étape
- Codes promo utilisés

### 📱 Onglet "Appareils"
- Répartition Desktop/Mobile/Tablet

---

## 📊 KPIs Affichés

### En haut de la page :
- 📌 Total Événements
- 👥 Sessions Uniques
- 👁️ Pages Vues
- 📊 Événements/Session

### Section E-commerce :
- 🛒 Ajouts au Panier
- 💳 Checkouts Démarrés
- ✅ Commandes
- 💰 Revenu Total
- 🎯 Taux de Conversion
- 📦 Panier Moyen
- 🚫 Taux Abandon Panier

---

## 🔧 Dépannage

### ❌ Erreur : "No module named 'streamlit'"
Solution :
```powershell
pip install streamlit
```

### ❌ Erreur : "Aucune donnée disponible"
Vérifiez :
1. Le dossier `../etape1-website/logs/` existe
2. Il contient des sous-dossiers (ex: `20260207`)
3. Les sous-dossiers contiennent des fichiers `.json`

### ❌ Le dashboard ne charge pas
1. Arrêter le serveur : `Ctrl+C`
2. Relancer : `streamlit run dashboard.py`

---

## 💡 Astuces

### Recharger les données
Appuyez sur **R** dans le navigateur ou cliquez sur "Rerun" en haut à droite

### Télécharger les données
Allez dans "Données Brutes" → Cliquez sur "📥 Télécharger CSV"

### Mode sombre
Cliquez sur ⋮ (menu) → Settings → Theme → Dark

---

## 📚 Prochaine Étape

Une fois le dashboard fonctionnel, vous êtes prêt pour :
**Étape 3 : Intégration Google Analytics** 🚀
