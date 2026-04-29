"""
Dashboard Streamlit - Visualisation des Analytics E-commerce
Étape 2 : Calcul de métriques et dashboard Python
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
from analytics import LogAnalyzer
import sys
sys.path.append('../etape3-google-analytics')
from ga_analytics import GAAnalytics, compare_metrics

# Configuration de la page
st.set_page_config(
    page_title="TechShop Analytics Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé professionnel
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Thème professionnel */
    .main {
        background: linear-gradient(to bottom, #f8f9fa, #ffffff);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header professionnel */
    .professional-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .professional-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .professional-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Cards professionnelles */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #3b82f6;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    /* Graphiques */
    .stPlotlyChart {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* Separator */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e2e8f0, transparent);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(to bottom, #f8fafc, #ffffff);
    }
    
    /* Filtres et tags multiselect - Style professionnel bleu */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: white !important;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Header professionnel
st.markdown("""
<div class="professional-header">
    <h1 class="professional-title"> TechShop Analytics</h1>
    <p class="professional-subtitle">Tableau de Bord Business Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Initialiser l'analyseur
@st.cache_data
def load_data():
    analyzer = LogAnalyzer()
    df = analyzer.load_all_logs()
    return analyzer, df

try:
    analyzer, df = load_data()
    
    # Sidebar professionnel
    st.sidebar.markdown("###  Panneau de Contrôle")
    st.sidebar.markdown("---")
    
    # Filtre par date
    if 'date' in df.columns and not df.empty:
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        date_range = st.sidebar.date_input(
            "Période",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Appliquer le filtre
        if len(date_range) == 2:
            df_filtered = df[
                (df['date'] >= date_range[0]) & 
                (df['date'] <= date_range[1])
            ]
            # Mettre à jour l'analyseur avec les données filtrées
            analyzer.df = df_filtered
    
    # Filtre par type d'événement
    event_types = df['event_type'].unique().tolist() if 'event_type' in df.columns else []
    selected_events = st.sidebar.multiselect(
        "Types d'événements",
        options=event_types,
        default=event_types
    )
    
    st.sidebar.info(f" Dernière mise à jour\n\n{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    
    # === SECTION 1: KPIs PRINCIPAUX ===
    st.markdown("##  Indicateurs Clés de Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_events = analyzer.get_total_events()
        st.metric(
            label=" ÉVÉNEMENTS TOTAUX",
            value=f"{total_events:,}",
            delta="Tous les événements collectés"
        )
    
    with col2:
        unique_sessions = analyzer.get_unique_sessions()
        st.metric(
            label=" VISITEURS UNIQUES",
            value=f"{unique_sessions:,}",
            delta="Sessions distinctes"
        )
    
    with col3:
        page_views = len(df[df['event_type'] == 'page_view']) if 'event_type' in df.columns else 0
        st.metric(
            label=" PAGES CONSULTÉES",
            value=f"{page_views:,}",
            delta="Vues de pages"
        )
    
    with col4:
        avg_events_per_session = total_events / unique_sessions if unique_sessions > 0 else 0
        st.metric(
            label=" ENGAGEMENT MOYEN",
            value=f"{avg_events_per_session:.1f}",
            delta="Actions par visiteur"
        )
    
    st.markdown("---")
    
    # === SECTION 2: MÉTRIQUES E-COMMERCE ===
    st.markdown("##  Performance E-commerce")
    st.markdown("")
    
    ecommerce_metrics = analyzer.get_ecommerce_metrics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label=" AJOUTS PANIER",
            value=ecommerce_metrics.get('total_add_to_cart', 0),
            delta="Produits ajoutés"
        )
    
    with col2:
        st.metric(
            label=" PROCESSUS PAIEMENT",
            value=ecommerce_metrics.get('total_checkout_started', 0),
            delta="Checkouts initiés"
        )
    
    with col3:
        st.metric(
            label=" COMMANDES VALIDÉES",
            value=ecommerce_metrics.get('total_orders', 0),
            delta="Achats finalisés"
        )
    
    with col4:
        revenue = ecommerce_metrics.get('total_revenue', 0)
        st.metric(
            label=" CHIFFRE D'AFFAIRES",
            value=f"{revenue:,.0f} €",
            delta="Revenu total"
        )
    
    with col5:
        conversion = ecommerce_metrics.get('conversion_rate', 0)
        st.metric(
            label=" TAUX CONVERSION",
            value=f"{conversion:.2f}%",
            delta="Visiteurs → Acheteurs"
        )
    
    st.markdown("---")
    st.markdown("###  Métriques Complémentaires")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_order = ecommerce_metrics.get('average_order_value', 0)
        st.metric(
            label=" PANIER MOYEN",
            value=f"{avg_order:,.0f} €",
            delta="Valeur moyenne commande"
        )
    
    with col2:
        abandonment = ecommerce_metrics.get('cart_abandonment_rate', 0)
        delta_color = "inverse" if abandonment > 50 else "normal"
        st.metric(
            label=" ABANDON PANIER",
            value=f"{abandonment:.1f}%",
            delta="Taux d'abandon",
            delta_color=delta_color
        )
    
    with col3:
        st.metric(
            label=" PRODUITS RETIRÉS",
            value=ecommerce_metrics.get('total_remove_from_cart', 0),
            delta="Retraits du panier"
        )
    
    with col4:
        bounce_rate = analyzer.get_bounce_rate()
        st.metric(
            label=" TAUX DE REBOND",
            value=f"{bounce_rate:.1f}%",
            delta="Sessions 1 page",
            delta_color="inverse"
        )
    
    with col5:
        avg_duration = analyzer.get_avg_session_duration()
        minutes = avg_duration / 60
        st.metric(
            label=" DURÉE MOY. SESSION",
            value=f"{minutes:.1f} min",
            delta="Temps moyen par visite"
        )
    
    st.markdown("---")
    
    # === SECTION 3: ANALYSES DÉTAILLÉES ===
    st.markdown("##  Analyses Détaillées")
    st.markdown("")
    
    # Onglets pour différentes visualisations
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        " Événements", " Produits", " Analyse Temporelle", " Tunnel de Conversion", " Appareils", " Google Analytics", " Machine Learning"
    ])
    
    with tab1:
        st.markdown("###  Distribution des Événements Utilisateur")
        
        events_by_type = analyzer.get_events_by_type()
        
        if not events_by_type.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique en barres professionnel
                fig_bar = px.bar(
                    x=events_by_type.values,
                    y=events_by_type.index,
                    orientation='h',
                    title="Volume d'Événements par Catégorie",
                    labels={'x': 'Nombre d\'Événements', 'y': 'Type d\'Événement'},
                    color=events_by_type.values,
                    color_continuous_scale=['#3b82f6', '#1e3a8a']
                )
                fig_bar.update_layout(
                    height=500, 
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_bar, width='stretch', key='events_bar_chart')
            
            with col2:
                # Graphique en anneau professionnel
                fig_pie = px.pie(
                    values=events_by_type.values,
                    names=events_by_type.index,
                    title="Parts de Marché des Événements",
                    hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig_pie.update_layout(
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_pie, width='stretch', key='events_pie_chart')
        else:
            st.info("Aucune donnée d'événement disponible")
        
        # Pages les plus vues
        st.markdown("###  Pages à Fort Trafic")
        page_views_df = analyzer.get_page_views()
        
        if not page_views_df.empty:
            page_views_df.columns = ['Page', 'Vues']
            
            fig_pages = px.bar(
                page_views_df.head(10),
                x='Vues',
                y='Page',
                orientation='h',
                title="Top 10 Pages les Plus Consultées",
                color='Vues',
                color_continuous_scale=['#60a5fa', '#1e40af']
            )
            fig_pages.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=16, color='#1e293b', family="Inter")
            )
            st.plotly_chart(fig_pages, width='stretch', key='pages_chart')
            
            # Tableau des pages
            st.dataframe(page_views_df, width='stretch')
        else:
            st.info("Aucune donnée de page vue disponible")
    
    with tab2:
        st.markdown("###  Analyse de Performance Produits")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("####  Produits les Plus Ajoutés au Panier")
            top_added = analyzer.get_top_products_added(10)
            
            if not top_added.empty:
                fig_added = px.bar(
                    top_added,
                    x='add_count',
                    y='product_name',
                    orientation='h',
                    title="Volume d'Ajouts par Produit",
                    color='price',
                    color_continuous_scale=['#86efac', '#166534'],
                    labels={'add_count': 'Nombre d\'Ajouts', 'product_name': 'Produit', 'price': 'Prix (€)'}
                )
                fig_added.update_layout(
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_added, width='stretch', key='products_added_chart')
                
                st.dataframe(top_added, width='stretch')
            else:
                st.info("Aucun produit ajouté au panier")
        
        with col2:
            st.markdown("####  Produits les Plus Vendus")
            top_purchased = analyzer.get_top_products_purchased(10)
            
            if not top_purchased.empty:
                fig_purchased = px.bar(
                    top_purchased,
                    x='purchase_count',
                    y='product_name',
                    orientation='h',
                    title="Performance de Vente par Produit",
                    color='revenue',
                    color_continuous_scale=['#c084fc', '#581c87'],
                    labels={'purchase_count': 'Quantité Vendue', 'product_name': 'Produit', 'revenue': 'Revenu (€)'}
                )
                fig_purchased.update_layout(
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_purchased, width='stretch', key='products_purchased_chart')
                
                st.dataframe(top_purchased, width='stretch')
            else:
                st.info("Aucun produit acheté")
    
    with tab3:
        st.markdown("###  Analyse Temporelle des Activités")
        
        # Événements par heure
        events_by_hour = analyzer.get_events_by_hour()
        
        if not events_by_hour.empty:
            events_by_hour.columns = ['Heure', 'Nombre']
            
            fig_hour = px.line(
                events_by_hour,
                x='Heure',
                y='Nombre',
                title="Distribution Horaire de l'Activité Utilisateur",
                markers=True
            )
            fig_hour.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=16, color='#1e293b', family="Inter")
            )
            fig_hour.update_traces(line_color='#3b82f6', marker=dict(size=8, color='#1e40af'))
            fig_hour.update_xaxes(dtick=1)
            st.plotly_chart(fig_hour, width='stretch', key='hourly_chart')
        
        # Événements au fil du temps
        events_over_time = analyzer.get_events_over_time('10T')  # 10 minutes
        
        if not events_over_time.empty:
            fig_timeline = px.area(
                events_over_time,
                x='timestamp',
                y='event_count',
                title="Évolution Temporelle de l'Activité (Intervalle 10 min)",
                labels={'timestamp': 'Temps', 'event_count': 'Nombre d\'Activités'}
            )
            fig_timeline.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=16, color='#1e293b', family="Inter")
            )
            fig_timeline.update_traces(fillcolor='rgba(59, 130, 246, 0.3)', line_color='#3b82f6')
            st.plotly_chart(fig_timeline, width='stretch', key='timeline_events_chart')
        
        # Temps moyen par page
        avg_time = analyzer.get_average_time_on_page()
        
        if not avg_time.empty:
            st.markdown("####  Engagement par Page (Temps Moyen)")
            
            fig_time = px.bar(
                avg_time.head(10),
                x='avg_minutes',
                y='page_url',
                orientation='h',
                title="Durée Moyenne de Consultation (minutes)",
                color='avg_minutes',
                color_continuous_scale=['#fbbf24', '#b45309']
            )
            fig_time.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=16, color='#1e293b', family="Inter")
            )
            st.plotly_chart(fig_time, width='stretch', key='time_on_page_chart')
        
        # Heatmap d'activité
        st.markdown("###  Heatmap d'activité (Clics par jour/heure)")
        heatmap_data = analyzer.get_click_heatmap_data()
        if not heatmap_data.empty:
            fig_heat = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=[f"{h}h" for h in heatmap_data.columns],
                y=heatmap_data.index,
                colorscale='YlOrRd',
                hovertemplate='Jour: %{y}<br>Heure: %{x}<br>Clics: %{z}<extra></extra>'
            ))
            fig_heat.update_layout(
                title="Intensité des clics par jour et heure",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12)
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("Pas assez de données de clics pour la heatmap")
    
    with tab4:
        st.markdown("###  Tunnel de Conversion Client")
        
        funnel_data = analyzer.get_conversion_funnel()
        
        if funnel_data:
            funnel_df = pd.DataFrame({
                'Étape': ['Visites', 'Vues Produits', 'Ajouts Panier', 'Paiement Initié', 'Commandes Validées'],
                'Nombre': [
                    funnel_data.get('1_visits', 0),
                    funnel_data.get('2_product_views', 0),
                    funnel_data.get('3_add_to_cart', 0),
                    funnel_data.get('4_checkout_started', 0),
                    funnel_data.get('5_orders', 0)
                ]
            })
            
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_df['Étape'],
                x=funnel_df['Nombre'],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']
                )
            ))
            
            fig_funnel.update_layout(
                title="Parcours d'Achat des Clients",
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=16, color='#1e293b', family="Inter")
            )
            
            st.plotly_chart(fig_funnel, width='stretch', key='conversion_funnel_chart')
            
            # Taux de conversion par étape
            st.markdown("####  Taux de Conversion par Étape")
            
            col1, col2, col3, col4 = st.columns(4)
            
            visits = funnel_data.get('1_visits', 1)
            
            with col1:
                rate = (funnel_data.get('3_add_to_cart', 0) / visits * 100) if visits > 0 else 0
                st.metric("🛒 Visite → Panier", f"{rate:.1f}%")
            
            with col2:
                rate = (funnel_data.get('4_checkout_started', 0) / visits * 100) if visits > 0 else 0
                st.metric(" Visite → Paiement", f"{rate:.1f}%")
            
            with col3:
                rate = (funnel_data.get('5_orders', 0) / visits * 100) if visits > 0 else 0
                st.metric(" Visite → Achat", f"{rate:.1f}%")
            
            with col4:
                checkouts = funnel_data.get('4_checkout_started', 1)
                rate = (funnel_data.get('5_orders', 0) / checkouts * 100) if checkouts > 0 else 0
                st.metric(" Paiement → Achat", f"{rate:.1f}%")
        
        # Codes promo
        st.markdown("####  Efficacité des Codes Promotionnels")
        promo_usage = analyzer.get_promo_code_usage()
        
        if not promo_usage.empty:
            st.dataframe(promo_usage, width='stretch')
        else:
            st.info("Aucun code promo utilisé")
    
    with tab5:
        st.markdown("###  Analyse Multi-Appareils")
        
        device_stats = analyzer.get_device_stats()
        
        if not device_stats.empty:
            device_stats.columns = ['Type d\'Appareil', 'Utilisations']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_device_pie = px.pie(
                    device_stats,
                    values='Utilisations',
                    names='Type d\'Appareil',
                    title="Répartition par Plateforme",
                    hole=0.5,
                    color_discrete_sequence=['#3b82f6', '#60a5fa', '#93c5fd']
                )
                fig_device_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_device_pie, width='stretch', key='device_pie_chart')
            
            with col2:
                fig_device_bar = px.bar(
                    device_stats,
                    x='Type d\'Appareil',
                    y='Utilisations',
                    title="Volume d'Activité par Type d'Appareil",
                    color='Utilisations',
                    color_continuous_scale=['#06b6d4', '#0e7490']
                )
                fig_device_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_device_bar, width='stretch', key='device_bar_chart')
        else:
            st.info("Aucune donnée d'appareil disponible")
    
    # === SECTION 4: DONNÉES BRUTES ===
    st.markdown("---")
    st.markdown("##  Export des Données")
    
    with st.expander(" Consulter les Données Brutes"):
        st.dataframe(df, width='stretch', height=400)
        
        # Téléchargement CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name=f"techshop_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            width='stretch'
        )
    
    # === SECTION 5: PARCOURS UTILISATEUR ===
    st.markdown("---")
    st.markdown("##  Analyse du Parcours Client")
    
    if 'session_id' in df.columns:
        sessions = df['session_id'].unique()
        
        selected_session = st.selectbox(
            " Sélectionner une Session Utilisateur",
            options=sessions,
            index=0 if len(sessions) > 0 else None
        )
        
        if selected_session:
            journey = analyzer.get_user_journey(selected_session)
            
            if not journey.empty:
                st.markdown(f"#### Parcours Complet - Session `{selected_session[:20]}...`")
                st.dataframe(journey, width='stretch')
                
                # Visualisation du parcours
                journey_summary = journey['page_url'].value_counts().reset_index()
                journey_summary.columns = ['Page', 'Visites']
                
                fig_journey = px.bar(
                    journey_summary,
                    x='Visites',
                    y='Page',
                    orientation='h',
                    title=f"Pages Consultées Durant la Session",
                    color='Visites',
                    color_continuous_scale=['#3b82f6', '#1e40af']
                )
                fig_journey.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=12),
                    title_font=dict(size=16, color='#1e293b', family="Inter")
                )
                st.plotly_chart(fig_journey, width='stretch', key='user_journey_chart')

    with tab6:
        st.markdown("###  Google Analytics - Données & Comparaison")
        
        # Charger les données GA
        ga = GAAnalytics(ga_dir="../etape3-google-analytics")
        ga.load_all()
        
        if ga.has_data():
            st.success(" Données Google Analytics chargées !")
            
            # Résumé GA
            ga_summary = ga.get_ga_summary()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(" Pages GA", ga_summary['pages_loaded'])
            with col2:
                st.metric(" Événements GA", ga_summary['events_loaded'])
            with col3:
                st.metric(" Acquisition GA", ga_summary['acquisition_loaded'])
            
            st.markdown("---")
            
            # Afficher les données de pages
            if ga.pages_df is not None and not ga.pages_df.empty:
                st.markdown("####  Pages et Écrans (Google Analytics)")
                st.dataframe(ga.pages_df, use_container_width=True)
                
                # Graphique des pages GA
                num_cols = ga.pages_df.select_dtypes(include=['number']).columns
                if len(num_cols) > 0 and len(ga.pages_df.columns) > 0:
                    first_col = ga.pages_df.columns[0]
                    first_num = num_cols[0]
                    fig_ga_pages = px.bar(
                        ga.pages_df.head(10),
                        x=first_col,
                        y=first_num,
                        title="Top 10 Pages (Google Analytics)",
                        color=first_num,
                        color_continuous_scale=['#f59e0b', '#ef4444']
                    )
                    fig_ga_pages.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter, sans-serif", size=12)
                    )
                    st.plotly_chart(fig_ga_pages, use_container_width=True)
            
            # Afficher les événements GA
            if ga.events_df is not None and not ga.events_df.empty:
                st.markdown("####  Événements (Google Analytics)")
                st.dataframe(ga.events_df, use_container_width=True)
            
            # Afficher l'acquisition GA
            if ga.acquisition_df is not None and not ga.acquisition_df.empty:
                st.markdown("####  Sources d'Acquisition (Google Analytics)")
                st.dataframe(ga.acquisition_df, use_container_width=True)
            
            st.markdown("---")
            
            # Comparaison locale vs GA
            st.markdown("####  Comparaison : Données Locales vs Google Analytics")
            local_events = analyzer.get_total_events()
            comparison = compare_metrics(local_events, {}, ga.pages_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#####  Données Locales (NiFi)")
                st.metric("Total événements", f"{local_events:,}")
                
                events_by_type = analyzer.get_events_by_type()
                if not events_by_type.empty:
                    fig_local = px.pie(
                        values=events_by_type.values,
                        names=events_by_type.index,
                        title="Répartition locale",
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig_local.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_local, use_container_width=True)
            
            with col2:
                st.markdown("#####  Données Google Analytics")
                st.metric("Total vues GA", f"{comparison['ga_total_views']:,}")
                
                if ga.events_df is not None and not ga.events_df.empty:
                    num_cols = ga.events_df.select_dtypes(include=['number']).columns
                    if len(num_cols) > 0 and len(ga.events_df.columns) > 0:
                        first_col = ga.events_df.columns[0]
                        first_num = num_cols[0]
                        fig_ga = px.pie(
                            ga.events_df.head(10),
                            values=first_num,
                            names=first_col,
                            title="Répartition GA",
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig_ga.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_ga, use_container_width=True)
            
            st.info(" Les données locales proviennent du pipeline NiFi. Les données GA proviennent de l'export CSV de Google Analytics.")
        
        else:
            st.warning("⚠ Aucune donnée Google Analytics trouvée.")
            st.markdown("""
            **Pour ajouter vos données Google Analytics :**
            
            1. Allez sur [Google Analytics](https://analytics.google.com)
            2. Sélectionnez votre propriété **TechShop**
            3. Exportez les rapports en CSV :
               - **Pages et écrans** → Sauvegardez comme `ga_data.csv`
               - **Événements** → Sauvegardez comme `ga_events.csv`  
               - **Acquisition** → Sauvegardez comme `ga_acquisition.csv`
            4. Placez les fichiers dans `etape3-google-analytics/`
            5. Rechargez ce dashboard
            """)

    # ===== ONGLET 7 : MACHINE LEARNING =====
    with tab7:
        st.markdown("###  Machine Learning - Prédiction & Segmentation")
        st.markdown("Analyse du comportement utilisateur avec des algorithmes d'apprentissage automatique.")
        
        ml_results_path = Path('../etape6-ml/results.csv')
        ml_images_dir = Path('../etape6-ml')
        
        if ml_results_path.exists():
            ml_df = pd.read_csv(ml_results_path)
            
            # Métriques résumées
            st.markdown("####  Résumé des données")
            col_ml1, col_ml2, col_ml3, col_ml4 = st.columns(4)
            with col_ml1:
                st.metric("Sessions analysées", len(ml_df))
            with col_ml2:
                st.metric("Événements totaux", f"{ml_df['nb_events'].sum():.0f}")
            with col_ml3:
                n_segments = ml_df['segment'].nunique() if 'segment' in ml_df.columns else 0
                st.metric("Segments identifiés", n_segments)
            with col_ml4:
                n_interactions = ml_df['has_interaction'].sum() if 'has_interaction' in ml_df.columns else 0
                st.metric("Sessions avec interaction", int(n_interactions))
            
            st.markdown("---")
            
            # Segmentation K-Means
            st.markdown("####  Segmentation des utilisateurs (K-Means)")
            st.markdown("L'algorithme K-Means regroupe les sessions par similarité de comportement.")
            
            if 'segment' in ml_df.columns:
                col_seg1, col_seg2 = st.columns(2)
                
                with col_seg1:
                    segment_counts = ml_df['segment'].value_counts()
                    fig_seg = px.pie(
                        values=segment_counts.values,
                        names=segment_counts.index,
                        title="Répartition des segments",
                        color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c']
                    )
                    st.plotly_chart(fig_seg, use_container_width=True)
                
                with col_seg2:
                    fig_bar = px.bar(
                        ml_df,
                        x='segment',
                        y='nb_events',
                        color='segment',
                        title="Événements par segment",
                        labels={'nb_events': 'Nombre d\'événements', 'segment': 'Segment'},
                        color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c']
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                # Tableau détaillé par segment
                st.markdown("#####  Détail par segment")
                segment_summary = ml_df.groupby('segment').agg(
                    sessions=('segment', 'count'),
                    events_moy=('nb_events', 'mean'),
                    clics_moy=('nb_clicks', 'mean'),
                    pages_moy=('nb_unique_pages', 'mean'),
                    interactions=('has_interaction', 'sum')
                ).round(1)
                segment_summary.columns = ['Sessions', 'Événements moy.', 'Clics moy.', 'Pages moy.', 'Interactions']
                st.dataframe(segment_summary, use_container_width=True)
            
            st.markdown("---")
            
            # Classification Random Forest
            st.markdown("####  Classification (Random Forest)")
            st.markdown("Le modèle Random Forest prédit si un utilisateur va interagir avec un produit.")
            
            col_img1, col_img2 = st.columns(2)
            
            # Matrice de confusion
            cm_path = ml_images_dir / 'confusion_matrix.png'
            if cm_path.exists():
                with col_img1:
                    st.image(str(cm_path), caption="Matrice de Confusion", use_container_width=True)
            
            # Importance des features
            fi_path = ml_images_dir / 'feature_importance.png'
            if fi_path.exists():
                with col_img2:
                    st.image(str(fi_path), caption="Importance des Features", use_container_width=True)
            
            # Graphique segments
            seg_path = ml_images_dir / 'user_segments.png'
            if seg_path.exists():
                st.markdown("####  Visualisation des segments")
                st.image(str(seg_path), caption="Segmentation des utilisateurs (K-Means)", use_container_width=True)
            
            # Méthode du coude
            elbow_path = ml_images_dir / 'elbow_method.png'
            if elbow_path.exists():
                st.markdown("####  Méthode du coude (choix du nombre de clusters)")
                st.image(str(elbow_path), caption="Méthode du coude", use_container_width=True)
            
            # Données brutes
            with st.expander(" Voir les données des sessions"):
                st.dataframe(ml_df, use_container_width=True)
        
        else:
            st.warning("⚠ Aucun résultat ML trouvé.")
            st.markdown("""
            **Pour générer les résultats ML :**
            1. Ouvrez un terminal
            2. Allez dans le dossier `etape6-ml/`
            3. Lancez : `python ml_model.py`
            """)

except Exception as e:
    st.error(f" Erreur lors du chargement des données: {str(e)}")
    st.info(" Assurez-vous que le dossier de logs existe et contient des données.")
    st.code("Chemin attendu: ../etape1-website/logs/", language="text")

# Footer professionnel
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #64748b;'>
    <p style='margin: 0; font-size: 14px;'> <strong>TechShop Analytics Dashboard</strong> - Business Intelligence Platform</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 12px;'>Propulsé par Streamlit & Plotly | Étape 2 du Projet Analytics</p>
</div>
""", unsafe_allow_html=True)
