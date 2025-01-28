Voici cinq descriptions textuelles de cas d'utilisation incluant des scénarios principaux et alternatifs :  

---

### Cas d'utilisation 1 : Authentification utilisateur  
**Description** :  
Un utilisateur souhaite accéder à son compte en saisissant ses identifiants.  

**Acteurs** : Utilisateur, système d'authentification.  
**Préconditions** :  
- L'utilisateur doit disposer d'un compte valide.  

**Postconditions** :  
- L'utilisateur est authentifié et redirigé vers son tableau de bord.  

**Scénarios** :  
- **Principal** :  
  1. L'utilisateur saisit son nom d'utilisateur et son mot de passe.  
  2. Le système vérifie les informations fournies.  
  3. L'utilisateur est redirigé vers son espace personnel.  
- **Alternatif** :  
  1. L'utilisateur saisit un mot de passe incorrect.  
  2. Le système affiche un message d'erreur et propose de réessayer ou de réinitialiser le mot de passe.  

---

### Cas d'utilisation 2 : Passage d’une commande  
**Description** :  
Un client souhaite commander des produits via une plateforme de e-commerce.  

**Acteurs** : Client, système de gestion des commandes.  
**Préconditions** :  
- Le client doit être connecté à son compte.  

**Postconditions** :  
- La commande est enregistrée et confirmée.  

**Scénarios** :  
- **Principal** :  
  1. Le client ajoute des produits au panier.  
  2. Le client confirme le panier et passe au paiement.  
  3. Le système enregistre la commande et affiche une confirmation.  
- **Alternatif** :  
  1. Le client tente de commander un produit indisponible.  
  2. Le système informe le client de l'indisponibilité et propose des alternatives.  

---

### Cas d'utilisation 3 : Réservation d’un billet en ligne  
**Description** :  
Un utilisateur souhaite réserver un billet pour un voyage via une plateforme en ligne.  

**Acteurs** : Utilisateur, système de réservation.  
**Préconditions** :  
- Les horaires et les trajets doivent être disponibles dans le système.  

**Postconditions** :  
- La réservation est confirmée et un billet électronique est généré.  

**Scénarios** :  
- **Principal** :  
  1. L'utilisateur choisit une destination et une date de voyage.  
  2. Le système affiche les options disponibles.  
  3. L'utilisateur sélectionne une option, saisit ses informations personnelles et effectue le paiement.  
  4. Le système génère un billet électronique.  
- **Alternatif** :  
  1. L'utilisateur tente de réserver pour une date sans disponibilité.  
  2. Le système propose d'autres options ou permet à l'utilisateur de modifier ses critères.  

---

### Cas d'utilisation 4 : Publication de contenu  
**Description** :  
Un auteur souhaite publier un article sur une plateforme en ligne.  

**Acteurs** : Auteur, éditeur, système de publication.  
**Préconditions** :  
- L'auteur doit être connecté à son compte.  

**Postconditions** :  
- L'article est publié et visible pour les lecteurs.  

**Scénarios** :  
- **Principal** :  
  1. L'auteur rédige un article et le soumet pour validation.  
  2. L'éditeur valide l'article.  
  3. Le système publie l'article sur la plateforme.  
- **Alternatif** :  
  1. L'article soumis contient des erreurs importantes.  
  2. L'éditeur rejette l'article et fournit des commentaires pour correction.  

---

### Cas d'utilisation 5 : Récupération de mot de passe  
**Description** :  
Un utilisateur souhaite réinitialiser son mot de passe en cas d’oubli.  

**Acteurs** : Utilisateur, système d'authentification.  
**Préconditions** :  
- L'utilisateur doit avoir une adresse e-mail associée à son compte.  

**Postconditions** :  
- Le mot de passe est réinitialisé avec succès.  

**Scénarios** :  
- **Principal** :  
  1. L'utilisateur clique sur "Mot de passe oublié".  
  2. Le système envoie un e-mail avec un lien de réinitialisation.  
  3. L'utilisateur clique sur le lien et définit un nouveau mot de passe.  
  4. Le système confirme la réinitialisation.  
- **Alternatif** :  
  1. L'utilisateur entre une adresse e-mail incorrecte ou non associée à un compte.  
  2. Le système informe l'utilisateur de l'échec et propose de réessayer.  

--- 

Ces descriptions peuvent être adaptées selon vos besoins spécifiques.