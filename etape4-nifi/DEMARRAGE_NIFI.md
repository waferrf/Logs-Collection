# 🚀 GUIDE : Démarrage et Utilisation d'Apache NiFi

## ✅ NiFi EST EN COURS DE DÉMARRAGE

Une fenêtre noire (console) s'est ouverte - **NE LA FERMEZ PAS !**  
C'est NiFi qui démarre. Cela prend **2-5 minutes**.

---

## 📋 ÉTAPES À SUIVRE (Pendant que NiFi démarre)

### **ÉTAPE 1 : Attendre le démarrage (2-5 minutes)**

Vous saurez que NiFi est prêt quand vous verrez dans la console :
```
NiFi has started. The UI is available at the following URLs:
```

⏱️ **En attendant, lisez les étapes suivantes...**

---

### **ÉTAPE 2 : Trouver vos identifiants de connexion**

**NiFi 2.x génère automatiquement un utilisateur et un mot de passe.**

#### Option A : Chercher dans les logs

**Ouvrez PowerShell et exécutez :**
```powershell
Get-Content "C:\nifi-2.7.2\logs\nifi-app.log" | Select-String -Pattern "Generated Username|Generated Password"
```

**Vous verrez quelque chose comme :**
```
Generated Username [abc12345-...]
Generated Password [random-password-here]
```

**📋 COPIEZ ces identifiants !**

#### Option B : Chercher dans le fichier conf (si Single User)

```powershell
Get-Content "C:\nifi-2.7.2\conf\login-identity-providers.xml"
```

---

### **ÉTAPE 3 : Accéder à l'interface NiFi**

Une fois NiFi démarré (2-5 min), ouvrez votre navigateur :

**URL principale (essayez dans cet ordre) :**

1. **HTTPS** : https://localhost:8443/nifi
2. **HTTP** : http://localhost:8080/nifi

**Si erreur de certificat SSL :**
- Cliquez "Avancé" → "Continuer vers localhost (dangereux)" → C'est normal pour localhost

---

### **ÉTAPE 4 : Se connecter**

1. Entrez le **Username** trouvé dans les logs
2. Entrez le **Password** trouvé dans les logs
3. Cliquez **"Log In"**

**✅ Vous êtes dans NiFi !**

---

## 🎨 ÉTAPE 5 : Créer votre premier pipeline (Option rapide)

### **Méthode 1 : Importer le Template (RECOMMANDÉ)** ⭐

**1. Upload du template**
- Cliquez sur le menu **☰** en haut à droite
- Sélectionnez **"Upload Template"**
- Parcourir → Choisissez :
  ```
  C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\templates\techshop_pipeline.xml
  ```
- Cliquez **"Upload"**

**2. Ajouter le template au canvas**
- Dans la barre d'outils en haut, glissez l'icône **"Template"** (📄) sur le canvas blanc
- Dans la liste, sélectionnez **"TechShop Logs Pipeline"**
- Cliquez **"Add"**

**3. Configurer les chemins (Important !)**

Le template utilise des chemins absolus. Vous devez les vérifier :

**Pour chaque processeur :**
- **Double-clic** sur le processeur "1-ListFile"
- Onglet **"Properties"**
- Vérifiez **"Input Directory"** :
  ```
  C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website\logs
  ```
- Cliquez **"Apply"**

- **Double-clic** sur le processeur "5-PutFile"
- Vérifiez **"Directory"** :
  ```
  C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output
  ```
- Cliquez **"Apply"**

**4. Démarrer le pipeline**
- Faites un clic droit sur le fond (sélectionnez tout) → **Ctrl+A**
- Clic droit → **"Start"**
- Les processeurs deviennent **verts** ✅

**5. Surveiller l'exécution**
- Les chiffres sur les connections doivent augmenter
- Regardez en haut à droite les stats globales

---

### **Méthode 2 : Création Manuelle (Si template ne fonctionne pas)**

**1. Glisser un processeur "Processor"** depuis la barre d'outils

**2. Chercher et ajouter ces processeurs (dans l'ordre) :**

#### Processeur 1 : **ListFile**
- **Glisser** "Processor" sur le canvas
- **Chercher** : "ListFile"
- **Double-clic** sur le processeur → Onglet **Properties**
- Configurer :
  - **Input Directory** : `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website\logs`
  - **Recurse Subdirectories** : `true`
  - **File Filter** : `.*\.json`
  - **Minimum File Age** : `0 sec`
- Onglet **Scheduling** :
  - **Run Schedule** : `30 sec`
- **Apply**

#### Processeur 2 : **FetchFile**
- Ajouter un nouveau processeur "FetchFile"
- **Properties** :
  - **File to Fetch** : `${absolute.path}/${filename}`
  - **Completion Strategy** : `None`
- **Apply**

**Connecter ListFile → FetchFile :**
- Survolez ListFile, une flèche apparaît
- Glissez la flèche vers FetchFile
- Cochez **"success"**
- **Add**

#### Processeur 3 : **EvaluateJsonPath**
- Ajouter "EvaluateJsonPath"
- **Properties** :
  - **Destination** : `flowfile-attribute`
  - **Return Type** : `json`
  
**Ajouter des propriétés personnalisées (clic sur + en haut à droite) :**
  - Propriété `event_type` = Valeur `$.event_type`
  - Propriété `timestamp` = Valeur `$.timestamp`
  - Propriété `session_id` = Valeur `$.session_id`
  - Propriété `page_url` = Valeur `$.page_url`
- **Apply**

**Connecter FetchFile → EvaluateJsonPath (relation "success")**

#### Processeur 4 : **AttributesToJSON**
- Ajouter "AttributesToJSON"
- **Properties** :
  - **Destination** : `flowfile-content`
  - **Include Core Attributes** : `false`
- **Apply**

**Connecter EvaluateJsonPath → AttributesToJSON (relation "matched")**

#### Processeur 5 : **PutFile**
- Ajouter "PutFile"
- **Properties** :
  - **Directory** : `C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output`
  - **Conflict Resolution Strategy** : `replace`
  - **Create Missing Directories** : `true`
- **Apply**

**Connecter AttributesToJSON → PutFile (relation "success")**

**3. Auto-terminer les relations inutilisées**

Pour chaque processeur, clic droit → **Configure** → Onglet **Settings** :
- Cochez les relations non connectées dans "Automatically Terminate Relationships"

**4. Démarrer tous les processeurs**
- Sélectionner tout (Ctrl+A)
- Clic droit → **"Start"**

---

## 📊 ÉTAPE 6 : Vérifier que ça fonctionne

### **Dans NiFi :**
- Les processeurs doivent être **verts**
- Les chiffres sur les connections augmentent
- Aucun triangle jaune ou rouge

### **Dans PowerShell :**
```powershell
# Vérifier que des fichiers sont créés
Get-ChildItem -Path "C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output" -Recurse
```

**Vous devriez voir des fichiers JSON !** ✅

---

## 📈 ÉTAPE 7 : Adapter le Dashboard pour lire depuis NiFi

**Ouvrez le fichier :**
```powershell
code "C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape2-dashboard\analytics.py"
```

**Trouvez la ligne 17 et modifiez :**
```python
def __init__(self, logs_dir: str = "../etape4-nifi/output"):
```

**Sauvegardez et relancez le dashboard :**
```powershell
cd "C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape2-dashboard"
python -m streamlit run dashboard.py
```

**Le dashboard lit maintenant les données traitées par NiFi !** 🎉

---

## 🔧 ARRÊTER NIFI

**Pour arrêter NiFi proprement :**
```powershell
cd C:\nifi-2.7.2\bin
.\nifi.cmd stop
```

**Ou fermez simplement la fenêtre console (moins propre)**

---

## 🐛 DÉPANNAGE

### **Problème : Je ne trouve pas mes identifiants**

**Solution 1 : Chercher dans les logs**
```powershell
Get-Content "C:\nifi-2.7.2\logs\nifi-app.log" -Tail 500 | Select-String -Pattern "Username|Password"
```

**Solution 2 : Réinitialiser le mot de passe**
```powershell
cd C:\nifi-2.7.2\bin
.\nifi.cmd set-single-user-credentials USERNAME PASSWORD
```

### **Problème : Port déjà utilisé**

Si le port 8443 est occupé, vérifiez dans :
```powershell
notepad "C:\nifi-2.7.2\conf\nifi.properties"
```
Cherchez : `nifi.web.https.port=8443`

### **Problème : Le template ne s'importe pas**

Créez le flux manuellement (Méthode 2 ci-dessus)

### **Problème : Aucun fichier dans output/**

1. Vérifiez que les chemins dans ListFile et PutFile sont corrects
2. Vérifiez que des fichiers JSON existent dans `logs/`
3. Regardez les erreurs dans les processeurs (triangles rouges)

---

## ✅ RÉSUMÉ DES COMMANDES UTILES

```powershell
# Démarrer NiFi
cd C:\nifi-2.7.2\bin
.\nifi.cmd run

# Arrêter NiFi
.\nifi.cmd stop

# Voir les logs
Get-Content "C:\nifi-2.7.2\logs\nifi-app.log" -Tail 50

# Vérifier les fichiers de sortie
Get-ChildItem "C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape4-nifi\output" -Recurse

# Relancer le dashboard
cd "C:\Users\wafae\OneDrive\Bureau\projet python avancer\etape2-dashboard"
python -m streamlit run dashboard.py
```

---

## 🎉 FÉLICITATIONS !

Une fois tout configuré, vous aurez :
- ✅ NiFi qui traite automatiquement vos logs
- ✅ Pipeline visuel et professionnel
- ✅ Données agrégées dans `output/`
- ✅ Dashboard qui affiche les résultats NiFi

**L'Étape 4 sera complète !** 🚀

---

**Besoin d'aide ? Dites-moi où vous êtes bloqué !** 😊
