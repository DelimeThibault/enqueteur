class Personne:
    """
    Classe représentant une Personne soit un enqueteur soit un suspect

    Attributs :
    - idPersonne (int) : l'identifiant de la personne
    - nom (string) : le nom de la personne
    - age (int) : l'age de la personne
    - Type (string): si la personne est un enqueteur ou un suspect
    """

    def __init__(self, idPersonne: int, nom: str, age: int, fonction: str):
        """
        Crée une instance de la classe Personne

        PRE : idPersonne doit être un entier, une personne doit etre soit suspect soit enqueteur
        POST : Une Personne a été crée
        RAISE :
        """

        self.idPersonne = idPersonne
        self.nom = nom
        self.age = age
        self.fonction = fonction