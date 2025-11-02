#!/usr/bin/env python3
"""
Script pour mettre à jour la base SQLite avec les données du fichier Excel
Utilise pandas pour lire Excel et SQLite3 pour mettre à jour la base
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path
from datetime import datetime

# Chemins des fichiers
EXCEL_FILE = "All Stats Energysoft.xlsx"
DB_FILE = "energysoft_stats.db"

# Feuilles Excel à importer (seulement ces 5 onglets)
REQUIRED_SHEETS = [
    "interventions",
    "exposition",
    "calculs_mensuel_sites",
    "calculs_annuel_sites",
    "spot_market_prices"
]

# Mots réservés SQLite à éviter
SQLITE_RESERVED_WORDS = {
    'index', 'select', 'insert', 'update', 'delete', 'create', 'drop',
    'alter', 'table', 'from', 'where', 'order', 'group', 'by', 'having',
    'join', 'union', 'intersect', 'except', 'limit', 'offset', 'as', 'and',
    'or', 'not', 'null', 'true', 'false', 'primary', 'key', 'foreign',
    'references', 'constraint', 'unique', 'check', 'default', 'values',
    'inner', 'outer', 'left', 'right', 'cross', 'natural', 'on', 'using'
}

def sanitize_table_name(sheet_name: str) -> str:
    """Nettoie le nom de la feuille pour créer un nom de table valide"""
    # Remplacer les espaces et caractères spéciaux
    table_name = sheet_name.replace(' ', '_').replace('-', '_').replace('.', '_')
    # Supprimer les caractères non alphanumériques sauf underscore
    table_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in table_name)
    table_name = table_name.lower()
    # Éviter les mots réservés en ajoutant un suffixe
    if table_name in SQLITE_RESERVED_WORDS:
        table_name = f"{table_name}_col"
    return table_name

def sanitize_column_name(col_name: str) -> str:
    """Nettoie le nom de colonne et évite les mots réservés SQLite"""
    # Convertir en string et nettoyer
    col_clean = str(col_name).replace(' ', '_').replace('-', '_').replace('.', '_')
    col_clean = ''.join(c if c.isalnum() or c == '_' else '_' for c in col_clean)
    col_clean = col_clean.lower()
    # Éviter les mots réservés
    if col_clean in SQLITE_RESERVED_WORDS:
        col_clean = f"{col_clean}_col"
    return col_clean

def infer_sqlite_type(series: pd.Series) -> str:
    """Infère le type SQLite approprié pour une colonne pandas"""
    # Vérifier si c'est une date/datetime
    if pd.api.types.is_datetime64_any_dtype(series):
        return "TEXT"
    
    # Vérifier si c'est numérique
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    
    # Vérifier si c'est booléen
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    
    # Par défaut, TEXT
    return "TEXT"

def update_database():
    """Met à jour la base SQLite avec les données Excel"""
    
    print(f"📊 Mise à jour de la base SQLite depuis Excel\n")
    print(f"📁 Fichier Excel: {EXCEL_FILE}")
    print(f"🗄️  Base SQLite: {DB_FILE}\n")
    
    # Vérifier que le fichier Excel existe
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Erreur: Le fichier Excel '{EXCEL_FILE}' n'existe pas")
        return False
    
    try:
        # Ouvrir le fichier Excel
        print("📖 Lecture du fichier Excel...")
        excel_file = pd.ExcelFile(EXCEL_FILE)
        all_sheet_names = excel_file.sheet_names
        print(f"📋 {len(all_sheet_names)} feuilles trouvées dans Excel: {', '.join(all_sheet_names)}")
        
        # Filtrer pour ne garder que les feuilles requises
        sheet_names = [s for s in all_sheet_names if s in REQUIRED_SHEETS]
        missing_sheets = [s for s in REQUIRED_SHEETS if s not in all_sheet_names]
        
        if missing_sheets:
            print(f"⚠️  ATTENTION: Feuilles requises manquantes: {', '.join(missing_sheets)}")
        
        print(f"✅ {len(sheet_names)} feuilles à importer: {', '.join(sheet_names)}\n")
        
        # Connexion à la base SQLite
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Supprimer toutes les tables qui ne sont pas dans la liste requise
        print("🗑️  Nettoyage des tables non nécessaires...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        tables_to_remove = [t for t in existing_tables if sanitize_table_name(t) not in [sanitize_table_name(s) for s in REQUIRED_SHEETS]]
        
        for table in tables_to_remove:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"   🗑️  Table '{table}' supprimée")
        
        if tables_to_remove:
            conn.commit()
            print(f"✅ {len(tables_to_remove)} table(s) supprimée(s)\n")
        
        # Statistiques globales
        total_rows = 0
        tables_updated = []
        
        # Traiter chaque feuille requise
        for sheet_name in sheet_names:
            print(f"📋 Traitement de la feuille: '{sheet_name}'")
            
            try:
                # Lire la feuille Excel
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                if df.empty:
                    print(f"   ⚠️  Feuille vide, ignorée\n")
                    continue
                
                # Nettoyer le nom de la table
                table_name = sanitize_table_name(sheet_name)
                print(f"   📊 {len(df)} lignes, {len(df.columns)} colonnes")
                print(f"   🗃️  Nom de table: '{table_name}'")
                
                # Préparer les données
                # Convertir les dates en chaînes pour SQLite
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                        # Remplacer NaT par None
                        df[col] = df[col].replace('NaT', None)
                
                # Remplacer NaN par None pour SQLite
                df = df.where(pd.notnull(df), None)
                
                # Supprimer la table existante si elle existe
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"   🗑️  Ancienne table supprimée (si existante)")
                
                # Créer la table avec les types corrects
                columns_sql = []
                for col in df.columns:
                    col_clean = sanitize_column_name(str(col))
                    sql_type = infer_sqlite_type(df[col])
                    columns_sql.append(f'"{col_clean}" {sql_type}')
                
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(columns_sql)}
                )
                """
                
                cursor.execute(create_table_sql)
                print(f"   ✅ Table '{table_name}' créée avec {len(df.columns)} colonnes")
                
                # Insérer les données
                # Nettoyer les noms de colonnes pour l'insertion
                df_insert = df.copy()
                df_insert.columns = [sanitize_column_name(str(col)) for col in df_insert.columns]
                
                # Insérer les données par lots pour meilleures performances
                # Pour les tables avec beaucoup de colonnes, utiliser None au lieu de 'multi'
                batch_size = 1000
                rows_inserted = 0
                insert_method = 'multi' if len(df_insert.columns) <= 20 else None
                
                for i in range(0, len(df_insert), batch_size):
                    batch = df_insert.iloc[i:i+batch_size]
                    if insert_method:
                        batch.to_sql(table_name, conn, if_exists='append', index=False, method=insert_method)
                    else:
                        batch.to_sql(table_name, conn, if_exists='append', index=False)
                    rows_inserted += len(batch)
                
                print(f"   ✅ {rows_inserted} lignes insérées")
                print(f"   ✅ Feuille '{sheet_name}' importée avec succès\n")
                
                total_rows += rows_inserted
                tables_updated.append((table_name, rows_inserted))
                
            except Exception as e:
                print(f"   ❌ Erreur lors du traitement de '{sheet_name}': {e}\n")
                continue
        
        # Valider les changements
        conn.commit()
        
        # Afficher le résumé
        print("=" * 60)
        print("📊 RÉSUMÉ DE LA MISE À JOUR")
        print("=" * 60)
        print(f"✅ Tables mises à jour: {len(tables_updated)}")
        print(f"✅ Total de lignes importées: {total_rows:,}\n")
        
        print("📋 Détail par table:")
        for table_name, row_count in tables_updated:
            print(f"   - {table_name}: {row_count:,} lignes")
        
        # Vérifier l'intégrité de la base
        print(f"\n🔍 Vérification de l'intégrité...")
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()
        if integrity_result[0] == "ok":
            print(f"✅ Base de données valide")
        else:
            print(f"⚠️  {integrity_result[0]}")
        
        conn.close()
        print(f"\n✅ Mise à jour terminée avec succès!")
        print(f"📁 Base SQLite: {os.path.abspath(DB_FILE)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 MISE À JOUR BASE SQLITE DEPUIS EXCEL")
    print("=" * 60)
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success = update_database()
    
    print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        exit(0)
    else:
        exit(1)

