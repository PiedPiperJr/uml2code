# 🌟 **DrawIO to Java**  
**Transformez vos diagrammes de classes DrawIO en code Java en un clin d'œil !**  

---  

## ✨ **Fonctionnalités**  
- 🛠️ **Génération automatique de classes Java :**  
  - ✔️ Prise en charge des attributs des classes.  
  - 🚧 Méthodes supportées (actuellement sans paramètres).  
- ⚙️ **Processus en 3 étapes :**  
  1️⃣ Extraction des données XML depuis les fichiers `.drawio`.  
  2️⃣ Conversion en JSON structuré.  
  3️⃣ Génération du code Java basé sur un **template simple et efficace**.  

---

## 🛑 **Limites actuelles**  
### 📌 **Types incorrects**  
🔍 Les types (attributs, méthodes) ne sont pas toujours standardisés.  
💡 **Solution envisagée :**  
- Implémenter des règles conditionnelles (`if-else`) pour mapper correctement les types.  
- 🔮 Explorer l’utilisation d’une IA pour gérer les cas ambigus ou non déterminés.  

### 📌 **Méthodes avec paramètres**  
⚠️ La génération ne prend pas encore en compte les paramètres de méthode.  

### 📌 **Relations entre classes**  
🔗 Les relations (héritage, associations, agrégations, etc.) ne sont pas encore gérées.  

---

## 🚀 **Améliorations futures**  
1️⃣ **Gestion des méthodes avec paramètres :** Ajout du support des paramètres pour les méthodes.  
2️⃣ **Relations entre classes :** Génération des relations (associations, héritage).  
3️⃣ **Support multi-langage :** Étendre la génération à d’autres langages de programmation (Python, C++, etc.).  
   📝 **Astuce :** Ajouter simplement des templates spécifiques au langage.  

---

## 📋 **Comment utiliser ?**  
### 🔧 **Installation :**  
1. Installez les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```  

### 📂 **Tester avec des exemples :**  
- Deux fichiers `.drawio` sont disponibles dans le dossier `data` :  
  - `class-diagram-example.drawio`  
  - `class_diagram.drawio`  
- Lancez `main.ipynb`, ajustez la constante **`XML_FILE_PATH`**, et exécutez toutes les cellules.  

### 📂 **Résultats générés :**  
📄 Les fichiers JSON intermédiaires sont dans `data/json_files/`.  
💻 Le code Java final est généré dans `data/generated_app/`.  

---

## 📂 **Structure du projet**  
```
📁 ihm  
├─ 📁 data  
│  ├─ 📄 class-diagram-example.drawio  # Exemple de diagramme de classe  
│  ├─ 📄 class_diagram.drawio          # Diagramme principal  
│  ├─ 📁 generated_app                 # Dossier pour le code Java généré  
│  │  └─ .gitkeep  
│  └─ 📁 json_files                    # Fichiers JSON intermédiaires  
│     └─ .gitkeep  
├─ 📄 main.ipynb                       # Notebook pour exécuter le programme  
├─ 📄 README.md                        # Documentation du projet  
├─ 📄 requirements.txt                 # Dépendances Python  
└─ 📁 templates  
   └─ 📁 java  
      └─ 📄 simple_class.html          # Template Java simple  
```  

---

## 🌟 **Pour aller plus loin**  
💡 **Idée innovante :**  
Créez un **générateur de modèles de bases de données** (relationnelles ou non) basé sur des diagrammes entité-association.  

📊 Cela pourrait inclure des outils pour :  
- Générer des schémas SQL.  
- Produire des scripts pour bases de données NoSQL comme MongoDB.  

---

✨ Merci d'utiliser **DrawIO to Java !** 😊  

--- 

Qu'en pensez-vous ? 🎉