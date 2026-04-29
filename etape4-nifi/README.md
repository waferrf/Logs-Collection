# 📊 Étape 4 : Pipeline Apache NiFi

## ✅ Prérequis Validés

- ✅ Java 21 installé
- ✅ Apache NiFi installé
- ✅ Dossiers créés :
  - `etape4-nifi/` - Dossier principal
  - `etape4-nifi/output/` - Résultats NiFi
  - `etape4-nifi/templates/` - Templates NiFi

---

## 🎯 Objectif

Créer un **pipeline NiFi** qui :
1. **Lit** les fichiers JSON de logs (`etape1-website/logs/`)
2. **Transforme** et **agrège** les données
3. **Écrit** les résultats dans `etape4-nifi/output/`
4. Le dashboard lit ensuite depuis `output/` au lieu des logs bruts

---

## 📋 GUIDE DE CRÉATION DU FLUX NIFI

### Étape 1 : Accéder à l'interface NiFi

1. Ouvrez votre navigateur
2. Allez sur l'URL de NiFi :
   - **HTTP** : http://localhost:8080/nifi
   - **HTTPS** : https://localhost:8443/nifi
3. Connectez-vous (si authentification requise)

---

### Étape 2 : Créer le flux de traitement

Voici le pipeline à créer :

```
┌──────────────────┐
│  ListFile        │ ← Lister les fichiers JSON
│  (logs/)         │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  FetchFile       │ ← Lire le contenu
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ EvaluateJsonPath │ ← Extraire les champs
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ RouteOnAttribute │ ← Filtrer/Router
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ AttributesToJSON │ ← Créer le JSON agrégé
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  PutFile         │ ← Écrire dans output/
│  (output/)       │
└──────────────────┘
```

---

## 🔧 CONFIGURATION DES PROCESSEURS

### 1️⃣ ListFile - Lister les fichiers de logs

**Glisser-déposer :** `ListFile` depuis la barre d'outils

**Configuration :**
- **Input Directory** : `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website\logs`
- **Recurse Subdirectories** : `true`
- **File Filter** : `.*\.json`
- **Minimum File Age** : `0 sec`
- **Run Schedule** : `30 sec` (scan toutes les 30 secondes)

**Relationships à auto-terminer :**
- ☑️ Auto-terminate : `success` ❌ (non, relier à FetchFile)

---

### 2️⃣ FetchFile - Lire le contenu des fichiers

**Configuration :**
- **File to Fetch** : `${absolute.path}/${filename}`
- **Completion Strategy** : `None`

**Relier :**
- ListFile `success` → FetchFile

---

### 3️⃣ EvaluateJsonPath - Extraire les données

**Configuration :**
- **Destination** : `flowfile-attribute`
- **Return Type** : `json`

**Ajouter des propriétés personnalisées :**
```
event_type = $.event_type
timestamp = $.timestamp
session_id = $.session_id
page_url = $.page_url
```

**Pour les événements e-commerce, ajouter aussi :**
```
product_id = $.product_id
product_name = $.product_name
product_price = $.product_price
quantity = $.quantity
total_amount = $.total_amount
```

**Relier :**
- FetchFile `success` → EvaluateJsonPath

---

### 4️⃣ RouteOnAttribute - Router par type d'événement

**Configuration :**

**Ajouter des routes personnalisées :**
```
page_view = ${event_type:equals('page_view')}
add_to_cart = ${event_type:equals('add_to_cart')}
purchase = ${event_type:equals('purchase')}
checkout = ${event_type:equals('checkout_started')}
```

**Relier :**
- EvaluateJsonPath `matched` → RouteOnAttribute

---

### 5️⃣ AttributesToJSON - Créer le JSON de sortie

**Configuration :**
- **Attributes List** : (laisser vide pour tout inclure)
- **Destination** : `flowfile-content`
- **Include Core Attributes** : `false`
- **Null Value** : `false`

**Relier :**
- RouteOnAttribute `page_view` → AttributesToJSON
- RouteOnAttribute `add_to_cart` → AttributesToJSON
- RouteOnAttribute `purchase` → AttributesToJSON
- RouteOnAttribute `checkout` → AttributesToJSON

---

### 6️⃣ PutFile - Écrire les résultats

**Configuration :**
- **Directory** : `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output`
- **Conflict Resolution Strategy** : `replace`
- **Create Missing Directories** : `true`
- **Permissions** : (laisser vide)

**Optionnel - Nomme les fichiers par type :**
- **Directory** : `${literal("C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output")}/${event_type}`

**Relier :**
- AttributesToJSON `success` → PutFile

---

## 🚀 DÉMARRAGE DU FLUX

### 1. Vérifier les connexions
- Toutes les relations doivent être connectées ou auto-terminées
- Pas de warnings (triangles jaunes)

### 2. Démarrer les processeurs
- Clic droit sur chaque processeur → **Start**
- OU sélectionner tous les processeurs → Clic droit → **Start**

### 3. Vérifier l'exécution
- Les chiffres sur les connexions doivent augmenter
- Vérifier le dossier `output/` pour voir les fichiers générés

---

## 📊 STRUCTURE DES FICHIERS DE SORTIE

NiFi créera des fichiers dans `etape4-nifi/output/` :

```
output/
├── page_view/
│   ├── result_001.json
│   ├── result_002.json
│   └── ...
├── add_to_cart/
│   ├── result_001.json
│   └── ...
├── purchase/
│   └── ...
└── aggregated_metrics.json  (optionnel)
```

---

## 🔧 PIPELINE AVANCÉ (OPTIONNEL)

Pour créer des **agrégations** (nombre de vues, sommes, moyennes) :

### Ajouter UpdateAttribute pour grouper par heure

**Processeur :** `UpdateAttribute`

**Propriétés :**
```
hour_bucket = ${timestamp:toDate('yyyy-MM-dd HH:mm:ss'):format('yyyy-MM-dd_HH')}
```

### Ajouter MergeContent pour agréger

**Processeur :** `MergeContent`

**Configuration :**
- **Merge Strategy** : `Bin-Packing`
- **Minimum Number of Entries** : `10`
- **Maximum Number of Entries** : `100`
- **Correlation Attribute Name** : `hour_bucket`

---

## 📈 ADAPTER LE DASHBOARD

Une fois NiFi actif, le dashboard doit lire depuis `output/` :

**Fichier à modifier :** `etape2-dashboard/analytics.py`

**Changement :**
```python
# Ancien
def __init__(self, logs_dir: str = "../etape1-website/logs"):

# Nouveau
def __init__(self, logs_dir: str = "../etape4-nifi/output"):
```

---

## ✅ VÉRIFICATION

### Test 1 : NiFi reçoit les fichiers
- Interface NiFi → Les processeurs doivent être verts
- Les connexions doivent montrer des flux de données

### Test 2 : Fichiers créés dans output/
```powershell
Get-ChildItem -Path "etape4-nifi\output" -Recurse
```

### Test 3 : Dashboard lit les données
```powershell
cd etape2-dashboard
python -m streamlit run dashboard.py
```

---

## 🎯 MÉTRIQUES À SURVEILLER DANS NIFI

Dans l'interface NiFi, surveillez :
- **In** : Nombre de fichiers entrants
- **Out** : Nombre de fichiers sortants
- **Read/Write** : Octets lus/écrits
- **Tasks** : Nombre de tâches exécutées

---

## 🐛 DÉPANNAGE

### Problème : Les processeurs ne démarrent pas
**Solution :** Vérifier que toutes les relations sont connectées

### Problème : Aucun fichier dans output/
**Solution :** Vérifier le chemin dans ListFile et PutFile

### Problème : Erreurs JSON
**Solution :** Vérifier EvaluateJsonPath - les chemins JSON doivent être corrects

### Problème : Permissions refusées
**Solution :** Vérifier que NiFi a les droits d'écriture sur `output/`

---

## 📝 NOTES IMPORTANTES

- **Automatique** : NiFi scanne les logs toutes les 30 secondes
- **Temps réel** : Les nouvelles données sont traitées automatiquement
- **Scalabilité** : NiFi peut traiter des millions de fichiers
- **Monitoring** : L'interface montre tout en temps réel

---

## 🎉 RÉSULTAT FINAL

Après configuration :

```
Site Web → Logs JSON → [NiFi Pipeline] → Output agrégé → Dashboard
```

**Avantages :**
- ✅ Traitement automatisé
- ✅ Transformations visuelles
- ✅ Monitoring en temps réel
- ✅ Scalable et professionnel

---

## 📚 PROCHAINES ÉTAPES

Une fois NiFi configuré :
- ✅ Étape 5 : Marquez (Data Lineage)
- ✅ Étape 6 : Machine Learning

**Besoin d'aide pour créer le flux ? Dites-le moi !** 😊
