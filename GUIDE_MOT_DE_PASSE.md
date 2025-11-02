# 🔒 Guide - Protection par Mot de Passe

Ce guide explique comment protéger votre dashboard Streamlit Cloud par un mot de passe.

## ✅ Configuration Effectuée

J'ai ajouté un système d'authentification :
- ✅ Module `auth.py` créé
- ✅ `dashboard_apex.py` modifié pour inclure la protection
- ✅ Interface de connexion élégante (glassmorphism)
- ✅ Compatible avec Streamlit Cloud

## 🚀 Configuration sur Streamlit Cloud

### Étape 1 : Ajouter le Secret dans Streamlit Cloud

1. **Allez sur https://share.streamlit.io**
2. **Connectez-vous** et sélectionnez votre app : `dashboard-exploit`
3. Cliquez sur **"Settings"** ou **"Manage app"**
4. Dans le menu de gauche, cliquez sur **"Secrets"**
5. Cliquez sur **"Edit secrets"** ou le bouton d'édition
6. Ajoutez votre mot de passe dans le format suivant :

```toml
[secrets]
DASHBOARD_PASSWORD = "votre_mot_de_passe_ici"
```

**Exemple :**
```toml
[secrets]
DASHBOARD_PASSWORD = "MonMotDePasseSecurise123"
```

7. Cliquez sur **"Save"**

### Étape 2 : Redéployer l'Application

Streamlit Cloud redéploiera automatiquement après avoir sauvegardé les secrets.

**OU** vous pouvez forcer le redéploiement :
1. Allez dans **"Manage app"**
2. Cliquez sur **"Reboot app"** ou **"Deploy"**

### Étape 3 : Tester l'Authentification

1. Allez sur https://dashboard-exploit.streamlit.app/
2. Vous devriez voir une **page de connexion** élégante
3. Entrez le mot de passe que vous avez configuré
4. Cliquez sur **"Se connecter"**
5. ✅ Vous accédez au dashboard !

## 🔐 Fonctionnalités

### ✅ Protection Complète
- Le dashboard est **totalement protégé** sans le mot de passe
- Aucune donnée n'est accessible sans authentification
- Interface de connexion professionnelle

### ✅ Session Persistante
- Une fois connecté, vous restez connecté pendant la session
- Pas besoin de ressaisir le mot de passe à chaque fois
- Bouton de déconnexion disponible dans la sidebar

### ✅ Design Glassmorphism
- Interface de connexion au même style que votre dashboard
- Design moderne et cohérent
- Expérience utilisateur agréable

## 🔧 Configuration Locale (Optionnel)

Pour tester en local, créez `.streamlit/secrets.toml` :

```toml
[secrets]
DASHBOARD_PASSWORD = "votre_mot_de_passe_local"
```

Puis lancez :
```bash
streamlit run dashboard_apex.py
```

## 🎯 Utilisation

### Accès au Dashboard
1. Ouvrez https://dashboard-exploit.streamlit.app/
2. Entrez votre mot de passe
3. Cliquez sur "Se connecter"
4. Profitez du dashboard !

### Déconnexion
- Cliquez sur le bouton **"🔒 Déconnexion"** dans la sidebar
- Vous serez redirigé vers la page de connexion

## 🔒 Sécurité

### ✅ Bonnes Pratiques

1. **Mot de passe Fort**
   - Utilisez au moins 12 caractères
   - Mélangez lettres, chiffres et symboles
   - Exemple : `D@shb0@rd-2024!`

2. **Ne Partagez Pas le Mot de Passe**
   - Partagez uniquement avec les personnes autorisées
   - Utilisez un gestionnaire de mots de passe

3. **Changez Régulièrement**
   - Changez le mot de passe périodiquement
   - Mettez à jour dans Streamlit Cloud Secrets

### ⚠️ Notes Importantes

- **Le mot de passe est stocké dans les secrets Streamlit Cloud** (sécurisé)
- **Pas de hashage** : Pour une sécurité maximale, on pourrait ajouter du hashage (SHA256)
- **Session en mémoire** : La session expire quand vous fermez le navigateur
- **Pas de limite de tentatives** : Une amélioration future pourrait ajouter un rate limiting

## 🔄 Mise à Jour du Mot de Passe

Pour changer le mot de passe :

1. Allez sur Streamlit Cloud → Votre app → Settings → Secrets
2. Modifiez la valeur de `DASHBOARD_PASSWORD`
3. Cliquez sur "Save"
4. L'app redéploiera automatiquement

## 🐛 Dépannage

### ❌ "Module auth not found"

**Solution :** Vérifiez que `auth.py` est bien dans votre dépôt GitHub :
```bash
git add auth.py
git commit -m "Ajout authentification"
git push origin main
```

### ❌ Le mot de passe ne fonctionne pas

**Vérifications :**
1. Le secret est bien configuré dans Streamlit Cloud ?
2. Le nom du secret est exactement `DASHBOARD_PASSWORD` ?
3. Pas d'espaces avant/après le mot de passe dans les secrets ?
4. L'app a été redéployée après l'ajout du secret ?

### ❌ Pas de page de connexion affichée

**Vérifications :**
1. Le fichier `auth.py` est bien présent dans le dépôt
2. Le code d'authentification est bien dans `dashboard_apex.py`
3. Vérifiez les logs Streamlit Cloud pour les erreurs

## 📝 Fichiers Modifiés/Créés

- ✅ `auth.py` - Nouveau module d'authentification
- ✅ `dashboard_apex.py` - Modifié pour inclure la protection
- ✅ `GUIDE_MOT_DE_PASSE.md` - Ce guide

## 🎉 C'est Tout !

Votre dashboard est maintenant protégé par un mot de passe.

**Prochaines étapes :**
1. Configurer le secret dans Streamlit Cloud
2. Tester l'authentification
3. Partager l'URL uniquement avec les personnes autorisées

---

**Questions ?** Consultez les logs Streamlit Cloud ou vérifiez que tous les fichiers sont bien poussés sur GitHub.

