from main import Personne
class Enqueteur(Personne):
    """
    Classe représentant un Enqueteur qui utilise une enquete

    Attributs :
    - attributs hérités de Personne ( nom , age, idPersonne, type )
    - idEnqueteur (int) : l'identifiant de l'enqueteur
    - grade: grade de l'enquêteur
    - enquetesAssignees = enquetes sous la charge de l'enquêteur

    """

    def __init__(self, idPersonne: int, nom: str, age: int, idEnqueteur: int, grade: str, fonction: str):
        """
                Crée une instance de la classe Enquteur

                PRE : idEnquteur doit être un entier, mdp doit etre un entier
                POST : Un enquteur a été crée
                """
        super().__init__(idPersonne, nom, age, fonction)
        self.idEnqueteur = idEnqueteur
        self.grade = grade
        self.enquetesAssignees = []  # Liste des enquêtes assignées à l'enquêteur
        self.estSupprime = False

    def toDict(self) -> dict:
        """
        Convertit l'instance de Enqueteur en un dictionnaire.

        POST : Retourne un dictionnaire contenant les informations de l'enquêteur
        """
        return {
            "idEnqueteur": self.idEnqueteur,
            "nom": self.nom,
            "age": self.age,
            "grade": self.grade,
            "enquetesAssignees": self.enquetesAssignees
        }

    def assignerEnquete(self, enquete) -> None:
        """
        Assigner une enquête à l'enquêteur.

        PRE : enquete: Instance de la classe Enquete à assigner.
        """
        if enquete not in self.enquetesAssignees:
            self.enquetesAssignees.append(enquete)

    def modifierEnqueteur(self, nouveau_nom: str, nouvel_age: int, nouveau_grade: str) -> None:
        """
        Modifie les informations de l'enquêteur.

        PRE : nouveau_nom doit être une chaîne, nouvel_age un entier, nouveau_grade une chaîne.
        POST : Les données de l'enquêteur ont été modifiées.
        """
        self.nom = nouveau_nom
        self.age = nouvel_age
        self.grade = nouveau_grade

    def SupprimerEnqueteur(self) -> None:
        """
        Marque l'enquêteur comme supprimé.

        POST : L'enquêteur est marqué comme supprimé.
        """
        self.estSupprime = True