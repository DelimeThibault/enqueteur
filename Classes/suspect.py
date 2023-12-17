class Suspect(Personne):
    """
      Classe représentant un suspect qui est lié a une enquête en cours

    Attributs :
    - attributs hérités de Personne ( nom , age, idPersonne, type )
    - idSuspect (int) : Identifiant du suspect
    - nom (string) : le nom du suspect
    - dateNaissance (date): la date de naissance du suspect
    - adresse (string) : l'adresse du suspect
    - utilisateur (int) : l'enquêteur qui a découvert le pot aux roses
    - nationalite (string) : la nationalité du suspect
    - taille (int) : la taille du suspect
    - enqueteAssociee (int) : l'enquete pour la quelle le suspect est suspecté
    - dateIncrimination (date) : date à la quelle l'humain est devenu suspect
    - adn (string) :
    - recidive : est ce que le Suspect est déjà connu pour des crimes antérieurs
    - elementsIncriminants (list(instance de Preuve -> l'id d'une preuve)) : la ou les preuves qui incrimine ce suspect


    """

    def __init__(self, idPersonne: int, idSuspect: int, nom: str, dateNaissance: date, age: int, fonction: str,
                 adresse: str, utilisateur: int, nationalite: str, taille: str, dateIncrimination: date, adn: str):
         """
         Auteur : Léon 
         Constructeur d'objet Suspect héritant de la classe Personne

         PRE: idSuspect et utilisateur doivent être des entiers
         POST: Un Suspect est crée avec ses attributs idSuspect, dateNaissance, addresse, utilisateur, nationalite, taille, dateIncrimination,adn qui prendront la valeur de ce qui a été passé en paramètre
         RAISES: Si idSuspect ou utilisateur sont négatifs -> ValueError
                 Si nationalité, adn, taille, addresse sont des chaînes vides -> ValueError
                 Si dateIncrimination n'est pas une instance de la classe date -> TypeError
         
         
         """
                     
        if idSuspect <= 0 or utilisateur <= 0 or age <= O:
            raise ValueError("idPreuve et utilisateur doivent être des entiers positifs.")

        if not all((nationalite, adn, taille, adresse)):
            raise ValueError("type, description, lieu ne doivent pas être des chaînes vides.")

        if not isinstance(dateIncrimination):
            raise TypeError("dateDecouverte doit être une instance de la classe date.")
        super().__init__(idPersonne, nom, age, fonction)
        self.idSuspect = idSuspect
        self.dateNaissance = dateNaissance
        self.adresse = adresse
        self.utilisateur = utilisateur
        self.nationalite = nationalite
        self.taille = taille
        self.dateIncrimination = dateIncrimination
        self.adn = adn
        self.elementsIncriminants = []
        self.enqueteAssociee = None

    def toDict(self) -> dict:
        """
        Auteur : Léon
        Convertit l'instance de Suspect en un dictionnaire.
        PRE : l'instance de la preuve doit être une instance valide, avec chacun de ses attributs correspondant au type exigé
        POST : Retourne un dictionnaire contenant les informations du Suspect.
        """
        return {
            "idSuspect": self.idSuspect,
            "dateNaissance": self.dateNaissance.isoformat(),
            "adresse": self.adresse,
            "utilisateur": self.utilisateur,
            "nationalite": self.nationalite,
            "taille": self.taille,
            "dateIncrimination": self.dateIncrimination.isoformat(),
            "adn": self.adn,
            "elementsIncriminants": self.elementsIncriminants,
        }

    def casierJudiciaire(self) -> str:
        """
        Auteur : Léon
        fonction qui interroge une base de données (fictive/crée pour le programme)
        qui contient le casier judiciaire de la population belge

        POST : renvoie une phrase qui liste son casier judiciaire
        """
        connection = sqlite3.connect("D:\#5_LILIAN\#2_EPHEC\\2ième\Dev2\PROJET_ENQUETEURPRO\\CasierJudiciareSQlite.db")
        curseur = connection.cursor()

        id = (self,)
        curseur.execute(
            'SELECT idCrime,description FROM Personnes as P JOIN Crimes as C ON P.idPersonne = C.idPersonne WHERE P.idPersonne == ?',
            id)
        resultat = curseur.fetchall()
        phrase = ''
        for i in resultat:
            phrase += f'Crime n°{i[0]} \nDescpription : {i[1]}\n\n'

        connection.close()

        return phrase

    def listeElementsIncriminants(self, preuve):
        """
        Auteur : Léon
        remplit la liste des différents identifiants de preuves qui incriminent le suspect

        PRE : preuve doit être une instnace de preuve
        POST : tableau contenant les identifiants de preuves
        RAISES : TypeError si preuve n'est pas une instance de Preuve
        """
        # Retourne une liste de dictionnaires pour chaque élément incriminant.
        if not isinstance(preuve, Preuve):
            raise TypeError("preuve doit être une instance de la classe Preuve")
        if preuve not in self.elementsIncriminants:
            self.elementsIncriminants.append(preuve)
