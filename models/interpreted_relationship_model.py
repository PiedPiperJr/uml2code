from dataclasses import dataclass
from typing import Optional


@dataclass
class InterpretedRelationShip:
    """
    Représente les informations interprétées pour une relation entre entités,
    utilisées par le template Jinja2 pour générer le code JPA.
    """
    role: str
    """
    Nom du champ (rôle) de la relation dans l'entité en cours de génération.
    Exemple: "author", "books", "profile"
    """

    comodel: str
    """
    Nom de la classe de l'entité cible (le "co-modèle") de la relation.
    Doit être capitalisé car il réfère directement au nom de la classe.
    Exemple: "Author", "Book", "UserProfile"
    """

    mapped_by_property: Optional[str] = None
    """
    Attribut optionnel. S'il est fourni, il indique que cette relation est
    le côté inverse (non-propriétaire) d'une relation bidirectionnelle.
    Sa valeur est le nom du champ sur l'entité propriétaire qui mappe cette relation.
    Si None ou non fourni, la relation est considérée comme unidirectionnelle
    ou comme le côté propriétaire d'une relation bidirectionnelle.
    Exemple: Pour un champ `List<Book> books` dans `Author`, si `Book` a un champ
             `Author author`, alors pour la relation `books` dans `Author`,
             `mapped_by_property` serait "author" sur la relation inverse définie dans `Book`.
             Pour la relation `author` dans `Book`, `mapped_by_property` ne serait pas défini.
    """