# 🌟 **UML2Code**  
**Transformez vos diagrammes de classes DrawIO en code Java en un clin d'œil !**  

---  

## ✨ **Fonctionnalités**  
- 🛠️ Génération automatique de classes Java via CLI  
- ✔️ Extraction de structures de classe depuis DrawIO  
- 🚧 Support des attributs et méthodes simples  

---

## 🚀 **Installation**  
```bash
# Cloner le dépôt
git clone https://github.com/PacomeKFP/uml2code
cd uml2code

# Installer les dépendances
pip install -r requirements.txt
```

## 📋 **Utilisation**  
```bash
# Conversion de base
python cli.py diagram.drawio

# Options avancées
python cli.py diagram.drawio -o ./generated_classes
python cli.py diagram.drawio --keep-temp
```

### 🔍 **Options CLI**  
- `input_file` : Chemin du diagramme DrawIO (obligatoire)
- `-o, --output` : Dossier de sortie pour les classes Java
- `--intermediate-dir` : Dossier pour les fichiers JSON temporaires
- `--keep-temp` : Conserver les fichiers intermédiaires

---

## 🛑 **Limitations actuelles**  
- ⚠️ Types de données limités mal supportés
- 🔗 Relations entre classes non supportées
- 📝 Arguments de méthodes non pris en charge

---

## 🚀 **Feuille de route**  
1. Support complet des types de données
2. Gestion des relations entre classes
3. Support multilangage
4. Amélioration de la gestion des méthodes

---

## 📂 **Structure du projet**  
```
uml_converter/
├── main.py           # Fichier principal de test
├── cli.py            # Point d'entrée CLI
├── config.py         # Configuration
├── converters/       # Logique de conversion
├── models/           # Modèles de données
├── utils/            # Utilitaires
└── templates/        # Templates de génération
```

---

✨ **DrawIO to Java** - Simplifiez votre génération de code ! 🚀