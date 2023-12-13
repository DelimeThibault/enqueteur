from datetime import date
class Preuve:
    """
        Classe représentant une preuve qui est liée a une enquête en cours

        Attributs :
        - idPreuve (int) : identifiant de la preuve
        - type (str) : type de preuve -> empreinte de doigt, adn, etc..
        - description (str) : description détaillée de la preuve
        - lieux (str) : lieu ou a été découverte la preuve
        - utilisateur (int) : identifiant de l'enquêteur qu'a découvert la preuve
        - dateDeDecouverte (date) : date de découverte de la preuve
        - enqueteAssociee (int) : recevra au moment de l'éxécution de la méthode ajouterPreuve l'identifiant de l'enquête

    """

    def __init__(self, idPreuve: int, type: str, description: str, lieu: str, utilisateur: int, dateDecouverte: date):
        """
        Initialise une instance de la classe Preuve.

        PRE :    idPreuve, utilisateur doivent être des entiers
                 type, description, lieu ne doivent pas être des chaînes vides
        POST :   Une Preuve a été crée
        RAISES : ValueError si idPreuve, utilisateur ne sont pas des entiers positifs.
                 ValueError si type, description, lieu sont des chaînes vides.
                 TypeError si dateDecouverte n'est pas une instance de la classe date.
        """

        if not isinstance(idPreuve, int) or idPreuve <= 0:
            raise ValueError("idPreuve doit être un entier positif.")
        if not isinstance(utilisateur, int) or utilisateur <= 0:
            raise ValueError("utilisateur doit être un entier positif.")
        if not all(isinstance(arg, str) and arg for arg in (type, description, lieu)):
            raise ValueError("type, description, lieu ne doivent pas être des chaînes vides.")
        if not isinstance(dateDecouverte, date):
            raise TypeError("dateDecouverte doit être une instance de la classe date.")

        self.idPreuve = idPreuve
        self.type = type
        self.description = description
        self.lieu = lieu
        self.utilisateur = utilisateur
        self.dateDecouverte = dateDecouverte
        self.enqueteAssociee = None  # Cet attribut sera défini lors de l'association avec une enquête
        self.supprime = False

    def modifierPreuve(self, nouveau_type: str, nouvelle_description: str, nouveau_lieu: str, nouvel_utilisateur: int,
                       nouvelle_dateDecouverte: date):
        """
        Modifie les attributs de l'instance courante de Preuve.

        PRE :    Les mêmes contraintes que pour le constructeur s'appliquent.
        POST :   Les attributs de l'instance sont mis à jour.
        RAISES : Les mêmes exceptions que pour le constructeur.
        """
        if not all(isinstance(arg, str) and arg for arg in (nouveau_type, nouvelle_description, nouveau_lieu)):
            raise ValueError("type, description, lieu ne doivent pas être des chaînes vides.")
        if not isinstance(nouvel_utilisateur, int) or nouvel_utilisateur <= 0:
            raise ValueError("utilisateur doit être un entier positif.")
        if not isinstance(nouvelle_dateDecouverte, date):
            raise TypeError("dateDecouverte doit être une instance de la classe date.")

        self.type = nouveau_type
        self.description = nouvelle_description
        self.lieu = nouveau_lieu
        self.utilisateur = nouvel_utilisateur
        self.dateDecouverte = nouvelle_dateDecouverte

    def supprimerPreuve(self):
        """
        Marque la preuve comme supprimée.

        POST : L'attribut 'supprime' de l'instance est mis à True.
        """
        self.supprime = True

    def toDict(self) -> dict:
        """
        Convertit l'instance de Preuve en un dictionnaire.

        POST : Retourne un dictionnaire contenant les informations de la preuve.
        """
        return {
            "idPreuve": self.idPreuve,
            "type": self.type,
            "description": self.description,
            "lieu": self.lieu,
            "utilisateur": self.utilisateur,
            "dateDecouverte": self.dateDecouverte.isoformat(),
            # Conversion de la date au format ISO pour la sérialisation
            "enqueteAssociee": self.enqueteAssociee.idEnquete if self.enqueteAssociee else None
        }