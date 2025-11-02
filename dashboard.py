"""
Dashboard Streamlit pour visualiser les données Energysoft depuis SQLite
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Energysoft",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "energysoft_stats.db"

# Styles CSS glassmorphism/iOS materials
st.markdown("""
    <style>
    /* Variables CSS iOS Materials - Thème Clair */
    :root {
        --bg: linear-gradient(120deg, #f0f4ff 0%, #f7fafc 50%, #ffffff 100%);
        --glass: rgba(255, 255, 255, 0.6);
        --glass-strong: rgba(255, 255, 255, 0.8);
        --border: rgba(0, 0, 0, 0.08);
        --border-strong: rgba(0, 0, 0, 0.12);
        --hairline: rgba(0, 0, 0, 0.1);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        --shadow-strong: 0 10px 30px rgba(0, 0, 0, 0.15);
        --radius: 20px;
        --blur: 20px;
        --accent: #0A84FF;
        --text: #1f2937;
        --text-secondary: #4b5563;
    }
    
    /* Reset et base */
    * {
        box-sizing: border-box;
    }
    
    /* Background principal avec gradient clair */
    .stApp {
        background: var(--bg) fixed;
        font-family: ui-sans-serif, system-ui, -apple-system, "SF Pro Text", "SF Pro Display", 
                     "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        color: var(--text);
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
    
    /* Main container */
    .main .block-container {
        background: transparent;
        padding-top: 2rem;
    }
    
    /* Header principal */
    .main-header {
        font-size: clamp(22px, 3.5vw, 34px);
        font-weight: 700;
        color: var(--text);
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.2px;
    }
    
    /* Cartes glass pour metrics */
    .metric-card-glass {
        padding: 20px 24px;
        border-radius: var(--radius);
        background: var(--glass);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        backdrop-filter: blur(var(--blur)) saturate(160%);
        -webkit-backdrop-filter: blur(var(--blur)) saturate(160%);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-glass::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: inherit;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.4));
        mix-blend-mode: overlay;
        pointer-events: none;
    }
    
    /* Styling des metric cards Streamlit */
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        opacity: 0.9;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--accent) !important;
    }
    
    /* Sections glass */
    .glass-section {
        padding: 24px;
        border-radius: var(--radius);
        background: var(--glass);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        backdrop-filter: blur(var(--blur)) saturate(160%);
        -webkit-backdrop-filter: blur(var(--blur)) saturate(160%);
        margin: 16px 0;
    }
    
    /* Hairline separator */
    .hairline {
        position: relative;
        padding-top: 16px;
        margin-top: 16px;
    }
    
    .hairline::before {
        content: "";
        position: absolute;
        inset: 0 0 auto;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--hairline), transparent);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text) !important;
    }
    
    /* Text colors */
    p, span, div {
        color: var(--text) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: var(--text) !important;
    }
    
    /* Buttons glass effect */
    .stButton > button {
        background: color-mix(in oklab, var(--accent) 85%, white 0%) !important;
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
    
    .stButton > button:active {
        transform: translateY(1px);
    }
    
    /* Selectbox et inputs glass */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        color: var(--text) !important;
    }
    
    /* Segment control iOS-style pour radio */
    [data-testid="stRadio"] {
        display: inline-flex;
        padding: 4px;
        gap: 4px;
        border-radius: 12px;
        background: var(--glass);
        border: 1px solid var(--border);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
    
    /* Dataframe glass container */
    [data-testid="stDataFrameContainer"] {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 12px;
    }
    
    /* Plotly charts container */
    [data-testid="stPlotlyChart"] {
        background: var(--glass);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    /* Expander glass */
    [data-testid="stExpander"] {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Slider glass */
    .stSlider > div > div {
        background: var(--glass) !important;
    }
    
    /* Info/Warning/Success boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        background: var(--glass) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Navbar sticky glass (simulation) */
    .navbar-glass {
        position: sticky;
        top: 0;
        z-index: 100;
        padding: 14px 18px;
        border-bottom: 1px solid var(--border);
        backdrop-filter: blur(18px) saturate(140%);
        -webkit-backdrop-filter: blur(18px) saturate(140%);
        background: var(--glass);
    }
    
    /* Override Streamlit default styles */
    .main {
        background: transparent !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(table_name, limit=None):
    """Charge les données depuis SQLite avec cache"""
    if not os.path.exists(DB_PATH):
        st.error(f"❌ Base de données non trouvée: {DB_PATH}")
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")
        return None

@st.cache_data
def get_tables():
    """Récupère la liste des tables"""
    if not os.path.exists(DB_PATH):
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except:
        return []

def parse_date(date_str):
    """Parse une date depuis différents formats"""
    if pd.isna(date_str) or date_str == '':
        return None
    try:
        if isinstance(date_str, str):
            # Essayer différents formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '%m/%d/%Y']:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except:
                    continue
        return pd.to_datetime(date_str)
    except:
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
    # Navbar glass sticky (simulation avec markdown)
    st.markdown("""
        <div class="navbar-glass">
            <div style="font-weight: 700; letter-spacing: 0.2px; font-size: 1.2rem; color: var(--text);">
                📊 Dashboard Energysoft
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # En-tête principal avec style glass
    st.markdown("""
        <div class="glass-section" style="text-align: center; margin-bottom: 2rem;">
            <h1 class="main-header" style="margin-bottom: 8px;">📊 Dashboard Energysoft</h1>
            <p style="color: var(--text-secondary); opacity: 0.9; margin: 0;">
                Analyse des données de maintenance et performance Energysoft
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar avec navigation glass
    st.sidebar.markdown("""
        <div style="
            padding: 14px 18px;
            background: var(--glass);
            border: 1px solid var(--border);
            border-radius: 12px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            margin-bottom: 16px;
        ">
            <h2 style="margin: 0; color: var(--text); font-weight: 700;">🎯 Navigation</h2>
        </div>
    """, unsafe_allow_html=True)
    
    pages = {
        "📈 Vue d'ensemble": "overview",
        "🔧 Interventions": "interventions",
        "💼 Sites": "sites",
        "📅 Évolution Temporelle": "timeline",
        "💰 Facturation": "billing",
        "📋 Données Brutes": "raw_data"
    }
    
    selected_page = st.sidebar.radio("Sélectionner une page", list(pages.keys()))
    
    # Informations de la base avec style glass
    st.sidebar.markdown("""
        <div style="
            padding: 16px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            margin-top: 16px;
        ">
            <h3 style="margin: 0 0 12px 0; color: var(--text);">💾 Base de données</h3>
        </div>
    """, unsafe_allow_html=True)
    
    tables = get_tables()
    if tables:
        st.sidebar.markdown(f"""
            <div style="
                padding: 12px;
                background: rgba(10, 132, 255, 0.15);
                border: 1px solid rgba(10, 132, 255, 0.3);
                border-radius: 10px;
                margin: 8px 0;
                color: var(--text);
            ">
                ✅ {len(tables)} tables disponibles
            </div>
        """, unsafe_allow_html=True)
        with st.sidebar.expander("📋 Voir les tables"):
            for table in tables:
                st.markdown(f"<div style='color: var(--text); opacity: 0.9;'>  • {table}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
            <div style="
                padding: 12px;
                background: rgba(239, 68, 68, 0.15);
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 10px;
                margin: 8px 0;
                color: var(--text);
            ">
                ❌ Aucune table trouvée
            </div>
        """, unsafe_allow_html=True)
    
    # Page: Vue d'ensemble
    if pages[selected_page] == "overview":
        show_overview()
    
    # Page: Interventions
    elif pages[selected_page] == "interventions":
        show_interventions()
    
    # Page: Sites
    elif pages[selected_page] == "sites":
        show_sites()
    
    # Page: Évolution Temporelle
    elif pages[selected_page] == "timeline":
        show_timeline()
    
    # Page: Facturation
    elif pages[selected_page] == "billing":
        show_billing()
    
    # Page: Données Brutes
    elif pages[selected_page] == "raw_data":
        show_raw_data()

def show_overview():
    """Page de vue d'ensemble"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">📈 Vue d'ensemble</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Charger les données principales
    df_interventions = load_data("interventions")
    
    if df_interventions is None or df_interventions.empty:
        st.markdown("""
            <div style="
                padding: 16px;
                background: rgba(251, 191, 36, 0.15);
                border: 1px solid rgba(251, 191, 36, 0.3);
                border-radius: 12px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                color: var(--text);
            ">
                ⚠️ Aucune donnée disponible pour les interventions
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Métriques principales avec container glass
    st.markdown("""
        <div class="glass-section">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Métriques Principales</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_interventions = len(df_interventions)
    col1.metric("📊 Total Interventions", f"{total_interventions:,}")
    
    # Compter les sites uniques
    sites_col = "Nom Site"
    if sites_col in df_interventions.columns:
        unique_sites = df_interventions[sites_col].nunique()
        col2.metric("🏢 Sites Uniques", f"{unique_sites:,}")
    else:
        col2.metric("🏢 Sites", "N/A")
    
    # Dates
    date_col = "Date creation intervention"
    if date_col in df_interventions.columns:
        df_interventions[date_col] = pd.to_datetime(df_interventions[date_col], errors='coerce')
        dates_valid = df_interventions[date_col].dropna()
        if not dates_valid.empty:
            col3.metric("📅 Première Date", dates_valid.min().strftime("%Y-%m-%d"))
            col4.metric("📅 Dernière Date", dates_valid.max().strftime("%Y-%m-%d"))
    
    # Séparateur hairline
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    
    # Graphiques avec containers glass
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Visualisations</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Graphique 1: Distribution par site (top 10)
    with col1:
        st.subheader("🏢 Top 10 Sites")
        if sites_col in df_interventions.columns:
            site_counts = df_interventions[sites_col].value_counts().head(10)
            if not site_counts.empty:
                fig = px.bar(
                    x=site_counts.values,
                    y=site_counts.index,
                    orientation='h',
                    labels={'x': 'Nombre d\'interventions', 'y': 'Site'},
                    title="Interventions par site",
                    color_discrete_sequence=['#0A84FF']
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Graphique 2: Évolution dans le temps
    with col2:
        st.subheader("📅 Évolution Temporelle")
        if date_col in df_interventions.columns:
            df_interventions[date_col] = pd.to_datetime(df_interventions[date_col], errors='coerce')
            df_time = df_interventions[df_interventions[date_col].notna()].copy()
            if not df_time.empty:
                df_time['Année-Mois'] = df_time[date_col].dt.to_period('M').astype(str)
                monthly_counts = df_time['Année-Mois'].value_counts().sort_index()
                
                fig = px.line(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    labels={'x': 'Mois', 'y': 'Nombre d\'interventions'},
                    title="Évolution mensuelle",
                    color_discrete_sequence=['#0A84FF']
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Table récapitulative avec container glass
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📋 Aperçu des Données</h3>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_interventions.head(100), use_container_width=True)

def show_interventions():
    """Page dédiée aux interventions"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">🔧 Analyse des Interventions</h2>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data("interventions")
    
    if df is None or df.empty:
        st.warning("⚠️ Aucune donnée disponible")
        return
    
    # Filtres avec container glass
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">🔍 Filtres</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sites = ["Tous"] + sorted(df["Nom Site"].dropna().unique().tolist()) if "Nom Site" in df.columns else ["Tous"]
        selected_site = st.selectbox("Site", sites)
    
    with col2:
        status_col = "Status Intervention"
        if status_col in df.columns:
            statuses = ["Tous"] + sorted(df[status_col].dropna().unique().tolist())
            selected_status = st.selectbox("Statut", statuses)
        else:
            selected_status = "Tous"
    
    with col3:
        date_col = "Date creation intervention"
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            dates_valid = df[date_col].dropna()
            if not dates_valid.empty:
                min_date = dates_valid.min().date()
                max_date = dates_valid.max().date()
                date_range = st.date_input("Période", value=(min_date, max_date), min_value=min_date, max_value=max_date)
            else:
                date_range = None
        else:
            date_range = None
    
    # Appliquer les filtres
    df_filtered = df.copy()
    
    if selected_site != "Tous" and "Nom Site" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Nom Site"] == selected_site]
    
    if selected_status != "Tous" and status_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[status_col] == selected_status]
    
    if date_range and len(date_range) == 2 and date_col in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered[date_col].dt.date >= date_range[0]) &
            (df_filtered[date_col].dt.date <= date_range[1])
        ]
    
    # Métriques filtrées
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Résultats Filtrés</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("📊 Interventions Filtrées", f"{len(df_filtered):,}")
    col2.metric("📈 % du Total", f"{(len(df_filtered)/len(df)*100):.1f}%")
    
    # Graphiques
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Visualisations</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # Graphique 1: Distribution par statut
    with col1:
        st.subheader("📊 Répartition par Statut")
        if status_col in df_filtered.columns:
            status_counts = df_filtered[status_col].value_counts()
            if not status_counts.empty:
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Distribution des statuts",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig = apply_glassmorphism_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    # Graphique 2: Top créateurs
    with col2:
        st.subheader("👤 Top Créateurs")
        creator_col = "Createur Intervention"
        if creator_col in df_filtered.columns:
            creator_counts = df_filtered[creator_col].value_counts().head(10)
            if not creator_counts.empty:
                fig = px.bar(
                    x=creator_counts.index,
                    y=creator_counts.values,
                    labels={'x': 'Créateur', 'y': 'Nombre'},
                    title="Interventions par créateur",
                    color_discrete_sequence=['#0A84FF']
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    
    # Table des données filtrées
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📋 Données Filtrées</h3>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True, height=400)

def show_sites():
    """Page d'analyse par site"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">🏢 Analyse par Site</h2>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data("interventions")
    
    if df is None or df.empty or "Nom Site" not in df.columns:
        st.warning("⚠️ Aucune donnée de sites disponible")
        return
    
    # Statistiques par site
    site_stats = df.groupby("Nom Site").agg({
        "Numero Intervention": "count",
    }).rename(columns={"Numero Intervention": "Nombre d'interventions"})
    
    # Ajouter d'autres statistiques si disponibles
    date_col = "Date creation intervention"
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        site_stats["Première intervention"] = df.groupby("Nom Site")[date_col].min()
        site_stats["Dernière intervention"] = df.groupby("Nom Site")[date_col].max()
    
    # Trier par nombre d'interventions
    site_stats = site_stats.sort_values("Nombre d'interventions", ascending=False)
    
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Statistiques par Site</h3>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(site_stats, use_container_width=True)
    
    # Graphique
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📈 Visualisation</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        top_n = st.slider("Nombre de sites à afficher", 5, 50, 20)
        top_sites = site_stats.head(top_n)
        
        fig = px.bar(
            x=top_sites.index,
            y=top_sites["Nombre d'interventions"],
            labels={'x': 'Site', 'y': 'Nombre d\'interventions'},
            title=f"Top {top_n} Sites",
            color_discrete_sequence=['#0A84FF']
        )
        fig = apply_glassmorphism_theme(fig)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart
        fig = px.pie(
            values=top_sites["Nombre d'interventions"],
            names=top_sites.index,
            title=f"Répartition Top {top_n} Sites",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

def show_timeline():
    """Page d'évolution temporelle"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">📅 Évolution Temporelle</h2>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data("interventions")
    
    if df is None or df.empty:
        st.warning("⚠️ Aucune donnée disponible")
        return
    
    date_col = "Date creation intervention"
    if date_col not in df.columns:
        st.warning("⚠️ Colonne de date non trouvée")
        return
    
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df_time = df[df[date_col].notna()].copy()
    
    if df_time.empty:
        st.warning("⚠️ Aucune date valide trouvée")
        return
    
    # Options d'agrégation
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">⚙️ Options d'affichage</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        period = st.selectbox("Période d'agrégation", ["Jour", "Semaine", "Mois", "Année"])
    
    with col2:
        group_by = st.selectbox("Grouper par", ["Aucun", "Site", "Statut"])
    
    # Préparer les données
    period_map = {
        "Jour": "D",
        "Semaine": "W",
        "Mois": "M",
        "Année": "Y"
    }
    
    df_time['Période'] = df_time[date_col].dt.to_period(period_map[period]).astype(str)
    
    if group_by == "Site" and "Nom Site" in df_time.columns:
        timeline_data = df_time.groupby(['Période', 'Nom Site']).size().reset_index(name='Count')
        fig = px.line(
            timeline_data,
            x='Période',
            y='Count',
            color='Nom Site',
            title=f"Évolution par {period.lower()} et par site",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    elif group_by == "Statut" and "Status Intervention" in df_time.columns:
        timeline_data = df_time.groupby(['Période', 'Status Intervention']).size().reset_index(name='Count')
        fig = px.line(
            timeline_data,
            x='Période',
            y='Count',
            color='Status Intervention',
            title=f"Évolution par {period.lower()} et par statut",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    else:
        timeline_data = df_time.groupby('Période').size().reset_index(name='Count')
        fig = px.line(
            timeline_data,
            x='Période',
            y='Count',
            title=f"Évolution par {period.lower()}",
            color_discrete_sequence=['#0A84FF']
        )
    
    fig = apply_glassmorphism_theme(fig)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Graphique en barres
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Vue en barres</h3>
        </div>
    """, unsafe_allow_html=True)
    fig_bar = px.bar(
        timeline_data if group_by == "Aucun" else timeline_data.pivot_table(
            index='Période',
            columns=group_by,
            values='Count',
            aggfunc='sum'
        ).reset_index().melt(id_vars='Période', var_name=group_by, value_name='Count'),
        x='Période',
        y='Count',
        color=group_by if group_by != "Aucun" else None,
        title=f"Nombre d'interventions par {period.lower()}",
        color_discrete_sequence=px.colors.qualitative.Set3 if group_by != "Aucun" else ['#0A84FF']
    )
    fig_bar = apply_glassmorphism_theme(fig_bar)
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

def show_billing():
    """Page d'analyse de facturation"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">💰 Analyse de Facturation</h2>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data("interventions")
    
    if df is None or df.empty:
        st.warning("⚠️ Aucune donnée disponible")
        return
    
    billing_col = "Facturation intervention"
    
    if billing_col not in df.columns:
        st.info("ℹ️ Colonne de facturation non disponible dans les données")
        
        # Afficher les colonnes disponibles pour référence
        st.subheader("📋 Colonnes disponibles")
        st.code(", ".join(df.columns.tolist()))
        return
    
    # Convertir en numérique si possible
    df[billing_col] = pd.to_numeric(df[billing_col], errors='coerce')
    df_billing = df[df[billing_col].notna() & (df[billing_col] > 0)].copy()
    
    if df_billing.empty:
        st.warning("⚠️ Aucune donnée de facturation valide")
        return
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    total_billing = df_billing[billing_col].sum()
    avg_billing = df_billing[billing_col].mean()
    median_billing = df_billing[billing_col].median()
    count_billing = len(df_billing)
    
    col1.metric("💰 Total Facturé", f"{total_billing:,.0f} €" if total_billing < 1000000 else f"{total_billing/1000:,.0f} K€")
    col2.metric("📊 Moyenne", f"{avg_billing:,.0f} €")
    col3.metric("📈 Médiane", f"{median_billing:,.0f} €")
    col4.metric("🔢 Interventions Facturées", f"{count_billing:,}")
    
    # Graphiques
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📊 Visualisations</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribution")
        fig = px.histogram(
            df_billing,
            x=billing_col,
            nbins=50,
            title="Distribution des montants facturés",
            color_discrete_sequence=['#0A84FF']
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Top 10 par Montant")
        top_billing = df_billing.nlargest(10, billing_col)
        fig = px.bar(
            x=top_billing[billing_col],
            y=top_billing.index,
            orientation='h',
            title="Top 10 interventions facturées",
            color_discrete_sequence=['#0A84FF']
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse par site si disponible
    if "Nom Site" in df_billing.columns:
        st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-section" style="margin-top: 24px;">
                <h3 style="margin: 0 0 16px 0; color: var(--text);">🏢 Facturation par Site</h3>
            </div>
        """, unsafe_allow_html=True)
        site_billing = df_billing.groupby("Nom Site")[billing_col].agg(['sum', 'mean', 'count']).sort_values('sum', ascending=False)
        site_billing.columns = ['Total Facturé', 'Moyenne', 'Nombre']
        st.dataframe(site_billing.head(20), use_container_width=True)
        
        fig = px.bar(
            x=site_billing.head(15).index,
            y=site_billing.head(15)['Total Facturé'],
            title="Facturation totale par site (Top 15)",
            color_discrete_sequence=['#0A84FF']
        )
        fig = apply_glassmorphism_theme(fig)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def show_raw_data():
    """Page de données brutes"""
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: var(--text);">📋 Données Brutes</h2>
        </div>
    """, unsafe_allow_html=True)
    
    tables = get_tables()
    
    if not tables:
        st.error("❌ Aucune table disponible")
        return
    
    selected_table = st.selectbox("Sélectionner une table", tables)
    
    df = load_data(selected_table)
    
    if df is None:
        st.error("❌ Erreur lors du chargement")
        return
    
    st.markdown(f"""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h3 style="margin: 0 0 8px 0; color: var(--text);">📊 Table: {selected_table}</h3>
            <p style="margin: 0; color: var(--text-secondary); opacity: 0.9;">📈 {len(df):,} lignes × {len(df.columns)} colonnes</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Options d'affichage
    st.markdown("""
        <div class="glass-section" style="margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">⚙️ Options d'affichage</h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        n_rows = st.slider("Nombre de lignes à afficher", 10, 1000, 100)
    with col2:
        show_all_cols = st.checkbox("Afficher toutes les colonnes", value=False)
    
    # Afficher les données
    df_display = df.head(n_rows)
    if not show_all_cols and len(df.columns) > 10:
        df_display = df_display.iloc[:, :10]
        st.info(f"⚠️ Affichage des 10 premières colonnes sur {len(df.columns)}. Cochez 'Afficher toutes les colonnes' pour voir tout.")
    
    st.dataframe(df_display, use_container_width=True, height=500)
    
    # Statistiques
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-section" style="margin-top: 24px;">
            <h3 style="margin: 0 0 16px 0; color: var(--text);">📈 Statistiques</h3>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df.describe(), use_container_width=True)

if __name__ == "__main__":
    main()

