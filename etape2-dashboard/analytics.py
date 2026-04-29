"""
Analytics Engine - Analyse des données de logs
Lit les fichiers JSON et calcule les KPIs
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import numpy as np


class LogAnalyzer:
    """Classe principale pour analyser les logs e-commerce"""
    
    def __init__(self, logs_dir: str = "../etape4-nifi/output"):
        self.logs_dir = Path(logs_dir)
        self.events = []
        self.df = None
        
    def load_all_logs(self) -> pd.DataFrame:
        """Charge tous les fichiers JSON dans un DataFrame"""
        all_events = []
        # Vérifier si on lit depuis output/ (fichiers fusionnés) ou logs/ (fichiers individuels)
        is_nifi_output = "output" in str(self.logs_dir)
        
        if is_nifi_output:
            # Lire fichiers fusionnés de NiFi (plusieurs JSON multi-lignes par fichier)
            import re
            for json_file in self.logs_dir.glob("*"):
                if json_file.is_file():
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:                            content = f.read()
                        # Séparer les objets JSON (séparés par }\n{ ou }{ )
                        # On utilise regex pour trouver chaque objet JSON
                        json_objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
                        for json_str in json_objects:
                            try:
                                event = json.loads(json_str)
                                all_events.append(event)
                            except:
                                pass
                    except Exception as e:
                        print(f" Erreur lecture {json_file}: {e}")
        else:
            # Lire fichiers individuels des logs
            for day_folder in self.logs_dir.iterdir():
                if day_folder.is_dir():
                    for json_file in day_folder.glob("*.json"):
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
                                event = json.load(f)
                                all_events.append(event)
                        except Exception as e:
                            print(f" Erreur lecture {json_file}: {e}")
        
        print(f" {len(all_events)} événements chargés")
        
        # Convertir en DataFrame
        self.df = pd.DataFrame(all_events)
        
        # Convertir les colonnes numériques
        numeric_cols = ['product_id', 'product_price', 'screen_width', 'screen_height', 
                       'viewport_width', 'viewport_height', 'seconds', 'quantity']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Convertir les timestamps en datetime
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')
            self.df['date'] = self.df['timestamp'].dt.date
            self.df['hour'] = self.df['timestamp'].dt.hour
            self.df['day_name'] = self.df['timestamp'].dt.day_name()
        
        if 'server_received_at' in self.df.columns:
            self.df['server_received_at'] = pd.to_datetime(self.df['server_received_at'])
        
        return self.df
    
    def get_total_events(self) -> int:
        """Nombre total d'événements"""
        return len(self.df) if self.df is not None else 0
    
    def get_events_by_type(self) -> pd.Series:
        """Événements groupés par type"""
        if self.df is None or 'event_type' not in self.df.columns:
            return pd.Series()
        return self.df['event_type'].value_counts()
    
    def get_unique_sessions(self) -> int:
        """Nombre de sessions uniques"""
        if self.df is None or 'session_id' not in self.df.columns:
            return 0
        return self.df['session_id'].nunique()
    
    def get_page_views(self) -> pd.DataFrame:
        """Pages les plus vues"""
        if self.df is None:
            return pd.DataFrame()
        
        page_views = self.df[self.df['event_type'] == 'page_view']
        if page_views.empty:
            return pd.DataFrame()
        
        return page_views['page_url'].value_counts().reset_index()
    
    def get_average_time_on_page(self) -> pd.DataFrame:
        """Temps moyen par page"""
        if self.df is None:
            return pd.DataFrame()
        
        time_events = self.df[self.df['event_type'] == 'time_on_page'].copy()
        if time_events.empty or 'seconds' not in time_events.columns:
            return pd.DataFrame()
        
        avg_time = time_events.groupby('page_url')['seconds'].mean().reset_index()
        avg_time.columns = ['page_url', 'avg_seconds']
        avg_time['avg_minutes'] = avg_time['avg_seconds'] / 60
        return avg_time.sort_values('avg_seconds', ascending=False)
    
    def get_ecommerce_metrics(self) -> Dict[str, Any]:
        """Métriques e-commerce"""
        if self.df is None:
            return {}
        
        metrics = {}
        
        # Produits ajoutés au panier
        add_to_cart = self.df[self.df['event_type'] == 'custom_add_to_cart']
        metrics['total_add_to_cart'] = len(add_to_cart)
        
        # Produits retirés du panier
        remove_from_cart = self.df[self.df['event_type'] == 'custom_remove_from_cart']
        metrics['total_remove_from_cart'] = len(remove_from_cart)
        
        # Commandes commencées
        checkout_started = self.df[self.df['event_type'] == 'custom_checkout_started']
        metrics['total_checkout_started'] = len(checkout_started)
        
        # Commandes complétées
        orders = self.df[self.df['event_type'] == 'custom_order_completed']
        metrics['total_orders'] = len(orders)
        
        # Revenu total
        if not orders.empty and 'total_amount' in orders.columns:
            metrics['total_revenue'] = orders['total_amount'].sum()
            metrics['average_order_value'] = orders['total_amount'].mean()
        else:
            metrics['total_revenue'] = 0
            metrics['average_order_value'] = 0
        
        # Taux de conversion (visites → commandes)
        total_sessions = self.get_unique_sessions()
        if total_sessions > 0:
            metrics['conversion_rate'] = (metrics['total_orders'] / total_sessions) * 100
        else:
            metrics['conversion_rate'] = 0
        
        # Taux d'abandon de panier
        if metrics['total_checkout_started'] > 0:
            metrics['cart_abandonment_rate'] = (
                (metrics['total_checkout_started'] - metrics['total_orders']) / 
                metrics['total_checkout_started']
            ) * 100
        else:
            metrics['cart_abandonment_rate'] = 0
        
        return metrics
    
    def get_top_products_added(self, limit: int = 10) -> pd.DataFrame:
        """Top produits ajoutés au panier"""
        if self.df is None:
            return pd.DataFrame()
        
        add_to_cart = self.df[self.df['event_type'] == 'custom_add_to_cart'].copy()
        if add_to_cart.empty or 'product_name' not in add_to_cart.columns:
            return pd.DataFrame()
        
        top_products = add_to_cart.groupby('product_name').agg({
            'product_id': 'count',
            'product_price': 'first'
        }).reset_index()
        top_products.columns = ['product_name', 'add_count', 'price']
        
        return top_products.sort_values('add_count', ascending=False).head(limit)
    
    def get_top_products_purchased(self, limit: int = 10) -> pd.DataFrame:
        """Top produits achetés"""
        if self.df is None:
            return pd.DataFrame()
        
        orders = self.df[self.df['event_type'] == 'custom_order_completed'].copy()
        if orders.empty:
            return pd.DataFrame(columns=['product_name', 'purchase_count', 'revenue'])
        
        # Extraire les produits des commandes
        products_list = []
        for _, order in orders.iterrows():
            if 'products' in order and isinstance(order['products'], list):
                for product in order['products']:
                    products_list.append({
                        'product_name': product.get('name'),
                        'quantity': product.get('quantity', 1),
                        'price': product.get('price', 0)
                    })
        
        if not products_list:
            return pd.DataFrame(columns=['product_name', 'purchase_count', 'revenue'])
        
        products_df = pd.DataFrame(products_list)
        top_purchased = products_df.groupby('product_name').agg({
            'quantity': 'sum',
            'price': lambda x: (x * products_df.loc[x.index, 'quantity']).sum()
        }).reset_index()
        top_purchased.columns = ['product_name', 'purchase_count', 'revenue']
        
        return top_purchased.sort_values('purchase_count', ascending=False).head(limit)
    
    def get_events_over_time(self, freq: str = 'H') -> pd.DataFrame:
        """Événements au fil du temps"""
        if self.df is None or 'timestamp' not in self.df.columns:
            return pd.DataFrame()
        
        time_series = self.df.set_index('timestamp').resample(freq).size()
        return time_series.reset_index(name='event_count')
    
    def get_events_by_hour(self) -> pd.DataFrame:
        """Événements par heure de la journée"""
        if self.df is None or 'hour' not in self.df.columns:
            return pd.DataFrame()
        
        return self.df['hour'].value_counts().sort_index().reset_index()
    
    def get_user_journey(self, session_id: str) -> pd.DataFrame:
        """Parcours utilisateur pour une session"""
        if self.df is None or 'session_id' not in self.df.columns:
            return pd.DataFrame()
        
        journey = self.df[self.df['session_id'] == session_id].copy()
        journey = journey.sort_values('timestamp')
        
        return journey[['timestamp', 'event_type', 'page_url', 'page_title']]
    
    def get_conversion_funnel(self) -> Dict[str, int]:
        """Entonnoir de conversion"""
        if self.df is None:
            return {}
        
        funnel = {}
        funnel['1_visits'] = self.get_unique_sessions()
        funnel['2_product_views'] = len(self.df[self.df['event_type'] == 'custom_product_viewed'])
        funnel['3_add_to_cart'] = len(self.df[self.df['event_type'] == 'custom_add_to_cart'])
        funnel['4_checkout_started'] = len(self.df[self.df['event_type'] == 'custom_checkout_started'])
        funnel['5_orders'] = len(self.df[self.df['event_type'] == 'custom_order_completed'])
        
        return funnel
    
    def get_device_stats(self) -> pd.DataFrame:
        """Statistiques par appareil"""
        if self.df is None or 'user_agent' not in self.df.columns:
            return pd.DataFrame()
        
        # Simplifier l'user agent pour détecter le type d'appareil
        def get_device_type(user_agent):
            if pd.isna(user_agent):
                return 'Unknown'
            ua = str(user_agent).lower()
            if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
                return 'Mobile'
            elif 'tablet' in ua or 'ipad' in ua:
                return 'Tablet'
            else:
                return 'Desktop'
        
        self.df['device_type'] = self.df['user_agent'].apply(get_device_type)
        
        return self.df['device_type'].value_counts().reset_index()
    
    def get_promo_code_usage(self) -> pd.DataFrame:
        """Utilisation des codes promo"""
        if self.df is None:
            return pd.DataFrame()
        
        orders = self.df[self.df['event_type'] == 'custom_order_completed'].copy()
        if orders.empty or 'promo_code' not in orders.columns:
            return pd.DataFrame(columns=['promo_code', 'usage_count', 'total_revenue'])
        
        # Filtrer les commandes avec code promo
        orders_with_promo = orders[orders['promo_code'].notna()].copy()
        
        if orders_with_promo.empty:
            return pd.DataFrame(columns=['promo_code', 'usage_count', 'total_revenue'])
        
        promo_stats = orders_with_promo.groupby('promo_code').agg({
            'order_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        promo_stats.columns = ['promo_code', 'usage_count', 'total_revenue']
        
        return promo_stats.sort_values('usage_count', ascending=False)

    def get_bounce_rate(self) -> float:
        """Taux de rebond : % de sessions avec 1 seule page visitée"""
        if self.df is None or 'session_id' not in self.df.columns:
            return 0.0
        pages_per_session = self.df[self.df['event_type'] == 'page_view'].groupby('session_id')['page_url'].nunique()
        if len(pages_per_session) == 0:
            return 0.0
        bounce_sessions = (pages_per_session == 1).sum()
        return (bounce_sessions / len(pages_per_session)) * 100

    def get_avg_session_duration(self) -> float:
        """Durée moyenne de session en secondes"""
        if self.df is None or 'session_id' not in self.df.columns or 'timestamp' not in self.df.columns:
            return 0.0
        session_duration = self.df.groupby('session_id')['timestamp'].agg(
            lambda x: (x.max() - x.min()).total_seconds()
        )
        return session_duration.mean() if len(session_duration) > 0 else 0.0

    def get_click_heatmap_data(self) -> pd.DataFrame:
        """Données pour la heatmap : nombre de clics par jour de semaine et par heure"""
        if self.df is None or 'hour' not in self.df.columns or 'day_name' not in self.df.columns:
            return pd.DataFrame()
        clicks = self.df[self.df['event_type'] == 'click']
        if clicks.empty:
            return pd.DataFrame()
        heatmap = clicks.groupby(['day_name', 'hour']).size().reset_index(name='count')
        heatmap_pivot = heatmap.pivot(index='day_name', columns='hour', values='count').fillna(0)
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_present = [d for d in days_order if d in heatmap_pivot.index]
        return heatmap_pivot.reindex(days_present)


if __name__ == "__main__":
    # Test de l'analyseur
    analyzer = LogAnalyzer()
    df = analyzer.load_all_logs()
    
    print("\n Résumé des données:")
    print(f"Total événements: {analyzer.get_total_events()}")
    print(f"Sessions uniques: {analyzer.get_unique_sessions()}")
    print(f"\nÉvénements par type:")
    print(analyzer.get_events_by_type().head(10))
    
    print("\n🛍 Métriques e-commerce:")
    metrics = analyzer.get_ecommerce_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
