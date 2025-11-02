"""
Script complet pour créer différentes bases de données à partir d'Excel
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path

EXCEL_FILE = "All Stats Energysoft.xlsx"

def create_sqlite(excel_path, db_path="energysoft_stats.db"):
    """Crée une base SQLite depuis Excel - RECOMMANDÉ pour débuter"""
    print("🗄️  Création de la base SQLite...")
    
    conn = sqlite3.connect(db_path)
    excel_file = pd.ExcelFile(excel_path)
    
    tables_created = []
    
    for sheet_name in excel_file.sheet_names:
        print(f"   📥 Importation: {sheet_name}...")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Nettoyer le nom de table
        table_name = clean_table_name(sheet_name)
        
        # Convertir les types de données intelligemment
        df = optimize_dataframe_types(df)
        
        # Créer la table (sans method='multi' pour éviter l'erreur "too many SQL variables")
        try:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        except Exception as e:
            # Si erreur, essayer par chunks
            print(f"      ⚠️  Importation en chunks...")
            chunk_size = 1000
            for i in range(0, len(df), chunk_size):
                chunk = df.iloc[i:i+chunk_size]
                if_exists = 'replace' if i == 0 else 'append'
                chunk.to_sql(table_name, conn, if_exists=if_exists, index=False)
        
        tables_created.append((table_name, len(df)))
        print(f"      ✅ {table_name}: {len(df)} lignes")
    
    conn.close()
    
    print(f"\n✅ Base SQLite créée: {db_path}")
    print(f"   Tables créées: {len(tables_created)}")
    
    return db_path

def clean_table_name(name):
    """Nettoie le nom pour être valide SQL"""
    name = name.replace(' ', '_').replace('-', '_').lower()
    name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
    # S'assurer que ça commence par une lettre
    if name and name[0].isdigit():
        name = 'table_' + name
    return name

def optimize_dataframe_types(df):
    """Optimise les types de données du DataFrame"""
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    
    for col in df.columns:
        # Convertir les colonnes numériques
        if df[col].dtype == 'object':
            try:
                # Essayer de convertir en numérique
                pd.to_numeric(df[col], errors='raise')
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
        
        # Convertir les dates (avec format explicite pour éviter les warnings)
        if df[col].dtype == 'object':
            try:
                # Essayer plusieurs formats de date courants
                df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=False)
            except:
                pass
    
    return df

def create_postgresql_import_script(excel_path, output_file="import_to_postgresql.py"):
    """Génère un script Python pour importer dans PostgreSQL"""
    
    script = '''"""
Script généré pour importer les données dans PostgreSQL

PRÉREQUIS:
1. Installer PostgreSQL: https://www.postgresql.org/download/
2. Installer les dépendances: pip install pandas psycopg2 sqlalchemy

UTILISATION:
1. Créer une base de données: createdb energysoft_stats
2. Modifier les paramètres de connexion ci-dessous
3. Exécuter: python import_to_postgresql.py
"""

import pandas as pd
from sqlalchemy import create_engine

# ⚙️ CONFIGURATION - MODIFIER SELON VOTRE ENVIRONNEMENT
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'energysoft_stats',
    'user': 'postgres',
    'password': 'votre_mot_de_passe'
}

EXCEL_FILE = "All Stats Energysoft.xlsx"

def create_connection_string():
    """Crée la chaîne de connexion PostgreSQL"""
    return f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

def import_excel_to_postgresql():
    """Importe les données Excel dans PostgreSQL"""
    print("🗄️  Connexion à PostgreSQL...")
    
    try:
        engine = create_engine(create_connection_string())
        
        # Tester la connexion
        with engine.connect() as conn:
            print("✅ Connexion réussie!")
        
        excel_file = pd.ExcelFile(EXCEL_FILE)
        
        for sheet_name in excel_file.sheet_names:
            print(f"\\n📥 Importation: {sheet_name}...")
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
            
            # Nettoyer le nom de table
            table_name = sheet_name.replace(' ', '_').replace('-', '_').lower()
            table_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in table_name)
            
            # Importer dans PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi')
            print(f"   ✅ Table '{table_name}' créée avec {len(df)} lignes")
        
        print("\\n✅ Importation terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\\n💡 Vérifiez:")
        print("   - PostgreSQL est installé et démarré")
        print("   - La base de données existe")
        print("   - Les identifiants sont corrects")

if __name__ == "__main__":
    import_excel_to_postgresql()
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"✅ Script PostgreSQL généré: {output_file}")

def create_supabase_guide():
    """Crée un guide pour Supabase"""
    
    guide = '''# 🚀 Guide: Importer vos données dans Supabase (Gratuit)

## Étape 1: Créer un compte Supabase
1. Allez sur https://supabase.com/
2. Créez un compte gratuit
3. Créez un nouveau projet

## Étape 2: Obtenir les informations de connexion
1. Dans votre projet Supabase, allez dans Settings > Database
2. Notez:
   - Host
   - Database name
   - Port (par défaut: 5432)
   - User
   - Password

## Étape 3: Utiliser le script Python

Modifiez `import_to_supabase.py` avec vos identifiants Supabase, puis:

```bash
pip install pandas psycopg2 sqlalchemy
python import_to_supabase.py
```

## Avantages de Supabase:
✅ Gratuit jusqu'à 500MB
✅ Interface web intuitive
✅ API REST automatique
✅ Authentification intégrée
✅ Base PostgreSQL complète
✅ Pas besoin d'installer PostgreSQL localement
'''
    
    with open("GUIDE_SUPABASE.md", 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Guide Supabase créé: GUIDE_SUPABASE.md")

def main():
    print("="*70)
    print("📊 IMPORTATION DES DONNÉES EXCEL VERS BASE DE DONNÉES")
    print("="*70)
    
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Fichier non trouvé: {EXCEL_FILE}")
        return
    
    print("\n🎯 Options disponibles:\n")
    print("1. SQLite (RECOMMANDÉ - Le plus simple, pas de serveur)")
    print("2. Générer script PostgreSQL (pour serveur local)")
    print("3. Générer script Supabase (pour cloud gratuit)")
    print("4. Tout créer")
    
    choice = input("\n👉 Votre choix (1-4): ").strip()
    
    if choice == "1" or choice == "4":
        db_path = create_sqlite(EXCEL_FILE)
        print(f"\n💡 Utilisation:")
        print(f"   - SQLite Browser: https://sqlitebrowser.org/")
        print(f"   - Python: sqlite3.connect('{db_path}')")
    
    if choice == "2" or choice == "4":
        create_postgresql_import_script(EXCEL_FILE)
    
    if choice == "3" or choice == "4":
        create_supabase_guide()
        # Créer aussi un script Supabase (identique à PostgreSQL)
        create_postgresql_import_script(EXCEL_FILE, "import_to_supabase.py")
    
    print("\n" + "="*70)
    print("✅ TERMINÉ!")
    print("="*70)

if __name__ == "__main__":
    main()

