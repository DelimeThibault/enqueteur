class Enquete:
    """
    Classe représentant une enquête.

    Auteurs : 2TL2 - 2
    Date : Decembre 2023

    Attributs:
    - idEnquete (int) = L'identifiant de l'enquête.
    - titre (str) = Le titre de l'enquête
    - dateDebut (date) : La date de l'enquête
    - statut (str) : Le statut de l'enquête
    - lieu (str) = Le lieu du crime
    - priorite (int) = La priorité de l'enquête
    - preuves (list) = la liste des preuves associées à cette enquête
    - suspects (list) = la liste des suspects associées à cette enquête

    """

    dictionnaireEnquetesResolues = {}

    def __init__(self, idEnquete: int, titre: str, dateDebut: date, lieu: str, priorite: int,
                 statut: str = 'En cours') -> None:
        """
        Initialise une instance de la classe Enquete.

        PRE : idEnquete et priorité doivent être des entiers
              titre,statut et lieu doivent être des chaînes de caractères
        POST : Une Enquête a été crée avec ses attributs idEnquete, titre, dateDebut, lieu, priorite qui prendront la valeur de ce qui a été passé en paramètre
        RAISE : ValueError si idEnquete ou priorite ne sont pas des entiers positifs
                ValueError si titre,statut ou lieu sont des chaînes vides
                TypeError si date n'est pas une instance de datetime.date
        """
        if idEnquete <= 0 or priorite <= 0:
            raise ValueError("idEnquete et priorite doivent être des entiers positifs.")

        if not all((statut, titre, lieu)):
            raise ValueError("statut, titre, lieu ne doivent pas être des chaînes vides.")

        if not isinstance(dateDebut, date):
            raise TypeError("dateDebut doit être une instance de la classe date.")

        self.idEnquete = idEnquete
        self.titre = titre
        self.dateDebut = dateDebut
        self.statut = statut
        self.lieu = lieu
        self.priorite = priorite
        self.preuves = []
        self.suspects = []

    def associerPreuve(self, preuve) -> None:
        """
        Ajoute des Preuves liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : La preuve a été ajoutée à la liste des preuves de l'enquête et la valeur de 
               l'attribut enqueteAssociee prend la valeur de l'idEnquete
        RAISE : TypeError Si la preuve n'est pas une instance de Preuve
        """
        if not isinstance(preuve, Preuve):
            raise TypeError("La preuve qui est ajoutée doit être une instance de Preuve")
        if preuve not in self.preuves:
            preuve.enqueteAssociee = self.idEnquete
            self.preuves.append(preuve)

    def associerSuspect(self, suspect) -> None:
        """
        Ajoute des Suspects liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : Le suspect a été ajoutée à la liste des suspects de l'enquête
        RAISE : TypeError Si le suspect n'est pas une instance de Suspect
        """

        if not isinstance(suspect, Suspect):
            raise TypeError("Le suspect qui est ajouté doit être une instance de Suspect")
        if suspect not in self.suspects:
            suspect.enqueteAssociee = self.idEnquete
            self.suspects.append(suspect)

    def modifierInformations(self, titre: str = None, dateDebut: date = None,
                             statut: str = None, lieu: str = None, priorite: int = None) -> None:
        """
        Modifie les informations de l'enquête.

        PRE :
        POST :
        """
        if titre is not None:
            self.titre = titre
        if dateDebut is not None:
            self.dateDebut = dateDebut
        if statut is not None:
            self.statut = statut
        if lieu is not None:
            self.lieu = lieu
        if priorite is not None:
            self.priorite = priorite

    def supprimerInformations(self) -> None:
        """
        Supprime les informations de l'enquête.

        PRE :
        POST :
        """
        self.idEnquete = None
        self.titre = None
        self.dateDebut = None
        self.statut = None
        self.lieu = None
        self.priorite = None
        self.preuves.clear()
        self.suspects.clear()

    def elementsFrise(self) -> List[Tuple]:
        """
        Récupère les différents éléments importants pour pouvoir les afficher dans une frise chronologique
        éléments importants : 
        Enquete : dateDebut, titre et le lieu 
        Preuve : dateDeDecouverte, idPreuve, lieu et le type de preuve 
        Suspect : dateIncrimination, idSuspect, nom, adresse

        PRE : /
        POST : retourne un tableau constitué de tuples avec les différentes informations qui ont été récupérées dans la liste des suspects et la liste des preuves
        """
        elements = [(self.dateDebut, 'Début Enquête', f'Titre : {self.titre}, Lieu : {self.lieu}')]

        for preuve in self.preuves:
            elements.append((preuve.dateDeDecouverte, f'Preuve n° {preuve.idPreuve}',
                             f"Lieu : {preuve.lieu}, Type : {preuve.type}"))
        for suspect in self.suspects:
            elements.append((suspect.dateIncrimination, f'Suspect n° {suspect.idSuspect}',
                             f"Nom : {suspect.nom}, Adresse : {suspect.adresse}"))
        elements.sort(key=lambda x: x[0])
        return elements

    def creerFriseChrono(self) -> None:
        """
        Crée une frise chronologique pour l'enquête avec les différents éléments
        repertoriés au cours du temps ( découverte d'une preuve, nouveau suspect, etc...)

        PRE : /
        POST : ouvre une fenêtre qui affiche la frise
        """
        FriseChronologiqueApp(enquete=self).run()

    def enqueteResolue(self, idCoupable: int) -> str:
        """
        Permet de cloturer une enquête qui est considérée comme résolue

        PRE : Identifiant du suspect qui a été désigné comme étant le coupable
        POST : Ajoute un dictionnaire contenant toutes les informations de l'enquête résolue à un dictionnaire "dictionnaireEnquetesResolues",
               change l'attribut statut en classée/Résolue, change l'attribut priorité en 0 et puis supprime cette instance.

        """
        self.statut = "Classée/Résolue"
        self.priorite = 0
        coupable = next((s for s in self.suspects if s.idSuspect == idCoupable), None)
        if coupable is None:
            return "Coupable non trouvé."

        infosEnquete = {
            "idEnquete": self.idEnquete,
            "titre": self.titre,
            "dateDebut": self.dateDebut.isoformat(),
            "statut": self.statut,
            "lieu": self.lieu,
            "priorite": self.priorite,
            "preuves": [p.toDict() for p in self.preuves],
            "coupable": coupable.toDict(),
        }
        Enquete.dictionnaireEnquetesResolues[f'Enquete n° {self.idEnquete}'] = infosEnquete

        # Supprimez l'instance de l'enquête ici, si nécessaire. Cela pourrait être compliqué dans Python car 'del self' n'est pas conseillé.
        # Vous pouvez définir une logique pour retirer cette enquête de toute collection active si applicable.
        return f"L'enquête {self.idEnquete} a bien été classée."

    def localiserLieuxPreuves(self) -> str:
        """
        Localise les lieux ou ont été trouvés les preuves liées à l'enquête

        PRE : /
        POST : Retourne l'addresse des lieux ou on été trouvé la preuve
        """
        pass

    def localiseAddresseSuspects(self) -> str:
        """Localise les différents suspects grâce à leur addresses

        PRE : /
        POST : Retourne l'addresse du suspect

        """
        pass
