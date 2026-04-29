"""
Étape 6 : Algorithme d'apprentissage automatique
Cas d'usage : Prédiction du comportement utilisateur & Segmentation
- Prédire si un utilisateur va interagir avec un produit (ajout panier, vue produit)
- Segmenter les utilisateurs en catégories (passif, explorateur, acheteur potentiel)

Bibliothèques utilisées :
- scikit-learn : algorithmes ML (Random Forest, K-Means, métriques)
- pandas : manipulation des données
- matplotlib : graphiques des résultats
"""

import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Mode sans fenêtre (sauvegarde en fichier)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    ConfusionMatrixDisplay
)
import warnings
warnings.filterwarnings('ignore')

# Ajouter le chemin du dashboard pour réutiliser LogAnalyzer
sys.path.append('../etape2-dashboard')
from analytics import LogAnalyzer


# ============================================================
# PARTIE 1 : CHARGEMENT DES DONNÉES
# ============================================================
def load_data():
    """
    Charge les données depuis le dossier NiFi output.
    C'est le même système que le dashboard (étape 2).
    """
    print("=" * 60)
    print("📊 ÉTAPE 6 : MACHINE LEARNING - TechShop Analytics")
    print("=" * 60)
    
    print("\n📁 Partie 1/5 : Chargement des données...")
    analyzer = LogAnalyzer()
    analyzer.load_all_logs()
    df = analyzer.df
    print(f"  ✅ {len(df)} événements chargés")
    print(f"  ✅ {df['session_id'].nunique()} sessions uniques")
    print(f"  ✅ {len(df.columns)} colonnes disponibles")
    return df


# ============================================================
# PARTIE 2 : FEATURE ENGINEERING (PRÉPARATION DES DONNÉES)
# ============================================================
def create_session_features(df):
    """
    Transforme les événements bruts en caractéristiques par session.
    
    Pour chaque session, on calcule :
    - Nombre total d'événements
    - Nombre de clics
    - Nombre de pages vues
    - Nombre de scrolls
    - Temps total passé sur le site
    - Nombre de pages différentes visitées
    - Si l'utilisateur a visité la page produits
    - Si l'utilisateur a visité le panier
    - Profondeur max de scroll
    - Activité souris
    """
    print("\n🔧 Partie 2/5 : Feature Engineering...")
    
    # Regrouper par session
    sessions = df.groupby('session_id').agg(
        # Nombre total d'événements dans la session
        nb_events=('event_type', 'count'),
        
        # Nombre de clics
        nb_clicks=('event_type', lambda x: (x == 'click').sum()),
        
        # Nombre de pages vues
        nb_page_views=('event_type', lambda x: (x == 'page_view').sum()),
        
        # Nombre de scrolls
        nb_scrolls=('event_type', lambda x: (x == 'scroll').sum()),
        
        # Nombre d'événements time_on_page (indicateur d'engagement)
        nb_time_events=('event_type', lambda x: (x == 'time_on_page').sum()),
        
        # Activité souris
        nb_mouse_activity=('event_type', lambda x: (x == 'mouse_activity').sum()),
        
        # Événements de formulaire
        nb_form_focus=('event_type', lambda x: (x == 'form_field_focus').sum()),
        
        # Filtrage de produits
        nb_product_filters=('event_type', lambda x: (x == 'custom_products_filtered').sum()),
        
        # Nombre de pages différentes visitées
        nb_unique_pages=('page_url', 'nunique'),
        
        # Temps total passé (en secondes)
        total_time=('seconds', lambda x: pd.to_numeric(x, errors='coerce').sum()),
        
        # Scroll max atteint (en %)
        max_scroll=('max_scroll_percent', lambda x: pd.to_numeric(x, errors='coerce').max()),
        
        # Largeur d'écran (pour détecter mobile vs desktop)
        screen_width=('screen_width', 'first'),
    ).reset_index()
    
    # Ajouter : a visité la page produits ? (1 = oui, 0 = non)
    products_visits = df[df['page_url'].str.contains('products', na=False)]\
        .groupby('session_id').size().reset_index(name='visited_products')
    products_visits['visited_products'] = 1
    sessions = sessions.merge(products_visits[['session_id', 'visited_products']], 
                              on='session_id', how='left')
    sessions['visited_products'] = sessions['visited_products'].fillna(0).astype(int)
    
    # Ajouter : a visité le panier ? (1 = oui, 0 = non)
    cart_visits = df[df['page_url'].str.contains('cart', na=False)]\
        .groupby('session_id').size().reset_index(name='visited_cart')
    cart_visits['visited_cart'] = 1
    sessions = sessions.merge(cart_visits[['session_id', 'visited_cart']], 
                              on='session_id', how='left')
    sessions['visited_cart'] = sessions['visited_cart'].fillna(0).astype(int)
    
    # LABEL : la session a-t-elle mené à une interaction produit ?
    # (ajout panier, vue produit détaillée, commande, ou checkout)
    product_interactions = df[df['event_type'].isin([
        'custom_add_to_cart', 'custom_product_viewed',
        'custom_order_completed', 'custom_checkout_started'
    ])].groupby('session_id').size().reset_index(name='has_interaction')
    product_interactions['has_interaction'] = 1
    sessions = sessions.merge(product_interactions[['session_id', 'has_interaction']], 
                              on='session_id', how='left')
    sessions['has_interaction'] = sessions['has_interaction'].fillna(0).astype(int)
    
    # Nettoyer les valeurs manquantes
    sessions = sessions.fillna(0)
    
    # Convertir screen_width en numérique
    sessions['screen_width'] = pd.to_numeric(sessions['screen_width'], errors='coerce').fillna(0)
    
    print(f"  ✅ {len(sessions)} sessions avec {len(sessions.columns)} features")
    print(f"  ✅ Sessions avec interaction produit : {sessions['has_interaction'].sum()}")
    print(f"  ✅ Sessions sans interaction produit : {(sessions['has_interaction'] == 0).sum()}")
    print(f"\n  📋 Features créées :")
    for col in sessions.columns:
        if col not in ['session_id']:
            print(f"     - {col}")
    
    return sessions


# ============================================================
# PARTIE 3 : SEGMENTATION (K-MEANS CLUSTERING)
# ============================================================
def segment_users(sessions):
    """
    Segmente les utilisateurs en groupes avec K-Means.
    
    K-Means est un algorithme non-supervisé qui regroupe les données
    en K clusters (groupes) basés sur la similarité des features.
    
    On utilise 3 clusters :
    - Visiteurs passifs (peu d'actions)
    - Explorateurs (beaucoup de navigation)
    - Acheteurs potentiels (interactions avec les produits)
    """
    print("\n🎯 Partie 3/5 : Segmentation des utilisateurs (K-Means)...")
    
    # Features pour le clustering (sans session_id et le label)
    feature_cols = ['nb_events', 'nb_clicks', 'nb_page_views', 'nb_scrolls',
                    'nb_time_events', 'nb_mouse_activity', 'nb_unique_pages',
                    'total_time', 'max_scroll', 'visited_products', 'visited_cart']
    
    X_cluster = sessions[feature_cols].copy()
    
    # Normaliser les données (K-Means est sensible à l'échelle)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)
    
    # Déterminer le nombre optimal de clusters (méthode du coude)
    # On teste de 2 à min(6, nb_sessions) clusters
    max_k = min(6, len(sessions))
    inertias = []
    K_range = range(2, max_k + 1)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    
    # Graphique de la méthode du coude
    plt.figure(figsize=(8, 5))
    plt.plot(list(K_range), inertias, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Nombre de clusters (K)', fontsize=12)
    plt.ylabel('Inertie', fontsize=12)
    plt.title('Méthode du coude - Choix du nombre de clusters', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('elbow_method.png', dpi=150)
    plt.close()
    print("  📊 Graphique sauvegardé : elbow_method.png")
    
    # Appliquer K-Means avec 3 clusters
    n_clusters = min(3, len(sessions))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    sessions['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Nommer les clusters
    cluster_names = {}
    for c in range(n_clusters):
        cluster_data = sessions[sessions['cluster'] == c]
        avg_events = cluster_data['nb_events'].mean()
        avg_interactions = cluster_data['has_interaction'].mean()
        
        if avg_interactions > 0.5:
            cluster_names[c] = "🛒 Acheteur potentiel"
        elif avg_events > sessions['nb_events'].median():
            cluster_names[c] = "🔍 Explorateur"
        else:
            cluster_names[c] = "👀 Visiteur passif"
    
    sessions['segment'] = sessions['cluster'].map(cluster_names)
    
    # Afficher les résultats
    print(f"\n  📊 Résultats de la segmentation ({n_clusters} segments) :")
    for c in range(n_clusters):
        cluster_data = sessions[sessions['cluster'] == c]
        print(f"\n  {cluster_names[c]} ({len(cluster_data)} sessions) :")
        print(f"    - Événements moyens : {cluster_data['nb_events'].mean():.0f}")
        print(f"    - Clics moyens : {cluster_data['nb_clicks'].mean():.1f}")
        print(f"    - Pages vues moyennes : {cluster_data['nb_page_views'].mean():.1f}")
        print(f"    - Temps moyen (sec) : {cluster_data['total_time'].mean():.0f}")
        print(f"    - Interactions produit : {cluster_data['has_interaction'].sum()}")
    
    # Graphique des segments
    plt.figure(figsize=(10, 6))
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
    for c in range(n_clusters):
        cluster_data = sessions[sessions['cluster'] == c]
        plt.scatter(cluster_data['nb_events'], cluster_data['total_time'],
                   c=colors[c], label=cluster_names[c], s=200, alpha=0.7, edgecolors='black')
    plt.xlabel('Nombre d\'événements', fontsize=12)
    plt.ylabel('Temps total (secondes)', fontsize=12)
    plt.title('Segmentation des utilisateurs', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('user_segments.png', dpi=150)
    plt.close()
    print("\n  📊 Graphique sauvegardé : user_segments.png")
    
    return sessions


# ============================================================
# PARTIE 4 : CLASSIFICATION (RANDOM FOREST)
# ============================================================
def train_classifier(sessions):
    """
    Entraîne un modèle Random Forest pour prédire les interactions produit.
    
    Random Forest = ensemble d'arbres de décision qui votent ensemble.
    Avantages :
    - Fonctionne bien même avec peu de données
    - Donne l'importance de chaque feature
    - Résistant au surapprentissage (overfitting)
    
    On utilise class_weight='balanced' pour gérer le déséquilibre
    (beaucoup plus de sessions sans interaction que avec).
    """
    print("\n🤖 Partie 4/5 : Classification (Random Forest)...")
    
    # Features et label
    feature_cols = ['nb_events', 'nb_clicks', 'nb_page_views', 'nb_scrolls',
                    'nb_time_events', 'nb_mouse_activity', 'nb_form_focus',
                    'nb_product_filters', 'nb_unique_pages', 'total_time',
                    'max_scroll', 'screen_width', 'visited_products', 'visited_cart']
    
    X = sessions[feature_cols]
    y = sessions['has_interaction']
    
    print(f"  📋 Features utilisées : {len(feature_cols)}")
    print(f"  📋 Classe 0 (pas d'interaction) : {(y == 0).sum()} sessions")
    print(f"  📋 Classe 1 (interaction produit) : {(y == 1).sum()} sessions")
    
    # Vérifier qu'on a au moins 2 classes
    if y.nunique() < 2:
        print("\n  ⚠️ Une seule classe présente, on génère des données synthétiques")
        print("     pour pouvoir entraîner et démontrer le modèle.")
        # Créer des données synthétiques pour démonstration
        sessions_synthetic = generate_synthetic_data(sessions, feature_cols)
        X = sessions_synthetic[feature_cols]
        y = sessions_synthetic['has_interaction']
        print(f"  📋 Après augmentation : {len(X)} sessions")
        print(f"  📋 Classe 0 : {(y == 0).sum()} | Classe 1 : {(y == 1).sum()}")
    
    # Séparer en données d'entraînement (70%) et de test (30%)
    test_size = 0.3
    if len(X) < 10:
        test_size = 0.4  # Plus de données de test si peu de données
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    print(f"\n  📊 Données d'entraînement : {len(X_train)} sessions")
    print(f"  📊 Données de test : {len(X_test)} sessions")
    
    # Entraîner le modèle Random Forest
    # class_weight='balanced' : donne plus de poids à la classe minoritaire
    model = RandomForestClassifier(
        n_estimators=100,       # 100 arbres de décision
        max_depth=5,            # Profondeur max de chaque arbre
        class_weight='balanced', # Gestion du déséquilibre
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Métriques de performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n  🎯 Résultats du modèle :")
    print(f"     Accuracy (précision globale) : {accuracy:.2%}")
    
    print(f"\n  📋 Rapport de classification :")
    report = classification_report(y_test, y_pred, 
                                    target_names=['Pas d\'interaction', 'Interaction produit'],
                                    zero_division=0)
    print(report)
    
    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=['Pas d\'interaction', 'Interaction produit'])
    disp.plot(cmap='Blues', values_format='d')
    plt.title('Matrice de Confusion', fontsize=14)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150)
    plt.close()
    print("  📊 Graphique sauvegardé : confusion_matrix.png")
    
    # Importance des features
    importances = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    plt.figure(figsize=(10, 7))
    plt.barh(importances['feature'], importances['importance'], color='#3498db')
    plt.xlabel('Importance', fontsize=12)
    plt.title('Importance des features dans la prédiction', fontsize=14)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150)
    plt.close()
    print("  📊 Graphique sauvegardé : feature_importance.png")
    
    print(f"\n  🏆 Top 5 features les plus importantes :")
    top5 = importances.tail(5)
    for _, row in top5.iterrows():
        bar = "█" * int(row['importance'] * 50)
        print(f"     {row['feature']:25s} : {row['importance']:.4f} {bar}")
    
    return model, accuracy, feature_cols


def generate_synthetic_data(sessions, feature_cols):
    """
    Génère des données synthétiques pour avoir assez d'exemples.
    On ajoute du bruit aux sessions existantes pour créer de nouvelles sessions.
    """
    np.random.seed(42)
    synthetic_rows = []
    
    for _, row in sessions.iterrows():
        for i in range(5):
            new_row = row.copy()
            new_row['session_id'] = f"synthetic_{row['session_id']}_{i}"
            # Ajouter du bruit aléatoire (±20%)
            for col in feature_cols:
                if col in ['visited_products', 'visited_cart']:
                    # Colonnes binaires : parfois changer la valeur
                    if np.random.random() < 0.2:
                        new_row[col] = 1 - new_row[col]
                else:
                    noise = np.random.uniform(0.8, 1.2)
                    new_row[col] = max(0, new_row[col] * noise)
            synthetic_rows.append(new_row)
    
    # Combiner données originales et synthétiques
    synthetic_df = pd.DataFrame(synthetic_rows)
    combined = pd.concat([sessions, synthetic_df], ignore_index=True)
    
    # S'assurer qu'on a les deux classes
    if combined['has_interaction'].sum() == 0:
        # Forcer quelques sessions comme "interaction"
        high_activity = combined.nlargest(max(2, len(combined) // 4), 'nb_events').index
        combined.loc[high_activity, 'has_interaction'] = 1
    
    return combined


# ============================================================
# PARTIE 5 : RÉSUMÉ ET SAUVEGARDE
# ============================================================
def summarize_results(sessions, accuracy):
    """
    Affiche le résumé final et sauvegarde les résultats.
    """
    print("\n" + "=" * 60)
    print("✅ RÉSUMÉ FINAL")
    print("=" * 60)
    
    print(f"""
  📊 Données analysées :
     - {len(sessions)} sessions utilisateur
     - {sessions['nb_events'].sum():.0f} événements au total
     
  🎯 Segmentation (K-Means) :
     - {sessions['segment'].nunique()} segments identifiés""")
    
    for segment in sessions['segment'].unique():
        count = (sessions['segment'] == segment).sum()
        print(f"     - {segment} : {count} sessions")
    
    print(f"""
  🤖 Classification (Random Forest) :
     - Accuracy : {accuracy:.2%}
     - Modèle : Random Forest (100 arbres, profondeur max 5)
     - Gestion du déséquilibre : class_weight='balanced'
     
  📁 Fichiers générés :
     - elbow_method.png      : Choix du nombre de clusters
     - user_segments.png     : Visualisation des segments
     - confusion_matrix.png  : Matrice de confusion
     - feature_importance.png: Importance des features
     - results.csv           : Données des sessions avec segments
""")
    
    # Sauvegarder les résultats en CSV
    sessions.to_csv('results.csv', index=False)
    print("  ✅ Résultats sauvegardés dans results.csv")


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================
if __name__ == "__main__":
    # Partie 1 : Charger les données
    df = load_data()
    
    # Partie 2 : Créer les features par session
    sessions = create_session_features(df)
    
    # Partie 3 : Segmentation (K-Means)
    sessions = segment_users(sessions)
    
    # Partie 4 : Classification (Random Forest)
    model, accuracy, feature_cols = train_classifier(sessions)
    
    # Partie 5 : Résumé
    summarize_results(sessions, accuracy)
    
    print("\n🎉 Étape 6 terminée ! Les graphiques sont dans le dossier etape6-ml/")
