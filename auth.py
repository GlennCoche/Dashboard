"""
Module d'authentification simple pour Streamlit
Utilise les secrets Streamlit Cloud pour stocker le mot de passe
"""

import streamlit as st
import hashlib


def check_password():
    """
    Vérifie le mot de passe via les secrets Streamlit ou une variable d'environnement.
    
    Utilisation :
    - Dans Streamlit Cloud : Configurez le secret DASHBOARD_PASSWORD
    - En local : Créez .streamlit/secrets.toml avec [secrets] password = "votre_mot_de_passe"
    """
    
    # Récupérer le mot de passe depuis les secrets
    # Essayer d'abord depuis st.secrets (Streamlit Cloud)
    try:
        password = st.secrets.get("DASHBOARD_PASSWORD", None)
    except:
        password = None
    
    # Si pas de secret, utiliser une variable d'environnement
    if password is None:
        import os
        password = os.environ.get("DASHBOARD_PASSWORD", None)
    
    # Si aucun mot de passe configuré, désactiver l'auth
    if password is None:
        return True  # Pas de protection si pas de mot de passe configuré
    
    # Initialiser la session
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    # Si déjà authentifié, permettre l'accès
    if st.session_state["password_correct"]:
        return True
    
    # Interface de connexion
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #d4e3fc 0%, #e0ebfa 20%, #ecf2fb 40%, #f5f8fc 60%, #fafcfe 80%, #ffffff 100%);
    }
    .login-box {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container"><div class="login-box">', unsafe_allow_html=True)
    
    st.markdown("# 🔒 Accès Protégé")
    st.markdown("---")
    st.markdown("Veuillez entrer le mot de passe pour accéder au dashboard.")
    
    password_input = st.text_input("Mot de passe", type="password", key="password_input")
    
    if st.button("🔓 Se connecter", type="primary", use_container_width=True):
        # Comparaison simple (en production, utilisez hashlib)
        if password_input == password:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return False


def logout_button():
    """Affiche un bouton de déconnexion dans la sidebar"""
    with st.sidebar:
        st.markdown("---")
        if st.button("🔒 Déconnexion", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()

