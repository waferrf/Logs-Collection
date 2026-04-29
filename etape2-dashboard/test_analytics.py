"""
Script de test pour l'analyseur de logs
Permet de vérifier que les données sont bien chargées
"""

from analytics import LogAnalyzer
import sys

def main():
    print("=" * 60)
    print(" TEST DE L'ANALYSEUR DE LOGS")
    print("=" * 60)
    
    try:
        # Initialiser l'analyseur
        print("\n Initialisation de l'analyseur...")
        analyzer = LogAnalyzer()
        
        # Charger les données
        print(" Chargement des logs...")
        df = analyzer.load_all_logs()
        
        if df is None or df.empty:
            print(" Aucune donnée chargée!")
            print("\nVérifiez que :")
            print("  - Le dossier ../etape1-website/logs/ existe")
            print("  - Il contient des fichiers JSON")
            return
        
        print(f" {len(df)} événements chargés\n")
        
        # Afficher les KPIs
        print("=" * 60)
        print(" KPIs PRINCIPAUX")
        print("=" * 60)
        
        print(f"\n Total événements: {analyzer.get_total_events():,}")
        print(f" Sessions uniques: {analyzer.get_unique_sessions():,}")
        
        print("\n" + "=" * 60)
        print(" DISTRIBUTION DES ÉVÉNEMENTS")
        print("=" * 60)
        
        events_by_type = analyzer.get_events_by_type()
        print("\nTop 10 types d'événements:")
        for event_type, count in events_by_type.head(10).items():
            print(f"  {event_type:30s} : {count:4d}")
        
        print("\n" + "=" * 60)
        print(" MÉTRIQUES E-COMMERCE")
        print("=" * 60)
        
        metrics = analyzer.get_ecommerce_metrics()
        
        print(f"\n Ajouts au panier       : {metrics.get('total_add_to_cart', 0)}")
        print(f" Retraits du panier     : {metrics.get('total_remove_from_cart', 0)}")
        print(f" Checkouts démarrés     : {metrics.get('total_checkout_started', 0)}")
        print(f" Commandes finalisées   : {metrics.get('total_orders', 0)}")
        print(f" Revenu total           : {metrics.get('total_revenue', 0):,.0f}€")
        print(f" Panier moyen           : {metrics.get('average_order_value', 0):,.0f}€")
        print(f" Taux de conversion     : {metrics.get('conversion_rate', 0):.2f}%")
        print(f" Taux abandon panier    : {metrics.get('cart_abandonment_rate', 0):.1f}%")
        
        # Top produits
        print("\n" + "=" * 60)
        print(" TOP PRODUITS")
        print("=" * 60)
        
        top_added = analyzer.get_top_products_added(5)
        if not top_added.empty:
            print("\nTop 5 produits ajoutés au panier:")
            for idx, row in top_added.iterrows():
                print(f"  {row['product_name']:30s} : {row['add_count']:2d} ajouts ({row['price']}€)")
        else:
            print("\n Aucun produit ajouté au panier")
        
        top_purchased = analyzer.get_top_products_purchased(5)
        if not top_purchased.empty:
            print("\nTop 5 produits achetés:")
            for idx, row in top_purchased.iterrows():
                print(f"  {row['product_name']:30s} : {row['purchase_count']:2d} ventes ({row['revenue']:.0f}€)")
        else:
            print("\n Aucun produit acheté")
        
        # Pages les plus vues
        print("\n" + "=" * 60)
        print(" PAGES LES PLUS VUES")
        print("=" * 60)
        
        page_views = analyzer.get_page_views()
        if not page_views.empty:
            print("\nTop 5 pages:")
            page_views.columns = ['page_url', 'count']
            for idx, row in page_views.head(5).iterrows():
                print(f"  {row['page_url']:30s} : {row['count']:4d} vues")
        else:
            print("\n Aucune page vue enregistrée")
        
        print("\n" + "=" * 60)
        print(" TEST TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        print("\n Vous pouvez maintenant lancer le dashboard:")
        print("   streamlit run dashboard.py")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n Erreur: Dossier de logs non trouvé")
        print(f"   Détails: {e}")
        print("\nAssurez-vous que le chemin ../etape1-website/logs/ existe")
    except Exception as e:
        print(f"\n Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
