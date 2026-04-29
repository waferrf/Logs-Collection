# 🎉 Guide Rapide - TechShop E-commerce

## ✅ Site E-commerce Créé !

Votre site **TechShop** est un site e-commerce complet avec :

- 🛒 **20 produits** répartis en 4 catégories
- 📊 **Système de tracking** automatique de tous les événements
- 💳 **Panier fonctionnel** avec checkout complet
- 📈 **Collecte de données** pour analyse

---

## 🚀 Démarrage Rapide

### 1. Le serveur est lancé

Le serveur tourne sur **http://localhost:5000**

Si ce n'est pas le cas, lancez :
```powershell
cd "c:\Users\wafae\OneDrive\Bureau\projet python avancer\etape1-website"
python server.py
```

### 2. Ouvrez le site

Allez sur : **http://localhost:5000**

---

## 🛍️ Guide d'Utilisation

### 📱 Page d'Accueil

1. **Cliquez sur une catégorie** (Smartphones, Ordinateurs, etc.)
2. **Consultez les produits en vedette** (4 meilleurs produits)
3. **Cliquez sur "Acheter maintenant"** pour aller aux produits
4. **Inscrivez-vous à la newsletter** pour 10% de réduction

### 🛒 Page Produits

1. **Utilisez les filtres** :
   - Catégorie : Toutes, Smartphones, Ordinateurs, etc.
   - Prix : Moins de 500€, 500-1000€, etc.
   - Tri : Prix croissant/décroissant, Nom

2. **Cliquez sur un produit** pour voir les détails

3. **Ajoutez au panier** avec le bouton "🛒 Ajouter au panier"

### 🛒 Page Panier

1. **Modifiez les quantités** avec les boutons + et -
2. **Supprimez des articles** avec l'icône 🗑️
3. **Appliquez un code promo** :
   - `WELCOME10` : 10% de réduction
   - `SAVE20` : 20% de réduction
   - `TECHSHOP` : 15% de réduction

4. **Passez commande** :
   - Cliquez sur "Passer la commande"
   - Remplissez vos informations
   - Choisissez le mode de paiement
   - Confirmez

### 📞 Page Contact

1. Envoyez un message
2. Consultez les informations pratiques
3. Lisez la FAQ (cliquez sur les questions)

---

## 🎯 Scénario de Test Complet

Pour générer des données riches :

### 🕐 Session 1 - L'acheteur pressé (2 minutes)
```
1. Accueil
2. Cliquer sur catégorie "Smartphones"
3. Ajouter "iPhone 15 Pro" au panier
4. Aller au panier
5. Valider la commande immédiatement
```

### 🕑 Session 2 - Le comparateur (5 minutes)
```
1. Accueil
2. Visiter toutes les catégories
3. Page Produits → Consulter 5-10 produits
4. Ajouter 3 produits au panier
5. Modifier les quantités
6. Supprimer 1 produit
7. Tester un code promo
8. Finaliser la commande
```

### 🕒 Session 3 - L'indécis (3 minutes)
```
1. Parcourir toutes les pages
2. Ajouter 2 produits au panier
3. Aller au panier
4. Revenir aux produits
5. Ajouter 1 produit supplémentaire
6. Lire la FAQ
7. Quitter sans acheter (abandon de panier)
```

---

## 📊 Vérifier les Données Collectées

### Dans PowerShell :

```powershell
# Compter les événements
Get-ChildItem -Path "logs" -Recurse -Filter *.json | Measure-Object

# Voir les statistiques
Invoke-WebRequest http://localhost:5000/stats | Select-Object -ExpandProperty Content

# Voir les 10 derniers événements
Invoke-WebRequest http://localhost:5000/events?limit=10 | Select-Object -ExpandProperty Content

# Lire un fichier de log
$lastLog = Get-ChildItem -Path "logs" -Recurse -Filter *.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $lastLog.FullName | ConvertFrom-Json | ConvertTo-Json
```

---

## 🎁 Codes Promo Disponibles

| Code | Réduction | Description |
|------|-----------|-------------|
| `WELCOME10` | 10% | Pour les nouveaux clients |
| `SAVE20` | 20% | Promo exceptionnelle |
| `TECHSHOP` | 15% | Code boutique |

---

## 📦 Produits Phares

### 💰 Les best-sellers (prix/qualité)
- OnePlus 12 : 699€ (4.5⭐)
- HP Pavilion : 899€ (4.3⭐)
- iPad Air : 699€ (4.7⭐)

### ⭐ Les mieux notés
- MacBook Pro 16" : 2799€ (4.9⭐)
- Sony WH-1000XM5 : 399€ (4.9⭐)
- iPhone 15 Pro : 1299€ (4.8⭐)

### 🔥 Les plus abordables
- Anker PowerBank : 45€
- Amazon Fire HD : 149€
- SanDisk SSD 1TB : 129€

---

## 📈 Événements Trackés

Chaque action génère un événement :

✅ Visite de page  
✅ Clic sur catégorie  
✅ Vue de produit  
✅ Ajout au panier  
✅ Modification du panier  
✅ Application code promo  
✅ Début de checkout  
✅ Commande confirmée  
✅ Soumission de formulaire  

---

## 🎓 Métriques à Analyser (Étape 2)

Ces données permettront de calculer :

- 📊 **Taux de conversion** : Visiteurs → Acheteurs
- 💰 **Panier moyen** : Montant par commande
- 🏆 **Produits populaires** : Top ventes
- 🛒 **Taux d'abandon** : Paniers non finalisés
- 📱 **Catégories préférées** : Distribution
- 🎁 **Efficacité promos** : Utilisation codes
- 🔄 **Parcours d'achat** : Navigation
- ⏱️ **Temps de conversion** : Visite → Achat

---

## ✨ Fonctionnalités E-commerce

### Gestion du Panier
- ✅ Ajout de produits
- ✅ Modification des quantités
- ✅ Suppression d'articles
- ✅ Persistance (localStorage)
- ✅ Badge compteur en temps réel

### Calculs Automatiques
- ✅ Sous-total
- ✅ TVA (20%)
- ✅ Frais de livraison (gratuit dès 50€)
- ✅ Total final

### Processus de Commande
- ✅ Formulaire complet
- ✅ Validation des champs
- ✅ Choix du paiement
- ✅ Acceptation CGV
- ✅ Confirmation

---

## 🐛 Problèmes Fréquents

### Le panier ne se met pas à jour
➡️ Vérifiez que JavaScript est activé  
➡️ Ouvrez la console (F12) pour voir les erreurs

### Les produits ne s'affichent pas
➡️ Actualisez la page (F5)  
➡️ Vérifiez que tous les fichiers JS sont chargés

### Les événements ne sont pas enregistrés
➡️ Vérifiez que le serveur est bien lancé  
➡️ Consultez la console du navigateur  
➡️ Vérifiez le dossier `logs/`

---

## 🎯 Objectif : Générer des Données

**Minimum recommandé : 50-100 événements**

Pour une analyse riche à l'Étape 2 :
- ✅ 5-10 sessions différentes
- ✅ Plusieurs produits consultés
- ✅ Quelques ajouts au panier
- ✅ 2-3 commandes finalisées
- ✅ 1-2 abandons de panier
- ✅ Utilisation des filtres
- ✅ Tests des codes promo

---

## ➡️ Prochaine Étape

Quand vous avez généré assez de données (50+ événements) :

### 📊 Étape 2 : Dashboard Python Analytics

Nous créerons un dashboard avec :
- 📈 Graphiques de vente
- 🎯 Métriques de conversion
- 🏆 Top produits
- 🛒 Analyse du panier
- 📱 Statistiques par catégorie
- 💰 Revenus et prévisions

---

## 🎉 Checklist de Validation

Avant de passer à l'Étape 2 :

- [ ] Le site fonctionne sur http://localhost:5000
- [ ] Les 4 pages sont accessibles
- [ ] Les 20 produits s'affichent
- [ ] On peut ajouter au panier
- [ ] Le panier se met à jour
- [ ] Le checkout fonctionne
- [ ] Au moins 50 événements générés
- [ ] Les fichiers JSON sont dans `logs/`

---

**✨ Amusez-vous à tester le site et à générer des données ! 🛒**

**Dites-moi quand vous êtes prêt pour l'Étape 2 ! 📊**
