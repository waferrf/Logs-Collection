# 🚀 Guide Rapide - Apache NiFi Pipeline

## ✅ ÉTAPE 4 - Démarrage Rapide

Vous avez déjà NiFi installé ! Voici comment créer le pipeline en **10 minutes**.

---

## 🎯 OPTION 1 : Importer le Template (LE PLUS RAPIDE)

### 1️⃣ Démarrer NiFi
```powershell
# Allez dans votre dossier d'installation NiFi (exemple)
cd C:\nifi\bin
.\run-nifi.bat
```

Attendez 2-5 minutes que NiFi démarre.

### 2️⃣ Accéder à l'interface
Ouvrez votre navigateur :
- **HTTP** : http://localhost:8080/nifi
- **HTTPS** : https://localhost:8443/nifi

### 3️⃣ Importer le template

1. Cliquez sur le bouton **menu** (☰) en haut à droite
2. Sélectionnez **"Upload Template"**
3. Choisissez le fichier : `etape4-nifi\templates\techshop_pipeline.xml`
4. Cliquez **"Upload"**

### 4️⃣ Utiliser le template

1. Glissez l'icône **"Template"** (📄) depuis la barre d'outils vers le canvas
2. Sélectionnez **"TechShop Logs Pipeline"**
3. Cliquez **"Add"**

### 5️⃣ Démarrer le flux

1. Sélectionnez tous les processeurs (Ctrl+A)
2. Clic droit → **"Start"**
3. Surveillez les données qui circulent !

### 6️⃣ Vérifier les résultats

```powershell
# Voir les fichiers créés
Get-ChildItem -Path "etape4-nifi\output" -Recurse
```

✅ **Terminé en 5 minutes !**

---

## 🎯 OPTION 2 : Création Manuelle

Si vous préférez créer le flux vous-même :

### Processeurs à ajouter (dans l'ordre) :

**1. ListFile** → Scanner les logs
- Input Directory: `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website\logs`
- Recurse: `true`
- File Filter: `.*\.json`

**2. FetchFile** → Lire les fichiers
- File to Fetch: `${absolute.path}/${filename}`

**3. EvaluateJsonPath** → Extraire les données
- Ajouter : `event_type = $.event_type`
- Ajouter : `timestamp = $.timestamp`
- Ajouter : `session_id = $.session_id`

**4. AttributesToJSON** → Créer le JSON
- Destination: `flowfile-content`

**5. PutFile** → Sauvegarder
- Directory: `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output`

### Connecter les processeurs :
ListFile → FetchFile → EvaluateJsonPath → AttributesToJSON → PutFile

---

## 📊 Adapter le Dashboard

Une fois NiFi actif, modifiez le dashboard pour lire depuis `output/` :

```powershell
# Ouvrir le fichier
code "etape2-dashboard\analytics.py"
```

**Ligne 17, changer :**
```python
def __init__(self, logs_dir: str = "../etape4-nifi/output"):
```

**Relancer le dashboard :**
```powershell
cd etape2-dashboard
python -m streamlit run dashboard.py
```

---

## ✅ VÉRIFICATION

**NiFi fonctionne si :**
- ✅ Les processeurs sont verts
- ✅ Les chiffres augmentent sur les connexions
- ✅ Des fichiers apparaissent dans `etape4-nifi\output\`

**Dashboard fonctionne si :**
- ✅ Il affiche les statistiques
- ✅ Pas d'erreurs dans la console

---

## 🎉 RÉSULTAT

Vous avez maintenant :
- ✅ Pipeline NiFi automatisé
- ✅ Transformation des logs en temps réel
- ✅ Dashboard qui lit les données NiFi

**L'Étape 4 est complète !** 🚀

---

## ❓ Besoin d'aide ?

**NiFi ne démarre pas ?**
→ Vérifiez Java : `java -version`

**Aucun fichier dans output/ ?**
→ Vérifiez les chemins dans ListFile et PutFile

**Le dashboard ne fonctionne plus ?**
→ Vérifiez que `logs_dir` pointe vers `output/`

**Questions ?** → Demandez-moi ! 😊
