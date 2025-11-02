import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sqlite3
from datetime import datetime
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Exploitation Apex",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = "Dashboard Apex.db"

# ============================================
# STYLES CSS GLASSMORPHISM iOS
# ============================================
st.markdown("""
    <style>
    /* Variables CSS iOS Materials - Thème Clair */
    :root {
        --bg: linear-gradient(135deg, #d4e3fc 0%, #e0ebfa 20%, #ecf2fb 40%, #f5f8fc 60%, #fafcfe 80%, #ffffff 100%);
        --glass: rgba(255, 255, 255, 0.65);
        --glass-strong: rgba(255, 255, 255, 0.85);
        --border: rgba(0, 0, 0, 0.1);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        --radius: 20px;
        --blur: 20px;
        --accent: #0A84FF;
        --text: #1f2937;
        --text-secondary: #4b5563;
    }
    
    /* Background principal avec gradient clair */
    html, body {
        background: linear-gradient(135deg, #d4e3fc 0%, #e0ebfa 20%, #ecf2fb 40%, #f5f8fc 60%, #fafcfe 80%, #ffffff 100%) fixed !important;
        background-attachment: fixed !important;
    }
    
    div[data-testid="stAppViewContainer"],
    section[data-testid="stAppViewContainer"],
    .stApp,
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
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}
    
    /* Metrics glass */
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        opacity: 0.9;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* Metric containers glass */
    div[data-testid="stMetricContainer"],
    div[data-testid="stMetricContainer"] > div {
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        backdrop-filter: blur(20px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        margin: 8px !important;
    }
    
    /* Buttons glassmorphism modern */
    .stButton > button {
        background: rgba(10, 132, 255, 0.15) !important;
        color: #0A84FF !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        border: 1.5px solid rgba(10, 132, 255, 0.4) !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        backdrop-filter: blur(10px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(10px) saturate(160%) !important;
        box-shadow: 0 4px 12px rgba(10, 132, 255, 0.15) !important;
        transition: all 0.2s ease !important;
        min-height: auto !important;
        height: auto !important;
    }
    
    .stButton > button:hover {
        background: rgba(10, 132, 255, 0.25) !important;
        border-color: rgba(10, 132, 255, 0.6) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(10, 132, 255, 0.25) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(10, 132, 255, 0.2) !important;
    }
    
    /* Cacher les divs vides avec style glassmorphism */
    div[style*="padding: 16px"][style*="background: rgba(255, 255, 255, 0.5)"][style*="border-radius: 20px"]:empty {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }
    </style>
    <script>
    // Supprime les divs vides avec style glassmorphism
    function removeEmptyGlassDivs() {
        // Sélectionner tous les divs avec le style glassmorphism
        const allDivs = document.querySelectorAll('div[style*="padding: 16px"][style*="background: rgba(255, 255, 255, 0.5)"][style*="border-radius: 20px"]');
        
        allDivs.forEach(div => {
            // Vérifier si le div est vide (pas de contenu texte ni d'éléments enfants)
            const hasText = div.textContent.trim().length > 0;
            const hasChildren = div.children.length > 0;
            const hasStreamlitContent = div.querySelector('[data-testid]') !== null;
            
            // Si le div est vide (pas de texte, pas d'enfants, pas de contenu Streamlit)
            if (!hasText && !hasChildren && !hasStreamlitContent) {
                // Supprimer le conteneur parent Streamlit si c'est un conteneur markdown vide
                const stMarkdownContainer = div.closest('[data-testid="stMarkdownContainer"]');
                const stElementContainer = div.closest('[data-testid="stElementContainer"]');
                
                if (stMarkdownContainer) {
                    // Vérifier si le conteneur markdown ne contient que ce div vide
                    const allContent = Array.from(stMarkdownContainer.querySelectorAll('*')).filter(el => {
                        const text = el.textContent.trim();
                        return text.length > 0 && !el.querySelector('[data-testid]');
                    });
                    if (allContent.length === 0) {
                        stElementContainer?.remove() || stMarkdownContainer.remove();
                    } else {
                        div.remove();
                    }
                } else {
                    div.remove();
                }
            }
        });
    }
    
    // Exécuter immédiatement et après chargement
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', removeEmptyGlassDivs);
    } else {
        removeEmptyGlassDivs();
    }
    
    // Réexécuter après délais pour capturer les divs créés dynamiquement
    setTimeout(removeEmptyGlassDivs, 100);
    setTimeout(removeEmptyGlassDivs, 500);
    setTimeout(removeEmptyGlassDivs, 1000);
    setTimeout(removeEmptyGlassDivs, 2000);
    
    // Observer les mutations du DOM pour détecter les nouveaux divs
    const observer = new MutationObserver(function(mutations) {
        removeEmptyGlassDivs();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    </script>
""", unsafe_allow_html=True)


# ============================================
# FONCTIONS DE FORMATAGE FRANÇAIS
# ============================================

def format_french_number(value, decimals=1, use_thousands_sep=False):
    """
    Formate un nombre en format français :
    - Virgule pour décimale
    - Pas de séparateur de milliers par défaut (ou espace si use_thousands_sep=True)
    """
    if value is None:
        return "0"
    
    # Arrondir selon le nombre de décimales
    if decimals > 0:
        formatted = f"{value:.{decimals}f}"
    else:
        formatted = f"{int(value)}"
    
    # Séparer partie entière et décimale
    if "." in formatted:
        integer_part, decimal_part = formatted.split(".")
        # Remplacer le point par une virgule pour la décimale
        formatted = integer_part + "," + decimal_part
    else:
        integer_part = formatted
        decimal_part = None
    
    # Ajouter séparateur de milliers si demandé (espace tous les 3 chiffres)
    if use_thousands_sep and len(integer_part) > 3:
        # Ajouter des espaces de droite à gauche
        reversed_part = integer_part[::-1]
        spaced_part = " ".join(reversed_part[i:i+3] for i in range(0, len(reversed_part), 3))
        integer_part = spaced_part[::-1]
        formatted = integer_part + ("," + decimal_part if decimal_part else "")
    
    return formatted

def format_energy(value_gwh, decimals=2):
    """
    Formate une valeur énergétique en GWh ou TWh selon la grandeur.
    Convertit automatiquement GWh → TWh si >= 1000.
    Format français avec virgule décimale.
    """
    if value_gwh is None:
        return "0 GWh"
    
    if value_gwh >= 1000:
        # Convertir en TWh
        value_twh = value_gwh / 1000
        formatted = format_french_number(value_twh, decimals=decimals)
        return f"{formatted} TWh"
    else:
        formatted = format_french_number(value_gwh, decimals=decimals)
        return f"{formatted} GWh"

def format_currency(value_keuro, decimals=3, use_thousands_sep=False):
    """
    Formate une valeur monétaire en k€ ou M€ selon la grandeur.
    Convertit automatiquement k€ → M€ si >= 1000.
    Format français avec virgule décimale (pas de séparateur de milliers pour les décimaux).
    """
    if value_keuro is None:
        return "0 k€"
    
    if value_keuro >= 1000:
        # Convertir en M€
        value_meuro = value_keuro / 1000
        # Pour les décimaux, on ne veut pas de séparateur de milliers
        formatted = format_french_number(value_meuro, decimals=decimals, use_thousands_sep=False)
        return f"{formatted} M€"
    else:
        formatted = format_french_number(value_keuro, decimals=0, use_thousands_sep=False)
        return f"{formatted} k€"

def format_count(value):
    """
    Formate un nombre entier sans séparateur de milliers.
    Format français : pas de séparateur, juste le nombre.
    """
    if value is None:
        return "0"
    
    return str(int(value))

def format_power(value_kw, decimals=1):
    """
    Formate une valeur de puissance avec optimisation automatique de l'unité.
    Si < 1 kW : convertit en W
    Si >= 1 kW et < 1000 kW : garde en kW
    Si >= 1000 kW : convertit en MW
    Format français avec virgule décimale.
    """
    if value_kw is None or value_kw == 0:
        return "0 W"
    
    if value_kw < 1:
        # Convertir en W (watts)
        value_w = value_kw * 1000
        formatted = format_french_number(value_w, decimals=0, use_thousands_sep=False)
        return f"{formatted} W"
    elif value_kw >= 1000:
        # Convertir en MWc (Méga Watt crête)
        value_mw = value_kw / 1000
        formatted = format_french_number(value_mw, decimals=decimals, use_thousands_sep=False)
        return f"{formatted} MWc"
    else:
        # Garder en kWc (kilo Watt crête)
        formatted = format_french_number(value_kw, decimals=decimals, use_thousands_sep=False)
        return f"{formatted} kWc"

def format_power_capacity(value_kwc, decimals=0):
    """
    Formate une valeur de puissance crête (kWc) avec optimisation automatique.
    Pour les puissances crête, on utilise kWc ou MWc selon la grandeur.
    Format français avec virgule décimale.
    """
    if value_kwc is None or value_kwc == 0:
        return "0 kWc"
    
    if value_kwc >= 1000:
        # Convertir en MWc (Méga Watt crête)
        value_mwc = value_kwc / 1000
        formatted = format_french_number(value_mwc, decimals=decimals, use_thousands_sep=False)
        return f"{formatted} MWc"
    else:
        # Garder en kWc (kilo Watt crête)
        formatted = format_french_number(value_kwc, decimals=decimals, use_thousands_sep=False)
        return f"{formatted} kWc"

# ============================================
# FONCTIONS DE CHARGEMENT DES DONNÉES
# ============================================

@st.cache_data(ttl=3600)
def load_data_from_db(query):
    """Charge les données depuis la base SQLite"""
    if not os.path.exists(DB_PATH):
        st.error(f"❌ Base de données '{DB_PATH}' introuvable")
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        return None


def get_header_stats():
    """Récupère les statistiques du header (date MAJ, nb sites, puissance totale)"""
    # Date de mise à jour
    query_date = "SELECT MAX(date_maj_donnees) as date_maj FROM exposition"
    df_date = load_data_from_db(query_date)
    date_maj = df_date['date_maj'].iloc[0] if df_date is not None and not df_date.empty else "N/A"
    
    # Nombre de sites
    query_sites = "SELECT COUNT(DISTINCT id_site) as nb_sites FROM exposition"
    df_sites = load_data_from_db(query_sites)
    nb_sites = int(df_sites['nb_sites'].iloc[0]) if df_sites is not None and not df_sites.empty else 0
    
    # Puissance totale
    query_puissance = "SELECT SUM(puissance_nominale__kWc_) as puissance_totale FROM exposition"
    df_puissance = load_data_from_db(query_puissance)
    puissance_totale = df_puissance['puissance_totale'].iloc[0] if df_puissance is not None and not df_puissance.empty else 0
    
    return date_maj, nb_sites, puissance_totale


def get_kpi_sites_mis_en_service(annee):
    """Nombre de sites mis en service pour une année donnée"""
    query = f"""
    SELECT COUNT(DISTINCT id_site) as nb_sites
    FROM exposition
    WHERE CAST(strftime('%Y', date_mise_en_service) AS INTEGER) = {annee}
    """
    df = load_data_from_db(query)
    return int(df['nb_sites'].iloc[0]) if df is not None and not df.empty else 0


def get_kpi_production_totale(annee):
    """Production réelle totale pour une année donnée (en GWh)"""
    query = f"""
    SELECT SUM(prod_reel) / 1000 as prod_totale_gwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    """
    df = load_data_from_db(query)
    return df['prod_totale_gwh'].iloc[0] if df is not None and not df.empty and df['prod_totale_gwh'].iloc[0] is not None else 0


def get_kpi_puissance_installee(annee):
    """Puissance installée cumulée jusqu'à une année donnée (en MW)"""
    query = f"""
    SELECT SUM(puissance_nominale__kWc_) / 1000 as puissance_mw
    FROM exposition
    WHERE CAST(strftime('%Y', date_mise_en_service) AS INTEGER) <= {annee}
    """
    df = load_data_from_db(query)
    return df['puissance_mw'].iloc[0] if df is not None and not df.empty and df['puissance_mw'].iloc[0] is not None else 0


def get_kpi_deviation_pr(annee):
    """Déviation moyenne du Performance Ratio pour une année donnée (en %)"""
    query = f"""
    SELECT AVG(dev_pr) as dev_pr_moyen
    FROM calculs_annuel_sites
    WHERE annee = {annee} AND dev_pr IS NOT NULL
    """
    df = load_data_from_db(query)
    return df['dev_pr_moyen'].iloc[0] if df is not None and not df.empty and df['dev_pr_moyen'].iloc[0] is not None else 0


def get_kpi_pr_moyen(annee):
    """Performance Ratio moyen pour une année donnée"""
    query = f"""
    SELECT AVG([pr_réel]) as pr_moyen
    FROM calculs_annuel_sites
    WHERE annee = {annee} AND [pr_réel] IS NOT NULL
    """
    df = load_data_from_db(query)
    return df['pr_moyen'].iloc[0] if df is not None and not df.empty and df['pr_moyen'].iloc[0] is not None else 0


def get_kpi_production_budget(annee):
    """Production budget pour une année donnée (en GWh)"""
    query = f"""
    SELECT SUM(prod_pvsyst) / 1000 as prod_budget_gwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    """
    df = load_data_from_db(query)
    return df['prod_budget_gwh'].iloc[0] if df is not None and not df.empty and df['prod_budget_gwh'].iloc[0] is not None else 0


def get_kpi_interventions(annee=None, mois=None):
    """Nombre total d'interventions"""
    if annee and mois:
        query = f"""
        SELECT COUNT(*) as nb_interventions
        FROM interventions
        WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
        AND CAST(strftime('%m', date_creation_intervention) AS INTEGER) = {mois}
        """
    elif annee:
        query = f"""
        SELECT COUNT(*) as nb_interventions
        FROM interventions
        WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
        """
    else:
        query = "SELECT COUNT(*) as nb_interventions FROM interventions"
    df = load_data_from_db(query)
    return int(df['nb_interventions'].iloc[0]) if df is not None and not df.empty else 0


def get_kpi_cout_maintenance(annee=None):
    """Coût total de maintenance (en k€)"""
    if annee:
        query = f"""
        SELECT SUM(facturation_intervention) / 1000 as cout_k
        FROM interventions
        WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
        AND facturation_intervention IS NOT NULL
        """
    else:
        query = """
        SELECT SUM(facturation_intervention) / 1000 as cout_k
        FROM interventions
        WHERE facturation_intervention IS NOT NULL
        """
    df = load_data_from_db(query)
    return df['cout_k'].iloc[0] if df is not None and not df.empty and df['cout_k'].iloc[0] is not None else 0


def get_kpi_disponibilite(annee):
    """Taux de disponibilité contractuelle moyen"""
    query = f"""
    SELECT AVG(dispo_contrat) as dispo_moyen
    FROM calculs_annuel_sites
    WHERE annee = {annee} AND dispo_contrat IS NOT NULL
    """
    df = load_data_from_db(query)
    return df['dispo_moyen'].iloc[0] if df is not None and not df.empty and df['dispo_moyen'].iloc[0] is not None else 0


def get_kpi_ca_total(annee):
    """Chiffre d'Affaires total (en k€)"""
    query = f"""
    SELECT SUM(prod_reel_distributeur * tarif_edf / 1000) as ca_k
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    """
    df = load_data_from_db(query)
    return df['ca_k'].iloc[0] if df is not None and not df.empty and df['ca_k'].iloc[0] is not None else 0


def get_kpi_taux_resolution(annee=None):
    """Taux de résolution des interventions"""
    if annee:
        query = f"""
        SELECT 
            COUNT(CASE WHEN ticket_resolu = 1 THEN 1 END) * 100.0 / COUNT(*) as taux_resolution
        FROM interventions
        WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
        """
    else:
        query = """
        SELECT 
            COUNT(CASE WHEN ticket_resolu = 1 THEN 1 END) * 100.0 / COUNT(*) as taux_resolution
        FROM interventions
        """
    df = load_data_from_db(query)
    return df['taux_resolution'].iloc[0] if df is not None and not df.empty and df['taux_resolution'].iloc[0] is not None else 0


def get_kpi_onduleurs_total():
    """Nombre total d'onduleurs"""
    query = "SELECT COUNT(*) as total FROM onduleurs_view"
    df = load_data_from_db(query)
    return int(df['total'].iloc[0]) if df is not None and not df.empty else 0


def get_kpi_puissance_onduleurs():
    """Puissance totale des onduleurs (en MW)"""
    query = "SELECT SUM(nominal_power) / 1000 as puissance_mw FROM onduleurs_view"
    df = load_data_from_db(query)
    return df['puissance_mw'].iloc[0] if df is not None and not df.empty and df['puissance_mw'].iloc[0] is not None else 0


# ============================================
# NOUVEAUX KPIs ANALYSE COMPARATIVE
# ============================================

def get_prevision_fin_annee_runrate(annee):
    """Prévision fin d'année - run-rate (Production_YTD * 12 / nb_mois_disponibles)"""
    # Compter le nombre de mois disponibles
    query_mois = f"""
    SELECT COUNT(DISTINCT CAST(strftime('%m', date) AS INTEGER)) as nb_mois
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND prod_reel IS NOT NULL
    """
    df_mois = load_data_from_db(query_mois)
    nb_mois = int(df_mois['nb_mois'].iloc[0]) if df_mois is not None and not df_mois.empty else 1
    
    # Production YTD
    prod_ytd = get_kpi_production_totale(annee)
    
    # Prévision run-rate
    prevision = (prod_ytd * 12 / nb_mois) if nb_mois > 0 else 0
    
    return prevision, prod_ytd, nb_mois


def get_delta_production_vs_2024(annee, mois_max=9):
    """Δ Production vs 2024 pour les mêmes mois (Jan-Sep)"""
    query_2025 = f"""
    SELECT SUM(prod_reel) / 1000 as prod_gwh
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND CAST(strftime('%m', date) AS INTEGER) <= {mois_max}
    AND prod_reel IS NOT NULL
    """
    
    query_2024 = f"""
    SELECT SUM(prod_reel) / 1000 as prod_gwh
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = 2024
    AND CAST(strftime('%m', date) AS INTEGER) <= {mois_max}
    AND prod_reel IS NOT NULL
    """
    
    df_2025 = load_data_from_db(query_2025)
    df_2024 = load_data_from_db(query_2024)
    
    prod_2025 = df_2025['prod_gwh'].iloc[0] if df_2025 is not None and not df_2025.empty else 0
    prod_2024 = df_2024['prod_gwh'].iloc[0] if df_2024 is not None and not df_2024.empty else 0
    
    delta_gwh = prod_2025 - prod_2024
    delta_pct = (delta_gwh / prod_2024 * 100) if prod_2024 > 0 else 0
    
    return delta_gwh, delta_pct, prod_2025, prod_2024


def get_taille_moyenne_site():
    """Taille moyenne d'un site (en kWc)"""
    query = """
    SELECT 
        SUM(puissance_nominale__kWc_) / COUNT(DISTINCT id_site) as taille_moyenne_kwc
    FROM exposition
    WHERE puissance_nominale__kWc_ > 0
    """
    df = load_data_from_db(query)
    return df['taille_moyenne_kwc'].iloc[0] if df is not None and not df.empty and df['taille_moyenne_kwc'].iloc[0] is not None else 0


def get_revenus_oa_vs_spot(annee):
    """Revenus OA vs Spot (OA uniquement car prod_spot n'existe pas dans calculs_annuel_sites)"""
    query = f"""
    SELECT 
        SUM(prod_reel_distributeur * tarif_edf) / 1000000 as revenus_oa_me,
        0 as revenus_spot_me,
        SUM(prod_reel_distributeur * tarif_edf) / 1000000 as revenus_totaux_me
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    """
    df = load_data_from_db(query)
    # Pour l'instant, les revenus spot ne sont pas disponibles dans calculs_annuel_sites
    # On utilise seulement les revenus OA (Obligation d'Achat)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_revenus_oa_vs_spot_mensuel(annee):
    """Revenus OA mensuel (spot non disponible dans calculs_mensuel_sites)"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        SUM(prod_reel_distributeur * tarif) / 1000000 as revenus_oa_me,
        0 as revenus_spot_me
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_prix_vente_moyen_realise(annee):
    """Prix de vente moyen réalisé (€/MWh)"""
    query = f"""
    SELECT 
        SUM(prod_reel_distributeur * tarif_edf) / 1000 as ca_total_k,
        SUM(prod_reel) / 1000 as production_mwh,
        SUM(prod_reel_distributeur * tarif_edf) / 1000 / NULLIF(SUM(prod_reel) / 1000, 0) as prix_moyen_euro_mwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel IS NOT NULL
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_evolution_production_annuelle():
    """Évolution production annuelle (3 dernières années)"""
    query = """
    SELECT 
        CAST(annee AS INTEGER) as annee,
        SUM(prod_reel) / 1000 as prod_gwh
    FROM calculs_annuel_sites
    WHERE annee >= (SELECT MAX(CAST(annee AS INTEGER)) - 2 FROM calculs_annuel_sites)
    GROUP BY annee
    ORDER BY annee
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_production_irradiation_mensuelle_cumulee():
    """Production cumulée mensuelle et déviation PR mensuelle pour 2023, 2024, 2025"""
    # Récupérer les données mensuelles pour chaque année
    data = {}
    mois_complets = pd.DataFrame({'mois': range(1, 13)})
    
    for annee in [2023, 2024, 2025]:
        query = f"""
        SELECT 
            CAST(strftime('%m', date) AS INTEGER) as mois,
            SUM(prod_reel) as prod_reel_mwh,
            SUM(prod_pvsyst) as prod_pvsyst_mwh,
            AVG(dev_pr) as dev_pr_moyenne
        FROM calculs_mensuel_sites
        WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
        AND dev_pr IS NOT NULL
        GROUP BY mois
        ORDER BY mois
        """
        df = load_data_from_db(query)
        
        if df is not None and not df.empty:
            # Créer un DataFrame complet pour les 12 mois
            df = mois_complets.merge(df, on='mois', how='left')
            df['annee'] = annee
            df['prod_reel_mwh'] = df['prod_reel_mwh'].fillna(0)
            df['prod_pvsyst_mwh'] = df['prod_pvsyst_mwh'].fillna(0)
            df['dev_pr_moyenne'] = df['dev_pr_moyenne'].fillna(0)
            
            # Calculer les cumuls pour la production réelle et PVsyst
            df['prod_cumule_mwh'] = df['prod_reel_mwh'].cumsum()
            df['prod_pvsyst_cumule_mwh'] = df['prod_pvsyst_mwh'].cumsum()
            
            data[annee] = df
    
    # Pour 2025, calculer la simulation Nov-Déc si manquante
    if 2025 in data:
        df_2025 = data[2025].copy()
        dernier_mois = df_2025[df_2025['prod_reel_mwh'] > 0]['mois'].max()
        
        if dernier_mois is not None and dernier_mois < 12:
            # Récupérer l'irradiation de Nov-Déc 2024 pour la simulation de production
            query_irra_2024 = """
            SELECT 
                CAST(strftime('%m', date) AS INTEGER) as mois,
                SUM(irra_reel) as irra_reel
            FROM calculs_mensuel_sites
            WHERE CAST(strftime('%Y', date) AS INTEGER) = 2024
            AND CAST(strftime('%m', date) AS INTEGER) IN (11, 12)
            GROUP BY mois
            ORDER BY mois
            """
            df_irra_2024 = load_data_from_db(query_irra_2024)
            
            # Récupérer la déviation PR moyenne de Nov-Déc 2024 pour estimer celle de 2025
            query_dev_pr_2024 = """
            SELECT 
                CAST(strftime('%m', date) AS INTEGER) as mois,
                AVG(dev_pr) as dev_pr_moyenne
            FROM calculs_mensuel_sites
            WHERE CAST(strftime('%Y', date) AS INTEGER) = 2024
            AND CAST(strftime('%m', date) AS INTEGER) IN (11, 12)
            AND dev_pr IS NOT NULL
            GROUP BY mois
            ORDER BY mois
            """
            df_dev_pr_2024 = load_data_from_db(query_dev_pr_2024)
            
            # Récupérer la production totale installée en 2025
            query_puissance_2025 = """
            SELECT 
                SUM(e.puissance_nominale__kWc_) as puissance_totale_kwc
            FROM exposition e
            WHERE e.date_mise_en_service <= '2025-12-31'
            """
            df_puissance = load_data_from_db(query_puissance_2025)
            
            if df_irra_2024 is not None and not df_irra_2024.empty and df_puissance is not None and not df_puissance.empty:
                puissance_totale_kwc = df_puissance.iloc[0]['puissance_totale_kwc']
                irra_nov_dec_2024_total = df_irra_2024['irra_reel'].sum()
                
                # Calculer le ratio production/irradiation moyen pour 2025 (mois 1-10)
                df_2025_data = df_2025[df_2025['mois'] <= dernier_mois]
                if not df_2025_data.empty:
                    prod_totale_m1_10 = df_2025_data['prod_reel_mwh'].sum()
                    prod_pvsyst_totale_m1_10 = df_2025_data['prod_pvsyst_mwh'].sum()
                    
                    # Calculer l'irradiation totale des mois 1-10 pour 2025
                    query_irra_2025_m1_10 = """
                    SELECT SUM(irra_reel) as irra_totale
                    FROM calculs_mensuel_sites
                    WHERE CAST(strftime('%Y', date) AS INTEGER) = 2025
                    AND CAST(strftime('%m', date) AS INTEGER) <= 10
                    """
                    df_irra_2025_m1_10 = load_data_from_db(query_irra_2025_m1_10)
                    irra_totale_m1_10 = df_irra_2025_m1_10.iloc[0]['irra_totale'] if df_irra_2025_m1_10 is not None and not df_irra_2025_m1_10.empty else 0
                    
                    # Récupérer la production PVsyst de Nov-Déc 2024 pour estimer celle de 2025
                    query_prod_pvsyst_2024 = """
                    SELECT 
                        CAST(strftime('%m', date) AS INTEGER) as mois,
                        SUM(prod_pvsyst) as prod_pvsyst_mwh
                    FROM calculs_mensuel_sites
                    WHERE CAST(strftime('%Y', date) AS INTEGER) = 2024
                    AND CAST(strftime('%m', date) AS INTEGER) IN (11, 12)
                    GROUP BY mois
                    ORDER BY mois
                    """
                    df_prod_pvsyst_2024 = load_data_from_db(query_prod_pvsyst_2024)
                    
                    if irra_totale_m1_10 > 0:
                        ratio_prod_irra = prod_totale_m1_10 / irra_totale_m1_10
                        ratio_prod_pvsyst = prod_pvsyst_totale_m1_10 / prod_totale_m1_10 if prod_totale_m1_10 > 0 else 1
                        
                        # Simuler la production pour Nov-Déc 2025
                        prod_simulee_nov_dec = irra_nov_dec_2024_total * ratio_prod_irra
                        
                        # Mettre à jour Nov et Dec dans df_2025
                        for mois in [11, 12]:
                            if mois > dernier_mois:
                                idx = df_2025[df_2025['mois'] == mois].index[0]
                                
                                # Mettre à jour la déviation PR avec la moyenne de 2024
                                if df_dev_pr_2024 is not None and not df_dev_pr_2024.empty:
                                    df_dev_pr_mois = df_dev_pr_2024[df_dev_pr_2024['mois'] == mois]
                                    if not df_dev_pr_mois.empty:
                                        df_2025.loc[idx, 'dev_pr_moyenne'] = df_dev_pr_mois.iloc[0]['dev_pr_moyenne']
                                
                                # Répartir proportionnellement la production réelle entre Nov et Dec
                                if mois == 11:
                                    df_irra_nov = df_irra_2024[df_irra_2024['mois'] == 11]
                                    if not df_irra_nov.empty and df_irra_nov.iloc[0]['irra_reel'] > 0:
                                        irra_nov = df_irra_nov.iloc[0]['irra_reel']
                                        prod_nov = irra_nov * ratio_prod_irra
                                        df_2025.loc[idx, 'prod_reel_mwh'] = prod_nov
                                    else:
                                        df_2025.loc[idx, 'prod_reel_mwh'] = prod_simulee_nov_dec / 2
                                    
                                    # Production PVsyst pour Nov (utiliser données 2024 ou ratio)
                                    if df_prod_pvsyst_2024 is not None and not df_prod_pvsyst_2024.empty:
                                        df_pvsyst_nov = df_prod_pvsyst_2024[df_prod_pvsyst_2024['mois'] == 11]
                                        if not df_pvsyst_nov.empty and df_pvsyst_nov.iloc[0]['prod_pvsyst_mwh'] > 0:
                                            df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_pvsyst_nov.iloc[0]['prod_pvsyst_mwh']
                                        else:
                                            df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_2025.loc[idx, 'prod_reel_mwh'] * ratio_prod_pvsyst
                                    else:
                                        df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_2025.loc[idx, 'prod_reel_mwh'] * ratio_prod_pvsyst
                                elif mois == 12:
                                    df_irra_dec = df_irra_2024[df_irra_2024['mois'] == 12]
                                    if not df_irra_dec.empty and df_irra_dec.iloc[0]['irra_reel'] > 0:
                                        irra_dec = df_irra_dec.iloc[0]['irra_reel']
                                        prod_dec = irra_dec * ratio_prod_irra
                                        df_2025.loc[idx, 'prod_reel_mwh'] = prod_dec
                                    else:
                                        df_2025.loc[idx, 'prod_reel_mwh'] = prod_simulee_nov_dec / 2
                                    
                                    # Production PVsyst pour Dec
                                    if df_prod_pvsyst_2024 is not None and not df_prod_pvsyst_2024.empty:
                                        df_pvsyst_dec = df_prod_pvsyst_2024[df_prod_pvsyst_2024['mois'] == 12]
                                        if not df_pvsyst_dec.empty and df_pvsyst_dec.iloc[0]['prod_pvsyst_mwh'] > 0:
                                            df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_pvsyst_dec.iloc[0]['prod_pvsyst_mwh']
                                        else:
                                            df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_2025.loc[idx, 'prod_reel_mwh'] * ratio_prod_pvsyst
                                    else:
                                        df_2025.loc[idx, 'prod_pvsyst_mwh'] = df_2025.loc[idx, 'prod_reel_mwh'] * ratio_prod_pvsyst
                        
                        # Recalculer les cumuls de production après avoir mis à jour Nov-Déc
                        df_2025['prod_cumule_mwh'] = df_2025['prod_reel_mwh'].cumsum()
                        df_2025['prod_pvsyst_cumule_mwh'] = df_2025['prod_pvsyst_mwh'].cumsum()
                        data[2025] = df_2025
    
    return data


def get_repartition_interventions():
    """Répartition interventions par catégorie"""
    query = """
    SELECT categorie, COUNT(*) as nb
    FROM interventions
    WHERE categorie IS NOT NULL
    GROUP BY categorie
    ORDER BY nb DESC
    LIMIT 5
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_tableau_interventions_par_type(annee=2025):
    """Tableau détaillé des interventions par type avec statistiques"""
    query = f"""
    SELECT 
        categorie,
        COUNT(*) as nb_interventions,
        COUNT(CASE WHEN severite_categorie IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as pct_severite,
        COUNT(CASE WHEN UPPER(status_intervention) IN ('CLOSED', 'TERMINATED') THEN 1 END) * 100.0 / COUNT(*) as pct_closed_terminated,
        AVG(CASE WHEN facturation_intervention IS NOT NULL THEN facturation_intervention ELSE NULL END) as moyenne_facturation
    FROM interventions
    WHERE categorie IS NOT NULL
    AND CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    GROUP BY categorie
    ORDER BY nb_interventions DESC
    """
    df = load_data_from_db(query)
    if df is not None and not df.empty:
        # Arrondir les valeurs
        df['pct_severite'] = df['pct_severite'].round(2)
        df['pct_closed_terminated'] = df['pct_closed_terminated'].round(2)
        df['moyenne_facturation'] = df['moyenne_facturation'].round(2)
        return df
    return pd.DataFrame()


def get_top5_sites_production(annee):
    """Top 5 sites par production"""
    query = f"""
    SELECT id_site as site, SUM(prod_reel) / 1000 as prod_gwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    GROUP BY id_site
    ORDER BY prod_gwh DESC
    LIMIT 5
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_alertes_sites_sous_performants(annee):
    """Nombre de sites sous-performants"""
    query = f"""
    SELECT COUNT(DISTINCT id_site) as nb_alertes
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND ([pr_réel] < 70 OR dev_pr < -10)
    """
    df = load_data_from_db(query)
    return int(df['nb_alertes'].iloc[0]) if df is not None and not df.empty else 0


def get_details_sites_sous_performants(annee):
    """Détails des sites sous-performants avec métriques"""
    query = f"""
    SELECT 
        cas.id_site as site,
        cas.[pr_réel] as pr_reel,
        cas.dev_pr as dev_pr,
        cas.pr_budget as pr_budget,
        SUM(cas.prod_reel) / 1000 as prod_gwh,
        e.puissance_nominale__kWc_ / 1000 as puissance_mw,
        CASE 
            WHEN cas.[pr_réel] < cas.pr_budget THEN 'PR < ' || ROUND(cas.pr_budget, 2) || '% (PR budget PVsyst)'
            WHEN cas.dev_pr < -10 THEN 'Dev PR < -10%'
            ELSE 'Multiple'
        END as raison
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE cas.annee = {annee}
    AND (cas.[pr_réel] < 70 OR cas.dev_pr < -10)
    GROUP BY cas.id_site, cas.[pr_réel], cas.dev_pr, cas.pr_budget, e.puissance_nominale__kWc_
    ORDER BY cas.[pr_réel] ASC, cas.dev_pr ASC
    LIMIT 50
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_sites_production_mwh(annee, limit=5):
    """Top sites par production en MWh"""
    query = f"""
    SELECT 
        id_site as site,
        SUM(prod_reel) as prod_mwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    GROUP BY id_site
    ORDER BY prod_mwh DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_sites_efficacite(annee, limit=5):
    """Top sites par efficacité (Production MWh / Puissance MWc)"""
    query = f"""
    SELECT 
        cas.id_site as site,
        SUM(cas.prod_reel) as prod_mwh,
        MAX(e.puissance_nominale__kWc_) / 1000 as puissance_mw,
        CASE 
            WHEN MAX(e.puissance_nominale__kWc_) > 0 
            THEN SUM(cas.prod_reel) / (MAX(e.puissance_nominale__kWc_) / 1000)
            ELSE 0
        END as efficacite_mwh_par_mwc
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE cas.annee = {annee}
    AND e.puissance_nominale__kWc_ IS NOT NULL
    AND e.puissance_nominale__kWc_ > 0
    GROUP BY cas.id_site
    HAVING efficacite_mwh_par_mwc > 0
    ORDER BY efficacite_mwh_par_mwc DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_sites_revenus(annee, limit=5):
    """Top sites par revenus (Tarif EDF x Production MWh)"""
    query = f"""
    SELECT 
        id_site as site,
        SUM(prod_reel_distributeur * tarif_edf) as revenus_euros,
        SUM(prod_reel_distributeur) as prod_mwh
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    GROUP BY id_site
    ORDER BY revenus_euros DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_mensuelles(annee):
    """Interventions mensuelles pour une année - utilise date_fin_intervention"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_fin_intervention) AS INTEGER) as mois,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_fin_intervention) AS INTEGER) = {annee}
    AND date_fin_intervention IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame(columns=['mois', 'nb_interventions'])
    return df


def get_cout_maintenance_mensuel(annee):
    """Coût maintenance mensuel"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        SUM(facturation_intervention) / 1000 as cout_k
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND facturation_intervention IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame(columns=['mois', 'cout_k'])
    return df


def apply_glassmorphism_theme(fig):
    """Applique le thème glassmorphism aux graphiques Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0.5)',
        font=dict(color='#1f2937', family="ui-sans-serif, system-ui, -apple-system"),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)', linecolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', linecolor='rgba(0,0,0,0.1)'),
    )
    return fig


# ============================================
# FONCTIONS VUE PERFORMANCE
# ============================================

def get_production_mensuelle(annees=None, sites=None, spvs=None):
    """Production mensuelle vs budget pour une ou plusieurs années"""
    where_conditions = []
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        SUM(prod_reel) as prod_reel_mwh,
        SUM(prod_pvsyst) as prod_budget_mwh
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame(columns=['mois', 'prod_reel_mwh', 'prod_budget_mwh'])
    return df


def get_irradiation_mensuelle(annees=None, sites=None, spvs=None):
    """Irradiation mensuelle réelle vs théorique pour calculer l'écart"""
    where_conditions = ["irra_reel IS NOT NULL", "irra_pvsyst_incl IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        AVG(irra_reel) as irra_reel,
        AVG(irra_pvsyst_incl) as irra_budget
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame(columns=['mois', 'irra_reel', 'irra_budget'])
    return df


def get_disponibilite_mensuelle_ecart(annees=None, sites=None, spvs=None):
    """Disponibilité mensuelle brut et contrat vs budget (99%) pour calculer les écarts"""
    where_conditions = ["dispo_brut IS NOT NULL", "dispo_contrat IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        AVG(dispo_brut) as dispo_brut,
        AVG(dispo_contrat) as dispo_contrat
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame(columns=['mois', 'dispo_brut', 'dispo_contrat'])
    return df


def get_pr_annuel_par_site(annees=None, sites=None, spvs=None):
    """PR moyen annuel par site"""
    where_conditions = ["cas.[pr_réel] IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"cas.id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cas.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        COALESCE(e.nom_site, cas.id_site) as site,
        AVG(cas.[pr_réel]) as pr_moyen
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    GROUP BY cas.id_site, e.nom_site
    ORDER BY pr_moyen ASC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_deviation_pr_par_site(annees=None, sites=None, spvs=None):
    """Déviation PR par site"""
    where_conditions = ["cas.dev_pr IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"cas.id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cas.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        COALESCE(e.nom_site, cas.id_site) as site,
        cas.dev_pr
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    ORDER BY cas.dev_pr ASC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_flop_sites_pr(annees=None, sites=None, spvs=None):
    """Top et Flop sites par PR"""
    where_conditions = ["cas.[pr_réel] IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"cas.id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cas.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query_top = f"""
    SELECT COALESCE(e.nom_site, cas.id_site) as site, cas.[pr_réel] as pr, cas.dev_pr, SUM(cas.prod_reel) / 1000 as prod_gwh
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    GROUP BY cas.id_site, e.nom_site
    ORDER BY cas.[pr_réel] DESC
    LIMIT 10
    """
    query_flop = f"""
    SELECT COALESCE(e.nom_site, cas.id_site) as site, cas.[pr_réel] as pr, cas.dev_pr, SUM(cas.prod_reel) / 1000 as prod_gwh
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    GROUP BY cas.id_site, e.nom_site
    ORDER BY cas.[pr_réel] ASC
    LIMIT 10
    """
    df_top = load_data_from_db(query_top)
    df_flop = load_data_from_db(query_flop)
    return df_top, df_flop


def get_evolution_pr_site(site=None):
    """Évolution PR par site sur 3 dernières années"""
    if site:
        query = """
        SELECT CAST(annee AS INTEGER) as annee, [pr_réel] as pr
        FROM calculs_annuel_sites
        WHERE id_site = ? AND [pr_réel] IS NOT NULL
        AND annee >= (SELECT MAX(CAST(annee AS INTEGER)) - 2 FROM calculs_annuel_sites)
        ORDER BY annee
        """
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn, params=(site,))
        conn.close()
    else:
        query = """
        SELECT 
            CAST(annee AS INTEGER) as annee,
            id_site as site,
            AVG([pr_réel]) as pr
        FROM calculs_annuel_sites
        WHERE [pr_réel] IS NOT NULL
        AND annee >= (SELECT MAX(CAST(annee AS INTEGER)) - 2 FROM calculs_annuel_sites)
        GROUP BY annee, id_site
        ORDER BY annee, id_site
        LIMIT 100
        """
        df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_pr_reel_vs_corrige(annee):
    """PR réel vs PR corrigé"""
    query = f"""
    SELECT 
        site,
        AVG([pr_réel]) as pr_reel,
        AVG(pr_reel_corrige) as pr_corrige
    FROM calculs_annuel_sites
    WHERE annee = {annee} 
    AND [pr_réel] IS NOT NULL 
    AND pr_reel_corrige IS NOT NULL
    GROUP BY site
    LIMIT 20
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_irradiation_reelle_vs_theorique(annees=None, spvs=None):
    """Irradiation réelle vs théorique"""
    where_conditions = ["irra_reel IS NOT NULL", "irra_pvsyst_incl IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        AVG(irra_reel) as irra_reel,
        AVG(irra_pvsyst_incl) as irra_theorique,
        AVG(dev_irra) as dev_irra
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_irradiation_reelle_2024(spvs=None):
    """Moyennes d'irradiation réelle 2024 par mois"""
    where_conditions = ["irra_reel IS NOT NULL", "CAST(strftime('%Y', date) AS INTEGER) = 2024"]
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        AVG(irra_reel) as irra_reel_2024
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_correlation_irradiation_production(annees=None, spvs=None):
    """Corrélation irradiation/production avec informations détaillées pour hover"""
    where_conditions = ["cms.irra_reel IS NOT NULL", "cms.prod_reel IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', cms.date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cms.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        cms.irra_reel,
        cms.prod_reel,
        cms.id_site,
        cms.date,
        COALESCE(e.nom_site, cms.id_site) as nom_site,
        cms.spv,
        CAST(strftime('%Y', cms.date) AS INTEGER) as annee,
        CAST(strftime('%m', cms.date) AS INTEGER) as mois,
        cms.prod_pvsyst,
        cms.pr_réel,
        cms.dispo_brut,
        cms.dispo_contrat,
        e.latitude,
        e.longitude
    FROM calculs_mensuel_sites cms
    LEFT JOIN exposition e ON cms.id_site = e.id_site
    WHERE {where_clause}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def determine_zone_france(latitude, longitude):
    """Détermine dans quelle zone de France se trouve un site (métropole ou outre-mer)"""
    if pd.isna(latitude) or pd.isna(longitude):
        return None
    
    # Vérifier d'abord les territoires d'outre-mer
    # Guadeloupe
    if 15.5 <= latitude <= 16.5 and -62.0 <= longitude <= -61.0:
        return "Guadeloupe"
    
    # Martinique
    if 14.3 <= latitude <= 14.9 and -61.3 <= longitude <= -60.7:
        return "Martinique"
    
    # Guyane
    if 2.0 <= latitude <= 6.0 and -54.5 <= longitude <= -51.5:
        return "Guyane"
    
    # La Réunion
    if -21.5 <= latitude <= -20.8 and 55.2 <= longitude <= 55.8:
        return "La Réunion"
    
    # Zones de France métropolitaine
    lat_center = 46.6
    lon_center = 2.5
    
    if latitude >= lat_center:
        # Nord
        if longitude < lon_center:
            return "Nord-Ouest"
        else:
            return "Nord-Est"
    else:
        # Sud
        if longitude < lon_center:
            return "Sud-Ouest"
        else:
            return "Sud-Est"


def get_correlation_par_zone(annees=None, spvs=None):
    """Calcule R² par zone géographique (métropole + outre-mer) pour chaque année"""
    zones = ["Sud-Ouest", "Sud-Est", "Nord-Ouest", "Nord-Est", "Guadeloupe", "Martinique", "Guyane", "La Réunion"]
    annees_analyse = [2023, 2024, 2025]
    
    # Récupérer toutes les données sans filtre d'année pour avoir 2023, 2024, 2025
    df_all = get_correlation_irradiation_production(annees=None, spvs=spvs)
    
    # Ajouter la colonne zone (même si df_all est vide, on doit quand même retourner toutes les zones)
    if not df_all.empty:
        df_all['zone'] = df_all.apply(lambda row: determine_zone_france(row['latitude'], row['longitude']), axis=1)
        
        # Filtrer les données avec zone valide et valeurs valides
        df_valid = df_all[(df_all['zone'].notna()) & (df_all['irra_reel'].notna()) & 
                          (df_all['prod_reel'].notna()) & (df_all['prod_reel'] > 0)]
    else:
        df_valid = pd.DataFrame()
    
    # Calculer R² par zone et par année
    # Toujours retourner toutes les zones, même si pas de données (pour afficher Guyane)
    correlations_zone = []
    
    for zone in zones:
        df_zone = df_valid[df_valid['zone'] == zone] if not df_valid.empty else pd.DataFrame()
        row_data = {'Zone': zone}
        
        for annee in annees_analyse:
            if len(df_zone) > 0:
                df_zone_annee = df_zone[df_zone['annee'] == annee]
                if len(df_zone_annee) > 1:
                    correlation = df_zone_annee['irra_reel'].corr(df_zone_annee['prod_reel'])
                    if not pd.isna(correlation):
                        r_squared = correlation ** 2
                        row_data[f'R² {annee}'] = r_squared
                    else:
                        row_data[f'R² {annee}'] = None
                else:
                    row_data[f'R² {annee}'] = None
            else:
                row_data[f'R² {annee}'] = None
        
        # Ajouter le nombre total de points (0 si pas de données)
        row_data['Nb points'] = len(df_zone) if len(df_zone) > 0 else 0
        correlations_zone.append(row_data)
    
    df_result = pd.DataFrame(correlations_zone)
    
    # Vérifier et garantir exactement 8 lignes (une par zone)
    if len(df_result) != 8:
        # Si le nombre de lignes n'est pas 8, reconstruire le DataFrame avec exactement 8 zones
        # dans l'ordre défini
        df_final = pd.DataFrame(columns=['Zone'] + [f'R² {annee}' for annee in annees_analyse] + ['Nb points'])
        for zone in zones:
            zone_row = df_result[df_result['Zone'] == zone]
            if len(zone_row) > 0:
                df_final = pd.concat([df_final, zone_row.head(1)], ignore_index=True)
            else:
                # Créer une ligne vide pour cette zone
                new_row = {'Zone': zone}
                for annee in annees_analyse:
                    new_row[f'R² {annee}'] = None
                new_row['Nb points'] = 0
                df_final = pd.concat([df_final, pd.DataFrame([new_row])], ignore_index=True)
        df_result = df_final
    
    # S'assurer qu'il n'y a pas de doublons (prendre la première occurrence de chaque zone)
    df_result = df_result.drop_duplicates(subset=['Zone'], keep='first')
    
    # Réorganiser pour garantir l'ordre des zones
    df_result['Zone'] = pd.Categorical(df_result['Zone'], categories=zones, ordered=True)
    df_result = df_result.sort_values('Zone').reset_index(drop=True)
    df_result['Zone'] = df_result['Zone'].astype(str)
    
    # Réorganiser les colonnes : Zone, R² 2023, R² 2024, R² 2025, Nb points
    cols_order = ['Zone'] + [f'R² {annee}' for annee in annees_analyse] + ['Nb points']
    cols_order = [col for col in cols_order if col in df_result.columns]
    if cols_order:
        df_result = df_result[cols_order]
    
    # S'assurer que toutes les colonnes nécessaires existent (avec None si manquantes)
    for col in [f'R² {annee}' for annee in annees_analyse]:
        if col not in df_result.columns:
            df_result[col] = None
    
    # Garantir exactement 8 lignes
    if len(df_result) > 8:
        df_result = df_result.head(8)
    elif len(df_result) < 8:
        # Ajouter les zones manquantes
        zones_presentes = set(df_result['Zone'].values)
        for zone in zones:
            if zone not in zones_presentes:
                new_row = {'Zone': zone}
                for annee in annees_analyse:
                    new_row[f'R² {annee}'] = None
                new_row['Nb points'] = 0
                df_result = pd.concat([df_result, pd.DataFrame([new_row])], ignore_index=True)
        # Réorganiser à nouveau
        df_result['Zone'] = pd.Categorical(df_result['Zone'], categories=zones, ordered=True)
        df_result = df_result.sort_values('Zone').reset_index(drop=True)
        df_result['Zone'] = df_result['Zone'].astype(str)
    
    return df_result


def get_correlation_par_mois(annees=None, spvs=None):
    """Calcule R² par mois de l'année (janvier à décembre) pour chaque année"""
    noms_mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    annees_analyse = [2023, 2024, 2025]
    
    # Récupérer toutes les données sans filtre d'année pour avoir 2023, 2024, 2025
    df_all = get_correlation_irradiation_production(annees=None, spvs=spvs)
    
    # Filtrer les données avec valeurs valides
    if not df_all.empty:
        df_valid = df_all[(df_all['irra_reel'].notna()) & (df_all['prod_reel'].notna()) & 
                          (df_all['prod_reel'] > 0) & (df_all['mois'].notna())]
    else:
        df_valid = pd.DataFrame()
    
    # Calculer R² par mois et par année
    # Toujours retourner les 12 mois, même si pas de données
    correlations_mois = []
    
    for mois_num in range(1, 13):
        df_mois = df_valid[df_valid['mois'] == mois_num] if not df_valid.empty else pd.DataFrame()
        row_data = {'Mois': noms_mois[mois_num - 1]}
        
        for annee in annees_analyse:
            if len(df_mois) > 0:
                df_mois_annee = df_mois[df_mois['annee'] == annee]
                if len(df_mois_annee) > 1:
                    correlation = df_mois_annee['irra_reel'].corr(df_mois_annee['prod_reel'])
                    if not pd.isna(correlation):
                        r_squared = correlation ** 2
                        row_data[f'R² {annee}'] = r_squared
                    else:
                        row_data[f'R² {annee}'] = None
                else:
                    row_data[f'R² {annee}'] = None
            else:
                row_data[f'R² {annee}'] = None
        
        # Ajouter le nombre total de points (0 si pas de données)
        row_data['Nb points'] = len(df_mois) if len(df_mois) > 0 else 0
        correlations_mois.append(row_data)
    
    df_result = pd.DataFrame(correlations_mois)
    # Réorganiser les colonnes : Mois, R² 2023, R² 2024, R² 2025, Nb points
    # Toujours retourner le DataFrame avec tous les mois (même vides)
    cols_order = ['Mois'] + [f'R² {annee}' for annee in annees_analyse] + ['Nb points']
    cols_order = [col for col in cols_order if col in df_result.columns]
    if cols_order:
        df_result = df_result[cols_order]
    
    # S'assurer que toutes les colonnes nécessaires existent (avec None si manquantes)
    for col in [f'R² {annee}' for annee in annees_analyse]:
        if col not in df_result.columns:
            df_result[col] = None
    
    return df_result


def get_deviation_irradiation_par_site(annee):
    """Déviation irradiation par site"""
    query = f"""
    SELECT 
        site,
        AVG((irra_reel - irra_pvsyst_incl) / irra_pvsyst_incl * 100) as dev_irra_pct
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND irra_reel IS NOT NULL
    AND irra_pvsyst_incl IS NOT NULL
    GROUP BY site
    ORDER BY dev_irra_pct DESC
    LIMIT 30
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_detail_pertes(annees=None, sites=None, spvs=None):
    """Détail des pertes pour waterfall chart"""
    where_conditions = []
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    
    query = f"""
    SELECT 
        SUM(prod_pvsyst) / 1000 as budget_gwh,
        SUM((1 - dispo_contrat/100) * prod_pvsyst) / 1000 as pertes_reseau_gwh,
        SUM((dispo_contrat/100 - dispo_brut/100) * prod_pvsyst) / 1000 as pertes_apex_gwh,
        SUM(prod_reel) / 1000 as prod_reelle_gwh
    FROM calculs_annuel_sites
    WHERE {where_clause}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_performance_specifique(annees=None, sites=None, spvs=None):
    """Ratio de performance spécifique (kWh/kWc) par site"""
    where_conditions = [
        "cas.prod_reel IS NOT NULL",
        "cas.puissance_site IS NOT NULL",
        "cas.puissance_site > 0"
    ]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"cas.id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cas.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        COALESCE(e.nom_site, cas.id_site) as site,
        SUM(cas.prod_reel) / 1000 as prod_mwh,
        AVG(cas.puissance_site) as puissance_mw,
        (SUM(cas.prod_reel) / 1000) / AVG(cas.puissance_site) as performance_specifique
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    GROUP BY cas.id_site, e.nom_site
    HAVING performance_specifique > 0
    ORDER BY performance_specifique DESC
    LIMIT 30
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_taux_atteinte_objectif(annees=None, spvs=None):
    """Taux d'atteinte objectif production par mois"""
    where_conditions = ["prod_pvsyst > 0"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"CAST(strftime('%Y', date) AS INTEGER) IN ({annees_str})")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        (SUM(prod_reel) / SUM(prod_pvsyst) * 100) as taux_atteinte
    FROM calculs_mensuel_sites
    WHERE {where_clause}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_production_reelle_vs_corrigee(annees=None, sites=None, spvs=None):
    """Production réelle vs corrigée (données annuelles seulement)"""
    where_conditions = [
        "cas.prod_reel IS NOT NULL",
        "cas.prod_reel_corrige IS NOT NULL"
    ]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    if sites:
        sites_str = "','".join(sites).replace("'", "''")
        where_conditions.append(f"cas.id_site IN ('{sites_str}')")
    
    if spvs:
        spvs_str = "','".join(spvs).replace("'", "''")
        where_conditions.append(f"cas.spv IN ('{spvs_str}')")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        COALESCE(e.nom_site, cas.id_site) as site,
        SUM(cas.prod_reel) / 1000 as prod_reelle_mwh,
        SUM(cas.prod_reel_corrige) / 1000 as prod_corrigee_mwh
    FROM calculs_annuel_sites cas
    LEFT JOIN exposition e ON cas.id_site = e.id_site
    WHERE {where_clause}
    GROUP BY cas.id_site, e.nom_site
    ORDER BY prod_reelle_mwh DESC
    LIMIT 20
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_tableau_indicateurs_mensuels(annee_principale):
    """Tableau mensuel des indicateurs comparatif Année N / Année N-1
    
    Args:
        annee_principale: Année principale pour la comparaison (ex: 2025)
    
    Returns:
        DataFrame avec les colonnes pour annee_principale et annee_principale - 1
    """
    annee_n1 = annee_principale - 1
    
    # Créer un DataFrame de base avec tous les mois
    mois_noms = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
                  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    df_result = pd.DataFrame({
        'mois': range(1, 13),  # Utiliser le numéro de mois pour le merge
        'mois_nom': mois_noms  # Garder le nom pour l'affichage
    })
    
    # Récupérer les données pour annee_principale et annee_n1
    for annee in [annee_n1, annee_principale]:
        # Première requête : données de base sans JOIN (pour éviter les problèmes SQLite)
        query_base = f"""
        SELECT 
            CAST(strftime('%m', date) AS INTEGER) as mois,
            COUNT(DISTINCT id_site) as nb_sites,
            SUM(prod_pvsyst) / 1000 as prod_pvsyst_gwh,
            AVG(irra_pvsyst_incl) as moy_irrad_pvsyst,
            SUM(prod_reel) / 1000 as prod_reelle_gwh,
            AVG(irra_reel) as moy_irrad_reelle,
            AVG(dispo_contrat) as dispo_contrat,
            AVG(dispo_brut) as dispo_brut,
            AVG(dev_prod) as dev_prod_pct,
            AVG(dev_irra) as dev_irrad_pct,
            AVG(pr_budget) as pr_budget,
            AVG(pr_réel) as pr_reel,
            AVG(dev_pr) as dev_pr_pct,
            -- Taux d'atteinte: 100 + Dév Prod (%)
            AVG(CASE WHEN dev_prod IS NOT NULL THEN (100 + dev_prod) ELSE NULL END) as taux_atteinte_pct
        FROM calculs_mensuel_sites
        WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
        AND date IS NOT NULL
        GROUP BY mois
        ORDER BY mois
        """
        df_base = load_data_from_db(query_base)
        
        # Deuxième requête : Performance spécifique avec JOIN (seulement pour cette métrique)
        query_perf = f"""
        SELECT 
            CAST(strftime('%m', cms.date) AS INTEGER) as mois,
            AVG(CASE WHEN e.puissance_nominale__kWc_ > 0 THEN (cms.prod_reel * 1000) / e.puissance_nominale__kWc_ ELSE NULL END) as perf_specifique_kwhkwc
        FROM calculs_mensuel_sites cms
        LEFT JOIN exposition e ON cms.id_site = e.id_site
        WHERE CAST(strftime('%Y', cms.date) AS INTEGER) = {annee}
        AND cms.date IS NOT NULL
        GROUP BY mois
        ORDER BY mois
        """
        df_perf = load_data_from_db(query_perf)
        
        # Fusionner les deux DataFrames
        if df_base is not None and not df_base.empty:
            if df_perf is not None and not df_perf.empty:
                df_base = df_base.merge(df_perf[['mois', 'perf_specifique_kwhkwc']], on='mois', how='left')
            else:
                df_base['perf_specifique_kwhkwc'] = None
            df = df_base
        else:
            df = None
        
        if df is not None and not df.empty:
            # Ajouter le suffixe de l'année aux colonnes (sauf mois)
            df = df.rename(columns={
                col: f"{col}_{annee}" if col != 'mois' else col 
                for col in df.columns
            })
            # Fusionner avec le DataFrame résultat (sur le numéro de mois)
            df_result = df_result.merge(df, on='mois', how='left')
    
    # Ajouter le nom du mois pour l'affichage
    df_result['mois'] = df_result['mois_nom']
    df_result = df_result.drop(columns=['mois_nom'])
    
    # S'assurer que les données sont triées par numéro de mois (ordre chronologique)
    # Créer une colonne temporaire avec les numéros de mois pour le tri
    mois_num_map = {
        'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4,
        'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8,
        'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
    }
    df_result['_mois_num'] = df_result['mois'].map(mois_num_map)
    df_result = df_result.sort_values('_mois_num').reset_index(drop=True)
    df_result = df_result.drop(columns=['_mois_num'])
    
    return df_result


def get_tableau_indicateurs_par_spv(annee_principale):
    """Tableau des indicateurs par SPV comparatif Année N / Année N-1
    
    Args:
        annee_principale: Année principale pour la comparaison (ex: 2025)
    
    Returns:
        DataFrame avec les colonnes pour annee_principale et annee_principale - 1
    """
    annee_n1 = annee_principale - 1
    
    # Récupérer toutes les SPV distinctes
    query_spvs = "SELECT DISTINCT spv FROM calculs_mensuel_sites WHERE spv IS NOT NULL ORDER BY spv"
    df_spvs = load_data_from_db(query_spvs)
    
    if df_spvs is None or df_spvs.empty:
        return pd.DataFrame()
    
    df_result = df_spvs.copy()
    df_result['spv'] = df_spvs['spv']
    
    # Récupérer les données pour annee_n1 et annee_principale
    for annee in [annee_n1, annee_principale]:
        # Première requête : données de base sans JOIN
        query_base = f"""
    SELECT 
        spv,
            COUNT(DISTINCT id_site) as nb_sites,
            SUM(prod_pvsyst) / 1000 as prod_pvsyst_gwh,
            AVG(irra_pvsyst_incl) as moy_irrad_pvsyst,
            SUM(prod_reel) / 1000 as prod_reelle_gwh,
            AVG(irra_reel) as moy_irrad_reelle,
            AVG(dispo_contrat) as dispo_contrat,
            AVG(dispo_brut) as dispo_brut,
            AVG(dev_prod) as dev_prod_pct,
            AVG(dev_irra) as dev_irrad_pct,
            AVG(pr_budget) as pr_budget,
            AVG(pr_réel) as pr_reel,
            AVG(dev_pr) as dev_pr_pct,
            -- Taux d'atteinte: 100 + Dév Prod (%)
            AVG(CASE WHEN dev_prod IS NOT NULL THEN (100 + dev_prod) ELSE NULL END) as taux_atteinte_pct
        FROM calculs_mensuel_sites
        WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
        AND date IS NOT NULL
        AND spv IS NOT NULL
    GROUP BY spv
        ORDER BY spv
        """
        df_base = load_data_from_db(query_base)
        
        # Deuxième requête : Performance spécifique avec JOIN
        query_perf = f"""
        SELECT 
            cms.spv,
            AVG(CASE WHEN e.puissance_nominale__kWc_ > 0 THEN (cms.prod_reel * 1000) / e.puissance_nominale__kWc_ ELSE NULL END) as perf_specifique_kwhkwc
        FROM calculs_mensuel_sites cms
        LEFT JOIN exposition e ON cms.id_site = e.id_site
        WHERE CAST(strftime('%Y', cms.date) AS INTEGER) = {annee}
        AND cms.date IS NOT NULL
        AND cms.spv IS NOT NULL
        GROUP BY cms.spv
        ORDER BY cms.spv
        """
        df_perf = load_data_from_db(query_perf)
        
        # Fusionner les deux DataFrames
        if df_base is not None and not df_base.empty:
            if df_perf is not None and not df_perf.empty:
                df_base = df_base.merge(df_perf[['spv', 'perf_specifique_kwhkwc']], on='spv', how='left')
            else:
                df_base['perf_specifique_kwhkwc'] = None
            df = df_base
        else:
            df = None
        
        if df is not None and not df.empty:
            # Ajouter le suffixe de l'année aux colonnes (sauf spv)
            df = df.rename(columns={
                col: f"{col}_{annee}" if col != 'spv' else col 
                for col in df.columns
            })
            # Fusionner avec le DataFrame résultat
            df_result = df_result.merge(df, on='spv', how='left')
    
    return df_result


def get_performance_par_spv(annees=None):
    """Performance par SPV"""
    where_conditions = ["cas.[pr_réel] IS NOT NULL"]
    
    if annees:
        annees_str = ','.join(map(str, annees))
        where_conditions.append(f"cas.annee IN ({annees_str})")
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT 
        cas.spv,
        AVG(cas.[pr_réel]) as pr_moyen,
        COUNT(DISTINCT cas.id_site) as nb_sites
    FROM calculs_annuel_sites cas
    WHERE {where_clause}
    GROUP BY cas.spv
    ORDER BY pr_moyen DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_liste_sites():
    """Liste des sites pour les filtres"""
    query = "SELECT DISTINCT id_site, nom_site FROM exposition ORDER BY nom_site"
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_liste_spv():
    """Liste des SPV pour les filtres"""
    query = "SELECT DISTINCT spv FROM exposition WHERE spv IS NOT NULL ORDER BY spv"
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def show_performance_view():
    """Affiche la vue Performance complète"""
    
    # Initialiser session state pour navigation
    if 'vue_active' not in st.session_state:
        st.session_state.vue_active = 'dashboard'
    
    st.markdown('''
    <div style="
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 3rem;
        padding: 28px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        📈 Vue Performance
    </div>
    ''', unsafe_allow_html=True)
    
    # Filtres
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 2rem;">', unsafe_allow_html=True)
    col_filtre1, col_filtre2, col_filtre3 = st.columns(3)
    with col_filtre1:
        annees_disponibles = [2025, 2024, 2023]
        annees_selectionnees = st.multiselect(
            "Année(s)", 
            annees_disponibles, 
            default=[2025],
            help="Sélectionnez une ou plusieurs années"
        )
        # Si rien n'est sélectionné, utiliser toutes les années
        if not annees_selectionnees:
            annees_selectionnees = annees_disponibles
    with col_filtre2:
        df_sites = get_liste_sites()
        sites_list = list(df_sites['id_site'].unique()) if not df_sites.empty else []
        sites_selectionnes = st.multiselect(
            "Site(s)", 
            sites_list,
            help="Sélectionnez un ou plusieurs sites (laisser vide pour tous)"
        )
    with col_filtre3:
        df_spv = get_liste_spv()
        spv_list = list(df_spv['spv'].unique()) if not df_spv.empty else []
        spv_selectionnes = st.multiselect(
            "SPV", 
            spv_list,
            help="Sélectionnez un ou plusieurs SPV (laisser vide pour tous)"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # SECTION A: Production & Budget
    # ============================================
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
    ">📊 Production & Budget</div>
    ''', unsafe_allow_html=True)
    
    # P.1 Production Mensuelle vs Budget
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_prod_mens = get_production_mensuelle(annees_selectionnees, sites_selectionnes, spv_selectionnes)
    if not df_prod_mens.empty:
        # Créer un graphique combiné avec barres et lignes cumulées
        fig = go.Figure()
        
        # Barres mensuelles
        fig.add_trace(go.Bar(
            name='Budget',
            x=df_prod_mens['mois'],
            y=df_prod_mens['prod_budget_mwh'] / 1000,
            marker_color='#1f77b4',
            opacity=0.7
        ))
        fig.add_trace(go.Bar(
            name='Réel',
            x=df_prod_mens['mois'],
            y=df_prod_mens['prod_reel_mwh'] / 1000,
            marker_color='#87ceeb',
            opacity=0.9
        ))
        
        # Lignes cumulées (axe secondaire)
        df_prod_mens['cumul_budget'] = df_prod_mens['prod_budget_mwh'].cumsum() / 1000
        df_prod_mens['cumul_reel'] = df_prod_mens['prod_reel_mwh'].cumsum() / 1000
        
        fig.add_trace(go.Scatter(
            name='Budget Cumulé',
            x=df_prod_mens['mois'],
            y=df_prod_mens['cumul_budget'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3, dash='dash'),
            yaxis='y2'
        ))
        fig.add_trace(go.Scatter(
            name='Réel Cumulé',
            x=df_prod_mens['mois'],
            y=df_prod_mens['cumul_reel'],
            mode='lines+markers',
            line=dict(color='#fbbf24', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='📊 Production Mensuelle vs Budget',
            xaxis_title='Mois',
            yaxis_title='Production Mensuelle (GWh)',
            yaxis2=dict(title='Production Cumulée (GWh)', overlaying='y', side='right'),
            barmode='group',
            height=450
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # P.3 : Écarts Production, Irradiation et Disponibilité vs Budget
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    
    # Récupérer toutes les données nécessaires
    df_prod_mens = get_production_mensuelle(annees_selectionnees, sites_selectionnes, spv_selectionnes)
    df_irra_mens = get_irradiation_mensuelle(annees_selectionnees, sites_selectionnes, spv_selectionnes)
    df_dispo_mens = get_disponibilite_mensuelle_ecart(annees_selectionnees, sites_selectionnes, spv_selectionnes)
    
    if not df_prod_mens.empty:
        # Calculer les écarts
        df_prod_mens['ecart_prod_pct'] = ((df_prod_mens['prod_reel_mwh'] - df_prod_mens['prod_budget_mwh']) / df_prod_mens['prod_budget_mwh'] * 100)
        
        # Fusionner les données par mois
        df_combined = df_prod_mens[['mois', 'ecart_prod_pct']].copy()
        
        if not df_irra_mens.empty:
            df_irra_mens['ecart_irra_pct'] = ((df_irra_mens['irra_reel'] - df_irra_mens['irra_budget']) / df_irra_mens['irra_budget'] * 100)
            df_combined = df_combined.merge(df_irra_mens[['mois', 'ecart_irra_pct']], on='mois', how='outer')
        else:
            df_combined['ecart_irra_pct'] = None
        
        if not df_dispo_mens.empty:
            # Écart par rapport à 99% (budget)
            df_dispo_mens['ecart_dispo_brut_pct'] = df_dispo_mens['dispo_brut'] - 99
            df_dispo_mens['ecart_dispo_contrat_pct'] = df_dispo_mens['dispo_contrat'] - 99
            df_combined = df_combined.merge(df_dispo_mens[['mois', 'ecart_dispo_brut_pct', 'ecart_dispo_contrat_pct']], on='mois', how='outer')
        else:
            df_combined['ecart_dispo_brut_pct'] = None
            df_combined['ecart_dispo_contrat_pct'] = None
        
        # Trier par mois
        df_combined = df_combined.sort_values('mois')
        
        fig = go.Figure()
        
        # 1. Barres Écart Production vs Budget (bleu foncé/clair) - Groupe 1
        colors_prod = df_combined['ecart_prod_pct'].apply(
            lambda x: '#1e40af' if x is not None and x > 0 else '#93c5fd'
        ).tolist()
        fig.add_trace(go.Bar(
            x=df_combined['mois'],
            y=df_combined['ecart_prod_pct'],
            name='Écart Production vs Budget',
            marker_color=colors_prod,
            marker_line_color='rgba(0,0,0,0.1)',
            marker_line_width=1,
            text=df_combined['ecart_prod_pct'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=10),
            offsetgroup='group1'
        ))
        
        # 2. Barres Écart Irradiation vs Budget (orange) - Groupe 2
        if df_combined['ecart_irra_pct'].notna().any():
            colors_irra = df_combined['ecart_irra_pct'].apply(
                lambda x: '#ea580c' if x is not None and x > 0 else '#fb923c'  # Orange foncé pour positif, orange clair pour négatif
            ).tolist()
            fig.add_trace(go.Bar(
                x=df_combined['mois'],
                y=df_combined['ecart_irra_pct'],
                name='Écart Irradiation vs Budget',
                marker_color=colors_irra,
                marker_line_color='rgba(0,0,0,0.1)',
                marker_line_width=1,
                text=df_combined['ecart_irra_pct'].round(1).astype(str) + '%',
                textposition='outside',
                textfont=dict(size=10),
                offsetgroup='group2'
            ))
        
        # 3. Barres Écart Disponibilité Brut vs Budget 99% (vert foncé) - Groupe 3 (base pour stack)
        if df_combined['ecart_dispo_brut_pct'].notna().any():
            colors_dispo_brut = df_combined['ecart_dispo_brut_pct'].apply(
                lambda x: '#16a34a' if x is not None and x > 0 else '#86efac'  # Vert foncé pour positif, vert clair pour négatif
            ).tolist()
            fig.add_trace(go.Bar(
                x=df_combined['mois'],
                y=df_combined['ecart_dispo_brut_pct'],
                name='Écart Disponibilité Brut vs Budget (99%)',
                marker_color=colors_dispo_brut,
                marker_line_color='rgba(0,0,0,0.1)',
                marker_line_width=1,
                text=df_combined['ecart_dispo_brut_pct'].round(1).astype(str) + '%',
                textposition='inside',
                textfont=dict(size=9),
                offsetgroup='group3'
            ))
        
        # 4. Barres Écart Disponibilité Contrat vs Budget 99% (vert clair, stackée sur Brut) - Groupe 3 (stack)
        if df_combined['ecart_dispo_contrat_pct'].notna().any():
            colors_dispo_contrat = df_combined['ecart_dispo_contrat_pct'].apply(
                lambda x: '#22c55e' if x is not None and x > 0 else '#bbf7d0'  # Vert moyen pour positif, vert très clair pour négatif
            ).tolist()
            # Calculer la base pour stacker le contrat sur le brut
            base_dispo_contrat = df_combined['ecart_dispo_brut_pct'].fillna(0).tolist()
            fig.add_trace(go.Bar(
                x=df_combined['mois'],
                y=df_combined['ecart_dispo_contrat_pct'],
                name='Écart Disponibilité Contrat vs Budget (99%)',
                marker_color=colors_dispo_contrat,
                marker_line_color='rgba(0,0,0,0.1)',
                marker_line_width=1,
                text=df_combined['ecart_dispo_contrat_pct'].round(1).astype(str) + '%',
                textposition='inside',
                textfont=dict(size=9),
                offsetgroup='group3',
                base=base_dispo_contrat  # Commence au-dessus du brut pour créer l'effet stack
            ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
        fig.update_layout(
            title='📉 Écarts Production, Irradiation et Disponibilité vs Budget',
            xaxis_title='Mois',
            yaxis_title='Écart (%)',
            height=500,
            barmode='group',  # Mode group : les offsetgroups sont côte à côte, et base permet le stack dans le même offsetgroup
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(b=80, t=80, l=50, r=50)  # Marges augmentées en haut pour la légende
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # P.4 : Détail des Pertes (Waterfall)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    # Simulation des données basées sur l'image (en attendant les vraies données de la base)
    # Valeurs en MWh selon l'image
    budget_p50 = 3172
    indisponibilite_reseau = -143
    prix_negatifs = 0
    indisponibilite_apex = -19
    irradiation_simulation = 174
    ecart_residuel = -14
    production_reelle = 3169
    
    # Création du waterfall chart avec les 7 éléments
    # Calcul des positions cumulatives pour le waterfall
    categories = ["Budget P50", "Indisponibilité Réseau", "Prix négatifs", "Indisponibilité APEX", "Irradiation & Simulation", "Écart résiduel", "Production réelle"]
    values = [budget_p50, indisponibilite_reseau, prix_negatifs, indisponibilite_apex, irradiation_simulation, ecart_residuel, production_reelle]
    measures = ["absolute", "relative", "relative", "relative", "relative", "relative", "absolute"]
    
    # Couleurs pour chaque segment
    colors_list = [
        "#1e40af",  # Budget P50 - bleu foncé (absolute)
        "#ef4444",  # Indisponibilité Réseau - rouge (relative négatif)
        "#ef4444",  # Prix négatifs - rouge (relative négatif)
        "#ef4444",  # Indisponibilité APEX - rouge (relative négatif)
        "#16a34a",  # Irradiation & Simulation - vert (relative positif)
        "#ef4444",  # Écart résiduel - rouge (relative négatif)
        "#1e40af"   # Production réelle - bleu foncé (absolute)
    ]
    
    # Textes pour chaque segment
    text_values = [
        f"{budget_p50:,} MWh".replace(",", " "),
        f"{indisponibilite_reseau:,} MWh".replace(",", " "),
        f"{prix_negatifs:,} MWh".replace(",", " "),
        f"{indisponibilite_apex:,} MWh".replace(",", " "),
        f"{irradiation_simulation:,} MWh".replace(",", " "),
        f"{ecart_residuel:,} MWh".replace(",", " "),
        f"{production_reelle:,} MWh".replace(",", " ")
    ]
    
    # Création du Waterfall avec les couleurs définies
    waterfall = go.Waterfall(
                orientation="v",
        measure=measures,
        x=categories,
                textposition="outside",
        text=text_values,
        y=values,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#16a34a"}},  # Vert pour les valeurs positives
        decreasing={"marker": {"color": "#ef4444"}},  # Rouge pour les valeurs négatives
        totals={"marker": {"color": "#1e40af"}}  # Bleu foncé pour les valeurs absolues
    )
    
    fig = go.Figure(waterfall)
    
    # Pour personnaliser chaque couleur individuellement, on doit utiliser une approche différente
    # On peut créer une liste de couleurs basée sur le type de mesure et la valeur
    # Mais Plotly Waterfall ne supporte pas directement les couleurs individuelles
    # On va donc définir les couleurs via les paramètres increasing/decreasing/totals qui sont les seuls supportés
    # Les couleurs seront appliquées selon les règles : totals (absolute) = bleu, decreasing = rouge, increasing = vert
    
    fig.update_layout(
        title="💧 Détail des Pertes (Waterfall)",
        yaxis_title="MWh",
        height=500,
        margin=dict(b=80, t=50, l=50, r=50)
    )
    fig = apply_glassmorphism_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # P.5 : Carte Gisement Solaire par Zone
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-top: 1rem;">', unsafe_allow_html=True)
    
    # Définition des territoires d'outre-mer avec leurs coordonnées (nécessaire pour le panneau)
    territoires_om = {
        "Guadeloupe": {
            "lat_range": [15.5, 16.5],
            "lon_range": [-62.0, -61.0],
            "center": {"lat": 16.15, "lon": -61.6},
            "color": "#3b82f6"  # Bleu
        },
        "Martinique": {
            "lat_range": [14.3, 14.9],
            "lon_range": [-61.3, -60.7],
            "center": {"lat": 14.64, "lon": -61.0},
            "color": "#3b82f6"  # Bleu
        },
        "Guyane": {
            "lat_range": [2.0, 6.0],
            "lon_range": [-54.5, -51.5],
            "center": {"lat": 4.0, "lon": -53.0},
            "color": "#10b981"  # Vert
        },
        "La Réunion": {
            "lat_range": [-21.5, -20.8],
            "lon_range": [55.2, 55.8],
            "center": {"lat": -21.15, "lon": 55.5},
            "color": "#3b82f6"  # Bleu
        }
    }
    
    # Fonction pour récupérer les sites d'un territoire (nécessaire pour le panneau)
    def get_sites_territoire(territoire_name, territoire_config, annees_selectionnees, spv_selectionnes):
        """Récupère les sites d'un territoire d'outre-mer"""
        lat_range = territoire_config["lat_range"]
        lon_range = territoire_config["lon_range"]
        
        query = f"""
        SELECT 
            e.id_site,
            e.nom_site,
            e.latitude,
            e.longitude,
            AVG(cms.irra_reel) as irra_reel_moyenne,
            AVG(cms.irra_pvsyst_incl) as irra_budget_moyenne
        FROM exposition e
        LEFT JOIN calculs_mensuel_sites cms ON e.id_site = cms.id_site
        WHERE e.latitude IS NOT NULL 
        AND e.longitude IS NOT NULL
        AND e.latitude BETWEEN {lat_range[0]} AND {lat_range[1]}
        AND e.longitude BETWEEN {lon_range[0]} AND {lon_range[1]}
        """
        
        where_conditions = []
        if annees_selectionnees:
            annees_str = ','.join(map(str, annees_selectionnees))
            where_conditions.append(f"CAST(strftime('%Y', cms.date) AS INTEGER) IN ({annees_str})")
        
        if spv_selectionnes:
            spvs_str = "','".join(spv_selectionnes).replace("'", "''")
            where_conditions.append(f"e.spv IN ('{spvs_str}')")
        
        if where_conditions:
            query += " AND " + " AND ".join(where_conditions)
        
        query += """
        GROUP BY e.id_site, e.nom_site, e.latitude, e.longitude
        HAVING irra_reel_moyenne IS NOT NULL
        """
        
        df = load_data_from_db(query)
        return df if df is not None and not df.empty else pd.DataFrame()
    
    # Fonction pour déterminer la zone d'un site selon ses coordonnées GPS
    def determine_zone_france(latitude, longitude):
        """Détermine dans quelle zone de France se trouve un site"""
        # Centre approximatif de la France : ~46.6°N, 2.5°E
        lat_center = 46.6
        lon_center = 2.5
        
        if latitude is None or longitude is None:
            return None
        
        if latitude >= lat_center:
            # Nord
            if longitude < lon_center:
                return "Nord-Ouest"
            else:
                return "Nord-Est"
        else:
            # Sud
            if longitude < lon_center:
                return "Sud-Ouest"
            else:
                return "Sud-Est"
    
    # Disposition : France Métropolitaine à gauche, 4 autres à droite en grille 2x2
    col_left, col_right = st.columns([1, 1])
    
    # Récupérer les sites avec leurs coordonnées et irradiation
    query_sites_irradiation = f"""
    SELECT 
        e.id_site,
        e.nom_site,
        e.latitude,
        e.longitude,
        AVG(cms.irra_reel) as irra_reel_moyenne,
        AVG(cms.irra_pvsyst_incl) as irra_budget_moyenne
    FROM exposition e
    LEFT JOIN calculs_mensuel_sites cms ON e.id_site = cms.id_site
    WHERE e.latitude IS NOT NULL 
    AND e.longitude IS NOT NULL
    """
    
    # Ajouter les filtres si nécessaire
    where_conditions = []
    if annees_selectionnees:
        annees_str = ','.join(map(str, annees_selectionnees))
        where_conditions.append(f"CAST(strftime('%Y', cms.date) AS INTEGER) IN ({annees_str})")
    
    if spv_selectionnes:
        spvs_str = "','".join(spv_selectionnes).replace("'", "''")
        where_conditions.append(f"e.spv IN ('{spvs_str}')")
    
    if where_conditions:
        query_sites_irradiation += " AND " + " AND ".join(where_conditions)
    
    query_sites_irradiation += """
    GROUP BY e.id_site, e.nom_site, e.latitude, e.longitude
    HAVING irra_reel_moyenne IS NOT NULL
    """
    
    df_sites = load_data_from_db(query_sites_irradiation)
    
    with col_left:
        if df_sites is not None and not df_sites.empty:
            # Déterminer la zone pour chaque site
            df_sites['zone'] = df_sites.apply(
                lambda row: determine_zone_france(row['latitude'], row['longitude']), 
                axis=1
            )
            
            # Filtrer les sites avec zone déterminée
            df_sites = df_sites[df_sites['zone'].notna()]
            
            if not df_sites.empty:
                # Calculer les moyennes par zone
                moyennes_zone = df_sites.groupby('zone').agg({
                    'irra_reel_moyenne': 'mean',
                    'irra_budget_moyenne': 'mean'
                }).reset_index()
                
                # Calculer l'écart en pourcentage par rapport au budget
                moyennes_zone['ecart_pct'] = ((moyennes_zone['irra_reel_moyenne'] - moyennes_zone['irra_budget_moyenne']) / moyennes_zone['irra_budget_moyenne'] * 100)
                
                # Couleurs par zone
                colors_zone = {
                    "Sud-Ouest": "#3b82f6",  # Bleu
                    "Sud-Est": "#fbbf24",    # Jaune
                    "Nord-Ouest": "#ef4444",  # Rouge
                    "Nord-Est": "#10b981"     # Vert
                }
                
                # Centres approximatifs des zones pour afficher les moyennes
                zone_centers = {
                    "Sud-Ouest": {"lat": 44.0, "lon": 0.5},
                    "Sud-Est": {"lat": 44.0, "lon": 5.0},
                    "Nord-Ouest": {"lat": 48.5, "lon": 0.5},
                    "Nord-Est": {"lat": 48.5, "lon": 5.0}
                }
                
                # Créer la carte avec Plotly - utiliser Scattermapbox comme dans le Dashboard
                fig = go.Figure()
                
                # Ajouter les points pour chaque zone avec leurs couleurs
                for zone in ["Sud-Ouest", "Sud-Est", "Nord-Ouest", "Nord-Est"]:
                    df_zone = df_sites[df_sites['zone'] == zone]
                    if not df_zone.empty:
                        fig.add_trace(go.Scattermapbox(
                            lat=df_zone['latitude'],
                            lon=df_zone['longitude'],
                            mode='markers',
                            name=zone,
                            marker=dict(
                                size=6,
                                color=colors_zone[zone],
                                opacity=0.9
                            ),
                            text=df_zone['nom_site'],
                            hovertemplate='<b>%{text}</b><br>' +
                                        'Irradiation réelle: %{customdata[0]:.1f} kWh/m²<br>' +
                                        'Irradiation budget: %{customdata[1]:.1f} kWh/m²<extra></extra>',
                            customdata=df_zone[['irra_reel_moyenne', 'irra_budget_moyenne']].values,
                            showlegend=True
                        ))
                
                # Ajouter les moyennes par zone comme annotations textuelles dans des boîtes blanches
                for _, row in moyennes_zone.iterrows():
                    zone = row['zone']
                    ecart_pct = row['ecart_pct']
                    center = zone_centers[zone]
                    
                    # Vérifier que ecart_pct n'est pas NaN
                    if pd.isna(ecart_pct):
                        continue
                    
                    # Format du texte avec signe +
                    text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                    # Note: Les pourcentages sont affichés via overlay HTML, pas de marqueurs blancs nécessaires
                
                # Calculer la moyenne globale d'irradiation réelle
                moyenne_globale_irra = df_sites['irra_reel_moyenne'].mean()
                moyenne_globale_budget = df_sites['irra_budget_moyenne'].mean()
                ecart_global_pct = ((moyenne_globale_irra - moyenne_globale_budget) / moyenne_globale_budget * 100)
                
                # Calculer le nombre de sites en France Métropolitaine
                nb_sites_metropole = len(df_sites)
                
                # Utiliser les mêmes paramètres que le Dashboard
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=dict(lat=46.8, lon=2.2),  # Même centre que Dashboard
                        zoom=5.2,  # Même zoom que Dashboard
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=700,
                    title=dict(
                        text=f'📍 France Métropolitaine<br><span style="font-size: 12px; color: #6b7280;">{nb_sites_metropole} site(s)</span>',
                        font=dict(size=15, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=True
                )
                
                # Grande carte France Métropolitaine avec overlay HTML
                col_map, col_text = st.columns([3, 1])
                
                with col_map:
                    # Afficher la carte
                    st.plotly_chart(fig, use_container_width=True, key="france_map")
                    
                    # Overlay HTML positionné au-dessus de la carte avec margin négatif
                    overlay_parts = []
                    for _, row in moyennes_zone.iterrows():
                        zone = row['zone']
                        ecart_pct = row['ecart_pct']
                        if pd.isna(ecart_pct):
                            continue
                        text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                        center = zone_centers[zone]
                        
                        # Convertir les coordonnées géographiques en position relative
                        lat_min, lat_max = 42, 51
                        lon_min, lon_max = -5, 10
                        
                        lat_percent = ((center['lat'] - lat_min) / (lat_max - lat_min)) * 100
                        lon_percent = ((center['lon'] - lon_min) / (lon_max - lon_min)) * 100
                        
                        overlay_parts.append(f'<div style="position: absolute; top: {100 - lat_percent}%; left: {lon_percent}%; transform: translate(-50%, -50%); background: rgba(255, 255, 255, 0.95); border-radius: 8px; padding: 8px 12px; font-size: 20px; font-weight: bold; color: #000000; font-family: Arial Black; pointer-events: auto; z-index: 1000; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">{text_value}</div>')
                    
                    overlay_html = f'<div style="position: relative; margin-top: -700px; height: 700px; pointer-events: none; width: 100%;">{"".join(overlay_parts)}</div>'
                    st.markdown(overlay_html, unsafe_allow_html=True)
                
                with col_text:
                    # Panneau de texte à droite de la carte - France Métropolitaine
                    st.markdown(
                        f"""
                        <div style="padding: 20px; text-align: center; margin-top: 10px;">
                            <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                                Gisement solaire France Métropolitaine<br>par rapport au budget
                            </p>
                            <p style="font-size: 36px; font-weight: bold; color: #fbbf24; margin: 20px 0;">
                                {"+" if ecart_global_pct > 0 else ""}{ecart_global_pct:.1f} %
                            </p>
                            <p style="font-size: 12px; color: #666; margin-top: 10px;">
                                Moyenne irradiation réelle : {moyenne_globale_irra:.1f} kWh/m²<br>
                                Moyenne irradiation budget : {moyenne_globale_budget:.1f} kWh/m²
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Calculer les moyennes globales pour tous les territoires d'outre-mer
                    toutes_moyennes_irra_om = []
                    toutes_moyennes_budget_om = []
                    
                    for territoire_name, config in territoires_om.items():
                        df_territoire = get_sites_territoire(territoire_name, config, annees_selectionnees, spv_selectionnes)
                        if not df_territoire.empty:
                            moyenne_irra = df_territoire['irra_reel_moyenne'].mean()
                            moyenne_budget = df_territoire['irra_budget_moyenne'].mean()
                            toutes_moyennes_irra_om.append(moyenne_irra)
                            toutes_moyennes_budget_om.append(moyenne_budget)
                    
                    # Calculer les moyennes globales des territoires d'outre-mer
                    if toutes_moyennes_irra_om and toutes_moyennes_budget_om:
                        moyenne_globale_irra_om = sum(toutes_moyennes_irra_om) / len(toutes_moyennes_irra_om)
                        moyenne_globale_budget_om = sum(toutes_moyennes_budget_om) / len(toutes_moyennes_budget_om)
                        ecart_global_pct_om = ((moyenne_globale_irra_om - moyenne_globale_budget_om) / moyenne_globale_budget_om * 100)
                    else:
                        moyenne_globale_irra_om = 0
                        moyenne_globale_budget_om = 0
                        ecart_global_pct_om = 0
                    
                    # Panneau pour les territoires d'outre-mer (sous le panneau France) - même style que France
                    st.markdown(
                        f"""
                        <div style="padding: 20px; text-align: center; margin-top: 20px;">
                            <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                                Gisement solaire Territoires d'Outre-Mer<br>par rapport au budget
                            </p>
                            <p style="font-size: 36px; font-weight: bold; color: #fbbf24; margin: 20px 0;">
                                {"+" if ecart_global_pct_om > 0 else ""}{ecart_global_pct_om:.1f} %
                            </p>
                            <p style="font-size: 12px; color: #666; margin-top: 10px;">
                                Moyenne irradiation réelle : {moyenne_globale_irra_om:.1f} kWh/m²<br>
                                Moyenne irradiation budget : {moyenne_globale_budget_om:.1f} kWh/m²
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Aucun site avec coordonnées GPS valides trouvé pour la France Métropolitaine")
        else:
            st.info("Aucune donnée disponible pour la carte France Métropolitaine")
    
    # P.6 : Cartes des Territoires d'Outre-Mer (à droite)
    # Créer les 4 cartes en grille 2x2 à droite
    with col_right:
        # Première ligne : 2 cartes
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            # Guadeloupe (top left)
            territoire = "Guadeloupe"
            config = territoires_om[territoire]
            df_territoire = get_sites_territoire(territoire, config, annees_selectionnees, spv_selectionnes)
            
            if not df_territoire.empty:
                nb_sites = len(df_territoire)
                moyenne_irra = df_territoire['irra_reel_moyenne'].mean()
                moyenne_budget = df_territoire['irra_budget_moyenne'].mean()
                ecart_pct = ((moyenne_irra - moyenne_budget) / moyenne_budget * 100)
                
                fig = go.Figure()
                
                # Utiliser Scattermapbox comme dans le Dashboard
                fig.add_trace(go.Scattermapbox(
                    lat=df_territoire['latitude'],
                    lon=df_territoire['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=config['color'],
                        opacity=0.9
                    ),
                    text=df_territoire['nom_site'],
                    hovertemplate='<b>%{text}</b><br>Irradiation: %{customdata[0]:.1f} kWh/m²<extra></extra>',
                    customdata=df_territoire[['irra_reel_moyenne']].values,
                    name='Sites'
                ))
                
                # Format du texte avec signe +
                text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                # Note: Les pourcentages sont affichés via overlay HTML, pas de marqueurs blancs nécessaires
                
                # Utiliser les mêmes paramètres de zoom que le Dashboard
                zoom_levels = {
                    "Guadeloupe": 8.2,
                    "Martinique": 8.8,
                    "Guyane": 5.5,
                    "La Réunion": 8.5
                }
                zoom = zoom_levels.get(territoire, 8.0)
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=config['center'],
                        zoom=zoom,
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'T {territoire}<br><span style="font-size: 11px; color: #6b7280;">{nb_sites} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                # Afficher la carte avec overlay HTML pour le pourcentage
                map_container = st.container()
                with map_container:
                    chart_placeholder = st.empty()
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    
                    # Overlay HTML pour le pourcentage du territoire
                    if not df_territoire.empty:
                        # Calculer les limites géographiques du territoire pour le positionnement
                        lat_min = config['lat_range'][0]
                        lat_max = config['lat_range'][1]
                        lon_min = config['lon_range'][0]
                        lon_max = config['lon_range'][1]
                        
                        # Position du centre en pourcentage
                        lat_percent = ((config['center']['lat'] - lat_min) / (lat_max - lat_min)) * 100
                        lon_percent = ((config['center']['lon'] - lon_min) / (lon_max - lon_min)) * 100
                        
                        overlay_html = f'''
                        <div style="position: relative; margin-top: -340px; height: 340px; pointer-events: none;">
                            <div style="position: absolute; 
                                        top: {100 - lat_percent}%; 
                                        left: {lon_percent}%; 
                                        transform: translate(-50%, -50%);
                                        background: rgba(255, 255, 255, 0.95);
                                        border-radius: 8px;
                                        padding: 8px 12px;
                                        font-size: 18px;
                                        font-weight: bold;
                                        color: #000000;
                                        font-family: Arial Black;
                                        pointer-events: auto;
                                        z-index: 1000;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                                {text_value}
                            </div>
                        </div>
                        '''
                        st.markdown(overlay_html, unsafe_allow_html=True)
                    else:
                        st.info(f"Aucun site trouvé pour {territoire}")
        
        with col_r2:
            # Martinique (top right)
            territoire = "Martinique"
            config = territoires_om[territoire]
            df_territoire = get_sites_territoire(territoire, config, annees_selectionnees, spv_selectionnes)
            
            if not df_territoire.empty:
                nb_sites = len(df_territoire)
                moyenne_irra = df_territoire['irra_reel_moyenne'].mean()
                moyenne_budget = df_territoire['irra_budget_moyenne'].mean()
                ecart_pct = ((moyenne_irra - moyenne_budget) / moyenne_budget * 100)
                
                fig = go.Figure()
                
                # Utiliser Scattermapbox comme dans le Dashboard
                fig.add_trace(go.Scattermapbox(
                    lat=df_territoire['latitude'],
                    lon=df_territoire['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=config['color'],
                        opacity=0.9
                    ),
                    text=df_territoire['nom_site'],
                    hovertemplate='<b>%{text}</b><br>Irradiation: %{customdata[0]:.1f} kWh/m²<extra></extra>',
                    customdata=df_territoire[['irra_reel_moyenne']].values,
                    name='Sites'
                ))
                
                # Format du texte avec signe +
                text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                # Note: Les pourcentages sont affichés via overlay HTML, pas de marqueurs blancs nécessaires
                
                # Utiliser les mêmes paramètres de zoom que le Dashboard
                zoom_levels = {
                    "Guadeloupe": 8.2,
                    "Martinique": 8.8,
                    "Guyane": 5.5,
                    "La Réunion": 8.5
                }
                zoom = zoom_levels.get(territoire, 8.0)
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=config['center'],
                        zoom=zoom,
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'T {territoire}<br><span style="font-size: 11px; color: #6b7280;">{nb_sites} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                # Afficher la carte avec overlay HTML pour le pourcentage
                map_container = st.container()
                with map_container:
                    chart_placeholder = st.empty()
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    
                    # Overlay HTML pour le pourcentage du territoire
                    if not df_territoire.empty:
                        # Calculer les limites géographiques du territoire pour le positionnement
                        lat_min = config['lat_range'][0]
                        lat_max = config['lat_range'][1]
                        lon_min = config['lon_range'][0]
                        lon_max = config['lon_range'][1]
                        
                        # Position du centre en pourcentage
                        lat_percent = ((config['center']['lat'] - lat_min) / (lat_max - lat_min)) * 100
                        lon_percent = ((config['center']['lon'] - lon_min) / (lon_max - lon_min)) * 100
                        
                        overlay_html = f'''
                        <div style="position: relative; margin-top: -340px; height: 340px; pointer-events: none;">
                            <div style="position: absolute; 
                                        top: {100 - lat_percent}%; 
                                        left: {lon_percent}%; 
                                        transform: translate(-50%, -50%);
                                        background: rgba(255, 255, 255, 0.95);
                                        border-radius: 8px;
                                        padding: 8px 12px;
                                        font-size: 18px;
                                        font-weight: bold;
                                        color: #000000;
                                        font-family: Arial Black;
                                        pointer-events: auto;
                                        z-index: 1000;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                                {text_value}
                            </div>
                        </div>
                        '''
                        st.markdown(overlay_html, unsafe_allow_html=True)
                    else:
                        st.info(f"Aucun site trouvé pour {territoire}")
        
        # Deuxième ligne : 2 cartes
        col_r3, col_r4 = st.columns(2)
        
        with col_r3:
            # Guyane (bottom left)
            territoire = "Guyane"
            config = territoires_om[territoire]
            df_territoire = get_sites_territoire(territoire, config, annees_selectionnees, spv_selectionnes)
            
            if not df_territoire.empty:
                nb_sites = len(df_territoire)
                moyenne_irra = df_territoire['irra_reel_moyenne'].mean()
                moyenne_budget = df_territoire['irra_budget_moyenne'].mean()
                ecart_pct = ((moyenne_irra - moyenne_budget) / moyenne_budget * 100)
                
                fig = go.Figure()
                
                # Utiliser Scattermapbox comme dans le Dashboard
                fig.add_trace(go.Scattermapbox(
                    lat=df_territoire['latitude'],
                    lon=df_territoire['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=config['color'],
                        opacity=0.9
                    ),
                    text=df_territoire['nom_site'],
                    hovertemplate='<b>%{text}</b><br>Irradiation: %{customdata[0]:.1f} kWh/m²<extra></extra>',
                    customdata=df_territoire[['irra_reel_moyenne']].values,
                    name='Sites'
                ))
                
                # Format du texte avec signe +
                text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                # Note: Les pourcentages sont affichés via overlay HTML, pas de marqueurs blancs nécessaires
                
                # Utiliser les mêmes paramètres de zoom que le Dashboard
                zoom_levels = {
                    "Guadeloupe": 8.2,
                    "Martinique": 8.8,
                    "Guyane": 5.5,
                    "La Réunion": 8.5
                }
                zoom = zoom_levels.get(territoire, 8.0)
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=config['center'],
                        zoom=zoom,
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'T {territoire}<br><span style="font-size: 11px; color: #6b7280;">{nb_sites} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                # Afficher la carte avec overlay HTML pour le pourcentage
                map_container = st.container()
                with map_container:
                    chart_placeholder = st.empty()
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    
                    # Overlay HTML pour le pourcentage du territoire
                    if not df_territoire.empty:
                        # Calculer les limites géographiques du territoire pour le positionnement
                        lat_min = config['lat_range'][0]
                        lat_max = config['lat_range'][1]
                        lon_min = config['lon_range'][0]
                        lon_max = config['lon_range'][1]
                        
                        # Position du centre en pourcentage
                        lat_percent = ((config['center']['lat'] - lat_min) / (lat_max - lat_min)) * 100
                        lon_percent = ((config['center']['lon'] - lon_min) / (lon_max - lon_min)) * 100
                        
                        overlay_html = f'''
                        <div style="position: relative; margin-top: -340px; height: 340px; pointer-events: none;">
                            <div style="position: absolute; 
                                        top: {100 - lat_percent}%; 
                                        left: {lon_percent}%; 
                                        transform: translate(-50%, -50%);
                                        background: rgba(255, 255, 255, 0.95);
                                        border-radius: 8px;
                                        padding: 8px 12px;
                                        font-size: 18px;
                                        font-weight: bold;
                                        color: #000000;
                                        font-family: Arial Black;
                                        pointer-events: auto;
                                        z-index: 1000;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                                {text_value}
                            </div>
                        </div>
                        '''
                        st.markdown(overlay_html, unsafe_allow_html=True)
                    else:
                        st.info(f"Aucun site trouvé pour {territoire}")
        
        with col_r4:
            # La Réunion (bottom right)
            territoire = "La Réunion"
            config = territoires_om[territoire]
            df_territoire = get_sites_territoire(territoire, config, annees_selectionnees, spv_selectionnes)
            
            if not df_territoire.empty:
                nb_sites = len(df_territoire)
                moyenne_irra = df_territoire['irra_reel_moyenne'].mean()
                moyenne_budget = df_territoire['irra_budget_moyenne'].mean()
                ecart_pct = ((moyenne_irra - moyenne_budget) / moyenne_budget * 100)
                
                fig = go.Figure()
                
                # Utiliser Scattermapbox comme dans le Dashboard
                fig.add_trace(go.Scattermapbox(
                    lat=df_territoire['latitude'],
                    lon=df_territoire['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=config['color'],
                        opacity=0.9
                    ),
                    text=df_territoire['nom_site'],
                    hovertemplate='<b>%{text}</b><br>Irradiation: %{customdata[0]:.1f} kWh/m²<extra></extra>',
                    customdata=df_territoire[['irra_reel_moyenne']].values,
                    name='Sites'
                ))
                
                # Format du texte avec signe +
                text_value = f"+{ecart_pct:.1f} %" if ecart_pct > 0 else f"{ecart_pct:.1f} %"
                # Note: Les pourcentages sont affichés via overlay HTML, pas de marqueurs blancs nécessaires
                
                # Utiliser les mêmes paramètres de zoom que le Dashboard
                zoom_levels = {
                    "Guadeloupe": 8.2,
                    "Martinique": 8.8,
                    "Guyane": 5.5,
                    "La Réunion": 8.5
                }
                zoom = zoom_levels.get(territoire, 8.0)
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=config['center'],
                        zoom=zoom,
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'T {territoire}<br><span style="font-size: 11px; color: #6b7280;">{nb_sites} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                # Afficher la carte avec overlay HTML pour le pourcentage
                map_container = st.container()
                with map_container:
                    chart_placeholder = st.empty()
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    
                    # Overlay HTML pour le pourcentage du territoire
                    if not df_territoire.empty:
                        # Calculer les limites géographiques du territoire pour le positionnement
                        lat_min = config['lat_range'][0]
                        lat_max = config['lat_range'][1]
                        lon_min = config['lon_range'][0]
                        lon_max = config['lon_range'][1]
                        
                        # Position du centre en pourcentage
                        lat_percent = ((config['center']['lat'] - lat_min) / (lat_max - lat_min)) * 100
                        lon_percent = ((config['center']['lon'] - lon_min) / (lon_max - lon_min)) * 100
                        
                        overlay_html = f'''
                        <div style="position: relative; margin-top: -340px; height: 340px; pointer-events: none;">
                            <div style="position: absolute; 
                                        top: {100 - lat_percent}%; 
                                        left: {lon_percent}%; 
                                        transform: translate(-50%, -50%);
                                        background: rgba(255, 255, 255, 0.95);
                                        border-radius: 8px;
                                        padding: 8px 12px;
                                        font-size: 18px;
                                        font-weight: bold;
                                        color: #000000;
                                        font-family: Arial Black;
                                        pointer-events: auto;
                                        z-index: 1000;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                                {text_value}
                            </div>
                        </div>
                        '''
                        st.markdown(overlay_html, unsafe_allow_html=True)
            else:
                st.info(f"Aucun site trouvé pour {territoire}")
    
    # Fermer le div principal de la section P.5 (carte France Métro + cartes outre-mer)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION C: Irradiation & Météo
    # ============================================
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
    ">☀️ Irradiation & Météo</div>
    ''', unsafe_allow_html=True)
    
    # Premier graphique : Irradiation Réelle vs Théorique (pleine largeur)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">', unsafe_allow_html=True)
    df_irra = get_irradiation_reelle_vs_theorique(annees_selectionnees, spv_selectionnes)
    df_irra_2024 = get_irradiation_reelle_2024(spv_selectionnes)
    
    if not df_irra.empty:
        fig = go.Figure()
        # Barre 1 : Irradiation réelle (période sélectionnée)
        fig.add_trace(go.Bar(name='Réelle', x=df_irra['mois'], y=df_irra['irra_reel'], marker_color='#0A84FF'))
        # Barre 2 : Irradiation théorique (période sélectionnée)
        fig.add_trace(go.Bar(name='Théorique', x=df_irra['mois'], y=df_irra['irra_theorique'], marker_color='#87ceeb', opacity=0.7))
        # Barre 3 : Irradiation réelle 2024 (toujours affichée pour comparaison)
        if not df_irra_2024.empty:
            fig.add_trace(go.Bar(name='Réelle 2024', x=df_irra_2024['mois'], y=df_irra_2024['irra_reel_2024'], marker_color='#10b981', opacity=0.8))
        # Ligne de déviation
        fig.add_trace(go.Scatter(
            name='Déviation',
            x=df_irra['mois'],
            y=df_irra['dev_irra'],
            mode='lines+markers',
            line=dict(color='#f59e0b', width=2),
            yaxis='y2'
        ))
        fig.update_layout(
            title='☀️ Irradiation Réelle vs Théorique',
            xaxis_title='Mois',
            yaxis_title='Irradiation (kWh/m²)',
            yaxis2=dict(title='Déviation', overlaying='y', side='right'),
            barmode='group',
            height=400
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Deuxième graphique : Corrélation Irradiation/Production (pleine largeur)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    df_corr = get_correlation_irradiation_production(annees_selectionnees, spv_selectionnes)
    if not df_corr.empty and len(df_corr) > 1:
        # Calculer corrélation
        correlation = df_corr['irra_reel'].corr(df_corr['prod_reel'])
        r_squared = correlation ** 2
        
        # Créer le graphique avec échelle logarithmique pour meilleure lisibilité
        # Utiliser hover_data pour inclure les informations supplémentaires (sans dispo_brut et dispo_contrat)
        fig = px.scatter(
            df_corr,
            x='irra_reel',
            y='prod_reel',
            title='📊 Corrélation Irradiation/Production',
            labels={'irra_reel': 'Irradiation (kWh/m²)', 'prod_reel': 'Production (kWh)'},
            log_y=True,  # Échelle logarithmique pour l'axe Y (Production)
            opacity=0.6,  # Transparence pour mieux voir les points superposés
            hover_data=['nom_site', 'id_site', 'annee', 'mois', 'spv', 'prod_pvsyst', 'pr_réel']
        )
        
        # Personnaliser le hover template avec plus de détails
        # Les données sont accessibles via %{customdata[0]}, %{customdata[1]}, etc.
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'ID Site: %{customdata[1]}<br>' +
                         'Date: %{customdata[2]:.0f}-%{customdata[3]:02.0f}<br>' +
                         'SPV: %{customdata[4]}<br>' +
                         'Irradiation: %{x:.2f} kWh/m²<br>' +
                         'Production réelle: %{y:,.0f} kWh<br>' +
                         'Production PVsyst: %{customdata[5]:,.0f} kWh<br>' +
                         'PR réel: %{customdata[6]:.2f}%<br>' +
                         '<extra></extra>'
        )
        
        # Calculer la ligne de régression manuellement pour la rendre rouge
        import numpy as np
        # Filtrer les valeurs valides (pas de NaN ou inf)
        x_data = df_corr['irra_reel'].values
        y_data = df_corr['prod_reel'].values
        valid_mask = np.isfinite(x_data) & np.isfinite(y_data) & (y_data > 0)
        x_valid = x_data[valid_mask]
        y_valid = y_data[valid_mask]
        
        if len(x_valid) > 1:
            # Calculer la régression linéaire en échelle logarithmique
            # Log(Y) = a * X + b
            log_y_valid = np.log10(y_valid)
            coeffs = np.polyfit(x_valid, log_y_valid, 1)
            
            # Générer les points pour la ligne de tendance
            x_trend = np.linspace(x_valid.min(), x_valid.max(), 100)
            log_y_trend = np.polyval(coeffs, x_trend)
            y_trend = 10 ** log_y_trend
            
            # Ajouter la ligne de tendance rouge manuellement
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                name='Tendance (OLS)',
                line=dict(color='#ef4444', width=4),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Appliquer le thème
        fig = apply_glassmorphism_theme(fig)
        
        fig.update_layout(
            height=400,
            xaxis_title='Irradiation (kWh/m²)',
            yaxis_title='Production (kWh) - Échelle logarithmique',
            yaxis=dict(type="log")  # Confirmer l'échelle logarithmique
        )
        
        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)
        
        # Message simplifié en dessous du graphique
        st.info(f"Corrélation R² = {r_squared:.3f}")
        
        # Détails du calcul en dessous du graphique
        st.markdown(f"""
            <div style="margin-top: 15px; padding: 15px; background: rgba(240, 248, 255, 0.7); border-radius: 10px; border-left: 4px solid #3b82f6;">
                <h4 style="color: #1f2937; margin-bottom: 10px; font-size: 14px;">📐 Calcul du Coefficient de Corrélation (R²)</h4>
                <p style="font-size: 12px; color: #4b5563; margin-bottom: 8px; line-height: 1.6;">
                    <strong>Étape 1 - Coefficient de corrélation de Pearson (r):</strong><br>
                    r = corrélation entre irradiation et production<br>
                    Valeur entre <strong>-1</strong> (corrélation négative parfaite) et <strong>+1</strong> (corrélation positive parfaite)<br>
                    <strong>r = {correlation:.3f}</strong>
                </p>
                <p style="font-size: 12px; color: #4b5563; margin-top: 10px; line-height: 1.6;">
                    <strong>🎯 Interprétation:</strong><br>
                    • <strong>R² &lt; 0.3</strong> = Corrélation faible → Problèmes techniques possibles<br>
                    • <strong>R² entre 0.3 et 0.7</strong> = Corrélation modérée<br>
                    • <strong>R² &gt; 0.7</strong> = Corrélation forte → Relation normale<br>
                    • <strong>R² = 1</strong> = Toute la production est expliquée par l'irradiation (théoriquement impossible)
                </p>
                <p style="font-size: 12px; color: #4b5563; margin-top: 10px; line-height: 1.6;">
                    <strong>🔍 Chaque point représente:</strong><br>
                    Un <strong>couple (irradiation, production)</strong> pour une <strong>combinaison Site × Mois</strong>.<br><br>
                    Si filtres appliqués : données des sites/mois sélectionnés.<br>
                    Sinon : tous les sites et mois disponibles dans la période.
                </p>
                <p style="font-size: 12px; color: #4b5563; margin-top: 10px; line-height: 1.6;">
                    <strong>📊 Comment lire ce graphique:</strong><br>
                    • Points alignés le long de la ligne de tendance rouge → Bonne corrélation<br>
                    • Points dispersés → Faible corrélation (comme ici)<br>
                    • Dispersion = autres facteurs influencent la production : panneaux sales, ombrages, pannes, erreurs de mesure
                </p>
                <p style="font-size: 12px; color: #4b5563; margin-top: 15px; line-height: 1.6;">
                    <strong>🗺️ Corrélation par zones (sud ouest, sud est, etc,...)</strong><br>
                    Analyse de la corrélation entre irradiation et production selon les zones géographiques (Sud-Ouest, Sud-Est, Nord-Ouest, Nord-Est) pour identifier les différences régionales de performance.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tableau des corrélations par zone
        df_corr_zone = get_correlation_par_zone(annees_selectionnees, spv_selectionnes)
        if not df_corr_zone.empty:
            # Configuration des colonnes dynamique selon les années présentes
            column_config = {"Zone": "Zone"}
            for annee in [2023, 2024, 2025]:
                if f'R² {annee}' in df_corr_zone.columns:
                    column_config[f'R² {annee}'] = st.column_config.NumberColumn(f'R² {annee}', format="%.3f")
            column_config["Nb points"] = st.column_config.NumberColumn("Nb points", format="%d")
            
            # Vérifier que le tableau contient exactement 8 lignes (zones)
            # Si ce n'est pas le cas, c'est un problème de données, mais on calcule quand même la hauteur
            nb_lignes = len(df_corr_zone)
            # Hauteur précise : 41px par ligne + 65px pour l'en-tête (sans marges excessives)
            hauteur_adaptative = nb_lignes * 41 + 65
            
            st.dataframe(
                df_corr_zone,
                column_config=column_config,
                hide_index=True,
                use_container_width=True,
                height=hauteur_adaptative  # Hauteur adaptative : exactement 8 lignes pour les zones
            )
        else:
            st.info("Aucune donnée disponible pour les corrélations par zone")
        
        st.markdown(f"""
        <div style="margin-top: 15px; padding: 15px; background: rgba(240, 248, 255, 0.7); border-radius: 10px; border-left: 4px solid #3b82f6;">
            <p style="font-size: 12px; color: #4b5563; margin-top: 10px; line-height: 1.6;">
                <strong>📅 Corrélation par Mois de l'année (de janvier à décembre)</strong><br>
                Analyse de la corrélation entre irradiation et production pour chaque mois de l'année afin de détecter les variations saisonnières et les périodes avec des problèmes techniques.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tableau des corrélations par mois
        df_corr_mois = get_correlation_par_mois(annees_selectionnees, spv_selectionnes)
        if not df_corr_mois.empty:
            # Configuration des colonnes dynamique selon les années présentes
            column_config = {"Mois": "Mois"}
            for annee in [2023, 2024, 2025]:
                if f'R² {annee}' in df_corr_mois.columns:
                    column_config[f'R² {annee}'] = st.column_config.NumberColumn(f'R² {annee}', format="%.3f")
            column_config["Nb points"] = st.column_config.NumberColumn("Nb points", format="%d")
            
            # Vérifier que le tableau contient exactement 12 lignes (mois)
            # Si ce n'est pas le cas, c'est un problème de données, mais on calcule quand même la hauteur
            nb_lignes = len(df_corr_mois)
            # Hauteur précise : 41px par ligne + 65px pour l'en-tête (sans marges excessives)
            hauteur_adaptative = nb_lignes * 41 + 65
            
            st.dataframe(
                df_corr_mois,
                column_config=column_config,
                hide_index=True,
                use_container_width=True,
                height=hauteur_adaptative  # Hauteur adaptative : exactement 12 lignes pour les mois
            )
        else:
            st.info("Aucune donnée disponible pour les corrélations par mois")
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION D: Analyses Complémentaires
    # ============================================
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
    ">🔍 Analyses Complémentaires</div>
    ''', unsafe_allow_html=True)
    
    # Déterminer l'année principale pour la comparaison (première année sélectionnée, ou la plus récente par défaut)
    annee_principale = max(annees_selectionnees) if annees_selectionnees else 2025
    annee_n1 = annee_principale - 1
    
    # Tableau mensuel des indicateurs (Année N / Année N-1)
    st.markdown(f"""
    <div style="
        padding: 16px 24px;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
    ">📊 Tableau mensuel des indicateurs ({annee_principale} / {annee_n1})</div>
    """, unsafe_allow_html=True)
    
    # Fonction pour formater une cellule combinée avec Année N, Année N-1 et évolution (format HTML)
    # Définie avant les tableaux pour être accessible aux deux
    def format_combined_cell_html(val_annee_n, val_annee_n1, format_type='float', annee_n=None, annee_n1=None):
        """Formate une cellule HTML avec valeur Année N (grande), Année N-1 (petite) et évolution colorée"""
        # Valeur Année N principale
        if pd.isna(val_annee_n):
            val_annee_n_str = "-"
        elif format_type == 'int':
            val_annee_n_str = f"{int(val_annee_n):,}"
        elif format_type == 'float':
            val_annee_n_str = f"{val_annee_n:.2f}"
        elif format_type == 'percent':
            val_annee_n_str = f"{val_annee_n:.1f}"
        else:
            val_annee_n_str = str(val_annee_n)
        
        # Valeur Année N-1 et évolution
        if pd.isna(val_annee_n1):
            label_n1 = f"Année N-1 ({annee_n1}): -" if annee_n1 else "Année N-1: -"
            return f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4px;"><div style="font-size: 14px; font-weight: 600; margin-bottom: 2px;">{val_annee_n_str}</div><div style="font-size: 11px; color: #6b7280; margin-bottom: 2px;">{label_n1}</div><div style="font-size: 11px; font-weight: 500; color: #888888;">-</div></div>'
        else:
            if format_type == 'int':
                val_annee_n1_str = f"{int(val_annee_n1):,}"
            elif format_type == 'float':
                val_annee_n1_str = f"{val_annee_n1:.2f}"
            elif format_type == 'percent':
                val_annee_n1_str = f"{val_annee_n1:.1f}"
            else:
                val_annee_n1_str = str(val_annee_n1)
            
            # Calcul de l'évolution avec couleur
            if pd.isna(val_annee_n) or val_annee_n1 == 0:
                evol_str = "-"
                evol_color = "#888888"
            else:
                evol = ((val_annee_n - val_annee_n1) / abs(val_annee_n1)) * 100
                if evol >= 0:
                    evol_str = f"+{evol:.1f}%"
                    evol_color = "#10b981"  # Vert
                else:
                    evol_str = f"{evol:.1f}%"
                    evol_color = "#ef4444"  # Rouge
            
            # Échapper les caractères spéciaux HTML
            val_annee_n_escaped = str(val_annee_n_str).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            val_annee_n1_escaped = str(val_annee_n1_str).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            evol_str_escaped = str(evol_str).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            label_n1 = f"Année N-1 ({annee_n1}):" if annee_n1 else "Année N-1:"
            
            return f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4px;"><div style="font-size: 14px; font-weight: 600; margin-bottom: 2px;">{val_annee_n_escaped}</div><div style="font-size: 11px; color: #6b7280; margin-bottom: 2px;">{label_n1} {val_annee_n1_escaped}</div><div style="font-size: 11px; font-weight: 500; color: {evol_color};">{evol_str_escaped}</div></div>'
    
    df_tableau = get_tableau_indicateurs_mensuels(annee_principale)
    
    if not df_tableau.empty:
        # S'assurer que le DataFrame est trié par ordre chronologique des mois
        mois_num_map = {
            'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4,
            'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8,
            'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
        }
        df_tableau['_mois_num'] = df_tableau['mois'].map(mois_num_map)
        df_tableau = df_tableau.sort_values('_mois_num').reset_index(drop=True)
        df_tableau = df_tableau.drop(columns=['_mois_num'])
        
        # Noms de colonnes dynamiques selon l'année
        col_annee_n = f'{annee_principale}'
        col_annee_n1 = f'{annee_n1}'
        
        # Créer un DataFrame avec colonnes combinées pour l'affichage
        df_display = pd.DataFrame()
        
        # Mapper les noms de mois aux numéros 1-12 pour l'affichage et le tri
        mois_to_num = {
            'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4,
            'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8,
            'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
        }
        # Convertir les noms de mois en numéros (1-12) comme entiers pour le tri numérique, garder TOTAL tel quel
        # Créer d'abord la colonne numérique pour le tri
        df_display['_Mois_num'] = df_tableau['mois'].apply(
            lambda x: mois_to_num.get(x, 99) if x != 'TOTAL' else 99
        )
        # Créer la colonne d'affichage : numéros comme entiers (pas de strings)
        df_display['Mois'] = df_display['_Mois_num'].apply(
            lambda x: int(x) if x != 99 else 'TOTAL'
        )
        
        # Colonnes pour le tri (cachées) - garder les valeurs numériques de l'année N
        df_display['_sort_Nb sites'] = df_tableau.get(f'nb_sites_{col_annee_n}', None)
        df_display['_sort_Prod Pvsyst'] = df_tableau.get(f'prod_pvsyst_gwh_{col_annee_n}', None)
        df_display['_sort_Moy Irrad Pvsyst'] = df_tableau.get(f'moy_irrad_pvsyst_{col_annee_n}', None)
        df_display['_sort_Prod Réelle'] = df_tableau.get(f'prod_reelle_gwh_{col_annee_n}', None)
        df_display['_sort_Moy Irrad Réelle'] = df_tableau.get(f'moy_irrad_reelle_{col_annee_n}', None)
        df_display['_sort_Dispo Contrat'] = df_tableau.get(f'dispo_contrat_{col_annee_n}', None)
        df_display['_sort_Dispo Brut'] = df_tableau.get(f'dispo_brut_{col_annee_n}', None)
        df_display['_sort_Dév Prod'] = df_tableau.get(f'dev_prod_pct_{col_annee_n}', None)
        df_display['_sort_Dév Irrad'] = df_tableau.get(f'dev_irrad_pct_{col_annee_n}', None)
        df_display['_sort_PR Budget'] = df_tableau.get(f'pr_budget_{col_annee_n}', None)
        df_display['_sort_PR Réel'] = df_tableau.get(f'pr_reel_{col_annee_n}', None)
        df_display['_sort_Dév PR'] = df_tableau.get(f'dev_pr_pct_{col_annee_n}', None)
        df_display['_sort_Performance Spécifique'] = df_tableau.get(f'perf_specifique_kwhkwc_{col_annee_n}', None)
        df_display['_sort_Taux d\'Atteinte'] = df_tableau.get(f'taux_atteinte_pct_{col_annee_n}', None)
        
        # Colonnes d'affichage combinées en HTML
        df_display['Nb sites'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'nb_sites_{col_annee_n}'), row.get(f'nb_sites_{col_annee_n1}'), 'int', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Prod Pvsyst (GWh)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'prod_pvsyst_gwh_{col_annee_n}'), row.get(f'prod_pvsyst_gwh_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Moy Irrad Pvsyst'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'moy_irrad_pvsyst_{col_annee_n}'), row.get(f'moy_irrad_pvsyst_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Prod Réelle (GWh)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'prod_reelle_gwh_{col_annee_n}'), row.get(f'prod_reelle_gwh_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Moy Irrad Réelle'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'moy_irrad_reelle_{col_annee_n}'), row.get(f'moy_irrad_reelle_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Dispo Contrat'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'dispo_contrat_{col_annee_n}'), row.get(f'dispo_contrat_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Dispo Brut'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'dispo_brut_{col_annee_n}'), row.get(f'dispo_brut_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Dév Prod (%)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_prod_pct_{col_annee_n}'), row.get(f'dev_prod_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Dév Irrad (%)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_irrad_pct_{col_annee_n}'), row.get(f'dev_irrad_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['PR Budget'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'pr_budget_{col_annee_n}'), row.get(f'pr_budget_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['PR Réel'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'pr_reel_{col_annee_n}'), row.get(f'pr_reel_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Dév PR (%)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_pr_pct_{col_annee_n}'), row.get(f'dev_pr_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Performance Spécifique (kWh/kWc)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'perf_specifique_kwhkwc_{col_annee_n}'), row.get(f'perf_specifique_kwhkwc_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display['Taux d\'Atteinte Objectif (%)'] = df_tableau.apply(
            lambda row: format_combined_cell_html(row.get(f'taux_atteinte_pct_{col_annee_n}'), row.get(f'taux_atteinte_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        
        # Ajouter ligne TOTAL avec format combiné HTML
        total_row = {'Mois': 'TOTAL'}
        # Colonnes de tri pour TOTAL
        total_row['_sort_Nb sites'] = df_tableau[f'nb_sites_{col_annee_n}'].max() if f'nb_sites_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Prod Pvsyst'] = df_tableau[f'prod_pvsyst_gwh_{col_annee_n}'].sum() if f'prod_pvsyst_gwh_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Moy Irrad Pvsyst'] = df_tableau[f'moy_irrad_pvsyst_{col_annee_n}'].mean() if f'moy_irrad_pvsyst_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Prod Réelle'] = df_tableau[f'prod_reelle_gwh_{col_annee_n}'].sum() if f'prod_reelle_gwh_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Moy Irrad Réelle'] = df_tableau[f'moy_irrad_reelle_{col_annee_n}'].mean() if f'moy_irrad_reelle_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Dispo Contrat'] = df_tableau[f'dispo_contrat_{col_annee_n}'].mean() if f'dispo_contrat_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Dispo Brut'] = df_tableau[f'dispo_brut_{col_annee_n}'].mean() if f'dispo_brut_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Dév Prod'] = df_tableau[f'dev_prod_pct_{col_annee_n}'].mean() if f'dev_prod_pct_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Dév Irrad'] = df_tableau[f'dev_irrad_pct_{col_annee_n}'].mean() if f'dev_irrad_pct_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_PR Budget'] = df_tableau[f'pr_budget_{col_annee_n}'].mean() if f'pr_budget_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_PR Réel'] = df_tableau[f'pr_reel_{col_annee_n}'].mean() if f'pr_reel_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Dév PR'] = df_tableau[f'dev_pr_pct_{col_annee_n}'].mean() if f'dev_pr_pct_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Performance Spécifique'] = df_tableau[f'perf_specifique_kwhkwc_{col_annee_n}'].mean() if f'perf_specifique_kwhkwc_{col_annee_n}' in df_tableau.columns else None
        total_row['_sort_Taux d\'Atteinte'] = df_tableau[f'taux_atteinte_pct_{col_annee_n}'].mean() if f'taux_atteinte_pct_{col_annee_n}' in df_tableau.columns else None
        
        # Colonnes d'affichage combinées HTML pour TOTAL
        total_nb_sites_annee_n = df_tableau[f'nb_sites_{col_annee_n}'].max() if f'nb_sites_{col_annee_n}' in df_tableau.columns else None
        total_nb_sites_annee_n1 = df_tableau[f'nb_sites_{col_annee_n1}'].max() if f'nb_sites_{col_annee_n1}' in df_tableau.columns else None
        total_row['Nb sites'] = format_combined_cell_html(total_nb_sites_annee_n, total_nb_sites_annee_n1, 'int', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_prod_pvsyst_annee_n = df_tableau[f'prod_pvsyst_gwh_{col_annee_n}'].sum() if f'prod_pvsyst_gwh_{col_annee_n}' in df_tableau.columns else None
        total_prod_pvsyst_annee_n1 = df_tableau[f'prod_pvsyst_gwh_{col_annee_n1}'].sum() if f'prod_pvsyst_gwh_{col_annee_n1}' in df_tableau.columns else None
        total_row['Prod Pvsyst (GWh)'] = format_combined_cell_html(total_prod_pvsyst_annee_n, total_prod_pvsyst_annee_n1, 'float', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_moy_irrad_pvsyst_annee_n = df_tableau[f'moy_irrad_pvsyst_{col_annee_n}'].mean() if f'moy_irrad_pvsyst_{col_annee_n}' in df_tableau.columns else None
        total_moy_irrad_pvsyst_annee_n1 = df_tableau[f'moy_irrad_pvsyst_{col_annee_n1}'].mean() if f'moy_irrad_pvsyst_{col_annee_n1}' in df_tableau.columns else None
        total_row['Moy Irrad Pvsyst'] = format_combined_cell_html(total_moy_irrad_pvsyst_annee_n, total_moy_irrad_pvsyst_annee_n1, 'float', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_prod_reelle_annee_n = df_tableau[f'prod_reelle_gwh_{col_annee_n}'].sum() if f'prod_reelle_gwh_{col_annee_n}' in df_tableau.columns else None
        total_prod_reelle_annee_n1 = df_tableau[f'prod_reelle_gwh_{col_annee_n1}'].sum() if f'prod_reelle_gwh_{col_annee_n1}' in df_tableau.columns else None
        total_row['Prod Réelle (GWh)'] = format_combined_cell_html(total_prod_reelle_annee_n, total_prod_reelle_annee_n1, 'float', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_moy_irrad_reelle_annee_n = df_tableau[f'moy_irrad_reelle_{col_annee_n}'].mean() if f'moy_irrad_reelle_{col_annee_n}' in df_tableau.columns else None
        total_moy_irrad_reelle_annee_n1 = df_tableau[f'moy_irrad_reelle_{col_annee_n1}'].mean() if f'moy_irrad_reelle_{col_annee_n1}' in df_tableau.columns else None
        total_row['Moy Irrad Réelle'] = format_combined_cell_html(total_moy_irrad_reelle_annee_n, total_moy_irrad_reelle_annee_n1, 'float', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_dispo_contrat_annee_n = df_tableau[f'dispo_contrat_{col_annee_n}'].mean() if f'dispo_contrat_{col_annee_n}' in df_tableau.columns else None
        total_dispo_contrat_annee_n1 = df_tableau[f'dispo_contrat_{col_annee_n1}'].mean() if f'dispo_contrat_{col_annee_n1}' in df_tableau.columns else None
        total_row['Dispo Contrat'] = format_combined_cell_html(total_dispo_contrat_annee_n, total_dispo_contrat_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_dispo_brut_annee_n = df_tableau[f'dispo_brut_{col_annee_n}'].mean() if f'dispo_brut_{col_annee_n}' in df_tableau.columns else None
        total_dispo_brut_annee_n1 = df_tableau[f'dispo_brut_{col_annee_n1}'].mean() if f'dispo_brut_{col_annee_n1}' in df_tableau.columns else None
        total_row['Dispo Brut'] = format_combined_cell_html(total_dispo_brut_annee_n, total_dispo_brut_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_dev_prod_annee_n = df_tableau[f'dev_prod_pct_{col_annee_n}'].mean() if f'dev_prod_pct_{col_annee_n}' in df_tableau.columns else None
        total_dev_prod_annee_n1 = df_tableau[f'dev_prod_pct_{col_annee_n1}'].mean() if f'dev_prod_pct_{col_annee_n1}' in df_tableau.columns else None
        total_row['Dév Prod (%)'] = format_combined_cell_html(total_dev_prod_annee_n, total_dev_prod_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_dev_irrad_annee_n = df_tableau[f'dev_irrad_pct_{col_annee_n}'].mean() if f'dev_irrad_pct_{col_annee_n}' in df_tableau.columns else None
        total_dev_irrad_annee_n1 = df_tableau[f'dev_irrad_pct_{col_annee_n1}'].mean() if f'dev_irrad_pct_{col_annee_n1}' in df_tableau.columns else None
        total_row['Dév Irrad (%)'] = format_combined_cell_html(total_dev_irrad_annee_n, total_dev_irrad_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_pr_budget_annee_n = df_tableau[f'pr_budget_{col_annee_n}'].mean() if f'pr_budget_{col_annee_n}' in df_tableau.columns else None
        total_pr_budget_annee_n1 = df_tableau[f'pr_budget_{col_annee_n1}'].mean() if f'pr_budget_{col_annee_n1}' in df_tableau.columns else None
        total_row['PR Budget'] = format_combined_cell_html(total_pr_budget_annee_n, total_pr_budget_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_pr_reel_annee_n = df_tableau[f'pr_reel_{col_annee_n}'].mean() if f'pr_reel_{col_annee_n}' in df_tableau.columns else None
        total_pr_reel_annee_n1 = df_tableau[f'pr_reel_{col_annee_n1}'].mean() if f'pr_reel_{col_annee_n1}' in df_tableau.columns else None
        total_row['PR Réel'] = format_combined_cell_html(total_pr_reel_annee_n, total_pr_reel_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_dev_pr_annee_n = df_tableau[f'dev_pr_pct_{col_annee_n}'].mean() if f'dev_pr_pct_{col_annee_n}' in df_tableau.columns else None
        total_dev_pr_annee_n1 = df_tableau[f'dev_pr_pct_{col_annee_n1}'].mean() if f'dev_pr_pct_{col_annee_n1}' in df_tableau.columns else None
        total_row['Dév PR (%)'] = format_combined_cell_html(total_dev_pr_annee_n, total_dev_pr_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_perf_spec_annee_n = df_tableau[f'perf_specifique_kwhkwc_{col_annee_n}'].mean() if f'perf_specifique_kwhkwc_{col_annee_n}' in df_tableau.columns else None
        total_perf_spec_annee_n1 = df_tableau[f'perf_specifique_kwhkwc_{col_annee_n1}'].mean() if f'perf_specifique_kwhkwc_{col_annee_n1}' in df_tableau.columns else None
        total_row['Performance Spécifique (kWh/kWc)'] = format_combined_cell_html(total_perf_spec_annee_n, total_perf_spec_annee_n1, 'float', annee_n=annee_principale, annee_n1=annee_n1)
        
        total_taux_atteinte_annee_n = df_tableau[f'taux_atteinte_pct_{col_annee_n}'].mean() if f'taux_atteinte_pct_{col_annee_n}' in df_tableau.columns else None
        total_taux_atteinte_annee_n1 = df_tableau[f'taux_atteinte_pct_{col_annee_n1}'].mean() if f'taux_atteinte_pct_{col_annee_n1}' in df_tableau.columns else None
        total_row['Taux d\'Atteinte Objectif (%)'] = format_combined_cell_html(total_taux_atteinte_annee_n, total_taux_atteinte_annee_n1, 'percent', annee_n=annee_principale, annee_n1=annee_n1)
        
        # Ajouter la ligne TOTAL au DataFrame
        df_display = pd.concat([df_display, pd.DataFrame([total_row])], ignore_index=True)
        
        # Créer un tableau HTML avec DataTables.js pour le tri et filtrage
        html_table = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
            <script type="text/javascript" src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
            <style>
            body {
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }
            #tableau-mensuel-indicateurs_wrapper .dataTables_filter input {
                margin-left: 10px;
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            #tableau-mensuel-indicateurs_wrapper .dataTables_length select {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 0 5px;
            }
            #tableau-mensuel-indicateurs thead th {
                cursor: pointer;
                user-select: none;
            }
            #tableau-mensuel-indicateurs thead th:hover {
                background: rgba(156, 163, 175, 0.6) !important;
            }
            .btn-reset-sort {
                background: rgba(10, 132, 255, 0.15) !important;
                color: #0A84FF !important;
                font-weight: 600 !important;
                font-size: 0.85rem !important;
                border: 1.5px solid rgba(10, 132, 255, 0.4) !important;
                border-radius: 12px !important;
                padding: 8px 16px !important;
                backdrop-filter: blur(10px) saturate(160%) !important;
                -webkit-backdrop-filter: blur(10px) saturate(160%) !important;
                box-shadow: 0 4px 12px rgba(10, 132, 255, 0.15) !important;
                transition: all 0.2s ease !important;
                cursor: pointer;
                margin-bottom: 10px;
            }
            .btn-reset-sort:hover {
                background: rgba(10, 132, 255, 0.25) !important;
                border-color: rgba(10, 132, 255, 0.6) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 16px rgba(10, 132, 255, 0.25) !important;
            }
            .btn-reset-sort:active {
                transform: translateY(0px) !important;
                box-shadow: 0 2px 8px rgba(10, 132, 255, 0.2) !important;
            }
            </style>
        </head>
        <body>
        <button id="btn-reset-sort-mensuel" class="btn-reset-sort">🔄 Réinitialiser tri</button>
        <div style="overflow-x: auto; margin: 20px 0;">
            <table id="tableau-mensuel-indicateurs" style="width: 100%; border-collapse: collapse; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr style="background: rgba(156, 163, 175, 0.4); backdrop-filter: blur(10px); color: #1f2937;">
                        <th style="padding: 12px 8px; text-align: left; font-weight: 600; border: none; position: sticky; left: 0; background: rgba(156, 163, 175, 0.4); backdrop-filter: blur(10px); z-index: 10; color: #1f2937;">Mois</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Nb sites</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Prod Pvsyst<br/>(GWh)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Moy Irrad<br/>Pvsyst</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Prod Réelle<br/>(GWh)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Moy Irrad<br/>Réelle</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dispo<br/>Contrat</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dispo<br/>Brut</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév Prod<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév Irrad<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">PR<br/>Budget</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">PR<br/>Réel</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév PR<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Performance<br/>Spécifique<br/>(kWh/kWc)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Taux d'Atteinte<br/>Objectif<br/>(%)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # S'assurer que df_display est trié par ordre chronologique avant génération HTML
        # Utiliser la colonne numérique _Mois_num pour le tri
        df_display = df_display.sort_values('_Mois_num').reset_index(drop=True)
        df_display = df_display.drop(columns=['_Mois_num'])
        
        # Remplir les lignes du tableau
        for idx, row in df_display.iterrows():
            mois = row['Mois']
            mois_escaped = str(mois).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Récupérer les cellules HTML formatées
            nb_sites_html = row.get('Nb sites', '')
            prod_pvsyst_html = row.get('Prod Pvsyst (GWh)', '')
            moy_irrad_pvsyst_html = row.get('Moy Irrad Pvsyst', '')
            prod_reelle_html = row.get('Prod Réelle (GWh)', '')
            moy_irrad_reelle_html = row.get('Moy Irrad Réelle', '')
            dispo_contrat_html = row.get('Dispo Contrat', '')
            dispo_brut_html = row.get('Dispo Brut', '')
            dev_prod_html = row.get('Dév Prod (%)', '')
            dev_irrad_html = row.get('Dév Irrad (%)', '')
            pr_budget_html = row.get('PR Budget', '')
            pr_reel_html = row.get('PR Réel', '')
            dev_pr_html = row.get('Dév PR (%)', '')
            perf_spec_html = row.get('Performance Spécifique (kWh/kWc)', '')
            taux_atteinte_html = row.get('Taux d\'Atteinte Objectif (%)', '')
            
            # Style de ligne spécial pour TOTAL
            row_style = "border-top: 2px solid rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.05); background: rgba(243, 244, 246, 0.5);" if mois == 'TOTAL' else "border-bottom: 1px solid rgba(0, 0, 0, 0.05);"
            td_style = "padding: 10px 8px; font-weight: 700; position: sticky; left: 0; background: rgba(243, 244, 246, 0.5); z-index: 5;" if mois == 'TOTAL' else "padding: 10px 8px; font-weight: 600; position: sticky; left: 0; background: rgba(255, 255, 255, 0.95); z-index: 5;"
            
            # Ajouter les attributs data-sort pour le tri avec DataTables
            sort_attrs = f'data-sort-nb-sites="{row.get("_sort_Nb sites", "") or 0}" data-sort-prod-pvsyst="{row.get("_sort_Prod Pvsyst", "") or 0}" data-sort-moy-irrad-pvsyst="{row.get("_sort_Moy Irrad Pvsyst", "") or 0}" data-sort-prod-reelle="{row.get("_sort_Prod Réelle", "") or 0}" data-sort-moy-irrad-reelle="{row.get("_sort_Moy Irrad Réelle", "") or 0}" data-sort-dispo-contrat="{row.get("_sort_Dispo Contrat", "") or 0}" data-sort-dispo-brut="{row.get("_sort_Dispo Brut", "") or 0}" data-sort-dev-prod="{row.get("_sort_Dév Prod", "") or 0}" data-sort-dev-irrad="{row.get("_sort_Dév Irrad", "") or 0}" data-sort-pr-budget="{row.get("_sort_PR Budget", "") or 0}" data-sort-pr-reel="{row.get("_sort_PR Réel", "") or 0}" data-sort-dev-pr="{row.get("_sort_Dév PR", "") or 0}" data-sort-perf-spec="{row.get("_sort_Performance Spécifique", "") or 0}" data-sort-taux="{row.get("_sort_Taux d\'Atteinte", "") or 0}"'
            html_table += f'<tr style="{row_style}" {sort_attrs}>'
            html_table += f'<td style="{td_style}">{mois_escaped}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{nb_sites_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{prod_pvsyst_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{moy_irrad_pvsyst_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{prod_reelle_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{moy_irrad_reelle_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{dispo_contrat_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{dispo_brut_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{dev_prod_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{dev_irrad_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{pr_budget_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{pr_reel_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{dev_pr_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{perf_spec_html}</td>'
            html_table += f'<td style="padding: 4px 8px; text-align: center;">{taux_atteinte_html}</td>'
            html_table += '</tr>'
        
        html_table += """
                </tbody>
            </table>
        </div>
        
        <script>
        (function() {
            function initDataTable() {
                if (typeof jQuery === 'undefined' || typeof jQuery.fn.dataTable === 'undefined') {
                    setTimeout(initDataTable, 100);
                    return;
                }
                
                if (jQuery('#tableau-mensuel-indicateurs').length === 0) {
                    setTimeout(initDataTable, 100);
                    return;
                }
                
                if (jQuery('#tableau-mensuel-indicateurs').hasClass('dataTable')) {
                    return; // Déjà initialisé
                }
                
                // Fonction de tri personnalisée pour les mois (maintenant numérotés 1-12)
                jQuery.fn.dataTable.ext.type.order['mois-ordre'] = function(data) {
                    const dataStr = String(data).trim().toLowerCase();
                    if (dataStr === 'total') {
                        return 99;  // TOTAL toujours en dernier
                    }
                    // Parser le numéro (1-12)
                    const num = parseInt(dataStr, 10);
                    return isNaN(num) ? 0 : num;
                };
                
                // Fonction de tri personnalisée pour les colonnes numériques avec attributs data-sort
                jQuery.fn.dataTable.ext.order['data-sort-num'] = function(settings, col) {
                    const sortAttrsMap = {
                        0: null,
                        1: 'data-sort-nb-sites',
                        2: 'data-sort-prod-pvsyst',
                        3: 'data-sort-moy-irrad-pvsyst',
                        4: 'data-sort-prod-reelle',
                        5: 'data-sort-moy-irrad-reelle',
                        6: 'data-sort-dispo-contrat',
                        7: 'data-sort-dispo-brut',
                        8: 'data-sort-dev-prod',
                        9: 'data-sort-dev-irrad',
                        10: 'data-sort-pr-budget',
                        11: 'data-sort-pr-reel',
                        12: 'data-sort-dev-pr',
                        13: 'data-sort-perf-spec',
                        14: 'data-sort-taux'
                    };
                    
                    return this.api().column(col, {order: 'index'}).nodes().map(function(td, index) {
                        const attr = sortAttrsMap[col];
                        const tr = jQuery(td).closest('tr');
                      if (col === 0) {
                          // Tri par numéro de mois (1-12) ou TOTAL (99)
                          const moisText = jQuery(td).text().trim().toLowerCase();
                          if (moisText === 'total') {
                              return 99;
                          }
                          const num = parseInt(moisText, 10);
                          return isNaN(num) ? 0 : num;
                        } else if (attr) {
                            // Tri par attribut data-sort pour colonnes numériques
                            const val = parseFloat(tr.attr(attr));
                            return isNaN(val) ? 0 : val;
                        }
                        return 0;
                    });
                };
                
                // Initialiser DataTable et stocker la référence
                const tableMensuel = jQuery('#tableau-mensuel-indicateurs').DataTable({
                    order: [[0, 'asc']],  // Tri par défaut : colonne 0 (Mois) en ordre croissant numérique (1-12)
                    ordering: true,  // Activer le tri
                    pageLength: -1,  // Afficher toutes les lignes par défaut (12 mois + TOTAL = 13 lignes)
                    lengthMenu: [[12, 15, 25, 50, -1], [12, 15, 25, 50, "Tous"]],
                    paging: false,  // Désactiver la pagination pour afficher tout le contenu
                    orderFixed: [[0, 'asc']],  // Fixer l'ordre par défaut sur la colonne Mois
                    columnDefs: [
                        {
                            targets: 0,
                            type: 'num',  // Utiliser le type numérique pour trier 1-12 correctement
                            orderDataType: 'mois-ordre'  // Utiliser la fonction personnalisée pour gérer TOTAL (99)
                        },
                        {
                            targets: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                            orderDataType: 'data-sort-num'
                        }
                    ],
                    language: {
                        search: "Rechercher:",
                        lengthMenu: "Afficher _MENU_ lignes",
                        info: "Affichage de _START_ à _END_ sur _TOTAL_ lignes",
                        infoEmpty: "Affichage de 0 à 0 sur 0 lignes",
                        infoFiltered: "(filtré sur _MAX_ lignes au total)",
                        paginate: {
                            first: "Premier",
                            last: "Dernier",
                            next: "Suivant",
                            previous: "Précédent"
                        }
                    },
                    drawCallback: function(settings) {
                        // Garder la ligne TOTAL en bas après tri ou initialisation
                        setTimeout(function() {
                            const totalRow = jQuery('#tableau-mensuel-indicateurs tbody tr').filter(function() {
                                return jQuery(this).find('td:first-child').text().trim() === 'TOTAL';
                            });
                            if (totalRow.length) {
                                totalRow.detach();
                                jQuery('#tableau-mensuel-indicateurs tbody').append(totalRow);
                            }
                        }, 50);
                    }
                });
                
                // Stocker la référence dans l'élément pour y accéder plus tard
                jQuery('#tableau-mensuel-indicateurs').data('dataTable', tableMensuel);
                
                // Forcer l'ordre chronologique initial immédiatement et mettre TOTAL en bas
                // Utiliser drawCallback pour s'assurer que le tri est appliqué dès le premier rendu
                // Gérer la position de TOTAL après chaque tri
                tableMensuel.on('draw', function() {
                    const totalRow = jQuery('#tableau-mensuel-indicateurs tbody tr').filter(function() {
                        return jQuery(this).find('td:first-child').text().trim() === 'TOTAL';
                    });
                    if (totalRow.length) {
                        totalRow.detach();
                        jQuery('#tableau-mensuel-indicateurs tbody').append(totalRow);
                    }
                });
                
                // Forcer le tri initial immédiatement après initialisation (1-12, puis TOTAL)
                tableMensuel.order([0, 'asc']).draw();
                
                // Attacher l'événement au bouton (utiliser off() pour éviter les doublons)
                jQuery('#btn-reset-sort-mensuel').off('click').on('click', function() {
                    const table = jQuery('#tableau-mensuel-indicateurs').data('dataTable') || 
                                  jQuery('#tableau-mensuel-indicateurs').DataTable();
                    
                    // Réinitialiser au tri chronologique (Janvier à Décembre)
                    // Trier par la colonne 0 (Mois) en ordre croissant
                    table.order([0, 'asc']).draw();
                    
                    // Réorganiser pour mettre TOTAL en bas après le tri
                    setTimeout(function() {
                        const totalRow = jQuery('#tableau-mensuel-indicateurs tbody tr').filter(function() {
                            return jQuery(this).find('td:first-child').text().trim() === 'TOTAL';
                        });
                        if (totalRow.length) {
                            totalRow.detach();
                            jQuery('#tableau-mensuel-indicateurs tbody').append(totalRow);
                        }
                    }, 150);
                });
            }
            
            // Initialiser quand le DOM est prêt
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initDataTable);
            } else {
                initDataTable();
            }
            
            // Retry avec délais pour s'assurer que jQuery est chargé
            setTimeout(initDataTable, 500);
            setTimeout(initDataTable, 1000);
        })();
        </script>
        </body>
        </html>
        """
        
        # Utiliser st.components.v1.html pour permettre l'exécution de JavaScript
        # Hauteur ajustée pour afficher tous les mois (12 mois + TOTAL = 13 lignes) sans scroll
        components.html(html_table, height=1000, scrolling=False)
    else:
        st.info("Aucune donnée disponible pour le tableau mensuel des indicateurs.")
    
    # Tableau par SPV
    st.markdown("""
    <div style="
        padding: 16px 24px;
        margin: 2rem 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
    ">📊 Tableau des indicateurs par SPV ({annee_principale} / {annee_n1})</div>
    """, unsafe_allow_html=True)
    
    df_tableau_spv = get_tableau_indicateurs_par_spv(annee_principale)
    
    if not df_tableau_spv.empty:
        # Noms de colonnes dynamiques selon l'année (même logique que tableau mensuel)
        col_annee_n = f'{annee_principale}'
        col_annee_n1 = f'{annee_n1}'
        
        # Créer un DataFrame avec colonnes combinées pour l'affichage (même logique que tableau mensuel)
        df_display_spv = pd.DataFrame()
        df_display_spv['SPV'] = df_tableau_spv['spv']
        
        # Colonnes pour le tri (cachées) - garder les valeurs numériques de l'année N
        df_display_spv['_sort_Nb sites'] = df_tableau_spv.get(f'nb_sites_{col_annee_n}', None)
        df_display_spv['_sort_Prod Pvsyst'] = df_tableau_spv.get(f'prod_pvsyst_gwh_{col_annee_n}', None)
        df_display_spv['_sort_Moy Irrad Pvsyst'] = df_tableau_spv.get(f'moy_irrad_pvsyst_{col_annee_n}', None)
        df_display_spv['_sort_Prod Réelle'] = df_tableau_spv.get(f'prod_reelle_gwh_{col_annee_n}', None)
        df_display_spv['_sort_Moy Irrad Réelle'] = df_tableau_spv.get(f'moy_irrad_reelle_{col_annee_n}', None)
        df_display_spv['_sort_Dispo Contrat'] = df_tableau_spv.get(f'dispo_contrat_{col_annee_n}', None)
        df_display_spv['_sort_Dispo Brut'] = df_tableau_spv.get(f'dispo_brut_{col_annee_n}', None)
        df_display_spv['_sort_Dév Prod'] = df_tableau_spv.get(f'dev_prod_pct_{col_annee_n}', None)
        df_display_spv['_sort_Dév Irrad'] = df_tableau_spv.get(f'dev_irrad_pct_{col_annee_n}', None)
        df_display_spv['_sort_PR Budget'] = df_tableau_spv.get(f'pr_budget_{col_annee_n}', None)
        df_display_spv['_sort_PR Réel'] = df_tableau_spv.get(f'pr_reel_{col_annee_n}', None)
        df_display_spv['_sort_Dév PR'] = df_tableau_spv.get(f'dev_pr_pct_{col_annee_n}', None)
        df_display_spv['_sort_Performance Spécifique'] = df_tableau_spv.get(f'perf_specifique_kwhkwc_{col_annee_n}', None)
        df_display_spv['_sort_Taux d\'Atteinte'] = df_tableau_spv.get(f'taux_atteinte_pct_{col_annee_n}', None)
        
        # Colonnes d'affichage combinées en HTML
        df_display_spv['Nb sites'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'nb_sites_{col_annee_n}'), row.get(f'nb_sites_{col_annee_n1}'), 'int', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Prod Pvsyst (GWh)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'prod_pvsyst_gwh_{col_annee_n}'), row.get(f'prod_pvsyst_gwh_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Moy Irrad Pvsyst'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'moy_irrad_pvsyst_{col_annee_n}'), row.get(f'moy_irrad_pvsyst_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Prod Réelle (GWh)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'prod_reelle_gwh_{col_annee_n}'), row.get(f'prod_reelle_gwh_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Moy Irrad Réelle'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'moy_irrad_reelle_{col_annee_n}'), row.get(f'moy_irrad_reelle_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Dispo Contrat'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'dispo_contrat_{col_annee_n}'), row.get(f'dispo_contrat_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Dispo Brut'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'dispo_brut_{col_annee_n}'), row.get(f'dispo_brut_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Dév Prod (%)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_prod_pct_{col_annee_n}'), row.get(f'dev_prod_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Dév Irrad (%)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_irrad_pct_{col_annee_n}'), row.get(f'dev_irrad_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['PR Budget'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'pr_budget_{col_annee_n}'), row.get(f'pr_budget_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['PR Réel'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'pr_reel_{col_annee_n}'), row.get(f'pr_reel_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Dév PR (%)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'dev_pr_pct_{col_annee_n}'), row.get(f'dev_pr_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Performance Spécifique (kWh/kWc)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'perf_specifique_kwhkwc_{col_annee_n}'), row.get(f'perf_specifique_kwhkwc_{col_annee_n1}'), 'float', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        df_display_spv['Taux d\'Atteinte Objectif (%)'] = df_tableau_spv.apply(
            lambda row: format_combined_cell_html(row.get(f'taux_atteinte_pct_{col_annee_n}'), row.get(f'taux_atteinte_pct_{col_annee_n1}'), 'percent', annee_n=annee_principale, annee_n1=annee_n1), axis=1
        )
        
        # Créer un tableau HTML avec DataTables.js pour le tri et filtrage
        html_table_spv = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
            <script type="text/javascript" src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
            <style>
            body {
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }
            #tableau-spv-indicateurs_wrapper .dataTables_filter input {
                margin-left: 10px;
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            #tableau-spv-indicateurs_wrapper .dataTables_length select {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 0 5px;
            }
            #tableau-spv-indicateurs thead th {
                cursor: pointer;
                user-select: none;
            }
            #tableau-spv-indicateurs thead th:hover {
                background: rgba(156, 163, 175, 0.6) !important;
            }
            .btn-reset-sort {
                background: rgba(10, 132, 255, 0.15) !important;
                color: #0A84FF !important;
                font-weight: 600 !important;
                font-size: 0.85rem !important;
                border: 1.5px solid rgba(10, 132, 255, 0.4) !important;
                border-radius: 12px !important;
                padding: 8px 16px !important;
                backdrop-filter: blur(10px) saturate(160%) !important;
                -webkit-backdrop-filter: blur(10px) saturate(160%) !important;
                box-shadow: 0 4px 12px rgba(10, 132, 255, 0.15) !important;
                transition: all 0.2s ease !important;
                cursor: pointer;
                margin-bottom: 10px;
            }
            .btn-reset-sort:hover {
                background: rgba(10, 132, 255, 0.25) !important;
                border-color: rgba(10, 132, 255, 0.6) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 16px rgba(10, 132, 255, 0.25) !important;
            }
            .btn-reset-sort:active {
                transform: translateY(0px) !important;
                box-shadow: 0 2px 8px rgba(10, 132, 255, 0.2) !important;
            }
            </style>
        </head>
        <body>
        <button id="btn-reset-sort-spv" class="btn-reset-sort">🔄 Réinitialiser tri</button>
        <div style="overflow-x: auto; margin: 20px 0;">
            <table id="tableau-spv-indicateurs" style="width: 100%; border-collapse: collapse; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <thead>
                    <tr style="background: rgba(156, 163, 175, 0.4); backdrop-filter: blur(10px); color: #1f2937;">
                        <th style="padding: 12px 8px; text-align: left; font-weight: 600; border: none; position: sticky; left: 0; background: rgba(156, 163, 175, 0.4); backdrop-filter: blur(10px); z-index: 10; color: #1f2937;">SPV</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Nb sites</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Prod Pvsyst<br/>(GWh)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Moy Irrad<br/>Pvsyst</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Prod Réelle<br/>(GWh)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Moy Irrad<br/>Réelle</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dispo<br/>Contrat</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dispo<br/>Brut</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév Prod<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév Irrad<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">PR<br/>Budget</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">PR<br/>Réel</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Dév PR<br/>(%)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Performance<br/>Spécifique<br/>(kWh/kWc)</th>
                        <th style="padding: 12px 8px; text-align: center; font-weight: 600; border: none; color: #1f2937;">Taux d'Atteinte<br/>Objectif<br/>(%)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Remplir les lignes du tableau par SPV
        for idx, row in df_display_spv.iterrows():
            spv = row['SPV']
            spv_escaped = str(spv).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Récupérer les cellules HTML formatées
            nb_sites_html = row.get('Nb sites', '')
            prod_pvsyst_html = row.get('Prod Pvsyst (GWh)', '')
            moy_irrad_pvsyst_html = row.get('Moy Irrad Pvsyst', '')
            prod_reelle_html = row.get('Prod Réelle (GWh)', '')
            moy_irrad_reelle_html = row.get('Moy Irrad Réelle', '')
            dispo_contrat_html = row.get('Dispo Contrat', '')
            dispo_brut_html = row.get('Dispo Brut', '')
            dev_prod_html = row.get('Dév Prod (%)', '')
            dev_irrad_html = row.get('Dév Irrad (%)', '')
            pr_budget_html = row.get('PR Budget', '')
            pr_reel_html = row.get('PR Réel', '')
            dev_pr_html = row.get('Dév PR (%)', '')
            perf_spec_html = row.get('Performance Spécifique (kWh/kWc)', '')
            taux_atteinte_html = row.get('Taux d\'Atteinte Objectif (%)', '')
            
            # Ajouter les attributs data-sort pour le tri avec DataTables
            sort_attrs_spv = f'data-sort-nb-sites="{row.get("_sort_Nb sites", "") or 0}" data-sort-prod-pvsyst="{row.get("_sort_Prod Pvsyst", "") or 0}" data-sort-moy-irrad-pvsyst="{row.get("_sort_Moy Irrad Pvsyst", "") or 0}" data-sort-prod-reelle="{row.get("_sort_Prod Réelle", "") or 0}" data-sort-moy-irrad-reelle="{row.get("_sort_Moy Irrad Réelle", "") or 0}" data-sort-dispo-contrat="{row.get("_sort_Dispo Contrat", "") or 0}" data-sort-dispo-brut="{row.get("_sort_Dispo Brut", "") or 0}" data-sort-dev-prod="{row.get("_sort_Dév Prod", "") or 0}" data-sort-dev-irrad="{row.get("_sort_Dév Irrad", "") or 0}" data-sort-pr-budget="{row.get("_sort_PR Budget", "") or 0}" data-sort-pr-reel="{row.get("_sort_PR Réel", "") or 0}" data-sort-dev-pr="{row.get("_sort_Dév PR", "") or 0}" data-sort-perf-spec="{row.get("_sort_Performance Spécifique", "") or 0}" data-sort-taux="{row.get("_sort_Taux d\'Atteinte", "") or 0}"'
            html_table_spv += f'<tr style="border-bottom: 1px solid rgba(0, 0, 0, 0.05);" {sort_attrs_spv}>'
            html_table_spv += f'<td style="padding: 10px 8px; font-weight: 600; position: sticky; left: 0; background: rgba(255, 255, 255, 0.95); z-index: 5;">{spv_escaped}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{nb_sites_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{prod_pvsyst_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{moy_irrad_pvsyst_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{prod_reelle_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{moy_irrad_reelle_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{dispo_contrat_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{dispo_brut_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{dev_prod_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{dev_irrad_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{pr_budget_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{pr_reel_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{dev_pr_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{perf_spec_html}</td>'
            html_table_spv += f'<td style="padding: 4px 8px; text-align: center;">{taux_atteinte_html}</td>'
            html_table_spv += '</tr>'
        
        html_table_spv += """
                </tbody>
            </table>
        </div>
        
        <script>
        (function() {
            function initDataTableSPV() {
                if (typeof jQuery === 'undefined' || typeof jQuery.fn.dataTable === 'undefined') {
                    setTimeout(initDataTableSPV, 100);
                    return;
                }
                
                if (jQuery('#tableau-spv-indicateurs').length === 0) {
                    setTimeout(initDataTableSPV, 100);
                    return;
                }
                
                if (jQuery('#tableau-spv-indicateurs').hasClass('dataTable')) {
                    return; // Déjà initialisé
                }
                
                // Fonction de tri personnalisée pour les colonnes numériques avec attributs data-sort (SPV)
                jQuery.fn.dataTable.ext.order['data-sort-num-spv'] = function(settings, col) {
                    const sortAttrsMapSPV = {
                        0: null,
                        1: 'data-sort-nb-sites',
                        2: 'data-sort-prod-pvsyst',
                        3: 'data-sort-moy-irrad-pvsyst',
                        4: 'data-sort-prod-reelle',
                        5: 'data-sort-moy-irrad-reelle',
                        6: 'data-sort-dispo-contrat',
                        7: 'data-sort-dispo-brut',
                        8: 'data-sort-dev-prod',
                        9: 'data-sort-dev-irrad',
                        10: 'data-sort-pr-budget',
                        11: 'data-sort-pr-reel',
                        12: 'data-sort-dev-pr',
                        13: 'data-sort-perf-spec',
                        14: 'data-sort-taux'
                    };
                    
                    return this.api().column(col, {order: 'index'}).nodes().map(function(td, index) {
                        const attr = sortAttrsMapSPV[col];
                        const tr = jQuery(td).closest('tr');
                        if (col === 0) {
                            // Tri alphabétique pour SPV
                            return jQuery(td).text().toLowerCase();
                        } else if (attr) {
                            // Tri par attribut data-sort pour colonnes numériques
                            const val = parseFloat(tr.attr(attr));
                            return isNaN(val) ? 0 : val;
                        }
                        return 0;
                    });
                };
                
                // Initialiser DataTable et stocker la référence
                const tableSPV = jQuery('#tableau-spv-indicateurs').DataTable({
                    order: [[0, 'asc']],  // Tri par défaut : colonne 0 (SPV) en ordre alphabétique croissant
                    pageLength: -1,  // Afficher toutes les lignes par défaut (toutes les SPV)
                    lengthMenu: [[10, 15, 25, 50, -1], [10, 15, 25, 50, "Tous"]],
                    paging: false,  // Désactiver la pagination pour afficher tout le contenu
                    language: {
                        search: "Rechercher:",
                        lengthMenu: "Afficher _MENU_ lignes",
                        info: "Affichage de _START_ à _END_ sur _TOTAL_ lignes",
                        infoEmpty: "Affichage de 0 à 0 sur 0 lignes",
                        infoFiltered: "(filtré sur _MAX_ lignes au total)",
                        paginate: {
                            first: "Premier",
                            last: "Dernier",
                            next: "Suivant",
                            previous: "Précédent"
                        }
                    },
                    columnDefs: [
                        {
                            targets: 0,
                            type: 'string'
                        },
                        {
                            targets: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                            orderDataType: 'data-sort-num-spv'
                        }
                    ]
                });
                
                // Stocker la référence dans l'élément pour y accéder plus tard
                jQuery('#tableau-spv-indicateurs').data('dataTable', tableSPV);
                
                // Attacher l'événement au bouton (utiliser off() pour éviter les doublons)
                jQuery('#btn-reset-sort-spv').off('click').on('click', function() {
                    const table = jQuery('#tableau-spv-indicateurs').data('dataTable') || 
                                  jQuery('#tableau-spv-indicateurs').DataTable();
                    
                    // Réinitialiser au tri alphabétique croissant (colonne SPV)
                    // Trier par la colonne 0 (SPV) en ordre croissant
                    table.order([0, 'asc']).draw();
                });
            }
            
            // Initialiser quand le DOM est prêt
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initDataTableSPV);
            } else {
                initDataTableSPV();
            }
            
            // Retry avec délais pour s'assurer que jQuery est chargé
            setTimeout(initDataTableSPV, 500);
            setTimeout(initDataTableSPV, 1000);
        })();
        </script>
        </body>
        </html>
        """
        
        # Calculer la hauteur nécessaire dynamiquement : ~50px par ligne + 200px pour en-tête et padding
        nb_lignes_spv = len(df_display_spv)
        hauteur_tableau_spv = max(3000, (nb_lignes_spv * 50) + 300)  # Minimum 3000px, sinon calcul dynamique
        
        # Utiliser st.components.v1.html pour permettre l'exécution de JavaScript
        # Hauteur ajustée dynamiquement pour afficher toutes les SPV sans scroll
        components.html(html_table_spv, height=int(hauteur_tableau_spv), scrolling=False)
    else:
        st.info("Aucune donnée disponible pour le tableau par SPV.")


# ============================================
# FONCTIONS VUE MAINTENANCE
# ============================================

def get_chronologie_maintenance(annee):
    """Chronologie maintenance par mois et catégorie"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        categorie,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND categorie IS NOT NULL
    GROUP BY mois, categorie
    ORDER BY mois, categorie
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_par_site(annee, limit=20):
    """Interventions par site"""
    query = f"""
    SELECT 
        nom_site,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND nom_site IS NOT NULL
    GROUP BY nom_site
    ORDER BY nb_interventions DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_par_severite(annee):
    """Interventions par sévérité"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        severite_categorie,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND severite_categorie IS NOT NULL
    GROUP BY mois, severite_categorie
    ORDER BY mois, severite_categorie
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_par_spv(annee):
    """Interventions par SPV"""
    query = f"""
    SELECT 
        spv,
        COUNT(*) as nb_interventions,
        SUM(facturation_intervention) / 1000 as cout_total_k,
        AVG(facturation_intervention) as cout_moyen
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND spv IS NOT NULL
    GROUP BY spv
    ORDER BY nb_interventions DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_mttr_par_categorie(annee):
    """Délai moyen de résolution (MTTR) par catégorie avec médiane"""
    # Récupérer les données brutes pour calculer médiane
    query = f"""
    SELECT 
        categorie,
        duree_intervention_sur_site as mttr_heures,
        JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) as mttr_jours
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND categorie IS NOT NULL
    AND date_creation_intervention IS NOT NULL
    AND date_fin_intervention IS NOT NULL
    AND (ticket_resolu = 1 OR status_intervention LIKE '%Résolu%' OR status_intervention LIKE '%Clôturé%')
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Calculer moyenne et médiane par catégorie
    result = df.groupby('categorie').agg({
        'mttr_jours': ['mean', 'median', 'count']
    }).reset_index()
    result.columns = ['categorie', 'mttr_moyen_jours', 'mttr_median_jours', 'nb_interventions']
    
    # Convertir en heures aussi
    result['mttr_moyen_heures'] = result['mttr_moyen_jours'] * 24
    result['mttr_median_heures'] = result['mttr_median_jours'] * 24
    
    return result.sort_values('mttr_moyen_jours', ascending=False)


def get_mttr_global(annee):
    """MTTR global avec moyenne et médiane"""
    query = f"""
    SELECT 
        duree_intervention_sur_site as mttr_heures,
        JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) as mttr_jours
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND date_creation_intervention IS NOT NULL
    AND date_fin_intervention IS NOT NULL
    AND duree_intervention_sur_site IS NOT NULL
    AND (ticket_resolu = 1 OR status_intervention LIKE '%Résolu%' OR status_intervention LIKE '%Clôturé%')
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return None, None, 0
    
    mttr_moyen = df['mttr_heures'].mean() if 'mttr_heures' in df.columns else None
    mttr_median = df['mttr_heures'].median() if 'mttr_heures' in df.columns else None
    nb_interventions = len(df)
    
    return mttr_moyen, mttr_median, nb_interventions


def get_interventions_en_cours(annee):
    """Interventions en cours (non résolues)"""
    query = f"""
    SELECT 
        numero_intervention,
        nom_site,
        categorie,
        titre_intervention,
        date_creation_intervention,
        JULIANDAY('now') - JULIANDAY(date_creation_intervention) as anciennete_jours,
        severite_categorie
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND (ticket_resolu = 0 OR ticket_resolu IS NULL)
    ORDER BY date_creation_intervention DESC
    LIMIT 100
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_temps_reponse_moyen(annee):
    """Temps de réponse moyen par catégorie"""
    query = f"""
    SELECT 
        categorie,
        AVG((JULIANDAY(date_debut_intervention) - JULIANDAY(date_creation_intervention)) * 24) as temps_reponse_heures,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND categorie IS NOT NULL
    AND date_creation_intervention IS NOT NULL
    AND date_debut_intervention IS NOT NULL
    GROUP BY categorie
    ORDER BY temps_reponse_heures DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_maintenance_detail(annee):
    """Détail des coûts de maintenance par mois"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        SUM(facturation_intervention) / 1000 as cout_total_k,
        COUNT(*) as nb_interventions,
        AVG(facturation_intervention) as cout_moyen
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND facturation_intervention IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_par_categorie(annee):
    """Coût par catégorie d'intervention"""
    query = f"""
    SELECT 
        categorie,
        SUM(facturation_intervention) / 1000 as cout_total_k,
        COUNT(*) as nb_interventions,
        AVG(facturation_intervention) as cout_moyen
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND categorie IS NOT NULL
    AND facturation_intervention IS NOT NULL
    GROUP BY categorie
    ORDER BY cout_total_k DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_par_site(annee, limit=20):
    """Coût par site"""
    query = f"""
    SELECT 
        nom_site,
        SUM(facturation_intervention) / 1000 as cout_total_k,
        COUNT(*) as nb_interventions,
        AVG(facturation_intervention) as cout_moyen
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND nom_site IS NOT NULL
    AND facturation_intervention IS NOT NULL
    GROUP BY nom_site
    ORDER BY cout_total_k DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_taux_resolution_mensuel(annee):
    """Taux de résolution mensuel"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        COUNT(CASE WHEN ticket_resolu = 1 OR status_intervention LIKE '%Résolu%' OR status_intervention LIKE '%Clôturé%' THEN 1 END) * 100.0 / COUNT(*) as taux_resolution
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sla_cloture_detail(annee):
    """SLA Clôture détaillé : ≤7j et ≤30j"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        COUNT(*) as nb_total,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 7 THEN 1 END) as nb_7j,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 30 THEN 1 END) as nb_30j,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 7 THEN 1 END) * 100.0 / COUNT(*) as sla_7j_pct,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 30 THEN 1 END) * 100.0 / COUNT(*) as sla_30j_pct
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND date_creation_intervention IS NOT NULL
    AND date_fin_intervention IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sla_cloture_global(annee):
    """SLA Clôture global : ≤7j et ≤30j"""
    query = f"""
    SELECT 
        COUNT(*) as nb_total,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 7 THEN 1 END) as nb_7j,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 30 THEN 1 END) as nb_30j,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 7 THEN 1 END) * 100.0 / COUNT(*) as sla_7j_pct,
        COUNT(CASE WHEN JULIANDAY(date_fin_intervention) - JULIANDAY(date_creation_intervention) <= 30 THEN 1 END) * 100.0 / COUNT(*) as sla_30j_pct
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND date_creation_intervention IS NOT NULL
    AND date_fin_intervention IS NOT NULL
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_disponibilite_mensuelle(annee):
    """Disponibilité contractuelle mensuelle"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        AVG(dispo_contrat) as dispo_moyenne,
        AVG(dispo_brut) as dispo_brute_moyenne
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND dispo_contrat IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_avec_coordonnees(annee):
    """Interventions avec coordonnées GPS pour la carte"""
    query = f"""
    SELECT 
        i.nom_site,
        i.categorie,
        COUNT(*) as nb_interventions,
        e.latitude,
        e.longitude
    FROM interventions i
    LEFT JOIN exposition e ON i.id_site = e.id_site
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND i.nom_site IS NOT NULL
    GROUP BY i.nom_site, i.categorie, e.latitude, e.longitude
    HAVING e.latitude IS NOT NULL AND e.longitude IS NOT NULL
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


# ============================================
# FONCTIONS KPIs ZONE MAINTENEUR
# ============================================

def get_kpis_par_zone_mainteneur(annee):
    """KPIs complets par Zone Mainteneur"""
    query = f"""
    SELECT 
        e.zone_mainteneur,
        COUNT(DISTINCT e.id_site) as nb_sites,
        COUNT(i.numero_intervention) as nb_interventions,
        COUNT(i.numero_intervention) * 100.0 / NULLIF(COUNT(DISTINCT e.id_site), 0) as interventions_par_site,
        AVG(julianday(i.date_debut_intervention) - julianday(i.date_creation_intervention)) * 24 as delai_moyen_prise_en_charge_heures,
        AVG(i.duree_intervention_sur_site) as mttr_heures,
        AVG(julianday(i.date_fin_intervention) - julianday(i.date_creation_intervention)) as delai_moyen_cloture_jours,
        SUM(i.facturation_intervention) / 1000 as cout_total_k,
        AVG(i.facturation_intervention) as cout_moyen_intervention,
        SUM(i.facturation_intervention) / 1000.0 / NULLIF(COUNT(DISTINCT e.id_site), 0) as cout_par_site_k,
        COUNT(CASE WHEN i.ticket_resolu = 1 OR i.status_intervention LIKE '%Résolu%' OR i.status_intervention LIKE '%Clôturé%' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as taux_resolution_pct,
        COUNT(CASE WHEN julianday(i.date_fin_intervention) - julianday(i.date_creation_intervention) <= 7 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as sla_7j_pct,
        COUNT(CASE WHEN julianday(i.date_fin_intervention) - julianday(i.date_creation_intervention) <= 30 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as sla_30j_pct
    FROM exposition e
    LEFT JOIN interventions i ON e.id_site = i.id_site 
        AND CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    WHERE e.zone_mainteneur IS NOT NULL
    GROUP BY e.zone_mainteneur
    HAVING COUNT(DISTINCT e.id_site) > 0
    ORDER BY nb_interventions DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_spv_metrics_2025(annee):
    """Métriques complètes par SPV pour 2025 (breakdown complet)"""
    query = f"""
    SELECT 
        i.spv,
        -- Volume
        COUNT(DISTINCT i.numero_intervention) as nb_interventions,
        COUNT(DISTINCT i.id_site) as nb_sites_intervenus,
        COUNT(DISTINCT CASE WHEN i.categorie = 'CURATIVE' THEN i.numero_intervention END) as nb_curatives,
        COUNT(DISTINCT CASE WHEN i.categorie = 'PREVENTIVE' THEN i.numero_intervention END) as nb_preventives,
        -- Réactivité
        AVG(JULIANDAY(i.date_debut_intervention) - JULIANDAY(i.date_creation_intervention)) * 24 as delai_prise_charge_moyen_heures,
        -- Résolution
        AVG(CASE WHEN i.ticket_resolu = 1 OR i.status_intervention LIKE '%Résolu%' OR i.status_intervention LIKE '%Clôturé%' 
            THEN JULIANDAY(i.date_fin_intervention) - JULIANDAY(i.date_creation_intervention) END) as mttr_moyen_jours,
        AVG(CASE WHEN i.ticket_resolu = 1 OR i.status_intervention LIKE '%Résolu%' OR i.status_intervention LIKE '%Clôturé%' 
            THEN i.duree_intervention_sur_site END) as mttr_moyen_heures,
        COUNT(CASE WHEN i.ticket_resolu = 1 OR i.status_intervention LIKE '%Résolu%' OR i.status_intervention LIKE '%Clôturé%' THEN 1 END) * 100.0 / COUNT(*) as taux_resolution_pct,
        COUNT(CASE WHEN JULIANDAY(i.date_fin_intervention) - JULIANDAY(i.date_creation_intervention) <= 7 THEN 1 END) * 100.0 / COUNT(*) as sla_7j_pct,
        COUNT(CASE WHEN JULIANDAY(i.date_fin_intervention) - JULIANDAY(i.date_creation_intervention) <= 30 THEN 1 END) * 100.0 / COUNT(*) as sla_30j_pct,
        -- Coûts
        SUM(i.facturation_intervention) / 1000 as cout_total_k,
        AVG(i.facturation_intervention) as cout_moyen_intervention,
        SUM(i.facturation_intervention) / 1000.0 / NULLIF(COUNT(DISTINCT i.id_site), 0) as cout_par_site_k,
        -- Performance des sites gérés
        AVG(cas.pr_réel) as pr_moyen_sites,
        SUM(cas.prod_reel) / 1000000 as production_totale_gwh,
        SUM(e.puissance_nominale__kWc_) / 1000000 as puissance_totale_mw
    FROM interventions i
    LEFT JOIN exposition e ON i.id_site = e.id_site
    LEFT JOIN calculs_annuel_sites cas ON i.id_site = cas.id_site AND cas.annee = {annee}
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND i.spv IS NOT NULL
    GROUP BY i.spv
    ORDER BY nb_interventions DESC
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Arrondir les valeurs pour meilleure lisibilité
    numeric_cols = ['delai_prise_charge_moyen_heures', 'mttr_moyen_jours', 'mttr_moyen_heures', 
                   'taux_resolution_pct', 'sla_7j_pct', 'sla_30j_pct', 'cout_moyen_intervention',
                   'pr_moyen_sites', 'production_totale_gwh', 'puissance_totale_mw']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].round(2)
    
    return df


def get_interventions_par_100_mw(annee):
    """Interventions normalisées par 100 MW (global et par zone)"""
    query = f"""
    SELECT 
        COALESCE(e.zone_mainteneur, 'Total') as zone_mainteneur,
        COUNT(i.numero_intervention) as nb_interventions,
        SUM(e.puissance_nominale__kWc_) / 1000000 as puissance_mw,
        COUNT(i.numero_intervention) * 100.0 / NULLIF((SUM(e.puissance_nominale__kWc_) / 10000), 0) as interventions_par_100mw
    FROM exposition e
    LEFT JOIN interventions i ON e.id_site = i.id_site 
        AND CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    WHERE e.puissance_nominale__kWc_ > 0
    GROUP BY e.zone_mainteneur
    HAVING SUM(e.puissance_nominale__kWc_) > 0
    ORDER BY interventions_par_100mw DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_delai_median_prise_en_charge(annee):
    """Délai médian de prise en charge par zone (calculé en Python)"""
    query = f"""
    SELECT 
        e.zone_mainteneur,
        i.date_creation_intervention,
        i.date_debut_intervention
    FROM interventions i
    JOIN exposition e ON i.id_site = e.id_site
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND i.date_creation_intervention IS NOT NULL
    AND i.date_debut_intervention IS NOT NULL
    AND e.zone_mainteneur IS NOT NULL
    """
    df = load_data_from_db(query)
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Calculer les délais en heures
    df['date_creation'] = pd.to_datetime(df['date_creation_intervention'])
    df['date_debut'] = pd.to_datetime(df['date_debut_intervention'])
    df['delai_heures'] = (df['date_debut'] - df['date_creation']).dt.total_seconds() / 3600
    
    # Calculer la médiane par zone
    result = df.groupby('zone_mainteneur')['delai_heures'].agg(['median', 'mean', 'count']).reset_index()
    result.columns = ['zone_mainteneur', 'delai_median_heures', 'delai_moyen_heures', 'nb_interventions']
    
    return result


def get_top_motifs_interventions(annee, limit=10):
    """Top motifs d'interventions"""
    query = f"""
    SELECT 
        titre_intervention as motif,
        COUNT(*) as nb_interventions
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND titre_intervention IS NOT NULL
    AND titre_intervention != ''
    GROUP BY titre_intervention
    ORDER BY nb_interventions DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_sites_curatif_par_mw(annee, limit=15):
    """Top sites avec interventions curatives normalisées par MW"""
    query = f"""
    SELECT 
        i.id_site,
        e.nom_site,
        COUNT(CASE WHEN i.categorie = 'CURATIVE' THEN 1 END) as nb_curatif,
        e.puissance_nominale__kWc_ / 1000 as puissance_mw,
        COUNT(CASE WHEN i.categorie = 'CURATIVE' THEN 1 END) * 100.0 / NULLIF((e.puissance_nominale__kWc_ / 10000), 0) as curatif_par_100mw
    FROM interventions i
    JOIN exposition e ON i.id_site = e.id_site
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND e.puissance_nominale__kWc_ > 0
    GROUP BY i.id_site, e.nom_site, e.puissance_nominale__kWc_
    HAVING nb_curatif > 0
    ORDER BY curatif_par_100mw DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def show_maintenance_view():
    """Affiche la vue Maintenance complète"""
    
    st.markdown('''
    <div style="
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 3rem;
        padding: 28px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        🔧 Vue Maintenance
    </div>
    ''', unsafe_allow_html=True)
    
    # Filtres
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 2rem;">', unsafe_allow_html=True)
    col_filtre1, col_filtre2 = st.columns(2)
    with col_filtre1:
        annee_selectionnee = st.selectbox("Année", [2025, 2024, 2023], index=0, key="maintenance_annee")
    with col_filtre2:
        categorie_selectionnee = st.selectbox("Catégorie", ['Toutes'] + ['CURATIVE', 'PREVENTIF', 'NETTOYAGE', 'AUT', 'EXPL'], index=0, key="maintenance_categorie")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # SECTION A: Volume & Fréquence
    # ============================================
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
    ">📊 Volume & Fréquence</div>
    ''', unsafe_allow_html=True)
    
    # M.1 Chronologie Maintenance
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_chrono = get_chronologie_maintenance(annee_selectionnee)
    df_dispo = get_disponibilite_mensuelle(annee_selectionnee)
    
    if not df_chrono.empty:
        fig = go.Figure()
        
        # Catégories principales
        categories = ['CURATIVE', 'PREVENTIF', 'NETTOYAGE']
        colors = {'CURATIVE': '#ef4444', 'PREVENTIF': '#f59e0b', 'NETTOYAGE': '#0A84FF'}
        
        for cat in categories:
            df_cat = df_chrono[df_chrono['categorie'] == cat]
            if not df_cat.empty:
                fig.add_trace(go.Bar(
                    name=cat,
                    x=df_cat['mois'],
                    y=df_cat['nb_interventions'],
                    marker_color=colors.get(cat, '#6b7280')
                ))
        
        # Autres catégories
        autres_cats = df_chrono[~df_chrono['categorie'].isin(categories)]
        if not autres_cats.empty:
            autres_par_mois = autres_cats.groupby('mois')['nb_interventions'].sum().reset_index()
            fig.add_trace(go.Bar(
                name='Autres',
                x=autres_par_mois['mois'],
                y=autres_par_mois['nb_interventions'],
                marker_color='#6b7280'
            ))
        
        # Ligne disponibilité (axe secondaire)
        if not df_dispo.empty:
            fig.add_trace(go.Scatter(
                name='Disponibilité (%)',
                x=df_dispo['mois'],
                y=df_dispo['dispo_moyenne'],
                mode='lines+markers',
                line=dict(color='#10b981', width=3, dash='dash'),
                yaxis='y2'
            ))
        
        fig.update_layout(
            title='📅 Chronologie Maintenance',
            xaxis_title='Mois',
            yaxis_title='Nombre d\'interventions',
            yaxis2=dict(title='Disponibilité (%)', overlaying='y', side='right', range=[0, 100]),
            barmode='stack',
            height=450
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # M.2 & M.3 : Répartition et Interventions par Site
    col_m2, col_m3 = st.columns(2)
    
    with col_m2:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_repart = get_repartition_interventions()
        if not df_repart.empty:
            fig = px.pie(
                df_repart,
                values='nb',
                names='categorie',
                title='🔧 Interventions par Catégorie',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m3:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_sites_interv = get_interventions_par_site(annee_selectionnee)
        if not df_sites_interv.empty:
            fig = px.bar(
                df_sites_interv.head(15),
                x='nb_interventions',
                y='nom_site',
                orientation='h',
                title='🏢 Interventions par Site (Top 15)',
                labels={'nb_interventions': 'Nombre', 'nom_site': 'Site'},
                color='nb_interventions',
                color_continuous_scale='Blues'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # M.5 & M.6 : Sévérité et SPV
    col_m5, col_m6 = st.columns(2)
    
    with col_m5:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_severite = get_interventions_par_severite(annee_selectionnee)
        if not df_severite.empty:
            fig = px.bar(
                df_severite,
                x='mois',
                y='nb_interventions',
                color='severite_categorie',
                title='⚠️ Interventions par Sévérité',
                labels={'mois': 'Mois', 'nb_interventions': 'Nombre', 'severite_categorie': 'Sévérité'},
                barmode='stack'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m6:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_spv_interv = get_interventions_par_spv(annee_selectionnee)
        if not df_spv_interv.empty:
            fig = px.bar(
                df_spv_interv.head(15),
                x='spv',
                y='nb_interventions',
                title='🏢 Interventions par SPV (Top 15)',
                labels={'spv': 'SPV', 'nb_interventions': 'Nombre'},
                color='nb_interventions',
                color_continuous_scale='Viridis',
                text='nb_interventions'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(xaxis=dict(tickangle=-45), height=350, showlegend=False)
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION B: Réactivité & Résolution
    # ============================================
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
    ">⚡ Réactivité & Résolution</div>
    ''', unsafe_allow_html=True)
    
    # M.9 & M.10 : Taux de Résolution et MTTR
    col_m9, col_m10 = st.columns(2)
    
    with col_m9:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_taux_res = get_taux_resolution_mensuel(annee_selectionnee)
        taux_res_global = get_kpi_taux_resolution(annee_selectionnee)
        
        if not df_taux_res.empty:
            fig = px.bar(
                df_taux_res,
                x='mois',
                y='taux_resolution',
                title=f'✅ Taux de Résolution (Moyen: {taux_res_global:.1f}%)',
                labels={'mois': 'Mois', 'taux_resolution': 'Taux (%)'},
                color='taux_resolution',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                color_continuous_midpoint=95
            )
            fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target 95%")
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m10:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_mttr = get_mttr_par_categorie(annee_selectionnee)
        mttr_moyen_global, mttr_median_global, nb_mttr = get_mttr_global(annee_selectionnee)
        
        # KPI MTTR global
        if mttr_moyen_global is not None:
            col_mttr1, col_mttr2 = st.columns(2)
            with col_mttr1:
                st.metric("MTTR Moyen", f"{mttr_moyen_global:.1f}h", help="Moyenne du temps de résolution")
            with col_mttr2:
                st.metric("MTTR Médian", f"{mttr_median_global:.1f}h" if mttr_median_global else "N/A", help="Médiane du temps de résolution")
        
        if not df_mttr.empty:
            # Graphique avec moyenne et médiane
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Moyenne (jours)',
                x=df_mttr['categorie'],
                y=df_mttr['mttr_moyen_jours'],
                marker_color='#3b82f6',
                text=[f"{x:.1f}j" for x in df_mttr['mttr_moyen_jours']],
                textposition='outside'
            ))
            fig.add_trace(go.Bar(
                name='Médiane (jours)',
                x=df_mttr['categorie'],
                y=df_mttr['mttr_median_jours'],
                marker_color='#10b981',
                text=[f"{x:.1f}j" for x in df_mttr['mttr_median_jours']],
                textposition='outside'
            ))
            fig.update_layout(
                title='⏱️ MTTR par Catégorie (Moyenne vs Médiane)',
                xaxis_title='Catégorie',
                yaxis_title='Délai (jours)',
                barmode='group',
                height=350,
                xaxis=dict(tickangle=-45),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig.add_hline(y=7, line_dash="dash", line_color="orange", annotation_text="Target 7j")
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # M.11 & M.13 : Interventions en Cours et Temps de Réponse
    col_m11, col_m13 = st.columns(2)
    
    with col_m11:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_en_cours = get_interventions_en_cours(annee_selectionnee)
        nb_en_cours = len(df_en_cours) if not df_en_cours.empty else 0
        
        if nb_en_cours > 0:
            if nb_en_cours > 20:
                st.warning(f"⚠️ {nb_en_cours} interventions en cours (seuil dépassé: >20)")
            else:
                st.success(f"✅ {nb_en_cours} interventions en cours")
            
            st.dataframe(
                df_en_cours.head(20),
                column_config={
                    "numero_intervention": "N°",
                    "nom_site": "Site",
                    "categorie": "Catégorie",
                    "titre_intervention": "Titre",
                    "anciennete_jours": st.column_config.NumberColumn("Ancienneté (jours)", format="%.0f"),
                    "severite_categorie": "Sévérité"
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.info("✅ Aucune intervention en cours")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m13:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_temps_rep = get_temps_reponse_moyen(annee_selectionnee)
        if not df_temps_rep.empty:
            fig = px.bar(
                df_temps_rep,
                x='categorie',
                y='temps_reponse_heures',
                title='⚡ Temps de Réponse Moyen (heures)',
                labels={'categorie': 'Catégorie', 'temps_reponse_heures': 'Heures'},
                color='temps_reponse_heures',
                color_continuous_scale='Blues',
                text='temps_reponse_heures'
            )
            fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False, xaxis=dict(tickangle=-45))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # M.SLA : SLA Clôture (≤7j et ≤30j)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    df_sla_global = get_sla_cloture_global(annee_selectionnee)
    df_sla_detail = get_sla_cloture_detail(annee_selectionnee)
    
    # KPIs SLA globaux
    if not df_sla_global.empty:
        sla_7j_pct = df_sla_global.iloc[0]['sla_7j_pct']
        sla_30j_pct = df_sla_global.iloc[0]['sla_30j_pct']
        nb_7j = int(df_sla_global.iloc[0]['nb_7j'])
        nb_30j = int(df_sla_global.iloc[0]['nb_30j'])
        nb_total = int(df_sla_global.iloc[0]['nb_total'])
        
        col_sla1, col_sla2, col_sla3 = st.columns(3)
        with col_sla1:
            delta_sla7 = sla_7j_pct - 80  # Target 80%
            st.metric("SLA ≤7j", f"{sla_7j_pct:.1f}%", f"{delta_sla7:+.1f}%", 
                     delta_color="normal" if sla_7j_pct >= 80 else "inverse",
                     help=f"{nb_7j}/{nb_total} interventions clôturées en ≤7j")
        with col_sla2:
            delta_sla30 = sla_30j_pct - 95  # Target 95%
            st.metric("SLA ≤30j", f"{sla_30j_pct:.1f}%", f"{delta_sla30:+.1f}%",
                     delta_color="normal" if sla_30j_pct >= 95 else "inverse",
                     help=f"{nb_30j}/{nb_total} interventions clôturées en ≤30j")
        with col_sla3:
            st.metric("Total Interventions", f"{nb_total}", help="Interventions résolues")
        
        # Graphique évolution mensuelle
        if not df_sla_detail.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                name='SLA ≤7j',
                x=df_sla_detail['mois'],
                y=df_sla_detail['sla_7j_pct'],
                mode='lines+markers',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8),
                fill='tonexty',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            fig.add_trace(go.Scatter(
                name='SLA ≤30j',
                x=df_sla_detail['mois'],
                y=df_sla_detail['sla_30j_pct'],
                mode='lines+markers',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8)
            ))
            fig.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="Target 80% (≤7j)")
            fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target 95% (≤30j)")
            fig.update_layout(
                title='📊 Évolution SLA Clôture (Mensuel)',
                xaxis_title='Mois',
                yaxis_title='Taux (%)',
                yaxis=dict(range=[0, 100]),
                height=350,
                hovermode='x unified'
            )
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée SLA disponible")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION C: Coûts
    # ============================================
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
    ">💰 Coûts</div>
    ''', unsafe_allow_html=True)
    
    # M.14 & M.15 : Coût Total et Coût Moyen
    col_m14, col_m15 = st.columns(2)
    
    with col_m14:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_mens = get_cout_maintenance_detail(annee_selectionnee)
        cout_total_2025 = get_kpi_cout_maintenance(annee_selectionnee)
        cout_total_2024 = get_kpi_cout_maintenance(2024)
        
        if not df_cout_mens.empty:
            fig = px.bar(
                df_cout_mens,
                x='mois',
                y='cout_total_k',
                title=f'💰 Coût Total Maintenance ({cout_total_2025:.0f} k€ vs {cout_total_2024:.0f} k€ en 2024)',
                labels={'mois': 'Mois', 'cout_total_k': 'Coût (k€)'},
                color='cout_total_k',
                color_continuous_scale='Reds'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m15:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_cat = get_cout_par_categorie(annee_selectionnee)
        if not df_cout_cat.empty:
            fig = px.bar(
                df_cout_cat,
                x='categorie',
                y='cout_moyen',
                title='💶 Coût Moyen par Intervention',
                labels={'categorie': 'Catégorie', 'cout_moyen': 'Coût moyen (€)'},
                color='cout_moyen',
                color_continuous_scale='Oranges',
                text='cout_moyen'
            )
            fig.update_traces(texttemplate='%{text:.0f}€', textposition='outside')
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350, showlegend=False, xaxis=dict(tickangle=-45))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # M.16 & M.18 : Coût par Site et Répartition par Type
    col_m16, col_m18 = st.columns(2)
    
    with col_m16:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_site = get_cout_par_site(annee_selectionnee)
        if not df_cout_site.empty:
            fig = px.bar(
                df_cout_site.head(15),
                x='cout_total_k',
                y='nom_site',
                orientation='h',
                title='🏢 Coût par Site (Top 15)',
                labels={'cout_total_k': 'Coût (k€)', 'nom_site': 'Site'},
                color='cout_total_k',
                color_continuous_scale='Reds'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_m18:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_type = get_cout_par_categorie(annee_selectionnee)
        if not df_cout_type.empty:
            fig = px.pie(
                df_cout_type,
                values='cout_total_k',
                names='categorie',
                title='💳 Répartition Coûts par Type',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION D: Disponibilité
    # ============================================
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
    ">📈 Disponibilité</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    df_dispo_mens = get_disponibilite_mensuelle(annee_selectionnee)
    if not df_dispo_mens.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            name='Disponibilité Contractuelle',
            x=df_dispo_mens['mois'],
            y=df_dispo_mens['dispo_moyenne'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3)
        ))
        fig.add_trace(go.Scatter(
            name='Disponibilité Brute',
            x=df_dispo_mens['mois'],
            y=df_dispo_mens['dispo_brute_moyenne'],
            mode='lines+markers',
            line=dict(color='#0A84FF', width=3, dash='dash')
        ))
        fig.add_hline(y=98, line_dash="dash", line_color="green", annotation_text="Target 98%")
        fig.update_layout(
            title='📊 Disponibilité Contractuelle vs Brute',
            xaxis_title='Mois',
            yaxis_title='Disponibilité (%)',
            height=400
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # SECTION E: Zone Mainteneur
    # ============================================
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
    ">🗺️ Zone Mainteneur</div>
    ''', unsafe_allow_html=True)
    
    # KPI Global Interventions / 100 MW
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_interv_100mw = get_interventions_par_100_mw(annee_selectionnee)
    if not df_interv_100mw.empty:
        # KPI global
        total_interv = df_interv_100mw['nb_interventions'].sum()
        total_puissance = df_interv_100mw['puissance_mw'].sum()
        global_interv_100mw = (total_interv / total_puissance * 100) if total_puissance > 0 else 0
        
        col_kpi1, col_kpi2 = st.columns(2)
        with col_kpi1:
            st.metric(
                label="Interventions / 100 MW (Global)",
                value=f"{global_interv_100mw:.1f}",
                delta=None
            )
        with col_kpi2:
            df_delai_median = get_delai_median_prise_en_charge(annee_selectionnee)
            if not df_delai_median.empty:
                median_global = df_delai_median['delai_median_heures'].median()
                st.metric(
                    label="Délai Médian Prise en Charge",
                    value=f"{median_global:.1f}h",
                    delta=None
                )
        
        # Graphique Interventions / 100 MW par zone
        st.markdown("<br>", unsafe_allow_html=True)
        df_zones = df_interv_100mw[df_interv_100mw['zone_mainteneur'] != 'Total'].head(10)
        if not df_zones.empty:
            fig = px.bar(
                df_zones,
                x='interventions_par_100mw',
                y='zone_mainteneur',
                orientation='h',
                title='📊 Interventions / 100 MW par Zone Mainteneur',
                labels={'interventions_par_100mw': 'Interventions / 100 MW', 'zone_mainteneur': 'Zone'},
                color='interventions_par_100mw',
                color_continuous_scale='Reds'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau complet KPIs par Zone
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_zones_kpis = get_kpis_par_zone_mainteneur(annee_selectionnee)
    if not df_zones_kpis.empty:
        st.markdown('<h4 style="color: #1f2937; margin-bottom: 16px;">KPIs Complets par Zone Mainteneur</h4>', unsafe_allow_html=True)
        st.dataframe(
            df_zones_kpis,
            column_config={
                "zone_mainteneur": "Zone",
                "nb_sites": "Nb Sites",
                "nb_interventions": "Nb Interv.",
                "interventions_par_site": st.column_config.NumberColumn("Interv./Site", format="%.1f"),
                "delai_moyen_prise_en_charge_heures": st.column_config.NumberColumn("Délai Prise Charge (h)", format="%.1f"),
                "mttr_heures": st.column_config.NumberColumn("MTTR (h)", format="%.2f"),
                "delai_moyen_cloture_jours": st.column_config.NumberColumn("Délai Clôture (j)", format="%.1f"),
                "cout_total_k": st.column_config.NumberColumn("Coût Total (k€)", format="%.0f"),
                "cout_par_site_k": st.column_config.NumberColumn("Coût/Site (k€)", format="%.1f"),
                "taux_resolution_pct": st.column_config.NumberColumn("Taux Résolution (%)", format="%.1f"),
                "sla_7j_pct": st.column_config.NumberColumn("SLA ≤7j (%)", format="%.1f"),
                "sla_30j_pct": st.column_config.NumberColumn("SLA ≤30j (%)", format="%.1f")
            },
            hide_index=True,
            use_container_width=True,
            height=500
        )
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Motifs et Top Sites Curatifs
    col_motifs, col_sites = st.columns(2)
    
    with col_motifs:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_top_motifs = get_top_motifs_interventions(annee_selectionnee, limit=10)
        if not df_top_motifs.empty:
            fig = px.bar(
                df_top_motifs.head(10),
                x='nb_interventions',
                y='motif',
                orientation='h',
                title='🏷️ Top 10 Motifs d\'Interventions',
                labels={'nb_interventions': 'Nb Interventions', 'motif': 'Motif'},
                color='nb_interventions',
                color_continuous_scale='Blues'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_sites:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_top_sites = get_top_sites_curatif_par_mw(annee_selectionnee, limit=15)
        if not df_top_sites.empty:
            fig = px.bar(
                df_top_sites.head(15),
                x='curatif_par_100mw',
                y='nom_site',
                orientation='h',
                title='⚠️ Top 15 Sites Curatifs / 100 MW',
                labels={'curatif_par_100mw': 'Curatif / 100 MW', 'nom_site': 'Site'},
                color='curatif_par_100mw',
                color_continuous_scale='Oranges'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION F: Analyses par SPV (spv_metrics_2025)
    # ============================================
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
    ">🏢 Analyses par SPV (Prestataire)</div>
    ''', unsafe_allow_html=True)
    
    df_spv_metrics = get_spv_metrics_2025(annee_selectionnee)
    
    if not df_spv_metrics.empty:
        # Tableau complet des métriques par SPV
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin-bottom: 16px;">📊 Métriques Complètes par SPV</h4>', unsafe_allow_html=True)
        
        # Sélection des colonnes à afficher
        display_cols = {
            "spv": "SPV",
            "nb_interventions": "Nb Interv.",
            "nb_sites_intervenus": "Nb Sites",
            "nb_curatives": "Curatives",
            "nb_preventives": "Préventives",
            "delai_prise_charge_moyen_heures": st.column_config.NumberColumn("Délai Prise Charge (h)", format="%.1f"),
            "mttr_moyen_jours": st.column_config.NumberColumn("MTTR (j)", format="%.1f"),
            "taux_resolution_pct": st.column_config.NumberColumn("Taux Résolution (%)", format="%.1f"),
            "sla_7j_pct": st.column_config.NumberColumn("SLA ≤7j (%)", format="%.1f"),
            "sla_30j_pct": st.column_config.NumberColumn("SLA ≤30j (%)", format="%.1f"),
            "cout_total_k": st.column_config.NumberColumn("Coût Total (k€)", format="%.0f"),
            "cout_moyen_intervention": st.column_config.NumberColumn("Coût Moyen (€)", format="%.0f"),
            "pr_moyen_sites": st.column_config.NumberColumn("PR Moyen Sites (%)", format="%.1f"),
            "production_totale_gwh": st.column_config.NumberColumn("Production (GWh)", format="%.2f")
        }
        
        st.dataframe(
            df_spv_metrics,
            column_config=display_cols,
            hide_index=True,
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graphiques comparatifs par SPV
        col_spv1, col_spv2 = st.columns(2)
        
        with col_spv1:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            fig = px.bar(
                df_spv_metrics.head(15),
                x='spv',
                y='nb_interventions',
                title='📊 Volume Interventions par SPV (Top 15)',
                labels={'spv': 'SPV', 'nb_interventions': 'Nb Interventions'},
                color='nb_interventions',
                color_continuous_scale='Blues',
                text='nb_interventions'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False, xaxis=dict(tickangle=-45))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_spv2:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            fig = px.bar(
                df_spv_metrics.head(15),
                x='spv',
                y='taux_resolution_pct',
                title='✅ Taux de Résolution par SPV (Top 15)',
                labels={'spv': 'SPV', 'taux_resolution_pct': 'Taux Résolution (%)'},
                color='taux_resolution_pct',
                color_continuous_scale='Greens',
                text='taux_resolution_pct'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.add_hline(y=95, line_dash="dash", line_color="orange", annotation_text="Target 95%")
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False, xaxis=dict(tickangle=-45), yaxis=dict(range=[0, 100]))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Graphiques SLA et Coûts par SPV
        col_spv3, col_spv4 = st.columns(2)
        
        with col_spv3:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='SLA ≤7j',
                x=df_spv_metrics.head(15)['spv'],
                y=df_spv_metrics.head(15)['sla_7j_pct'],
                marker_color='#10b981'
            ))
            fig.add_trace(go.Bar(
                name='SLA ≤30j',
                x=df_spv_metrics.head(15)['spv'],
                y=df_spv_metrics.head(15)['sla_30j_pct'],
                marker_color='#3b82f6'
            ))
            fig.update_layout(
                title='⏱️ SLA Clôture par SPV (Top 15)',
                xaxis_title='SPV',
                yaxis_title='Taux (%)',
                barmode='group',
                height=400,
                xaxis=dict(tickangle=-45),
                yaxis=dict(range=[0, 100])
            )
            fig.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="Target 80% (≤7j)")
            fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target 95% (≤30j)")
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_spv4:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            fig = px.bar(
                df_spv_metrics.head(15),
                x='spv',
                y='cout_total_k',
                title='💰 Coût Total par SPV (Top 15)',
                labels={'spv': 'SPV', 'cout_total_k': 'Coût Total (k€)'},
                color='cout_total_k',
                color_continuous_scale='Reds',
                text='cout_total_k'
            )
            fig.update_traces(texttemplate='%{text:,.0f}k€', textposition='outside')
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False, xaxis=dict(tickangle=-45))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Aucune donnée SPV disponible")


# ============================================
# FONCTIONS VUE SITES
# ============================================

def get_liste_sites_complete():
    """Liste complète des sites avec KPIs"""
    query = """
    SELECT 
        e.id_site,
        e.nom_site,
        e.spv,
        e.puissance_nominale__kWc_ / 1000 as puissance_mw,
        e.date_mise_en_service,
        e.latitude,
        e.longitude,
        cas.pr_réel as pr_reel,
        SUM(cas.prod_reel) / 1000 as prod_annuelle_gwh,
        COUNT(DISTINCT i.numero_intervention) as nb_interventions,
        SUM(i.facturation_intervention) / 1000 as cout_maintenance_k
    FROM exposition e
    LEFT JOIN calculs_annuel_sites cas ON e.id_site = cas.id_site AND cas.annee = (SELECT MAX(CAST(annee AS INTEGER)) FROM calculs_annuel_sites)
    LEFT JOIN interventions i ON e.id_site = i.id_site AND CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = (SELECT MAX(CAST(annee AS INTEGER)) FROM calculs_annuel_sites)
    GROUP BY e.id_site, e.nom_site, e.spv, e.puissance_nominale__kWc_, e.date_mise_en_service, e.latitude, e.longitude, cas.pr_réel
    ORDER BY e.nom_site
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_tableau_detaille_sites(annee):
    """Tableau détaillé par site avec toutes les métriques"""
    query = f"""
    SELECT 
        cas.id_site as site,
        cas.dev_prod as deviation_prod_pct,
        cas.dev_irra as deviation_irra_pct,
        (1 - cas.dispo_contrat/100) * 100 as pertes_reseau_pct,
        (cas.dispo_contrat/100 - cas.dispo_brut/100) * 100 as pertes_apex_pct,
        0 as pertes_prix_negatifs_pct,
        cas.dev_prod - cas.dev_irra - ((1 - cas.dispo_contrat/100) * 100) - ((cas.dispo_contrat/100 - cas.dispo_brut/100) * 100) as ecart_residuel_pct,
        e.puissance_nominale__kWc_ / 1000 as puissance_mw,
        CAST((JULIANDAY('now') - JULIANDAY(e.date_mise_en_service)) / 365.25 AS INTEGER) as age_annees
    FROM calculs_annuel_sites cas
    JOIN exposition e ON cas.id_site = e.id_site
    WHERE cas.annee = {annee}
    ORDER BY cas.id_site
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_par_annee():
    """Sites par année de mise en service"""
    query = """
    SELECT 
        CAST(strftime('%Y', date_mise_en_service) AS INTEGER) as annee,
        COUNT(*) as nb_sites,
        SUM(puissance_nominale__kWc_) / 1000 as puissance_mw
    FROM exposition
    WHERE date_mise_en_service IS NOT NULL
    GROUP BY annee
    ORDER BY annee
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_distribution_age_sites():
    """Distribution de l'âge des sites"""
    query = """
    SELECT 
        CAST((JULIANDAY('now') - JULIANDAY(date_mise_en_service)) / 365.25 AS INTEGER) as age_annees,
        COUNT(*) as nb_sites
    FROM exposition
    WHERE date_mise_en_service IS NOT NULL
    GROUP BY age_annees
    ORDER BY age_annees
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_performance_site(site, annee):
    """Performance détaillée d'un site"""
    query = f"""
    SELECT 
        date,
        prod_reel / 1000 as prod_mwh,
        prod_pvsyst / 1000 as prod_budget_mwh,
        pr_réel as pr_reel
    FROM calculs_mensuel_sites
    WHERE site = ? AND CAST(strftime('%Y', date) AS INTEGER) = {annee}
    ORDER BY date
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=(site,))
    conn.close()
    return df if df is not None and not df.empty else pd.DataFrame()


def get_interventions_site(site, annee):
    """Interventions pour un site"""
    query = f"""
    SELECT 
        numero_intervention,
        date_creation_intervention,
        categorie,
        titre_intervention,
        facturation_intervention
    FROM interventions
    WHERE id_site = ? AND CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    ORDER BY date_creation_intervention DESC
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=(site,))
    conn.close()
    return df if df is not None and not df.empty else pd.DataFrame()


# ============================================
# FONCTIONS ONDULEURS PAR SITE
# ============================================

def get_onduleurs_par_site():
    """Nombre d'onduleurs par site"""
    query = """
    SELECT 
        code as id_site,
        COUNT(*) as nb_onduleurs,
        SUM(nominal_power) / 1000 as puissance_totale_mw,
        AVG(nominal_power) / 1000 as puissance_moyenne_mw
    FROM onduleurs_view
    WHERE code IS NOT NULL
    GROUP BY code
    ORDER BY nb_onduleurs DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_ecart_puissance_onduleurs_site():
    """Écart puissance onduleurs vs puissance site"""
    query = """
    SELECT 
        o.code as id_site,
        e.nom_site,
        SUM(o.nominal_power) / 1000 as puissance_onduleurs_mw,
        e.puissance_nominale__kWc_ / 1000 as puissance_site_mw,
        (SUM(o.nominal_power) / 1000 - e.puissance_nominale__kWc_ / 1000) / (e.puissance_nominale__kWc_ / 1000) * 100 as ecart_pct
    FROM onduleurs_view o
    JOIN exposition e ON o.code = e.id_site
    GROUP BY o.code, e.nom_site, e.puissance_nominale__kWc_
    ORDER BY ABS(ecart_pct) DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_fabricants_par_site():
    """Nombre de fabricants par site"""
    query = """
    SELECT 
        code as id_site,
        COUNT(DISTINCT manufacturername) as nb_fabricants,
        GROUP_CONCAT(DISTINCT manufacturername) as fabricants_liste
    FROM onduleurs_view
    WHERE code IS NOT NULL AND manufacturername IS NOT NULL
    GROUP BY code
    ORDER BY nb_fabricants DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_repartition_fabricants_site(site):
    """Répartition onduleurs par fabricant pour un site"""
    query = """
    SELECT 
        manufacturername,
        COUNT(*) as nb_onduleurs,
        SUM(nominal_power) / 1000 as puissance_mw
    FROM onduleurs_view
    WHERE code = ? AND manufacturername IS NOT NULL
    GROUP BY manufacturername
    ORDER BY nb_onduleurs DESC
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=(site,))
    conn.close()
    return df if df is not None and not df.empty else pd.DataFrame()


def get_modeles_par_site():
    """Nombre de modèles par site"""
    query = """
    SELECT 
        code as id_site,
        COUNT(DISTINCT modelname) as nb_modeles
    FROM onduleurs_view
    WHERE code IS NOT NULL AND modelname IS NOT NULL
    GROUP BY code
    ORDER BY nb_modeles DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_modele_principal_site():
    """Modèle principal par site"""
    query = """
    SELECT 
        code as id_site,
        modelname as modele_principal,
        COUNT(*) as nb_onduleurs,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM onduleurs_view o2 WHERE o2.code = o1.code) as pourcentage
    FROM onduleurs_view o1
    WHERE code IS NOT NULL AND modelname IS NOT NULL
    GROUP BY code, modelname
    HAVING nb_onduleurs = (
        SELECT MAX(cnt) FROM (
            SELECT COUNT(*) as cnt FROM onduleurs_view o2 
            WHERE o2.code = o1.code GROUP BY modelname
        )
    )
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_multi_fabricants():
    """Sites avec plusieurs fabricants"""
    query = """
    SELECT 
        code as id_site,
        COUNT(DISTINCT manufacturername) as nb_fabricants,
        GROUP_CONCAT(DISTINCT manufacturername) as fabricants
    FROM onduleurs_view
    WHERE code IS NOT NULL AND manufacturername IS NOT NULL
    GROUP BY code
    HAVING nb_fabricants > 1
    ORDER BY nb_fabricants DESC
    """
    df = load_data_from_db(query)
    # Remplacer les virgules par des virgules avec espaces pour l'affichage
    if not df.empty and 'fabricants' in df.columns:
        df['fabricants'] = df['fabricants'].str.replace(',', ', ')
    return df if df is not None and not df.empty else pd.DataFrame()


def get_coefficient_variation_puissance():
    """Coefficient de variation puissance par site (calculé avec Python)"""
    query = """
    SELECT 
        code as id_site,
        nominal_power
    FROM onduleurs_view
    WHERE code IS NOT NULL
    ORDER BY code, nominal_power
    """
    df = load_data_from_db(query)
    if df.empty:
        return pd.DataFrame()
    
    # Calculer coefficient de variation par site
    results = []
    for site in df['id_site'].unique():
        site_data = df[df['id_site'] == site]['nominal_power']
        if len(site_data) > 1:
            mean_power = site_data.mean()
            if mean_power > 0:
                std_power = site_data.std()
                coef_var = (std_power / mean_power) * 100
                results.append({
                    'id_site': site,
                    'puissance_moyenne': mean_power / 1000,
                    'nb_onduleurs': len(site_data),
                    'coef_variation_pct': coef_var
                })
    
    result_df = pd.DataFrame(results)
    return result_df.sort_values('coef_variation_pct', ascending=False)


def get_disponibilite_onduleurs_par_site():
    """Disponibilité des onduleurs par site (depuis onduleurs_perf si disponible)"""
    # Vérifier si la table existe
    try:
        query = """
        SELECT 
            "ID Site" as id_site,
            COUNT(*) as nb_onduleurs,
            AVG(CASE WHEN disponibilite IS NOT NULL THEN disponibilite ELSE NULL END) as dispo_moyenne,
            COUNT(CASE WHEN disponibilite IS NOT NULL THEN 1 END) as nb_onduleurs_avec_dispo
        FROM onduleurs_perf
        WHERE "ID Site" IS NOT NULL
        GROUP BY "ID Site"
        ORDER BY dispo_moyenne DESC
        """
        df = load_data_from_db(query)
        return df if df is not None and not df.empty else pd.DataFrame()
    except:
        # Table n'existe pas encore
        return pd.DataFrame()


def get_analyse_disponibilite_onduleurs():
    """Analyse complète de disponibilité des onduleurs"""
    try:
        query = """
        SELECT 
            "ID Site" as id_site,
            COUNT(*) as nb_onduleurs_total,
            AVG(disponibilite) as dispo_moyenne,
            MIN(disponibilite) as dispo_min,
            MAX(disponibilite) as dispo_max,
            COUNT(CASE WHEN disponibilite >= 99 THEN 1 END) as nb_onduleurs_hautes_perf,
            COUNT(CASE WHEN disponibilite < 95 THEN 1 END) as nb_onduleurs_alertes
        FROM onduleurs_perf
        WHERE "ID Site" IS NOT NULL AND disponibilite IS NOT NULL
        GROUP BY "ID Site"
        ORDER BY dispo_moyenne ASC
        """
        df = load_data_from_db(query)
        return df if df is not None and not df.empty else pd.DataFrame()
    except:
        return pd.DataFrame()


def get_liste_onduleurs_site(site):
    """Liste complète des onduleurs d'un site"""
    query = """
    SELECT 
        code,
        modelname,
        manufacturername,
        nominal_power / 1000 as puissance_kw
    FROM onduleurs_view
    WHERE code = ?
    ORDER BY manufacturername, modelname, nominal_power DESC
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=(site,))
    conn.close()
    return df if df is not None and not df.empty else pd.DataFrame()


def get_statistiques_globales_onduleurs():
    """Statistiques globales onduleurs"""
    query = """
    SELECT 
        COUNT(*) as total_onduleurs,
        SUM(nominal_power) / 1000 as puissance_totale_mw,
        COUNT(DISTINCT manufacturername) as nb_fabricants,
        COUNT(DISTINCT modelname) as nb_modeles,
        COUNT(DISTINCT code) as nb_sites_equipes
    FROM onduleurs_view
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_fabricants_globaux(limit=10):
    """Top fabricants globaux"""
    query = f"""
    SELECT 
        manufacturername,
        COUNT(*) as nb_onduleurs,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM onduleurs_view) as pourcentage,
        SUM(nominal_power) / 1000 as puissance_totale_mw
    FROM onduleurs_view
    WHERE manufacturername IS NOT NULL
    GROUP BY manufacturername
    ORDER BY nb_onduleurs DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_top_modeles_globaux(limit=10):
    """Top modèles globaux"""
    query = f"""
    SELECT 
        modelname,
        COUNT(*) as nb_onduleurs,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM onduleurs_view) as pourcentage,
        AVG(nominal_power) / 1000 as puissance_moyenne_mw
    FROM onduleurs_view
    WHERE modelname IS NOT NULL
    GROUP BY modelname
    ORDER BY nb_onduleurs DESC
    LIMIT {limit}
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_avec_onduleurs_anormaux():
    """Sites avec onduleurs anormaux (écart >10%, >5 fabricants, >10 modèles)"""
    query = """
    SELECT 
        code as id_site,
        COUNT(*) as nb_onduleurs,
        COUNT(DISTINCT manufacturername) as nb_fabricants,
        COUNT(DISTINCT modelname) as nb_modeles,
        (SUM(nominal_power) / 1000 - (SELECT e.puissance_nominale__kWc_ / 1000 FROM exposition e WHERE e.id_site = o.code)) / 
        (SELECT e.puissance_nominale__kWc_ / 1000 FROM exposition e WHERE e.id_site = o.code) * 100 as ecart_puissance_pct
    FROM onduleurs_view o
    JOIN exposition e ON o.code = e.id_site
    GROUP BY code
    HAVING ABS(ecart_puissance_pct) > 10 
       OR nb_fabricants > 5 
       OR nb_modeles > 10
    ORDER BY nb_fabricants DESC, nb_modeles DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


# ============================================
# FONCTIONS KPIs SITES FUTURS (AXELOR)
# ============================================

def get_projection_sites_axelor():
    """Projection sites futurs depuis axelor"""
    query = """
    SELECT 
        phase,
        statut,
        COUNT(DISTINCT id_site) as nb_sites,
        SUM(puissance__kwc_) / 1000 as puissance_mw
    FROM axelor
    WHERE id_site IS NOT NULL
    GROUP BY phase, statut
    ORDER BY phase, statut
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_par_phase():
    """Répartition des sites par phase (Exploitation, Construction, Développement, Pipe)"""
    query = """
    SELECT 
        phase,
        COUNT(DISTINCT id_site) as nb_sites,
        SUM(puissance__kwc_) / 1000 as puissance_mw,
        AVG(puissance__kwc_) as puissance_moyenne_kwc
    FROM axelor
    WHERE id_site IS NOT NULL
    AND phase IS NOT NULL
    GROUP BY phase
    ORDER BY 
        CASE phase
            WHEN 'Exploitation' THEN 1
            WHEN 'Construction' THEN 2
            WHEN 'DÈveloppement' THEN 3
            WHEN 'Pipe' THEN 4
            ELSE 5
        END
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_construction_avenir():
    """Sites en construction et à venir avec détails"""
    query = """
    SELECT 
        id_site,
        nom,
        adresse_du_projet,
        phase,
        statut,
        puissance__kwc_,
        date_t0_rèelle,
        date_mes_visèe,
        date_mes_rèelle
    FROM axelor
    WHERE phase IN ('Construction', 'DÈveloppement', 'Pipe')
    OR statut IN ('En cours')
    ORDER BY phase, puissance__kwc_ DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_puissance_installee_future():
    """Puissance installée future (sites en construction + à venir)"""
    query = """
    SELECT 
        SUM(CASE WHEN phase = 'Construction' THEN puissance__kwc_ ELSE 0 END) / 1000 as puissance_construction_mw,
        SUM(CASE WHEN phase = 'DÈveloppement' THEN puissance__kwc_ ELSE 0 END) / 1000 as puissance_developpement_mw,
        SUM(CASE WHEN phase = 'Pipe' THEN puissance__kwc_ ELSE 0 END) / 1000 as puissance_pipe_mw,
        SUM(CASE WHEN phase IN ('Construction', 'DÈveloppement', 'Pipe') THEN puissance__kwc_ ELSE 0 END) / 1000 as puissance_totale_future_mw
    FROM axelor
    WHERE puissance__kwc_ IS NOT NULL
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_sites_exploitation_vs_futurs():
    """Comparaison sites en exploitation vs sites futurs"""
    query = """
    SELECT 
        CASE 
            WHEN phase = 'Exploitation' THEN 'En Exploitation'
            ELSE 'Futurs (Construction + Développement + Pipe)'
        END as type_site,
        COUNT(DISTINCT id_site) as nb_sites,
        SUM(puissance__kwc_) / 1000 as puissance_mw
    FROM axelor
    WHERE puissance__kwc_ IS NOT NULL
    GROUP BY 
        CASE 
            WHEN phase = 'Exploitation' THEN 'En Exploitation'
            ELSE 'Futurs (Construction + Développement + Pipe)'
        END
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def show_sites_view():
    """Affiche la vue Sites complète"""
    
    st.markdown('''
    <div style="
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 3rem;
        padding: 28px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        🏢 Vue Sites
    </div>
    ''', unsafe_allow_html=True)
    
    # Tabs pour différentes sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Liste Sites", "📊 Tableau Détaillé", "⚡ Onduleurs par Site", "🌍 Carte & Distribution", "🚀 Projection Sites"])
    
    with tab1:
        # S.1 Liste Complète des Sites
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">📋 Liste Complète des Sites</div>
        ''', unsafe_allow_html=True)
        
        # Filtres
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            df_spv = load_data_from_db("SELECT DISTINCT spv FROM exposition WHERE spv IS NOT NULL ORDER BY spv")
            spv_list = ['Tous'] + df_spv['spv'].tolist() if not df_spv.empty else ['Tous']
            spv_filter = st.selectbox("SPV", spv_list, key="sites_spv")
        with col_f2:
            annee_filter = st.selectbox("Année", [2025, 2024, 2023], index=0, key="sites_annee")
        with col_f3:
            search_term = st.text_input("🔍 Rechercher site", key="sites_search")
        
        df_sites = get_liste_sites_complete()
        if not df_sites.empty:
            # Appliquer filtres
            if spv_filter != 'Tous':
                df_sites = df_sites[df_sites['spv'] == spv_filter]
            if search_term:
                df_sites = df_sites[df_sites['nom_site'].str.contains(search_term, case=False, na=False)]
            
            st.dataframe(
                df_sites,
                column_config={
                    "id_site": "Code",
                    "nom_site": "Nom Site",
                    "spv": "SPV",
                    "puissance_mw": st.column_config.NumberColumn("Puissance (MW)", format="%.2f"),
                    "date_mise_en_service": "Mise en Service",
                    "pr_reel": st.column_config.NumberColumn("PR (%)", format="%.1f"),
                    "prod_annuelle_gwh": st.column_config.NumberColumn("Prod (GWh)", format="%.2f"),
                    "nb_interventions": "Nb Interv.",
                    "cout_maintenance_k": st.column_config.NumberColumn("Coût (k€)", format="%.0f")
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.info("Aucune donnée disponible")
    
    with tab2:
        # S.2 Tableau Détaillé par Site
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">📊 Tableau Détaillé par Site</div>
        ''', unsafe_allow_html=True)
        
        annee_tab2 = st.selectbox("Année", [2025, 2024, 2023], index=0, key="tab2_annee")
        df_detaille = get_tableau_detaille_sites(annee_tab2)
        
        if not df_detaille.empty:
            st.dataframe(
                df_detaille,
                column_config={
                    "site": "Site",
                    "deviation_prod_pct": st.column_config.NumberColumn("Dév. Prod (%)", format="%.2f"),
                    "deviation_irra_pct": st.column_config.NumberColumn("Dév. Irra (%)", format="%.2f"),
                    "pertes_reseau_pct": st.column_config.NumberColumn("Pertes Réseau (%)", format="%.2f"),
                    "pertes_apex_pct": st.column_config.NumberColumn("Pertes APEX (%)", format="%.2f"),
                    "ecart_residuel_pct": st.column_config.NumberColumn("Écart Résiduel (%)", format="%.2f"),
                    "puissance_mw": st.column_config.NumberColumn("Puissance (MW)", format="%.2f"),
                    "age_annees": "Âge (ans)"
                },
                hide_index=True,
                use_container_width=True,
                height=500
            )
        else:
            st.info("Aucune donnée disponible")
        
        # S.3 Fiche Détaillée Site
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">📄 Fiche Détaillée Site</div>
        ''', unsafe_allow_html=True)
        
        df_liste = get_liste_sites()
        if not df_liste.empty:
            site_selectionne = st.selectbox("Sélectionner un site", df_liste['id_site'].tolist(), key="fiche_site")
            annee_fiche = st.selectbox("Année", [2025, 2024, 2023], index=0, key="fiche_annee")
            
            # Production mensuelle
            df_prod = get_performance_site(site_selectionne, annee_fiche)
            if not df_prod.empty:
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    fig = px.bar(
                        df_prod,
                        x='date',
                        y='prod_mwh',
                        title=f'Production Mensuelle - {site_selectionne}',
                        labels={'date': 'Mois', 'prod_mwh': 'Production (MWh)'},
                        color='prod_mwh',
                        color_continuous_scale='Blues'
                    )
                    fig = apply_glassmorphism_theme(fig)
                    fig.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_p2:
                    fig = px.line(
                        df_prod,
                        x='date',
                        y='pr_reel',
                        title=f'PR Mensuel - {site_selectionne}',
                        labels={'date': 'Mois', 'pr_reel': 'PR (%)'},
                        markers=True
                    )
                    fig.update_traces(line_color='#0A84FF', line_width=3)
                    fig = apply_glassmorphism_theme(fig)
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Interventions
            df_interv = get_interventions_site(site_selectionne, annee_fiche)
            if not df_interv.empty:
                st.markdown('<h4 style="color: #1f2937; margin-top: 2rem;">Interventions</h4>', unsafe_allow_html=True)
                st.dataframe(df_interv, hide_index=True, use_container_width=True, height=300)
            else:
                st.info(f"Aucune intervention pour {site_selectionne} en {annee_fiche}")
    
    with tab3:
        # S.O Onduleurs par Site
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">⚡ Onduleurs par Site</div>
        ''', unsafe_allow_html=True)
        
        # Statistiques Globales
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Statistiques Globales Onduleurs</h4>', unsafe_allow_html=True)
        df_stats_glob = get_statistiques_globales_onduleurs()
        if not df_stats_glob.empty:
            col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
            with col_s1:
                st.metric("Total Onduleurs", format_count(int(df_stats_glob['total_onduleurs'].iloc[0])))
            with col_s2:
                # Convertir MW en kWc pour format_power_capacity (multiplier par 1000)
                puissance_totale_kwc = df_stats_glob['puissance_totale_mw'].iloc[0] * 1000 if df_stats_glob['puissance_totale_mw'].iloc[0] is not None else 0
                st.metric("Puissance Totale", format_power_capacity(puissance_totale_kwc, decimals=1))
            with col_s3:
                st.metric("Fabricants", int(df_stats_glob['nb_fabricants'].iloc[0]))
            with col_s4:
                st.metric("Modèles", int(df_stats_glob['nb_modeles'].iloc[0]))
            with col_s5:
                st.metric("Sites Équipés", int(df_stats_glob['nb_sites_equipes'].iloc[0]))
        
        # Top Fabricants et Modèles
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            df_top_fab = get_top_fabricants_globaux()
            if not df_top_fab.empty:
                fig = px.bar(
                    df_top_fab,
                    x='nb_onduleurs',
                    y='manufacturername',
                    orientation='h',
                    title='🏭 Top 10 Fabricants',
                    labels={'nb_onduleurs': 'Nombre', 'manufacturername': 'Fabricant'},
                    color='nb_onduleurs',
                    color_continuous_scale='Blues'
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_t2:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            df_top_mod = get_top_modeles_globaux()
            if not df_top_mod.empty:
                fig = px.bar(
                    df_top_mod,
                    x='nb_onduleurs',
                    y='modelname',
                    orientation='h',
                    title='📦 Top 10 Modèles',
                    labels={'nb_onduleurs': 'Nombre', 'modelname': 'Modèle'},
                    color='nb_onduleurs',
                    color_continuous_scale='Greens'
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Onduleurs par Site
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Nombre d\'Onduleurs par Site</h4>', unsafe_allow_html=True)
        df_ond_site = get_onduleurs_par_site()
        if not df_ond_site.empty:
            col_o1, col_o2 = st.columns(2)
            
            with col_o1:
                st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                fig = px.bar(
                    df_ond_site.head(20),
                    x='nb_onduleurs',
                    y='id_site',
                    orientation='h',
                    title='⚡ Top 20 Sites par Nombre d\'Onduleurs',
                    labels={'nb_onduleurs': 'Nombre', 'id_site': 'Site'},
                    color='nb_onduleurs',
                    color_continuous_scale='Viridis'
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_o2:
                st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                st.dataframe(
                    df_ond_site.head(30),
                    column_config={
                        "id_site": "Site",
                        "nb_onduleurs": "Nb Onduleurs",
                        "puissance_totale_mw": st.column_config.NumberColumn("Puissance (MW)", format="%.2f"),
                        "puissance_moyenne_mw": st.column_config.NumberColumn("Puissance Moy. (MW)", format="%.3f")
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=500
                )
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Disponibilité Onduleurs (onduleurs_perf si disponible)
        df_dispo = get_disponibilite_onduleurs_par_site()
        df_analyse_dispo = get_analyse_disponibilite_onduleurs()
        
        if not df_dispo.empty or not df_analyse_dispo.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">📊 Disponibilité des Onduleurs (Performance)</h4>', unsafe_allow_html=True)
            
            if not df_analyse_dispo.empty:
                col_dispo1, col_dispo2 = st.columns(2)
                
                with col_dispo1:
                    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                    fig = px.bar(
                        df_analyse_dispo.head(20),
                        x='dispo_moyenne',
                        y='id_site',
                        orientation='h',
                        title='📊 Disponibilité Moyenne par Site (Top 20)',
                        labels={'dispo_moyenne': 'Disponibilité (%)', 'id_site': 'Site'},
                        color='dispo_moyenne',
                        color_continuous_scale='RdYlGn'
                    )
                    fig.add_vline(x=95, line_dash="dash", line_color="orange", annotation_text="Seuil 95%")
                    fig = apply_glassmorphism_theme(fig)
                    fig.update_layout(height=500, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_dispo2:
                    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                    st.dataframe(
                        df_analyse_dispo.head(30),
                        column_config={
                            "id_site": "Site",
                            "nb_onduleurs_total": "Nb Total",
                            "dispo_moyenne": st.column_config.NumberColumn("Dispo Moy. (%)", format="%.2f"),
                            "dispo_min": st.column_config.NumberColumn("Dispo Min (%)", format="%.2f"),
                            "dispo_max": st.column_config.NumberColumn("Dispo Max (%)", format="%.2f"),
                            "nb_onduleurs_hautes_perf": "Nb ≥99%",
                            "nb_onduleurs_alertes": st.column_config.NumberColumn("Nb <95%", format="%d")
                        },
                        hide_index=True,
                        use_container_width=True,
                        height=500
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Écart Puissance
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Écart Puissance Onduleurs vs Site</h4>', unsafe_allow_html=True)
        df_ecart = get_ecart_puissance_onduleurs_site()
        if not df_ecart.empty:
            # Marquer les alertes
            df_ecart['alerte'] = df_ecart['ecart_pct'].apply(lambda x: '⚠️' if abs(x) > 5 else '✅')
            st.dataframe(
                df_ecart.head(30),
                column_config={
                    "id_site": "Site",
                    "nom_site": "Nom",
                    "puissance_onduleurs_mw": st.column_config.NumberColumn("Puiss. Ond. (MW)", format="%.2f"),
                    "puissance_site_mw": st.column_config.NumberColumn("Puiss. Site (MW)", format="%.2f"),
                    "ecart_pct": st.column_config.NumberColumn("Écart (%)", format="%.2f")
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        
        # Sites Multi-Fabricants
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Sites Multi-Fabricants</h4>', unsafe_allow_html=True)
        df_multi_fab = get_sites_multi_fabricants()
        if not df_multi_fab.empty:
            # Alerte si >3 fabricants
            df_multi_fab['alerte'] = df_multi_fab['nb_fabricants'].apply(lambda x: '⚠️ >3' if x > 3 else '✅')
            st.dataframe(
                df_multi_fab,
                column_config={
                    "id_site": "Site",
                    "nb_fabricants": "Nb Fabricants",
                    "fabricants": "Fabricants"
                },
                hide_index=True,
                use_container_width=True,
                height=300
            )
        
        # Détail onduleurs d'un site
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Détail Onduleurs d\'un Site</h4>', unsafe_allow_html=True)
        df_liste_ond = get_liste_sites()
        if not df_liste_ond.empty:
            site_ond = st.selectbox("Sélectionner un site", df_liste_ond['id_site'].tolist(), key="detail_ond_site")
            df_detail_ond = get_liste_onduleurs_site(site_ond)
            if not df_detail_ond.empty:
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.dataframe(
                        df_detail_ond,
                        column_config={
                            "code": "Code",
                            "modelname": "Modèle",
                            "manufacturername": "Fabricant",
                            "puissance_kw": st.column_config.NumberColumn("Puissance (kW)", format="%.2f")
                        },
                        hide_index=True,
                        use_container_width=True,
                        height=400
                    )
                
                with col_d2:
                    df_repart_fab = get_repartition_fabricants_site(site_ond)
                    if not df_repart_fab.empty:
                        fig = px.pie(
                            df_repart_fab,
                            values='nb_onduleurs',
                            names='manufacturername',
                            title=f'Répartition par Fabricant - {site_ond}',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        fig = apply_glassmorphism_theme(fig)
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # S.5 Carte Interactive
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">🌍 Carte & Distribution</div>
        ''', unsafe_allow_html=True)
        
        df_carte = get_liste_sites_complete()
        if not df_carte.empty and df_carte['latitude'].notna().any() and df_carte['longitude'].notna().any():
            # Nettoyer les données : supprimer NaN dans lat/lon/puissance
            df_carte_clean = df_carte.dropna(subset=['latitude', 'longitude', 'puissance_mw'])
            
            # Remplacer les NaN dans pr_reel par une valeur par défaut pour le color mapping
            df_carte_clean['pr_reel'] = df_carte_clean['pr_reel'].fillna(75.0)
            
            if not df_carte_clean.empty:
                # Créer la carte avec scatter_mapbox
                fig = px.scatter_mapbox(
                    df_carte_clean,
                    lat="latitude",
                    lon="longitude",
                    hover_name="nom_site",
                    hover_data=["spv", "puissance_mw", "pr_reel"],
                    size="puissance_mw",
                    color="pr_reel",
                    color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                    size_max=30,
                    zoom=5,
                    height=600,
                    title="🗺️ Carte Interactive des Sites"
                )
                fig.update_layout(
                    mapbox_style="open-street-map",
                    margin={"r":0,"t":0,"l":0,"b":0}
                )
                fig = apply_glassmorphism_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée de géolocalisation valide disponible")
        else:
            st.info("Aucune donnée de géolocalisation disponible")
        
        # S.7 Sites par Année
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Sites par Année de Mise en Service</h4>', unsafe_allow_html=True)
        df_annee = get_sites_par_annee()
        if not df_annee.empty:
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                fig = px.bar(
                    df_annee,
                    x='annee',
                    y='nb_sites',
                    title='📅 Nombre de Sites par Année',
                    labels={'annee': 'Année', 'nb_sites': 'Nombre de Sites'},
                    color='nb_sites',
                    color_continuous_scale='Blues'
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_a2:
                st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
                df_annee['cumul'] = df_annee['nb_sites'].cumsum()
                fig = px.line(
                    df_annee,
                    x='annee',
                    y='cumul',
                    title='📈 Cumul de Sites',
                    labels={'annee': 'Année', 'cumul': 'Cumul'},
                    markers=True
                )
                fig.update_traces(line_color='#0A84FF', line_width=3, marker_size=10)
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # S.8 Distribution Âge
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1f2937; margin: 1rem 0;">Distribution de l\'Âge des Sites</h4>', unsafe_allow_html=True)
        df_age = get_distribution_age_sites()
        if not df_age.empty:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            fig = px.bar(
                df_age,
                x='age_annees',
                y='nb_sites',
                title='📊 Histogramme d\'Âge des Sites',
                labels={'age_annees': 'Âge (années)', 'nb_sites': 'Nombre de Sites'},
                color='nb_sites',
                color_continuous_scale='Oranges'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        # Projection Sites Futurs (Axelor)
        st.markdown('''
        <div style="
            padding: 16px 24px;
            margin: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        ">🚀 Projection Sites Futurs</div>
        ''', unsafe_allow_html=True)
        
        # KPIs Principaux
        df_puissance_future = get_puissance_installee_future()
        df_sites_phase = get_sites_par_phase()
        df_exploitation_vs_futurs = get_sites_exploitation_vs_futurs()
        
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            if not df_sites_phase.empty:
                sites_construction = df_sites_phase[df_sites_phase['phase'] == 'Construction']['nb_sites'].iloc[0] if len(df_sites_phase[df_sites_phase['phase'] == 'Construction']) > 0 else 0
                st.metric("Sites en Construction", f"{int(sites_construction)}", delta=None)
        
        with col_kpi2:
            if not df_sites_phase.empty:
                sites_dev = df_sites_phase[df_sites_phase['phase'] == 'DÈveloppement']['nb_sites'].iloc[0] if len(df_sites_phase[df_sites_phase['phase'] == 'DÈveloppement']) > 0 else 0
                st.metric("Sites en Développement", f"{int(sites_dev)}", delta=None)
        
        with col_kpi3:
            if not df_puissance_future.empty:
                puiss_future_mw = df_puissance_future['puissance_totale_future_mw'].iloc[0] if df_puissance_future['puissance_totale_future_mw'].iloc[0] is not None else 0
                # Convertir MW en kWc pour format_power_capacity (multiplier par 1000)
                puiss_future_kwc = puiss_future_mw * 1000
                st.metric("Puissance Future Totale", format_power_capacity(puiss_future_kwc, decimals=1), delta=None)
        
        with col_kpi4:
            if not df_exploitation_vs_futurs.empty:
                sites_futurs = df_exploitation_vs_futurs[df_exploitation_vs_futurs['type_site'] == 'Futurs (Construction + Développement + Pipe)']['nb_sites'].iloc[0] if len(df_exploitation_vs_futurs[df_exploitation_vs_futurs['type_site'] == 'Futurs (Construction + Développement + Pipe)']) > 0 else 0
                st.metric("Sites Futurs (Total)", f"{int(sites_futurs)}", delta=None)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graphiques
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            if not df_sites_phase.empty:
                fig = px.bar(
                    df_sites_phase,
                    x='phase',
                    y='nb_sites',
                    title='📊 Nombre de Sites par Phase',
                    labels={'phase': 'Phase', 'nb_sites': 'Nombre de Sites'},
                    color='phase',
                    color_discrete_map={
                        'Exploitation': '#10b981',
                        'Construction': '#f59e0b',
                        'DÈveloppement': '#0A84FF',
                        'Pipe': '#6b7280'
                    }
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée disponible")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_g2:
            st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            if not df_sites_phase.empty:
                fig = px.pie(
                    df_sites_phase,
                    values='puissance_mw',
                    names='phase',
                    title='⚡ Puissance Installée par Phase',
                    color_discrete_map={
                        'Exploitation': '#10b981',
                        'Construction': '#f59e0b',
                        'DÈveloppement': '#0A84FF',
                        'Pipe': '#6b7280'
                    }
                )
                fig = apply_glassmorphism_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée disponible")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Comparaison Exploitation vs Futurs
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
        if not df_exploitation_vs_futurs.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Nombre de Sites',
                x=df_exploitation_vs_futurs['type_site'],
                y=df_exploitation_vs_futurs['nb_sites'],
                marker_color='#0A84FF',
                yaxis='y'
            ))
            fig.add_trace(go.Bar(
                name='Puissance (MW)',
                x=df_exploitation_vs_futurs['type_site'],
                y=df_exploitation_vs_futurs['puissance_mw'],
                marker_color='#10b981',
                yaxis='y2'
            ))
            fig.update_layout(
                title='📊 Sites en Exploitation vs Sites Futurs',
                xaxis_title='Type',
                yaxis_title='Nombre de Sites',
                yaxis2=dict(title='Puissance (MW)', overlaying='y', side='right'),
                barmode='group',
                height=400
            )
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tableau détaillé sites en construction/à venir
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_sites_futurs = get_sites_construction_avenir()
        if not df_sites_futurs.empty:
            st.markdown('<h4 style="color: #1f2937; margin-bottom: 16px;">Détails Sites en Construction et à Venir</h4>', unsafe_allow_html=True)
            st.dataframe(
                df_sites_futurs.head(50),
                column_config={
                    "id_site": "Code Site",
                    "nom": "Nom",
                    "adresse_du_projet": "Adresse",
                    "phase": "Phase",
                    "statut": "Statut",
                    "puissance__kwc_": st.column_config.NumberColumn("Puissance (kWc)", format="%.2f"),
                    "date_t0_rèelle": "Date T0",
                    "date_mes_visèe": "MES Visée",
                    "date_mes_rèelle": "MES Réelle"
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# FONCTIONS VUE FINANCE
# ============================================

def get_ca_total(annee):
    """Chiffre d'Affaires total pour une année"""
    query = f"""
    SELECT 
        SUM(prod_reel_distributeur * tarif_edf / 1000) as ca_total_k
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    """
    df = load_data_from_db(query)
    return df['ca_total_k'].iloc[0] if df is not None and not df.empty and df['ca_total_k'].iloc[0] is not None else 0


def get_ca_par_site(annee):
    """CA par site"""
    query = f"""
    SELECT 
        site,
        SUM(prod_reel_distributeur * tarif_edf / 1000) as ca_k
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    GROUP BY site
    ORDER BY ca_k DESC
    LIMIT 20
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_ca_mensuel(annee):
    """CA mensuel"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        SUM(prod_reel_distributeur * tarif / 1000) as ca_k,
        SUM(prod_reel_distributeur * tarif) as ca_cumul_k
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    if df is not None and not df.empty:
        df['ca_cumul'] = df['ca_k'].cumsum()
    return df if df is not None and not df.empty else pd.DataFrame()


def get_ca_par_spv(annee):
    """CA par SPV"""
    query = f"""
    SELECT 
        spv,
        SUM(prod_reel_distributeur * tarif_edf / 1000) as ca_k,
        COUNT(DISTINCT site) as nb_sites
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_reel_distributeur IS NOT NULL
    AND tarif_edf IS NOT NULL
    GROUP BY spv
    ORDER BY ca_k DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_maintenance_par_production(annee):
    """Coût maintenance / production (€/MWh)"""
    # Calculer les coûts par mois
    query_cout = f"""
    SELECT 
        CAST(strftime('%m', date_creation_intervention) AS INTEGER) as mois,
        SUM(facturation_intervention) / 1000 as cout_k
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND facturation_intervention IS NOT NULL
    GROUP BY mois
    """
    
    # Calculer la production par mois
    query_prod = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        SUM(prod_reel) / 1000 as prod_mwh
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND prod_reel IS NOT NULL
    AND prod_reel > 0
    GROUP BY mois
    """
    
    df_cout = load_data_from_db(query_cout)
    df_prod = load_data_from_db(query_prod)
    
    if df_cout is not None and not df_cout.empty and df_prod is not None and not df_prod.empty:
        # Fusionner les deux DataFrames
        df = pd.merge(df_cout, df_prod, on='mois', how='outer')
        df = df.fillna(0)
        # Calculer le ratio
        df['cout_par_mwh'] = (df['cout_k'] / df['prod_mwh'] * 1000).replace([float('inf'), float('-inf')], 0)
        df = df[df['mois'].notna()]
        df = df.sort_values('mois')
        return df
    return pd.DataFrame()


def get_cout_maintenance_par_kwc(annee):
    """Coût maintenance / kWc par site"""
    query = f"""
    SELECT 
        i.id_site as site,
        e.nom_site,
        SUM(i.facturation_intervention) / 1000 as cout_k,
        e.puissance_nominale__kWc_ / 1000 as puissance_mw,
        (SUM(i.facturation_intervention) / 1000) / (e.puissance_nominale__kWc_ / 1000) as cout_par_kwc
    FROM interventions i
    JOIN exposition e ON i.id_site = e.id_site
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND i.facturation_intervention IS NOT NULL
    AND e.puissance_nominale__kWc_ IS NOT NULL
    AND e.puissance_nominale__kWc_ > 0
    GROUP BY i.id_site, e.nom_site, e.puissance_nominale__kWc_
    ORDER BY cout_par_kwc DESC
    LIMIT 30
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_manque_a_gagner(annee):
    """Manque à gagner (pertes de revenus)"""
    query = f"""
    SELECT 
        SUM((prod_pvsyst - prod_reel) * tarif_edf / 1000) as manque_a_gagner_k,
        SUM(prod_pvsyst * tarif_edf / 1000) as ca_budget_k,
        SUM(prod_reel * tarif_edf / 1000) as ca_reel_k
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_pvsyst IS NOT NULL
    AND prod_reel IS NOT NULL
    AND tarif_edf IS NOT NULL
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_manque_a_gagner_par_cause(annee):
    """Manque à gagner par cause (météo, pannes, maintenance)"""
    query = f"""
    SELECT 
        site,
        SUM(prod_pvsyst * tarif_edf / 1000) as ca_budget_k,
        SUM(prod_reel * tarif_edf / 1000) as ca_reel_k,
        SUM((prod_pvsyst - prod_reel) * tarif_edf / 1000) as manque_a_gagner_k,
        SUM((1 - dispo_contrat/100) * prod_pvsyst * tarif_edf / 1000) as pertes_reseau_k,
        SUM((dispo_contrat/100 - dispo_brut/100) * prod_pvsyst * tarif_edf / 1000) as pertes_apex_k
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND prod_pvsyst IS NOT NULL
    AND prod_reel IS NOT NULL
    AND tarif_edf IS NOT NULL
    GROUP BY site
    ORDER BY manque_a_gagner_k DESC
    LIMIT 20
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_budget_production_vs_realise(annee):
    """Budget production vs réalisé"""
    query = f"""
    SELECT 
        CAST(strftime('%m', date) AS INTEGER) as mois,
        SUM(prod_pvsyst * tarif / 1000) as ca_budget_k,
        SUM(prod_reel_distributeur * tarif / 1000) as ca_reel_k,
        (SUM(prod_reel_distributeur * tarif / 1000) - SUM(prod_pvsyst * tarif / 1000)) / SUM(prod_pvsyst * tarif / 1000) * 100 as ecart_pct
    FROM calculs_mensuel_sites
    WHERE CAST(strftime('%Y', date) AS INTEGER) = {annee}
    AND prod_pvsyst IS NOT NULL
    AND prod_reel_distributeur IS NOT NULL
    AND tarif IS NOT NULL
    AND prod_pvsyst > 0
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_evolution_prix_spot():
    """Évolution prix spot market"""
    query = """
    SELECT 
        CAST(strftime('%Y', timestamp) AS INTEGER) as annee,
        CAST(strftime('%m', timestamp) AS INTEGER) as mois,
        AVG(value) as prix_moyen,
        MIN(value) as prix_min,
        MAX(value) as prix_max
    FROM spot_market_prices
    WHERE timestamp IS NOT NULL AND value IS NOT NULL
    GROUP BY annee, mois
    ORDER BY annee, mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_tarif_edf_moyen_par_site(annee):
    """Tarif EDF moyen par site"""
    query = f"""
    SELECT 
        site,
        AVG(tarif_edf) as tarif_moyen
    FROM calculs_annuel_sites
    WHERE annee = {annee}
    AND tarif_edf IS NOT NULL
    GROUP BY site
    ORDER BY tarif_moyen DESC
    LIMIT 30
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_rentabilite_nette(annee):
    """Rentabilité nette (CA - Coûts maintenance)"""
    query = f"""
    SELECT 
        CAST(strftime('%m', cms.date) AS INTEGER) as mois,
        SUM(cms.prod_reel_distributeur * cms.tarif / 1000) as ca_k,
        COALESCE(SUM(i.facturation_intervention) / 1000, 0) as cout_maintenance_k,
        SUM(cms.prod_reel_distributeur * cms.tarif / 1000) - COALESCE(SUM(i.facturation_intervention) / 1000, 0) as rentabilite_nette_k
    FROM calculs_mensuel_sites cms
    LEFT JOIN interventions i ON cms.site = i.id_site 
        AND CAST(strftime('%m', i.date_creation_intervention) AS INTEGER) = CAST(strftime('%m', cms.date) AS INTEGER)
        AND CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = CAST(strftime('%Y', cms.date) AS INTEGER)
    WHERE CAST(strftime('%Y', cms.date) AS INTEGER) = {annee}
    AND cms.prod_reel_distributeur IS NOT NULL
    AND cms.tarif IS NOT NULL
    GROUP BY mois
    ORDER BY mois
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_analyse_marge_par_site(annee):
    """Analyse marge par site (CA - Coûts) / CA * 100"""
    query = f"""
    SELECT 
        cas.id_site as site,
        SUM(cas.prod_reel_distributeur * cas.tarif_edf / 1000) as ca_k,
        COALESCE(SUM(i.facturation_intervention) / 1000, 0) as cout_maintenance_k,
        (SUM(cas.prod_reel_distributeur * cas.tarif_edf / 1000) - COALESCE(SUM(i.facturation_intervention) / 1000, 0)) / 
        SUM(cas.prod_reel_distributeur * cas.tarif_edf / 1000) * 100 as marge_pct
    FROM calculs_annuel_sites cas
    LEFT JOIN interventions i ON cas.id_site = i.id_site 
        AND CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    WHERE cas.annee = {annee}
    AND cas.prod_reel_distributeur IS NOT NULL
    AND cas.tarif_edf IS NOT NULL
    AND cas.prod_reel_distributeur * cas.tarif_edf > 0
    GROUP BY cas.id_site
    ORDER BY marge_pct DESC
    LIMIT 30
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_par_type_intervention(annee):
    """Coûts par type d'intervention"""
    query = f"""
    SELECT 
        categorie,
        SUM(facturation_intervention) / 1000 as cout_total_k,
        COUNT(*) as nb_interventions,
        AVG(facturation_intervention) as cout_moyen
    FROM interventions
    WHERE CAST(strftime('%Y', date_creation_intervention) AS INTEGER) = {annee}
    AND categorie IS NOT NULL
    AND facturation_intervention IS NOT NULL
    GROUP BY categorie
    ORDER BY cout_total_k DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def get_cout_maintenance_par_prestataire(annee):
    """Coûts maintenance par prestataire (SPV)"""
    query = f"""
    SELECT 
        i.spv,
        SUM(i.facturation_intervention) / 1000 as cout_total_k,
        COUNT(*) as nb_interventions,
        AVG(i.facturation_intervention) as cout_moyen
    FROM interventions i
    WHERE CAST(strftime('%Y', i.date_creation_intervention) AS INTEGER) = {annee}
    AND i.spv IS NOT NULL
    AND i.facturation_intervention IS NOT NULL
    GROUP BY i.spv
    ORDER BY cout_total_k DESC
    """
    df = load_data_from_db(query)
    return df if df is not None and not df.empty else pd.DataFrame()


def show_finance_view():
    """Affiche la vue Finance complète"""
    
    st.markdown('''
    <div style="
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 3rem;
        padding: 28px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        💰 Vue Finance
    </div>
    ''', unsafe_allow_html=True)
    
    # Filtres
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 2rem;">', unsafe_allow_html=True)
    annee_finance = st.selectbox("Année", [2025, 2024, 2023], index=0, key="finance_annee")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # SECTION A: Revenus
    # ============================================
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
    ">💰 Revenus</div>
    ''', unsafe_allow_html=True)
    
    # KPI Cards Revenus
    ca_2025 = get_ca_total(annee_finance)
    ca_2024 = get_ca_total(2024)
    delta_ca = ca_2025 - ca_2024
    delta_ca_pct = (delta_ca / ca_2024 * 100) if ca_2024 != 0 else 0
    
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        # CA : augmentation = bon (normal si delta > 0)
        delta_color_ca_finance = "normal" if delta_ca > 0 else ("inverse" if delta_ca < 0 else "normal")
        st.metric(
            label="Chiffre d'Affaires Total",
            value=format_currency(ca_2025, decimals=3),
            delta=f"2024: {format_currency(ca_2024, decimals=3)} ({delta_ca_pct:+.1f}%)",
            delta_color=delta_color_ca_finance
        )
    
    with col_f2:
        ca_budget = get_manque_a_gagner(annee_finance)
        ca_budget_val = ca_budget['ca_budget_k'].iloc[0] if not ca_budget.empty else 0
        ecart_ca_budget = ((ca_2025 - ca_budget_val) / ca_budget_val * 100) if ca_budget_val != 0 else 0
        # Si CA < Budget (écart négatif), afficher en rouge
        delta_color_ca_budget = "inverse" if ecart_ca_budget < 0 else "normal"
        st.metric(
            label="CA Budget",
            value=format_currency(ca_budget_val, decimals=3),
            delta=f"Écart: {ecart_ca_budget:+.1f}%" if ca_budget_val != 0 else None,
            delta_color=delta_color_ca_budget if ca_budget_val != 0 else None
        )
    
    with col_f3:
        manque = get_manque_a_gagner(annee_finance)
        manque_val = manque['manque_a_gagner_k'].iloc[0] if not manque.empty else 0
        st.metric(
            label="Manque à Gagner",
            value=format_currency(manque_val, decimals=3),
            delta_color="inverse"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Nouveaux KPIs : Revenus OA vs Spot et Prix de vente moyen
    df_revenus_oa_spot = get_revenus_oa_vs_spot(annee_finance)
    df_prix_moyen = get_prix_vente_moyen_realise(annee_finance)
    
    if not df_revenus_oa_spot.empty:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
        col_f_oa, col_f_spot, col_f_prix = st.columns(3)
        
        with col_f_oa:
            revenus_oa = df_revenus_oa_spot['revenus_oa_me'].iloc[0] if df_revenus_oa_spot['revenus_oa_me'].iloc[0] is not None else 0
            revenus_totaux = df_revenus_oa_spot['revenus_totaux_me'].iloc[0] if df_revenus_oa_spot['revenus_totaux_me'].iloc[0] is not None else 1
            pct_oa = (revenus_oa / revenus_totaux * 100) if revenus_totaux > 0 else 0
            st.metric(
                label="Revenus OA YTD",
                value=f"{revenus_oa:.2f} M€",
                delta=f"{pct_oa:.1f}% du total"
            )
        
        with col_f_spot:
            revenus_spot = df_revenus_oa_spot['revenus_spot_me'].iloc[0] if df_revenus_oa_spot['revenus_spot_me'].iloc[0] is not None else 0
            pct_spot = (revenus_spot / revenus_totaux * 100) if revenus_totaux > 0 else 0
            st.metric(
                label="Revenus Spot YTD",
                value=f"{revenus_spot:.2f} M€",
                delta=f"{pct_spot:.1f}% du total"
            )
        
        with col_f_prix:
            prix_moyen = df_prix_moyen['prix_moyen_euro_mwh'].iloc[0] if not df_prix_moyen.empty and df_prix_moyen['prix_moyen_euro_mwh'].iloc[0] is not None else 0
            st.metric(
                label="Prix de Vente Moyen Réalisé",
                value=f"{prix_moyen:.2f} €/MWh",
                delta=None
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graphique répartition OA vs Spot
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
        col_cam, col_bar = st.columns(2)
        
        with col_cam:
            # Camembert répartition
            fig = px.pie(
                values=[revenus_oa, revenus_spot],
                names=['OA (Obligation d\'Achat)', 'Spot Market'],
                title='💳 Répartition Revenus OA vs Spot',
                color_discrete_map={'OA (Obligation d\'Achat)': '#0A84FF', 'Spot Market': '#10b981'}
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_bar:
            # Barres comparatives mensuelles
            df_revenus_mens = get_revenus_oa_vs_spot_mensuel(annee_finance)
            if not df_revenus_mens.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Revenus OA',
                    x=df_revenus_mens['mois'],
                    y=df_revenus_mens['revenus_oa_me'],
                    marker_color='#0A84FF'
                ))
                fig.add_trace(go.Bar(
                    name='Revenus Spot',
                    x=df_revenus_mens['mois'],
                    y=df_revenus_mens['revenus_spot_me'],
                    marker_color='#10b981'
                ))
                fig.update_layout(
                    title='📊 Évolution Revenus OA vs Spot (Mensuel)',
                    xaxis_title='Mois',
                    yaxis_title='Revenus (M€)',
                    barmode='group',
                    height=350
                )
                fig = apply_glassmorphism_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée disponible")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # F.3 CA Mensuel
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_ca_mens = get_ca_mensuel(annee_finance)
    if not df_ca_mens.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='CA Mensuel',
            x=df_ca_mens['mois'],
            y=df_ca_mens['ca_k'],
            marker_color='#0A84FF',
            opacity=0.8
        ))
        fig.add_trace(go.Scatter(
            name='CA Cumulé',
            x=df_ca_mens['mois'],
            y=df_ca_mens['ca_cumul'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            yaxis='y2'
        ))
        fig.update_layout(
            title='📊 CA Mensuel et Cumulé',
            xaxis_title='Mois',
            yaxis_title='CA Mensuel (k€)',
            yaxis2=dict(title='CA Cumulé (k€)', overlaying='y', side='right'),
            height=450
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # F.2 & F.5 : CA par Site et CA par SPV
    col_f2, col_f5 = st.columns(2)
    
    with col_f2:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_ca_site = get_ca_par_site(annee_finance)
        if not df_ca_site.empty:
            fig = px.bar(
                df_ca_site,
                x='ca_k',
                y='site',
                orientation='h',
                title='🏢 CA par Site (Top 20)',
                labels={'ca_k': 'CA (k€)', 'site': 'Site'},
                color='ca_k',
                color_continuous_scale='Blues'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_f5:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_ca_spv = get_ca_par_spv(annee_finance)
        if not df_ca_spv.empty:
            fig = px.bar(
                df_ca_spv.head(15),
                x='spv',
                y='ca_k',
                title='📊 CA par SPV (Top 15)',
                labels={'spv': 'SPV', 'ca_k': 'CA (k€)'},
                color='nb_sites',
                color_continuous_scale='Viridis',
                text='ca_k'
            )
            fig.update_traces(texttemplate='%{text:,.0f}k€', textposition='outside')
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, showlegend=False)
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION B: Coûts & Rentabilité
    # ============================================
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
    ">💶 Coûts & Rentabilité</div>
    ''', unsafe_allow_html=True)
    
    # F.9 Manque à Gagner Waterfall
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_manque = get_manque_a_gagner(annee_finance)
    if not df_manque.empty:
        budget = df_manque['ca_budget_k'].iloc[0]
        reel = df_manque['ca_reel_k'].iloc[0]
        perte = -df_manque['manque_a_gagner_k'].iloc[0]
        
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute", "relative", "absolute"],
            x=["Budget P50", "Pertes", "CA Réel"],
            textposition="outside",
            text=[format_count(int(budget)), format_count(int(abs(perte))), format_count(int(reel))],
            y=[budget, perte, reel],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig.update_layout(
            title="💧 Manque à Gagner (Waterfall)",
            yaxis_title="Montant (k€)",
            height=400
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # F.7 & F.8 : Coût/Production et Coût/kWc
    col_f7, col_f8 = st.columns(2)
    
    with col_f7:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_prod = get_cout_maintenance_par_production(annee_finance)
        if not df_cout_prod.empty:
            fig = px.bar(
                df_cout_prod,
                x='mois',
                y='cout_par_mwh',
                title='⚡ Coût Maintenance / Production (€/MWh)',
                labels={'mois': 'Mois', 'cout_par_mwh': '€/MWh'},
                color='cout_par_mwh',
                color_continuous_scale='Reds'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_f8:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_kwc = get_cout_maintenance_par_kwc(annee_finance)
        if not df_cout_kwc.empty:
            fig = px.bar(
                df_cout_kwc.head(15),
                x='cout_par_kwc',
                y='nom_site',
                orientation='h',
                title='⚡ Coût Maintenance / kWc (Top 15)',
                labels={'cout_par_kwc': '€/kWc', 'nom_site': 'Site'},
                color='cout_par_kwc',
                color_continuous_scale='Oranges'
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # F.25 Analyse Marge par Site
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    df_marge = get_analyse_marge_par_site(annee_finance)
    if not df_marge.empty:
        fig = px.bar(
            df_marge.head(20),
            x='marge_pct',
            y='site',
            orientation='h',
            title='📊 Marge par Site (Top 20)',
            labels={'marge_pct': 'Marge (%)', 'site': 'Site'},
            color='marge_pct',
            color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
            color_continuous_midpoint=50
        )
        fig = apply_glassmorphism_theme(fig)
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # F.11 Rentabilité Nette
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    df_renta = get_rentabilite_nette(annee_finance)
    if not df_renta.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            name='CA',
            x=df_renta['mois'],
            y=df_renta['ca_k'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3)
        ))
        fig.add_trace(go.Scatter(
            name='Coûts Maintenance',
            x=df_renta['mois'],
            y=df_renta['cout_maintenance_k'],
            mode='lines+markers',
            line=dict(color='#ef4444', width=3)
        ))
        fig.add_trace(go.Scatter(
            name='Rentabilité Nette',
            x=df_renta['mois'],
            y=df_renta['rentabilite_nette_k'],
            mode='lines+markers',
            line=dict(color='#0A84FF', width=3, dash='dash')
        ))
        fig.update_layout(
            title='📈 Rentabilité Nette Mensuelle',
            xaxis_title='Mois',
            yaxis_title='Montant (k€)',
            height=400
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION C: Budget vs Réalisé
    # ============================================
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
    ">📊 Budget vs Réalisé</div>
    ''', unsafe_allow_html=True)
    
    # F.14 Budget Production vs Réalisé
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); margin-bottom: 1rem;">', unsafe_allow_html=True)
    df_budget = get_budget_production_vs_realise(annee_finance)
    if not df_budget.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Budget',
            x=df_budget['mois'],
            y=df_budget['ca_budget_k'],
            marker_color='#1f77b4',
            opacity=0.7
        ))
        fig.add_trace(go.Bar(
            name='Réalisé',
            x=df_budget['mois'],
            y=df_budget['ca_reel_k'],
            marker_color='#87ceeb',
            opacity=0.9
        ))
        fig.update_layout(
            title='📊 Budget Production vs Réalisé',
            xaxis_title='Mois',
            yaxis_title='CA (k€)',
            barmode='group',
            height=450
        )
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # F.17 Écart Budget Production
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    if not df_budget.empty:
        fig = px.bar(
            df_budget,
            x='mois',
            y='ecart_pct',
            title='📉 Écart Budget Production (%)',
            labels={'mois': 'Mois', 'ecart_pct': 'Écart (%)'},
            color='ecart_pct',
            color_continuous_scale=['#ef4444', '#10b981'],
            color_continuous_midpoint=0
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig = apply_glassmorphism_theme(fig)
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION D: Prix & Marché
    # ============================================
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
    ">📈 Prix & Marché</div>
    ''', unsafe_allow_html=True)
    
    col_f19, col_f22 = st.columns(2)
    
    with col_f19:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_spot = get_evolution_prix_spot()
        if not df_spot.empty:
            # Filtrer pour l'année sélectionnée
            df_spot_annee = df_spot[df_spot['annee'] == annee_finance]
            if not df_spot_annee.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    name='Prix Moyen',
                    x=df_spot_annee['mois'],
                    y=df_spot_annee['prix_moyen'],
                    mode='lines+markers',
                    line=dict(color='#0A84FF', width=3)
                ))
                fig.add_trace(go.Scatter(
                    name='Prix Min',
                    x=df_spot_annee['mois'],
                    y=df_spot_annee['prix_min'],
                    mode='lines',
                    line=dict(color='#10b981', width=1, dash='dot'),
                    opacity=0.5
                ))
                fig.add_trace(go.Scatter(
                    name='Prix Max',
                    x=df_spot_annee['mois'],
                    y=df_spot_annee['prix_max'],
                    mode='lines',
                    line=dict(color='#ef4444', width=1, dash='dot'),
                    opacity=0.5,
                    fill='tonexty',
                    fillcolor='rgba(239, 68, 68, 0.1)'
                ))
                fig.update_layout(
                    title='📈 Évolution Prix Spot Market',
                    xaxis_title='Mois',
                    yaxis_title='Prix (€/MWh)',
                    height=400
                )
                fig = apply_glassmorphism_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Aucune donnée spot market pour {annee_finance}")
        else:
            st.info("Aucune donnée spot market disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_f22:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_tarif = get_tarif_edf_moyen_par_site(annee_finance)
        if not df_tarif.empty:
            fig = px.bar(
                df_tarif.head(20),
                x='site',
                y='tarif_moyen',
                title='💶 Tarif EDF Moyen par Site (Top 20)',
                labels={'site': 'Site', 'tarif_moyen': 'Tarif (€/MWh)'},
                color='tarif_moyen',
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, showlegend=False)
            fig = apply_glassmorphism_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION E: Analyses Avancées
    # ============================================
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
    ">🔍 Analyses Avancées</div>
    ''', unsafe_allow_html=True)
    
    # F.23 & F.24 : Coûts par Type et par Prestataire
    col_f23, col_f24 = st.columns(2)
    
    with col_f23:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_type = get_cout_par_type_intervention(annee_finance)
        if not df_cout_type.empty:
            fig = px.pie(
                df_cout_type,
                values='cout_total_k',
                names='categorie',
                title='💳 Répartition Coûts par Type d\'Intervention',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig = apply_glassmorphism_theme(fig)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_f24:
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        df_cout_presta = get_cout_maintenance_par_prestataire(annee_finance)
        if not df_cout_presta.empty:
            st.markdown('<h4 style="color: #1f2937; margin-bottom: 16px;">Coûts par Prestataire</h4>', unsafe_allow_html=True)
            st.dataframe(
                df_cout_presta.head(15),
                column_config={
                    "spv": "Prestataire",
                    "cout_total_k": st.column_config.NumberColumn("Coût Total (k€)", format="%.0f"),
                    "nb_interventions": "Nb Interv.",
                    "cout_moyen": st.column_config.NumberColumn("Coût Moyen (€)", format="%.0f")
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.info("Aucune donnée disponible")
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# INTERFACE PRINCIPALE
# ============================================

def main():
    # ============================================
    # HEADER : Date MAJ, Sites, Puissance + Bouton Actualiser
    # ============================================
    date_maj, nb_sites, puissance_totale = get_header_stats()
    
    # Formatter la date
    try:
        date_obj = datetime.strptime(date_maj, "%Y-%m-%d %H:%M:%S")
        date_formatted = date_obj.strftime("%d/%m/%Y")
    except:
        date_formatted = date_maj
    
    # Formatter la puissance totale
    puissance_totale_formatted = format_power_capacity(puissance_totale, decimals=1)
    
    # Header avec glassmorphism
    col_left, col_right = st.columns([3, 0.5])
    
    with col_left:
        st.markdown(f'''
        <div style="
            padding: 16px 24px;
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            display: flex;
            gap: 32px;
            align-items: center;
            font-size: 0.95rem;
        ">
            <div>📅 <strong>Dernière mise à jour:</strong> <span style="color: #10b981; font-weight: 600;">{date_formatted}</span></div>
            <div>📊 <strong>Sites:</strong> <span style="color: #0A84FF; font-weight: 600;">{format_count(nb_sites)}</span></div>
            <div>⚡ <strong>Puissance Sites Totale:</strong> <span style="color: #f59e0b; font-weight: 600;">{puissance_totale_formatted}</span></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_right:
        # Bouton Actualiser avec style moderne glassmorphism
        if st.button("🔄 Actualiser", use_container_width=False):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # NAVIGATION : Dashboard, Performance, Maintenance, Sites, Finance
    # ============================================
    
    # Initialiser session state
    if 'vue_active' not in st.session_state:
        st.session_state.vue_active = 'dashboard'
    
    # Navigation avec boutons
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    
    with nav_col1:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.vue_active == 'dashboard' else "secondary"):
            st.session_state.vue_active = 'dashboard'
            st.rerun()
    
    with nav_col2:
        if st.button("📈 Performance", use_container_width=True, type="primary" if st.session_state.vue_active == 'performance' else "secondary"):
            st.session_state.vue_active = 'performance'
            st.rerun()
    
    with nav_col3:
        if st.button("🔧 Maintenance", use_container_width=True, type="primary" if st.session_state.vue_active == 'maintenance' else "secondary"):
            st.session_state.vue_active = 'maintenance'
            st.rerun()
    
    with nav_col4:
        if st.button("🏢 Sites", use_container_width=True, type="primary" if st.session_state.vue_active == 'sites' else "secondary"):
            st.session_state.vue_active = 'sites'
            st.rerun()
    
    with nav_col5:
        if st.button("💰 Finance", use_container_width=True, type="primary" if st.session_state.vue_active == 'finance' else "secondary"):
            st.session_state.vue_active = 'finance'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Router vers la vue active
    if st.session_state.vue_active == 'performance':
        show_performance_view()
        return
    elif st.session_state.vue_active == 'maintenance':
        show_maintenance_view()
        return
    elif st.session_state.vue_active == 'sites':
        show_sites_view()
        return
    elif st.session_state.vue_active == 'finance':
        show_finance_view()
        return
    # Sinon, continuer avec la vue Dashboard
    
    # ============================================
    # TITRE : Dashboard Exploitation Apex
    # ============================================
    st.markdown('''
    <div style="
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
        padding: 28px;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        Dashboard Exploitation Apex
    </div>
    ''', unsafe_allow_html=True)
    
    # ============================================
    # KPI LIGNE 1 : Avec comparaison 2024
    # ============================================
    
    # Récupération des données 2025 et 2024
    sites_2025 = get_kpi_sites_mis_en_service(2025)
    sites_2024 = get_kpi_sites_mis_en_service(2024)
    
    prod_2025 = get_kpi_production_totale(2025)
    prod_2024 = get_kpi_production_totale(2024)
    
    puissance_2025 = get_kpi_puissance_installee(2025)
    puissance_2024 = get_kpi_puissance_installee(2024)
    
    dev_pr_2025 = get_kpi_deviation_pr(2025)
    dev_pr_2024 = get_kpi_deviation_pr(2024)
    
    # Calculs des variations
    delta_sites = sites_2025 - sites_2024
    delta_sites_pct = (delta_sites / sites_2024 * 100) if sites_2024 != 0 else 0
    
    delta_prod = prod_2025 - prod_2024
    delta_prod_pct = (delta_prod / prod_2024 * 100) if prod_2024 != 0 else 0
    
    delta_puissance = puissance_2025 - puissance_2024
    delta_puissance_pct = (delta_puissance / puissance_2024 * 100) if puissance_2024 != 0 else 0
    
    delta_dev_pr = dev_pr_2025 - dev_pr_2024
    delta_dev_pr_pct = (delta_dev_pr / abs(dev_pr_2024) * 100) if dev_pr_2024 != 0 else 0
    
    # Wrapper glassmorphism pour les KPI
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Sites : augmentation = bon (normal si delta > 0)
        delta_color_sites = "normal" if delta_sites > 0 else ("inverse" if delta_sites < 0 else "normal")
        st.metric(
            label="Sites mis en service en 2025",
            value=f"{sites_2025} sites",
            delta=f"2024: {sites_2024} ({delta_sites_pct:+.1f}%)",
            delta_color=delta_color_sites
        )
    
    with col2:
        # Production : augmentation = bon (normal si delta > 0)
        delta_color_prod = "normal" if delta_prod > 0 else ("inverse" if delta_prod < 0 else "normal")
        st.metric(
            label="Production Totale en 2025",
            value=format_energy(prod_2025, decimals=2),
            delta=f"2024: {format_energy(prod_2024, decimals=2)} ({delta_prod_pct:+.1f}%)",
            delta_color=delta_color_prod
        )
    
    with col3:
        # Puissance : augmentation = bon (normal si delta > 0)
        delta_color_puissance = "normal" if delta_puissance > 0 else ("inverse" if delta_puissance < 0 else "normal")
        st.metric(
            label="Puissance Installée en 2025",
            value=f"{puissance_2025:.1f} MWc",
            delta=f"2024: {puissance_2024:.1f} MWc ({delta_puissance_pct:+.1f}%)",
            delta_color=delta_color_puissance
        )
    
    with col4:
        st.metric(
            label="Déviation Performance Ratio en 2025",
            value=f"{dev_pr_2025:.1f} %",
            delta=f"2024: {dev_pr_2024:.1f} ({delta_dev_pr:+.1f}%)",
            delta_color="inverse"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # KPI LIGNE 2 : KPI Additionnels
    # ============================================
    
    # Récupération données 2025 et 2024 pour comparaisons
    pr_2025 = get_kpi_pr_moyen(2025)
    pr_2024 = get_kpi_pr_moyen(2024)
    prod_budget_2025 = get_kpi_production_budget(2025)
    prod_budget_2024 = get_kpi_production_budget(2024)
    nb_interventions_2025 = get_kpi_interventions(2025)
    nb_interventions_2024 = get_kpi_interventions(2024)
    cout_maintenance_2025 = get_kpi_cout_maintenance(2025)
    cout_maintenance_2024 = get_kpi_cout_maintenance(2024)
    dispo_2025 = get_kpi_disponibilite(2025)
    ca_2025 = get_kpi_ca_total(2025)
    ca_2024 = get_kpi_ca_total(2024)
    taux_resolution_2025 = get_kpi_taux_resolution(2025)
    nb_onduleurs = get_kpi_onduleurs_total()
    puissance_onduleurs = get_kpi_puissance_onduleurs()
    
    # Nouveaux KPIs Analyse Comparative
    prevision_2025, prod_ytd_2025, nb_mois_2025 = get_prevision_fin_annee_runrate(2025)
    delta_gwh, delta_pct, prod_2025_m1_9, prod_2024_m1_9 = get_delta_production_vs_2024(2025, mois_max=9)
    taille_moyenne = get_taille_moyenne_site()
    
    # Calculs écarts
    ecart_prod = ((prod_2025 - prod_budget_2025) / prod_budget_2025 * 100) if prod_budget_2025 != 0 else 0
    delta_ca = ca_2025 - ca_2024
    delta_ca_pct = (delta_ca / ca_2024 * 100) if ca_2024 != 0 else 0
    
    # Section KPI Additionnels
    st.markdown('''
    <div style="
        padding: 16px 24px;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">📊 KPI Complémentaires</div>
    ''', unsafe_allow_html=True)
    
    # Wrapper glassmorphism pour KPI ligne 2
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    # Première ligne de KPI additionnels (3 colonnes)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # PR Moyen Global
        pr_color = "#10b981" if pr_2025 >= 80 else "#f59e0b" if pr_2025 >= 70 else "#ef4444"
        delta_pr = pr_2025 - pr_2024
        # Si PR 2025 < PR 2024 (dégradation), afficher en rouge
        delta_color_pr = "inverse" if delta_pr < 0 else "normal"
        st.metric(
            label="Performance Ratio Moyen",
            value=f"{pr_2025:.1f} %",
            delta=f"2024: {pr_2024:.1f} ({delta_pr:+.1f}%)",
            delta_color=delta_color_pr
        )
    
    with col2:
        # Production vs Budget
        # Si production < budget (écart négatif), afficher en rouge
        delta_color_budget = "inverse" if ecart_prod < 0 else "normal"
        st.metric(
            label="Production vs Budget",
            value=format_energy(prod_2025, decimals=2),
            delta=f"Budget: {format_energy(prod_budget_2025, decimals=2)} ({ecart_prod:+.1f}%)",
            delta_color=delta_color_budget
        )
    
    with col3:
        # Disponibilité
        dispo_color = "#10b981" if dispo_2025 >= 98 else "#f59e0b" if dispo_2025 >= 95 else "#ef4444"
        st.metric(
            label="Disponibilité Contractuelle",
            value=f"{dispo_2025:.1f} %",
            delta="Target: ≥98%" if dispo_2025 >= 98 else None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Deuxième ligne de KPI additionnels (3 colonnes)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Interventions
        delta_inter = nb_interventions_2025 - nb_interventions_2024
        delta_inter_pct = (delta_inter / nb_interventions_2024 * 100) if nb_interventions_2024 != 0 else 0
        # Si interventions augmentent (mauvais), afficher en rouge
        delta_color_inter = "inverse" if delta_inter > 0 else "normal"
        st.metric(
            label="Interventions Total 2025",
            value=format_count(nb_interventions_2025),
            delta=f"2024: {format_count(nb_interventions_2024)} ({delta_inter_pct:+.1f}%)",
            delta_color=delta_color_inter
        )
    
    with col5:
        # Coût Maintenance
        delta_cout = cout_maintenance_2025 - cout_maintenance_2024
        delta_cout_pct = (delta_cout / cout_maintenance_2024 * 100) if cout_maintenance_2024 != 0 else 0
        # Si coûts augmentent (mauvais), afficher en rouge
        delta_color_cout = "inverse" if delta_cout > 0 else "normal"
        st.metric(
            label="Coût Maintenance 2025",
            value=format_currency(cout_maintenance_2025, decimals=3),
            delta=f"2024: {format_currency(cout_maintenance_2024, decimals=3)} ({delta_cout_pct:+.1f}%)",
            delta_color=delta_color_cout
        )
    
    with col6:
        # CA Total
        # Si CA diminue (mauvais), afficher en rouge
        delta_color_ca = "inverse" if delta_ca < 0 else "normal"
        st.metric(
            label="Chiffre d'Affaires 2025",
            value=format_currency(ca_2025, decimals=3),
            delta=f"2024: {format_currency(ca_2024, decimals=3)} ({delta_ca_pct:+.1f}%)",
            delta_color=delta_color_ca
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Troisième ligne de KPI additionnels (3 colonnes)
    col7, col8, col9 = st.columns(3)
    
    with col7:
        # Taux Résolution
        resolution_color = "#10b981" if taux_resolution_2025 >= 95 else "#f59e0b" if taux_resolution_2025 >= 90 else "#ef4444"
        st.metric(
            label="Taux Résolution Interventions",
            value=f"{taux_resolution_2025:.1f} %",
            delta="Target: ≥95%" if taux_resolution_2025 >= 95 else None
        )
    
    with col8:
        # Nombre Onduleurs
        st.metric(
            label="Total Onduleurs",
            value=format_count(nb_onduleurs),
            delta=None
        )
    
    with col9:
        # Bénéfices (CA vente électricité - coûts interventions)
        benefices_2025 = ca_2025 - cout_maintenance_2025
        benefices_2024 = ca_2024 - cout_maintenance_2024
        delta_benefices = benefices_2025 - benefices_2024
        delta_benefices_pct = (delta_benefices / benefices_2024 * 100) if benefices_2024 != 0 else 0
        # Si bénéfices diminuent (mauvais), afficher en rouge
        delta_color_benefices = "inverse" if delta_benefices < 0 else "normal"
        st.metric(
            label="Bénéfices (CA vente électricité - coûts interventions) 2025",
            value=format_currency(benefices_2025, decimals=3),
            delta=f"2024: {format_currency(benefices_2024, decimals=3)} ({delta_benefices_pct:+.1f}%)",
            delta_color=delta_color_benefices
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quatrième ligne de KPI additionnels (nouveaux KPIs Analyse Comparative)
    col10, col11, col12 = st.columns(3)
    
    with col10:
        # Prévision fin d'année - run-rate
        progress_pct = (prod_ytd_2025 / prevision_2025 * 100) if prevision_2025 > 0 else 0
        st.metric(
            label="Prévision Fin d'Année (Run-Rate)",
            value=format_energy(prevision_2025, decimals=2),
            delta=f"YTD: {format_energy(prod_ytd_2025, decimals=2)} ({nb_mois_2025} mois)"
        )
        # Barre de progression
        st.progress(progress_pct / 100)
        st.caption(f"Progression: {progress_pct:.1f}%")
    
    with col11:
        # Δ Production vs 2024 (Jan-Sep)
        # Si delta < 0 (production < 2024), afficher en rouge
        delta_color_delta_prod = "inverse" if delta_pct < 0 else "normal"
        st.metric(
            label="Δ Production vs 2024 (Jan-Sep)",
            value=f"{delta_pct:+.1f}%",
            delta=f"{format_energy(delta_gwh, decimals=2)} ({format_energy(prod_2025_m1_9, decimals=2)} vs {format_energy(prod_2024_m1_9, decimals=2)})",
            delta_color=delta_color_delta_prod
        )
    
    with col12:
        # Taille moyenne d'un site (en kWc)
        st.metric(
            label="Taille Moyenne d'un Site",
            value=format_power_capacity(taille_moyenne, decimals=0),
            delta=None
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # GRAPHIQUES SYNTHÈSE
    # ============================================
    
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
    ">📈 Graphiques Synthèse</div>
    ''', unsafe_allow_html=True)
    
    # Graphique Évolution Production Annuelle - Pleine largeur
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    data_mensuelle = get_production_irradiation_mensuelle_cumulee()
    
    if data_mensuelle:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Créer la figure avec deux sous-graphiques (production en haut, déviation PR en bas)
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],  # Production 70%, Déviation PR 30%
            vertical_spacing=0.05,
            subplot_titles=('', ''),
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        
        mois_noms = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        couleurs_prod = {'2023': '#F59E0B', '2024': '#10B981', '2025': '#0A84FF'}  # Orange 2023, Vert 2024, Bleu 2025
        couleurs_dev_pr = {'2023': '#F59E0B', '2024': '#10B981', '2025': '#0A84FF'}  # Mêmes couleurs que les courbes
        
        # Dernier mois avec données réelles pour 2025
        dernier_mois_2025 = None
        if 2025 in data_mensuelle:
            df_2025 = data_mensuelle[2025]
            dernier_mois_2025 = df_2025[df_2025['prod_reel_mwh'] > 0]['mois'].max()
            if pd.isna(dernier_mois_2025):
                dernier_mois_2025 = None
        
        # Ajouter les lignes de production cumulée pour chaque année
        for annee in [2023, 2024, 2025]:
            if annee in data_mensuelle:
                df = data_mensuelle[annee]
                
                # Déterminer si les mois Nov-Déc sont simulés (pour 2025)
                has_simulated = (annee == 2025 and dernier_mois_2025 is not None and dernier_mois_2025 < 12)
                
                # Séparer les données réelles et simulées pour 2025
                if has_simulated:
                    df_real = df[df['mois'] <= dernier_mois_2025].copy()
                    df_sim = df[df['mois'] > dernier_mois_2025].copy()
                    
                    # Production cumulée réelle - données réelles (en haut, row=1)
                    fig.add_trace(go.Scatter(
                        x=df_real['mois'],
                        y=df_real['prod_cumule_mwh'] / 1000,  # Convertir en GWh
                        mode='lines+markers',
                        name=f'Production {annee}',
                        line=dict(color=couleurs_prod[str(annee)], width=3, dash='solid'),
                        marker=dict(size=8, color=couleurs_prod[str(annee)]),
                        hovertemplate=f'<b>Production {annee}</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>'
                    ), row=1, col=1)
                    
                    # Production PVsyst cumulée - données réelles (pointillés larges)
                    fig.add_trace(go.Scatter(
                        x=df_real['mois'],
                        y=df_real['prod_pvsyst_cumule_mwh'] / 1000,
                        mode='lines',
                        name=f'Production PVsyst {annee}',
                        line=dict(color=couleurs_prod[str(annee)], width=2, dash='dash'),
                        hovertemplate=f'<b>Production PVsyst {annee}</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>'
                    ), row=1, col=1)
                    
                    # Production PVsyst cumulée - données simulées (pointillés larges)
                    if not df_sim.empty:
                        fig.add_trace(go.Scatter(
                            x=df_sim['mois'],
                            y=df_sim['prod_pvsyst_cumule_mwh'] / 1000,
                            mode='lines',
                            name=f'Production PVsyst {annee} (estimée)',
                            line=dict(color=couleurs_prod[str(annee)], width=2, dash='dash'),
                            hovertemplate=f'<b>Production PVsyst {annee} (estimée)</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>',
                            showlegend=False
                        ), row=1, col=1)
                    
                    # Production cumulée - données simulées (pointillée)
                    if not df_sim.empty:
                        fig.add_trace(go.Scatter(
                            x=df_sim['mois'],
                            y=df_sim['prod_cumule_mwh'] / 1000,
                            mode='lines+markers',
                            name=f'Production {annee} (estimée)',
                            line=dict(color=couleurs_prod[str(annee)], width=3, dash='dash'),
                            marker=dict(size=8, color=couleurs_prod[str(annee)], symbol='diamond'),
                            hovertemplate=f'<b>Production {annee} (estimée)</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>',
                            showlegend=False
                        ), row=1, col=1)
                    
                else:
                    # Pour 2023 et 2024, afficher toutes les données normalement (en haut, row=1)
                    # Production cumulée réelle
                    fig.add_trace(go.Scatter(
                        x=df['mois'],
                        y=df['prod_cumule_mwh'] / 1000,  # Convertir en GWh
                        mode='lines+markers',
                        name=f'Production {annee}',
                        line=dict(color=couleurs_prod[str(annee)], width=3, dash='solid'),
                        marker=dict(size=8, color=couleurs_prod[str(annee)]),
                        hovertemplate=f'<b>Production {annee}</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>'
                    ), row=1, col=1)
                    
                    # Production PVsyst cumulée (pointillés larges)
                    fig.add_trace(go.Scatter(
                        x=df['mois'],
                        y=df['prod_pvsyst_cumule_mwh'] / 1000,
                        mode='lines',
                        name=f'Production PVsyst {annee}',
                        line=dict(color=couleurs_prod[str(annee)], width=2, dash='dash'),
                        hovertemplate=f'<b>Production PVsyst {annee}</b><br>Mois: %{{x}}<br>Cumul: %{{y:.2f}} GWh<extra></extra>'
                    ), row=1, col=1)
        
        # Ajouter les barres de déviation PR mensuelle pour chaque année
        for annee in [2023, 2024, 2025]:
            if annee in data_mensuelle:
                df = data_mensuelle[annee]
                
                # Déterminer si les mois Nov-Déc sont simulés (pour 2025)
                has_simulated = (annee == 2025 and dernier_mois_2025 is not None and dernier_mois_2025 < 12)
                
                if has_simulated:
                    df_real = df[df['mois'] <= dernier_mois_2025].copy()
                    df_sim = df[df['mois'] > dernier_mois_2025].copy()
                    
                    # Déviation PR - données réelles (barres en bas, row=2)
                    fig.add_trace(go.Bar(
                        x=df_real['mois'],
                        y=df_real['dev_pr_moyenne'],
                        name=f'Déviation PR {annee}',
                        marker=dict(
                            color=couleurs_dev_pr[str(annee)],
                            opacity=0.6,
                            line=dict(width=0.5, color=couleurs_dev_pr[str(annee)])
                        ),
                        hovertemplate=f'<b>Déviation PR {annee}</b><br>Mois: %{{x}}<br>Déviation: %{{y:.2f}}%<extra></extra>',
                        width=0.7
                    ), row=2, col=1)
                    
                    # Déviation PR - données simulées (barres pointillées)
                    if not df_sim.empty:
                        fig.add_trace(go.Bar(
                            x=df_sim['mois'],
                            y=df_sim['dev_pr_moyenne'],
                            name=f'Déviation PR {annee} (estimée)',
                            marker=dict(
                                color=couleurs_dev_pr[str(annee)],
                                opacity=0.4,
                                line=dict(width=0.5, color=couleurs_dev_pr[str(annee)])
                            ),
                            hovertemplate=f'<b>Déviation PR {annee} (estimée)</b><br>Mois: %{{x}}<br>Déviation: %{{y:.2f}}%<extra></extra>',
                            showlegend=False,
                            width=0.7
                        ), row=2, col=1)
                else:
                    # Pour 2023 et 2024, afficher toutes les données normalement (barres en bas, row=2)
                    fig.add_trace(go.Bar(
                        x=df['mois'],
                        y=df['dev_pr_moyenne'],
                        name=f'Déviation PR {annee}',
                        marker=dict(
                            color=couleurs_dev_pr[str(annee)],
                            opacity=0.6,
                            line=dict(width=0.5, color=couleurs_dev_pr[str(annee)])
                        ),
                        hovertemplate=f'<b>Déviation PR {annee}</b><br>Mois: %{{x}}<br>Déviation: %{{y:.2f}}%<extra></extra>',
                        width=0.7
                    ), row=2, col=1)
        
        # Configuration des axes et mise en page
        fig.update_layout(
            title='📈 Évolution Production Cumulée et Déviation PR Mensuelle',
            height=700,  # Augmenter la hauteur pour meilleure lisibilité
            hovermode='x unified',
            barmode='group',  # Grouper les barres côte à côte
            showlegend=True
        )
        
        # Configuration de l'axe X pour le graphique supérieur (production)
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=mois_noms,
            title='',
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            row=1, col=1,
            showticklabels=True
        )
        
        # Configuration de l'axe X pour le graphique inférieur (déviation PR)
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=mois_noms,
            title='Mois',
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            row=2, col=1,
            showticklabels=True
        )
        
        # Configuration de l'axe Y pour la production (en haut)
        fig.update_yaxes(
            title='Production Cumulée (GWh)',
            side='left',
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            row=1, col=1
        )
        
        # Configuration de l'axe Y pour la déviation PR (en bas)
        fig.update_yaxes(
            title='Déviation PR Mensuelle (%)',
            side='left',
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            row=2, col=1
        )
        
        # Ajouter une ligne horizontale de séparation
        fig.add_hline(
            y=0,  # Ligne à y=0 pour le graphique du bas
            line_dash="dash",
            line_color="gray",
            opacity=0.5,
            row=2, col=1
        )
        
        # Mettre à jour la mise en page générale
        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            ),
            margin=dict(l=50, r=80, t=60, b=50)
        )
        
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Deuxième ligne de graphiques - colonnes égales pour alignement parfait
    col_g3, col_g4 = st.columns([1, 1], gap="medium")
    
    # Hauteur uniforme pour tous les tableaux
    TABLE_HEIGHT = 500
    
    with col_g3:
        # D.G.3 Top Sites (3 types de comparaisons)
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        
        # Titre "Top Sites" aligné à gauche
        st.markdown('<h4 style="color: #1f2937; margin-bottom: 0; margin-top: 0;">🏆 Top Sites</h4>', unsafe_allow_html=True)
        
        # Onglets pour les 3 types de comparaisons (directement sous le titre, aligné à gauche)
        tab_prod, tab_eff, tab_rev = st.tabs(["📊 Production", "⚡ Efficacité", "💰 Revenus"])
        
        with tab_prod:
            df_top_prod = get_top_sites_production_mwh(2025, limit=50)
            if not df_top_prod.empty:
                st.dataframe(
                    df_top_prod,
                    column_config={
                        "site": st.column_config.TextColumn("Site", width="medium"),
                        "prod_mwh": st.column_config.NumberColumn("Production (MWh)", format="%.0f", width="large")
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=TABLE_HEIGHT
                )
            else:
                st.info("Aucune donnée disponible")
        
        with tab_eff:
            df_top_eff = get_top_sites_efficacite(2025, limit=50)
            if not df_top_eff.empty:
                # Convertir MWc en kWc (multiplier par 1000)
                df_top_eff['puissance_kwc'] = df_top_eff['puissance_mw'] * 1000
                # Recalculer l'efficacité en MWh/kWc
                df_top_eff['efficacite_mwh_par_kwc'] = df_top_eff['prod_mwh'] / df_top_eff['puissance_kwc']
                st.dataframe(
                    df_top_eff[['site', 'prod_mwh', 'puissance_kwc', 'efficacite_mwh_par_kwc']],
                    column_config={
                        "site": st.column_config.TextColumn("Site", width="medium"),
                        "prod_mwh": st.column_config.NumberColumn("Production (MWh)", format="%.0f", width="large"),
                        "puissance_kwc": st.column_config.NumberColumn("Puissance (kWc)", format="%.2f", width="medium"),
                        "efficacite_mwh_par_kwc": st.column_config.NumberColumn("Efficacité (MWh/kWc)", format="%.4f", width="medium")
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=TABLE_HEIGHT
                )
            else:
                st.info("Aucune donnée disponible")
        
        with tab_rev:
            df_top_rev = get_top_sites_revenus(2025, limit=50)
            if not df_top_rev.empty:
                # Convertir les revenus en k€ pour l'affichage
                df_top_rev['revenus_keuro'] = df_top_rev['revenus_euros'] / 1000
                st.dataframe(
                    df_top_rev[['site', 'revenus_keuro', 'prod_mwh']],
                    column_config={
                        "site": st.column_config.TextColumn("Site", width="medium"),
                        "revenus_keuro": st.column_config.NumberColumn("Revenus (k€)", format="%.2f", width="large"),
                        "prod_mwh": st.column_config.NumberColumn("Production (MWh)", format="%.0f", width="large")
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=TABLE_HEIGHT
                )
            else:
                st.info("Aucune donnée disponible")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Fermeture div principal
    
    with col_g4:
        # D.G.4 Sites Sous-Performants
        st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
        
        # Calcul des sites sous-performants
        nb_alertes = get_alertes_sites_sous_performants(2025)
        df_sous_perf = get_details_sites_sous_performants(2025)
        
        # Titre "Sites Sous-Performants" aligné à gauche (même structure que Top Sites)
        st.markdown('<h4 style="color: #1f2937; margin-bottom: 0; margin-top: 0;">⚠️ Sites Sous-Performants</h4>', unsafe_allow_html=True)
        
        # Espaceur invisible pour aligner les tableaux (compense la hauteur des onglets à gauche)
        # Les onglets Streamlit prennent environ 40-45px de hauteur
        st.markdown('<div style="height: 45px; margin-bottom: 0;"></div>', unsafe_allow_html=True)
        
        # Tableau détaillé des sites sous-performants
        if not df_sous_perf.empty:
            # Hauteur uniforme avec les autres tableaux (même que TABLE_HEIGHT = 500)
            st.dataframe(
                df_sous_perf,
                column_config={
                    "site": st.column_config.TextColumn("Site", width="small"),
                    "pr_reel": st.column_config.NumberColumn("PR Réel (%)", format="%.2f", width="small"),
                    "dev_pr": st.column_config.NumberColumn("Dév. PR (%)", format="%.2f", width="small"),
                    "pr_budget": st.column_config.NumberColumn("PR Budget (%)", format="%.2f", width="small"),
                    "prod_gwh": st.column_config.NumberColumn("Production (GWh)", format="%.2f", width="small"),
                    "puissance_mw": st.column_config.NumberColumn("Puissance (MWc)", format="%.2f", width="small"),
                    "raison": st.column_config.TextColumn("Raison", width="medium")
                },
                hide_index=True,
                use_container_width=True,
                height=TABLE_HEIGHT
            )
        elif nb_alertes == 0:
            st.markdown(f'''
            <div style="
                padding: 16px;
                background: rgba(16, 185, 129, 0.1);
                border: 2px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
                margin-bottom: 16px;
            ">
                <h4 style="color: #10b981; margin: 0;">✅ Tous les sites performants</h4>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphique combiné : Interventions et Coût Maintenance Mensuels 2025 vs 2024
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    # Récupération des données pour 2024 et 2025
    df_interv_mois_2025 = get_interventions_mensuelles(2025)
    df_interv_mois_2024 = get_interventions_mensuelles(2024)
    df_cout_mois_2025 = get_cout_maintenance_mensuel(2025)
    df_cout_mois_2024 = get_cout_maintenance_mensuel(2024)
    
    # Création d'un DataFrame complet avec tous les mois (1-12) pour assurer l'affichage complet
    mois_complets = pd.DataFrame({'mois': range(1, 13)})
    
    # Fusion des données 2024 et 2025 pour les interventions
    df_interv_2024_merged = mois_complets.merge(
        df_interv_mois_2024 if not df_interv_mois_2024.empty else pd.DataFrame({'mois': [], 'nb_interventions': []}),
        on='mois', how='left'
    ).fillna(0)
    
    df_interv_2025_merged = mois_complets.merge(
        df_interv_mois_2025 if not df_interv_mois_2025.empty else pd.DataFrame({'mois': [], 'nb_interventions': []}),
        on='mois', how='left'
    ).fillna(0)
    
    # Fusion des données 2024 et 2025 pour les coûts
    df_cout_2024_merged = mois_complets.merge(
        df_cout_mois_2024 if not df_cout_mois_2024.empty else pd.DataFrame({'mois': [], 'cout_k': []}),
        on='mois', how='left'
    ).fillna(0)
    
    df_cout_2025_merged = mois_complets.merge(
        df_cout_mois_2025 if not df_cout_mois_2025.empty else pd.DataFrame({'mois': [], 'cout_k': []}),
        on='mois', how='left'
    ).fillna(0)
    
    # Création du graphique combiné avec deux axes Y
    if not df_interv_2024_merged.empty or not df_interv_2025_merged.empty or not df_cout_2024_merged.empty or not df_cout_2025_merged.empty:
        fig = go.Figure()
        
        # Barres pour les interventions 2024 (axe Y gauche)
        if not df_interv_2024_merged.empty:
            fig.add_trace(go.Bar(
                x=df_interv_2024_merged['mois'],
                y=df_interv_2024_merged['nb_interventions'],
                name='Interventions 2024',
                marker_color='#9CA3AF',
                yaxis='y',
                opacity=0.7,
                legendgroup='interventions'
            ))
        
        # Barres pour les interventions 2025 (axe Y gauche)
        if not df_interv_2025_merged.empty:
            fig.add_trace(go.Bar(
                x=df_interv_2025_merged['mois'],
                y=df_interv_2025_merged['nb_interventions'],
                name='Interventions 2025',
                marker_color='#0A84FF',
                yaxis='y',
                opacity=0.7,
                legendgroup='interventions'
            ))
        
        # Ligne pour les coûts 2024 (axe Y droit)
        if not df_cout_2024_merged.empty:
            fig.add_trace(go.Scatter(
                x=df_cout_2024_merged['mois'],
                y=df_cout_2024_merged['cout_k'],
                name='Coût Maintenance 2024 (k€)',
                mode='lines+markers',
                line=dict(color='#9CA3AF', width=2.5, dash='dash'),
                marker=dict(color='#9CA3AF', size=7, symbol='circle'),
                yaxis='y2',
                legendgroup='cout'
            ))
        
        # Ligne pour les coûts 2025 (axe Y droit)
        if not df_cout_2025_merged.empty:
            fig.add_trace(go.Scatter(
                x=df_cout_2025_merged['mois'],
                y=df_cout_2025_merged['cout_k'],
                name='Coût Maintenance 2025 (k€)',
                mode='lines+markers',
                line=dict(color='#f59e0b', width=3),
                marker=dict(color='#f59e0b', size=8, symbol='circle'),
                yaxis='y2',
                legendgroup='cout'
            ))
        
        # Configuration des axes
        fig.update_layout(
            title='📊 Interventions Mensuelles & Coût Maintenance 2025 vs 2024',
            barmode='group',  # Groupement des barres pour comparaison
            xaxis=dict(
                title='Mois',
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
            ),
            yaxis=dict(
                title=dict(text='Nombre d\'Interventions', font=dict(color='#0A84FF')),
                tickfont=dict(color='#0A84FF'),
                side='left'
            ),
            yaxis2=dict(
                title=dict(text='Coût Maintenance (k€)', font=dict(color='#f59e0b')),
                tickfont=dict(color='#f59e0b'),
                overlaying='y',
                side='right'
            ),
            legend=dict(
                x=1.02,
                y=0.95,
                xanchor='left',
                yanchor='top',
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='rgba(0, 0, 0, 0.15)',
                borderwidth=1,
                font=dict(size=11),
                itemwidth=30,
                traceorder='normal'
            ),
            margin=dict(r=120),
            height=400,
            hovermode='x unified'
        )
        
        # Application du thème glassmorphism
        fig = apply_glassmorphism_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # CARTES GÉOGRAPHIQUES DES SITES
    # ============================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="padding: 16px; background: rgba(255, 255, 255, 0.5); border-radius: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1f2937; margin-bottom: 24px; text-align: center;">🗺️ Localisation des Sites Photovoltaïques</h3>', unsafe_allow_html=True)
    
    # Fonction pour obtenir les sites par région avec informations complètes
    def get_sites_by_region(region_name, lat_range, lon_range):
        """Récupère les sites dans une région géographique avec détails onduleurs"""
        # Vérifier si la table onduleurs_view existe
        try:
            check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='onduleurs_view'"
            check_df = load_data_from_db(check_query)
            has_onduleurs = check_df is not None and not check_df.empty
        except:
            has_onduleurs = False
        
        if has_onduleurs:
            query = f"""
            SELECT 
                e.id_site,
                e.nom_site,
                e.latitude,
                e.longitude,
                e.puissance_nominale__kWc_,
                e.spv,
                (SELECT GROUP_CONCAT(modelname || ' (' || cnt || ')', ', ')
                 FROM (
                     SELECT modelname, COUNT(*) as cnt
                     FROM onduleurs_view o
                     WHERE o.id_site = e.id_site AND o.modelname IS NOT NULL
                     GROUP BY modelname
                 )) as modeles_et_nb
            FROM exposition e
            WHERE e.latitude IS NOT NULL 
            AND e.longitude IS NOT NULL
            AND e.latitude BETWEEN {lat_range[0]} AND {lat_range[1]}
            AND e.longitude BETWEEN {lon_range[0]} AND {lon_range[1]}
            """
        else:
            # Si pas de table onduleurs, récupérer juste les infos de base
            query = f"""
            SELECT 
                e.id_site,
                e.nom_site,
                e.latitude,
                e.longitude,
                e.puissance_nominale__kWc_,
                e.spv,
                0 as nb_modeles_distincts,
                0 as nb_onduleurs_total,
                NULL as modeles_et_nb
            FROM exposition e
            WHERE e.latitude IS NOT NULL 
            AND e.longitude IS NOT NULL
            AND e.latitude BETWEEN {lat_range[0]} AND {lat_range[1]}
            AND e.longitude BETWEEN {lon_range[0]} AND {lon_range[1]}
            """
        df = load_data_from_db(query)
        return df if df is not None and not df.empty else pd.DataFrame()
    
    # Fonction helper pour déterminer la couleur selon la puissance crête
    def get_color_by_power(puissance_kwc):
        """Retourne la couleur en fonction de la puissance crête (kWc)
        - < 100 kWc = Bleu
        - 101-300 kWc = Vert
        - 301-500 kWc = Orange
        - 501-1000 kWc = Jaune
        - > 1000 kWc = Rouge
        """
        if pd.isna(puissance_kwc) or puissance_kwc is None:
            return '#808080'  # Gris pour données manquantes
        
        puissance = float(puissance_kwc)
        if puissance < 100:
            return '#0A84FF'  # Bleu (< 100 kWc)
        elif 100 <= puissance <= 300:
            return '#10B981'  # Vert (101-300 kWc)
        elif 301 <= puissance <= 500:
            return '#F59E0B'  # Orange (301-500 kWc)
        elif 501 <= puissance <= 1000:
            return '#FBBF24'  # Jaune (501-1000 kWc)
        else:  # > 1000
            return '#EF4444'  # Rouge (> 1001 kWc)
    
    # Fonction helper pour créer le texte de hover personnalisé
    def create_hover_text(df_region):
        """Crée le texte personnalisé pour chaque point de la carte"""
        custom_texts = []
        for idx, row in df_region.iterrows():
            id_site = str(row['id_site']) if pd.notna(row['id_site']) else 'N/A'
            nom_site = str(row['nom_site']) if pd.notna(row['nom_site']) else 'N/A'
            puissance = f"{row['puissance_nominale__kWc_']:.2f}" if pd.notna(row['puissance_nominale__kWc_']) else 'N/A'
            
            # Informations sur les onduleurs
            if pd.notna(row.get('modeles_et_nb')) and str(row.get('modeles_et_nb')) != 'None' and str(row.get('modeles_et_nb')) != '':
                modeles = str(row['modeles_et_nb'])
            else:
                modeles = 'Aucun onduleur'
            
            hover_text = f"<b>{nom_site}</b><br>" + \
                        f"ID Site: {id_site}<br>" + \
                        f"Puissance crête: {puissance} kWc<br>" + \
                        f"Onduleurs: {modeles}"
            custom_texts.append(hover_text)
        return custom_texts
    
    # Fonction helper pour créer les couleurs pour chaque point
    def create_colors_by_power(df_region):
        """Crée une liste de couleurs en fonction de la puissance crête"""
        colors = []
        for idx, row in df_region.iterrows():
            puissance = row['puissance_nominale__kWc_']
            colors.append(get_color_by_power(puissance))
        return colors
    
    # Définition des régions avec leurs coordonnées (ajustées selon l'image 2)
    regions = {
        "France Métropolitaine": {
            "lat_range": [42.0, 51.5],
            "lon_range": [-5.0, 10.0],
            "center": {"lat": 46.8, "lon": 2.2},
            "zoom": 5.2
        },
        "Guadeloupe": {
            "lat_range": [15.5, 16.5],
            "lon_range": [-62.0, -61.0],
            "center": {"lat": 16.15, "lon": -61.6},
            "zoom": 8.2
        },
        "Martinique": {
            "lat_range": [14.3, 14.9],
            "lon_range": [-61.3, -60.7],
            "center": {"lat": 14.64, "lon": -61.0},
            "zoom": 8.8
        },
        "Guyane": {
            "lat_range": [2.0, 6.0],
            "lon_range": [-54.5, -51.5],
            "center": {"lat": 4.0, "lon": -53.0},
            "zoom": 5.5
        },
        "La Réunion": {
            "lat_range": [-21.5, -20.8],
            "lon_range": [55.2, 55.8],
            "center": {"lat": -21.15, "lon": 55.5},
            "zoom": 8.5
        }
    }
    
    # Disposition : France Métropolitaine à gauche, 4 autres à droite en grille 2x2
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Grande carte France Métropolitaine
        region_name = "France Métropolitaine"
        region_params = regions[region_name]
        
        df_region = get_sites_by_region(
            region_name,
            region_params["lat_range"],
            region_params["lon_range"]
        )
        
        if not df_region.empty:
            fig = go.Figure()
            
            # Préparer le texte personnalisé et les couleurs pour chaque point
            custom_texts = create_hover_text(df_region)
            colors = create_colors_by_power(df_region)
            
            fig.add_trace(go.Scattermapbox(
                lat=df_region['latitude'],
                lon=df_region['longitude'],
                mode='markers',
                marker=dict(
                    size=6,
                    color=colors,
                    opacity=0.9
                ),
                text=df_region['nom_site'],
                customdata=custom_texts,
                hovertemplate='%{customdata}<extra></extra>',
                name='Sites'
            ))
            
            fig.update_layout(
                mapbox=dict(
                    style='open-street-map',
                    center=region_params["center"],
                    zoom=region_params["zoom"],
                    bearing=0,
                    pitch=0
                ),
                margin=dict(l=0, r=0, t=50, b=0),
                height=700,
                title=dict(
                    text=f'📍 {region_name}<br><span style="font-size: 12px; color: #6b7280;">{len(df_region)} site(s)</span>',
                    font=dict(size=15, color='#1f2937'),
                    x=0.02,
                    xanchor='left',
                    y=0.98,
                    yanchor='top'
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key="map_france")
        else:
            st.info(f"Aucun site dans {region_name}")
    
    with col_right:
        # Grille 2x2 pour les 4 autres cartes
        regions_other = {k: v for k, v in regions.items() if k != "France Métropolitaine"}
        
        # Première ligne : 2 cartes
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            region_name = list(regions_other.keys())[0]
            region_params = regions_other[region_name]
            
            df_region = get_sites_by_region(
                region_name,
                region_params["lat_range"],
                region_params["lon_range"]
            )
            
            if not df_region.empty:
                fig = go.Figure()
                
                # Préparer le texte personnalisé et les couleurs pour chaque point
                custom_texts = create_hover_text(df_region)
                colors = create_colors_by_power(df_region)
                
                fig.add_trace(go.Scattermapbox(
                    lat=df_region['latitude'],
                    lon=df_region['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=colors,
                        opacity=0.9
                    ),
                    text=df_region['nom_site'],
                    customdata=custom_texts,
                    hovertemplate='%{customdata}<extra></extra>',
                    name='Sites'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=region_params["center"],
                        zoom=region_params["zoom"],
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'📍 {region_name}<br><span style="font-size: 11px; color: #6b7280;">{len(df_region)} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"map_{region_name}")
            else:
                st.info(f"Aucun site dans {region_name}")
        
        with col_r2:
            region_name = list(regions_other.keys())[1]
            region_params = regions_other[region_name]
            
            df_region = get_sites_by_region(
                region_name,
                region_params["lat_range"],
                region_params["lon_range"]
            )
            
            if not df_region.empty:
                fig = go.Figure()
                
                # Préparer le texte personnalisé et les couleurs pour chaque point
                custom_texts = create_hover_text(df_region)
                colors = create_colors_by_power(df_region)
                
                fig.add_trace(go.Scattermapbox(
                    lat=df_region['latitude'],
                    lon=df_region['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=colors,
                        opacity=0.9
                    ),
                    text=df_region['nom_site'],
                    customdata=custom_texts,
                    hovertemplate='%{customdata}<extra></extra>',
                    name='Sites'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=region_params["center"],
                        zoom=region_params["zoom"],
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'📍 {region_name}<br><span style="font-size: 11px; color: #6b7280;">{len(df_region)} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"map_{region_name}")
            else:
                st.info(f"Aucun site dans {region_name}")
        
        # Deuxième ligne : 2 cartes
        col_r3, col_r4 = st.columns(2)
        
        with col_r3:
            region_name = list(regions_other.keys())[2]
            region_params = regions_other[region_name]
            
            df_region = get_sites_by_region(
                region_name,
                region_params["lat_range"],
                region_params["lon_range"]
            )
            
            if not df_region.empty:
                fig = go.Figure()
                
                # Préparer le texte personnalisé et les couleurs pour chaque point
                custom_texts = create_hover_text(df_region)
                colors = create_colors_by_power(df_region)
                
                fig.add_trace(go.Scattermapbox(
                    lat=df_region['latitude'],
                    lon=df_region['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=colors,
                        opacity=0.9
                    ),
                    text=df_region['nom_site'],
                    customdata=custom_texts,
                    hovertemplate='%{customdata}<extra></extra>',
                    name='Sites'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=region_params["center"],
                        zoom=region_params["zoom"],
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'📍 {region_name}<br><span style="font-size: 11px; color: #6b7280;">{len(df_region)} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"map_{region_name}")
            else:
                st.info(f"Aucun site dans {region_name}")
        
        with col_r4:
            region_name = list(regions_other.keys())[3]
            region_params = regions_other[region_name]
            
            df_region = get_sites_by_region(
                region_name,
                region_params["lat_range"],
                region_params["lon_range"]
            )
            
            if not df_region.empty:
                fig = go.Figure()
                
                # Préparer le texte personnalisé et les couleurs pour chaque point
                custom_texts = create_hover_text(df_region)
                colors = create_colors_by_power(df_region)
                
                fig.add_trace(go.Scattermapbox(
                    lat=df_region['latitude'],
                    lon=df_region['longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=colors,
                        opacity=0.9
                    ),
                    text=df_region['nom_site'],
                    customdata=custom_texts,
                    hovertemplate='%{customdata}<extra></extra>',
                    name='Sites'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=region_params["center"],
                        zoom=region_params["zoom"],
                        bearing=0,
                        pitch=0
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=340,
                    title=dict(
                        text=f'📍 {region_name}<br><span style="font-size: 11px; color: #6b7280;">{len(df_region)} site(s)</span>',
                        font=dict(size=13, color='#1f2937'),
                        x=0.02,
                        xanchor='left',
                        y=0.98,
                        yanchor='top'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"map_{region_name}")
            else:
                st.info(f"Aucun site dans {region_name}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f'''
    <div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 20px;">
        ⚡ Dashboard Exploitation Apex - Généré le {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()

