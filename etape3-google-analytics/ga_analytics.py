"""
Google Analytics Data Reader
Lit les données exportées en CSV depuis Google Analytics
et les prépare pour le dashboard
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json


class GAAnalytics:
    """Classe pour lire et analyser les données Google Analytics exportées en CSV"""
    
    def __init__(self, ga_dir: str = "."):
        self.ga_dir = Path(ga_dir)
        self.pages_df = None
        self.events_df = None
        self.acquisition_df = None
        
    def load_ga_pages(self) -> pd.DataFrame:
        """Charge les données de pages depuis le CSV exporté de GA"""
        csv_path = self.ga_dir / "ga_data.csv"
        if csv_path.exists():
            try:
                # GA exporte avec des lignes d'en-tête à ignorer
                self.pages_df = pd.read_csv(csv_path, skiprows=range(0, 9), encoding='utf-8')
                # Nettoyer les noms de colonnes
                self.pages_df.columns = self.pages_df.columns.str.strip()
                print(f"✅ Pages GA chargées: {len(self.pages_df)} lignes")
                return self.pages_df
            except Exception as e:
                # Essayer sans skip rows
                try:
                    self.pages_df = pd.read_csv(csv_path, encoding='utf-8')
                    self.pages_df.columns = self.pages_df.columns.str.strip()
                    print(f"✅ Pages GA chargées: {len(self.pages_df)} lignes")
                    return self.pages_df
                except Exception as e2:
                    print(f"⚠️ Erreur lecture {csv_path}: {e2}")
        else:
            print(f"⚠️ Fichier {csv_path} non trouvé")
        return pd.DataFrame()
    
    def load_ga_events(self) -> pd.DataFrame:
        """Charge les données d'événements depuis le CSV exporté de GA"""
        csv_path = self.ga_dir / "ga_events.csv"
        if csv_path.exists():
            try:
                self.events_df = pd.read_csv(csv_path, skiprows=range(0, 9), encoding='utf-8')
                self.events_df.columns = self.events_df.columns.str.strip()
                print(f"✅ Événements GA chargés: {len(self.events_df)} lignes")
                return self.events_df
            except Exception:
                try:
                    self.events_df = pd.read_csv(csv_path, encoding='utf-8')
                    self.events_df.columns = self.events_df.columns.str.strip()
                    print(f"✅ Événements GA chargés: {len(self.events_df)} lignes")
                    return self.events_df
                except Exception as e:
                    print(f"⚠️ Erreur lecture {csv_path}: {e}")
        else:
            print(f"⚠️ Fichier {csv_path} non trouvé")
        return pd.DataFrame()
    
    def load_ga_acquisition(self) -> pd.DataFrame:
        """Charge les données d'acquisition depuis le CSV exporté de GA"""
        csv_path = self.ga_dir / "ga_acquisition.csv"
        if csv_path.exists():
            try:
                self.acquisition_df = pd.read_csv(csv_path, skiprows=range(0, 9), encoding='utf-8')
                self.acquisition_df.columns = self.acquisition_df.columns.str.strip()
                print(f"✅ Acquisition GA chargée: {len(self.acquisition_df)} lignes")
                return self.acquisition_df
            except Exception:
                try:
                    self.acquisition_df = pd.read_csv(csv_path, encoding='utf-8')
                    self.acquisition_df.columns = self.acquisition_df.columns.str.strip()
                    print(f"✅ Acquisition GA chargée: {len(self.acquisition_df)} lignes")
                    return self.acquisition_df
                except Exception as e:
                    print(f"⚠️ Erreur lecture {csv_path}: {e}")
        else:
            print(f"⚠️ Fichier {csv_path} non trouvé")
        return pd.DataFrame()
    
    def load_all(self):
        """Charge toutes les données GA disponibles"""
        self.load_ga_pages()
        self.load_ga_events()
        self.load_ga_acquisition()
        
    def get_ga_summary(self) -> dict:
        """Retourne un résumé des données GA"""
        summary = {
            "pages_loaded": len(self.pages_df) if self.pages_df is not None and not self.pages_df.empty else 0,
            "events_loaded": len(self.events_df) if self.events_df is not None and not self.events_df.empty else 0,
            "acquisition_loaded": len(self.acquisition_df) if self.acquisition_df is not None and not self.acquisition_df.empty else 0,
        }
        return summary
    
    def has_data(self) -> bool:
        """Vérifie si des données GA sont disponibles"""
        return any([
            self.pages_df is not None and not self.pages_df.empty,
            self.events_df is not None and not self.events_df.empty,
            self.acquisition_df is not None and not self.acquisition_df.empty,
        ])


def compare_metrics(local_events: int, local_pages: dict, ga_pages_df: pd.DataFrame) -> dict:
    """Compare les métriques locales avec celles de Google Analytics"""
    comparison = {
        "local_total_events": local_events,
        "ga_total_views": 0,
        "pages": []
    }
    
    if ga_pages_df is not None and not ga_pages_df.empty:
        # Chercher la colonne des vues (peut varier selon la langue de GA)
        view_cols = [c for c in ga_pages_df.columns if 'vue' in c.lower() or 'view' in c.lower() or 'consultation' in c.lower()]
        if view_cols:
            try:
                ga_pages_df[view_cols[0]] = pd.to_numeric(ga_pages_df[view_cols[0]].astype(str).str.replace(',', ''), errors='coerce')
                comparison["ga_total_views"] = int(ga_pages_df[view_cols[0]].sum())
            except:
                pass
    
    return comparison


if __name__ == "__main__":
    ga = GAAnalytics()
    ga.load_all()
    print("\n📊 Résumé GA:")
    print(json.dumps(ga.get_ga_summary(), indent=2))
    
    if ga.has_data():
        print("\n✅ Données GA disponibles !")
        if ga.pages_df is not None and not ga.pages_df.empty:
            print("\n📄 Colonnes Pages:", list(ga.pages_df.columns))
            print(ga.pages_df.head())
        if ga.events_df is not None and not ga.events_df.empty:
            print("\n📄 Colonnes Events:", list(ga.events_df.columns))
            print(ga.events_df.head())
    else:
        print("\n⚠️ Aucune donnée GA trouvée.")
        print("Exportez vos données depuis https://analytics.google.com")
        print("Sauvegardez les fichiers CSV dans ce dossier :")
        print(f"  - ga_data.csv (Pages et écrans)")
        print(f"  - ga_events.csv (Événements)")
        print(f"  - ga_acquisition.csv (Acquisition)")
