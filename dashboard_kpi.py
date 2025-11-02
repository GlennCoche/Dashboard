"""
Dashboard KPI Energysoft - Interface moderne style taostat
10 KPIs visuels avec graphiques, tableaux et cartes géographiques
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Dashboard KPI Energysoft",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = "energysoft_stats.db"

# Styles CSS glassmorphism/iOS materials - Thème Clair
# Injection du CSS via JavaScript pour forcer l'application après le chargement
st.markdown("""
    <script>
    // Force l'injection du CSS après le chargement de la page
    function injectGlassmorphismCSS() {
        const style = document.createElement('style');
        style.id = 'glassmorphism-style';
        style.innerHTML = `
    /* Variables CSS iOS Materials - Thème Clair */
    :root {
        --bg: linear-gradient(120deg, #f0f4ff 0%, #f7fafc 50%, #ffffff 100%);
        --glass: rgba(255, 255, 255, 0.65);
        --glass-strong: rgba(255, 255, 255, 0.85);
        --border: rgba(0, 0, 0, 0.1);
        --border-strong: rgba(0, 0, 0, 0.15);
        --hairline: rgba(0, 0, 0, 0.12);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        --shadow-strong: 0 10px 30px rgba(0, 0, 0, 0.2);
        --radius: 20px;
        --blur: 20px;
        --accent: #0A84FF;
        --text: #1f2937;
        --text-secondary: #4b5563;
    }
    
    /* Force le background sur html et body */
    html, body {
        background: linear-gradient(120deg, #f0f4ff 0%, #f7fafc 50%, #ffffff 100%) fixed !important;
        background-attachment: fixed !important;
    }
    
    /* Background principal avec gradient clair - Ultra spécifique */
    div[data-testid="stAppViewContainer"],
    div[data-testid="stAppViewContainer"] > div,
    section[data-testid="stAppViewContainer"],
    .stApp,
    .stApp > div,
    .main,
    body {
        background: linear-gradient(135deg, #d4e3fc 0%, #e0ebfa 20%, #ecf2fb 40%, #f5f8fc 60%, #fafcfe 80%, #ffffff 100%) !important;
        background-attachment: fixed !important;
        font-family: ui-sans-serif, system-ui, -apple-system, "SF Pro Text", "SF Pro Display", 
                     "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        color: #1f2937 !important;
        min-height: 100vh !important;
    }
    
    /* Override Streamlit default styles */
    .stApp > header,
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        backdrop-filter: blur(18px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(140%) !important;
    }
    
    /* Main container */
    .main .block-container,
    div[data-testid="stAppViewContainer"] > div > div,
    .element-container {
        background: transparent !important;
    }
    
    .main .block-container {
        padding-top: 2rem !important;
    }
    
    /* Sidebar glass effect */
    [data-testid="stSidebar"] {
        background: var(--glass) !important;
        backdrop-filter: blur(18px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(140%) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    /* Main header glass */
    .main-header,
    h1.main-header {
        font-size: clamp(22px, 3.5vw, 34px) !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding: 24px !important;
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(20px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        display: block !important;
    }
    
    /* Section headers glass */
    .section-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
        margin: 2rem 0 1rem 0 !important;
        padding: 16px 24px !important;
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(20px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        display: block !important;
    }
    
    /* Metrics glass */
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-weight: 700;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        opacity: 0.9;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--accent) !important;
    }
    
    /* Metric containers glass - Wrapper des metrics */
    div[data-testid="stMetricContainer"],
    div[data-testid="stMetricContainer"] > div,
    .stMetric,
    .metric-container,
    div[data-baseweb="card"] {
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        backdrop-filter: blur(20px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        margin: 8px !important;
    }
    
    /* Plotly charts glass container - Ultra spécifique */
    [data-testid="stPlotlyChart"],
    div[data-testid="stPlotlyChart"],
    div[data-testid="stPlotlyChart"] > div,
    .js-plotly-plot,
    .plotly {
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        margin: 12px 0 !important;
    }
    
    /* Wrapper des graphiques Plotly */
    .element-container:has([data-testid="stPlotlyChart"]) {
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Dataframes glass */
    [data-testid="stDataFrameContainer"] {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 12px !important;
    }
    
    /* Buttons glass */
    .stButton > button {
        background: var(--accent) !important;
        color: #fff !important;
        font-weight: 600 !important;
        border: 0 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        box-shadow: 0 8px 20px rgba(10, 132, 255, 0.35) !important;
        transition: transform 0.12s ease, filter 0.12s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        filter: saturate(120%);
    }
    
    /* Info boxes glass */
    .stInfo, .stWarning, .stSuccess, .stError {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* All text colors */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: var(--text) !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: var(--text) !important;
    }
        `;
        
        // Supprime l'ancien style s'il existe
        const oldStyle = document.getElementById('glassmorphism-style');
        if (oldStyle) oldStyle.remove();
        
        // Injecte le nouveau style
        document.head.appendChild(style);
        
        // Force l'application immédiate sur les éléments existants
        document.body.style.background = 'linear-gradient(120deg, #f0f4ff 0%, #f7fafc 50%, #ffffff 100%) fixed';
        const appContainer = document.querySelector('[data-testid="stAppViewContainer"]');
        if (appContainer) {
            appContainer.style.background = 'linear-gradient(120deg, #f0f4ff 0%, #f7fafc 50%, #ffffff 100%) fixed';
        }
    }
    
    // Exécute immédiatement et après le chargement
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectGlassmorphismCSS);
    } else {
        injectGlassmorphismCSS();
    }
    
    // Réexécute après un court délai pour s'assurer que Streamlit a fini
    setTimeout(injectGlassmorphismCSS, 100);
    setTimeout(injectGlassmorphismCSS, 500);
    setTimeout(injectGlassmorphismCSS, 1000);
    </script>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data(table_name, query=None):
    """Charge les données depuis SQLite avec cache"""
    if not os.path.exists(DB_PATH):
        st.error(f"❌ Base de données non trouvée: {DB_PATH}")
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        if query:
            df = pd.read_sql_query(query, conn)
        else:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")
        return None

def apply_glassmorphism_theme(fig):
    """Applique un thème glassmorphism/iOS materials clair aux graphiques Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(255, 255, 255, 0.6)',
        font=dict(
            family='ui-sans-serif, system-ui, -apple-system, "SF Pro Text", "SF Pro Display", sans-serif',
            color='#1f2937',
            size=12
        ),
        title=dict(
            font=dict(size=16, color='#1f2937'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0, 0, 0, 0.08)',
            linecolor='rgba(0, 0, 0, 0.15)',
            zerolinecolor='rgba(0, 0, 0, 0.1)',
            tickfont=dict(color='#4b5563')
        ),
        yaxis=dict(
            gridcolor='rgba(0, 0, 0, 0.08)',
            linecolor='rgba(0, 0, 0, 0.15)',
            zerolinecolor='rgba(0, 0, 0, 0.1)',
            tickfont=dict(color='#4b5563')
        ),
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='rgba(0, 0, 0, 0.08)',
            borderwidth=1,
            font=dict(color='#1f2937')
        ),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def main():
    # En-tête moderne avec glassmorphism inline
    st.markdown('''
    <div style="
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        padding: 24px;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        ⚡ Dashboard KPI Energysoft
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar minimaliste
    with st.sidebar:
        st.markdown("### ⚙️ Paramètres")
        refresh = st.button("🔄 Actualiser", type="primary", use_container_width=True)
        if refresh:
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Données")
        st.info(f"**Base:** {DB_PATH}")
    
    # Chargement des données
    with st.spinner("🔄 Chargement des données..."):
        df_interventions = load_data("interventions")
        df_exposition = load_data("exposition")
        df_calc_mensuel = load_data("calculs_mensuel_sites")
        df_calc_annuel = load_data("calculs_annuel_sites")
        df_spot_prices = load_data("spot_market_prices")
    
    if df_interventions is None or df_interventions.empty:
        st.error("❌ Impossible de charger les données")
        return
    
    # ==========================================
    # KPI 1 & 2: Métriques principales (Top)
    # ==========================================
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 1.5rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">📊 Vue d'ensemble</div>
    ''', unsafe_allow_html=True)
    
    # Wrapper glassmorphism pour les métriques
    st.markdown('<div style="padding: 12px; background: rgba(255, 255, 255, 0.4); border-radius: 16px; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI 1: Total interventions
    total_interventions = len(df_interventions)
    with col1:
        st.metric(
            label="Total Interventions",
            value=f"{total_interventions:,}",
            delta=None
        )
    
    # KPI 2: Taux de résolution
    if 'ticket_resolu' in df_interventions.columns:
        resolues = df_interventions['ticket_resolu'].sum()
        taux_resolution = (resolues / total_interventions * 100) if total_interventions > 0 else 0
        with col2:
            st.metric(
                label="Taux de Résolution",
                value=f"{taux_resolution:.1f}%",
                delta=f"{resolues:,} résolues"
            )
    else:
        with col2:
            st.metric("Taux de Résolution", "N/A")
    
    # KPI 3: Sites uniques
    if 'nom_site' in df_interventions.columns:
        sites_count = df_interventions['nom_site'].nunique()
        with col3:
            st.metric(
                label="Sites Uniques",
                value=f"{sites_count:,}",
                delta=None
            )
    else:
        with col3:
            st.metric("Sites Uniques", "N/A")
    
    # KPI 4: Coût moyen
    if 'facturation_intervention' in df_interventions.columns:
        df_interventions['facturation_intervention'] = pd.to_numeric(
            df_interventions['facturation_intervention'], errors='coerce'
        )
        cout_moyen = df_interventions['facturation_intervention'].mean()
        with col4:
            st.metric(
                label="Coût Moyen",
                value=f"{cout_moyen:.0f} €" if pd.notna(cout_moyen) else "N/A",
                delta=None
            )
    else:
        with col4:
            st.metric("Coût Moyen", "N/A")
    
    # Fermer le wrapper glassmorphism des métriques
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # KPI 5: Graphique - Évolution temporelle mensuelle
    # ==========================================
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">📈 Évolution Temporelle</div>
    ''', unsafe_allow_html=True)
    
    # Wrapper pour les graphiques temporels
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'date_creation_intervention' in df_interventions.columns:
            df_interventions['date_creation_intervention'] = pd.to_datetime(
                df_interventions['date_creation_intervention'], errors='coerce'
            )
            df_time = df_interventions[df_interventions['date_creation_intervention'].notna()].copy()
            df_time['Mois'] = df_time['date_creation_intervention'].dt.to_period('M').astype(str)
            monthly_counts = df_time.groupby('Mois').size().reset_index(name='Nombre')
            monthly_counts = monthly_counts.sort_values('Mois')
            
            fig = px.line(
                monthly_counts,
                x='Mois',
                y='Nombre',
                title="📅 Évolution Mensuelle des Interventions",
                markers=True,
                line_shape='spline',
                color_discrete_sequence=['#0A84FF']
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(
                height=400,
                xaxis_title="Mois",
                yaxis_title="Nombre d'interventions",
                hovermode='x unified'
            )
            fig.update_traces(line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Données temporelles non disponibles")
    
    with col2:
        st.markdown("### 📊 Statistiques")
        if 'date_creation_intervention' in df_interventions.columns:
            df_interventions['date_creation_intervention'] = pd.to_datetime(
                df_interventions['date_creation_intervention'], errors='coerce'
            )
            dates_valid = df_interventions['date_creation_intervention'].dropna()
            if not dates_valid.empty:
                st.metric("Première", dates_valid.min().strftime("%Y-%m-%d"))
                st.metric("Dernière", dates_valid.max().strftime("%Y-%m-%d"))
                st.metric("Période", f"{(dates_valid.max() - dates_valid.min()).days} jours")
    
    # Fermer le wrapper glassmorphism des graphiques temporels
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # KPI 6: Graphique - Distribution par catégorie
    # ==========================================
    # Wrapper pour les graphiques de distribution
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'categorie' in df_interventions.columns:
            categorie_counts = df_interventions['categorie'].value_counts().head(8)
            fig = px.bar(
                x=categorie_counts.values,
                y=categorie_counts.index,
                orientation='h',
                title="📊 Distribution par Catégorie",
                labels={'x': 'Nombre', 'y': 'Catégorie'},
                color=categorie_counts.values,
                color_continuous_scale='Blues'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Données de catégorie non disponibles")
    
    # ==========================================
    # KPI 7: Graphique - Taux de résolution (Camembert)
    # ==========================================
    with col2:
        if 'ticket_resolu' in df_interventions.columns:
            resolution_data = df_interventions['ticket_resolu'].value_counts()
            labels = ['Non Résolu' if idx == 0 else 'Résolu' for idx in resolution_data.index]
            values = resolution_data.values
            
            fig = px.pie(
                values=values,
                names=labels,
                title="✅ Taux de Résolution",
                color_discrete_map={'Résolu': '#10b981', 'Non Résolu': '#ef4444'}
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Données de résolution non disponibles")
    
    # Fermer le wrapper glassmorphism des graphiques de distribution
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # KPI 8: Tableau - Top 10 Sites
    # ==========================================
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">🏢 Top Sites par Interventions</div>
    ''', unsafe_allow_html=True)
    
    # Vérifier les noms de colonnes (peuvent être en minuscules ou avec espaces)
    site_col = 'nom_site' if 'nom_site' in df_interventions.columns else 'Nom Site' if 'Nom Site' in df_interventions.columns else None
    num_col = 'numero_intervention' if 'numero_intervention' in df_interventions.columns else 'Numero Intervention' if 'Numero Intervention' in df_interventions.columns else None
    fact_col = 'facturation_intervention' if 'facturation_intervention' in df_interventions.columns else 'Facturation intervention' if 'Facturation intervention' in df_interventions.columns else None
    
    if site_col:
        site_stats = df_interventions.groupby(site_col).size().reset_index(name='Interventions')
        
        if fact_col:
            df_interventions[fact_col] = pd.to_numeric(df_interventions[fact_col], errors='coerce')
            fact_sum = df_interventions.groupby(site_col)[fact_col].sum().reset_index(name='Coût Total')
            site_stats = site_stats.merge(fact_sum, on=site_col, how='left')
        else:
            site_stats['Coût Total'] = 0
        
        site_stats.columns = ['Site', 'Interventions', 'Coût Total']
        site_stats = site_stats.sort_values('Interventions', ascending=False).head(10)
        site_stats['Coût Total'] = site_stats['Coût Total'].fillna(0)
        site_stats['Coût Moyen'] = (site_stats['Coût Total'] / site_stats['Interventions']).round(2)
        
        # Style le tableau
        st.dataframe(
            site_stats.style.format({
                'Interventions': '{:,}',
                'Coût Total': '{:,.0f} €',
                'Coût Moyen': '{:,.2f} €'
            }).background_gradient(subset=['Interventions', 'Coût Total'], cmap='YlOrRd'),
            use_container_width=True,
            height=400
        )
    else:
        st.info("ℹ️ Données de sites non disponibles")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # KPI 9: Carte Géographique des Sites
    # ==========================================
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">🗺️ Localisation des Sites</div>
    ''', unsafe_allow_html=True)
    
    if df_exposition is not None and not df_exposition.empty:
        # Préparer les données géographiques
        df_map = df_exposition[['latitude', 'longitude', 'nom_site', 'puissance_nominale__kwh_']].copy()
        df_map = df_map.dropna(subset=['latitude', 'longitude'])
        df_map['puissance_nominale__kwh_'] = pd.to_numeric(df_map['puissance_nominale__kwh_'], errors='coerce')
        
        # Supprimer les lignes avec puissance_nominale__kwh_ NaN pour éviter l'erreur de taille
        df_map = df_map.dropna(subset=['puissance_nominale__kwh_'])
        
        # Remplacer les valeurs nulles ou négatives par une valeur par défaut minimale
        df_map['puissance_nominale__kwh_'] = df_map['puissance_nominale__kwh_'].fillna(1)
        df_map = df_map[df_map['puissance_nominale__kwh_'] > 0]
        
        if not df_map.empty:
            # Créer la carte avec scatter_mapbox
            fig = px.scatter_mapbox(
                df_map,
                lat='latitude',
                lon='longitude',
                hover_name='nom_site',
                hover_data=['puissance_nominale__kwh_'],
                size='puissance_nominale__kwh_',
                size_max=30,
                color='puissance_nominale__kwh_',
                color_continuous_scale='Viridis',
                zoom=5,
                height=600,
                title="📍 Carte Interactive des Sites"
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(
                mapbox_style="open-street-map",
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Données géographiques incomplètes")
    else:
        st.info("ℹ️ Données d'exposition non disponibles")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # KPI 10: Graphique - Production vs Prévision
    # ==========================================
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">⚡ Performance de Production</div>
    ''', unsafe_allow_html=True)
    
    if df_calc_mensuel is not None and not df_calc_mensuel.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique Production Réelle vs Prévisionnelle
            if 'prod_reel' in df_calc_mensuel.columns and 'prod_pvsyst' in df_calc_mensuel.columns:
                df_prod = df_calc_mensuel[['date', 'prod_reel', 'prod_pvsyst']].copy()
                df_prod['prod_reel'] = pd.to_numeric(df_prod['prod_reel'], errors='coerce')
                df_prod['prod_pvsyst'] = pd.to_numeric(df_prod['prod_pvsyst'], errors='coerce')
                df_prod = df_prod.dropna(subset=['prod_reel', 'prod_pvsyst'])
                df_prod['date'] = pd.to_datetime(df_prod['date'], errors='coerce')
                df_prod = df_prod[df_prod['date'].notna()]
                df_prod = df_prod.sort_values('date')
                
                if not df_prod.empty:
                    # Agrégation mensuelle
                    df_prod['Mois'] = df_prod['date'].dt.to_period('M').astype(str)
                    df_monthly = df_prod.groupby('Mois').agg({
                        'prod_reel': 'sum',
                        'prod_pvsyst': 'sum'
                    }).reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_monthly['Mois'],
                        y=df_monthly['prod_pvsyst'],
                        name='Prévisionnelle',
                        line=dict(color='#0A84FF', width=3)
                    ))
                    fig.add_trace(go.Scatter(
                        x=df_monthly['Mois'],
                        y=df_monthly['prod_reel'],
                        name='Réelle',
                        line=dict(color='#10b981', width=3, dash='dash')
                    ))
                    fig = apply_glassmorphism_theme(fig)
                    fig.update_layout(
                        title="📊 Production Réelle vs Prévisionnelle",
                        xaxis_title="Mois",
                        yaxis_title="Production (kWh)",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("ℹ️ Données de production insuffisantes")
            else:
                st.info("ℹ️ Colonnes de production non disponibles")
        
        with col2:
            # Graphique Performance Ratio (PR)
            if 'pr_réel' in df_calc_mensuel.columns:
                df_pr = df_calc_mensuel[['date', 'pr_réel']].copy()
                df_pr['pr_réel'] = pd.to_numeric(df_pr['pr_réel'], errors='coerce')
                df_pr = df_pr.dropna(subset=['pr_réel'])
                df_pr['date'] = pd.to_datetime(df_pr['date'], errors='coerce')
                df_pr = df_pr[df_pr['date'].notna()].sort_values('date')
                
                if not df_pr.empty:
                    df_pr['Mois'] = df_pr['date'].dt.to_period('M').astype(str)
                    df_pr_monthly = df_pr.groupby('Mois')['pr_réel'].mean().reset_index()
                    
                    fig = px.bar(
                        df_pr_monthly,
                        x='Mois',
                        y='pr_réel',
                        title="📈 Performance Ratio (PR) Moyen",
                        labels={'pr_réel': 'PR (%)', 'Mois': 'Mois'},
                        color='pr_réel',
                        color_continuous_scale='Greens'
                    )
                    fig = apply_glassmorphism_theme(fig)
                    fig.update_layout(
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("ℹ️ Données PR insuffisantes")
            else:
                st.info("ℹ️ Colonne PR non disponible")
    
    # Footer
    st.markdown('<div class="footer">⚡ Dashboard KPI Energysoft - Généré le ' + 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

