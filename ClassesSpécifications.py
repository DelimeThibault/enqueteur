import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from datetime import date
from typing import List


class Enquete:
    """
    Classe représentant une enquête.

    Auteurs : 2TL2 - 2
    Date : Novembre 2023
    """

    dictionnaireEnquetesResolues = {}

    """
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

    def __init__(self, idEnquete: int, titre: str, dateDebut: date, lieu: str, priorite: int,
                 statut: str = 'En cours') -> None:
        """
        Initialise une instance de la classe Enquete.

        PRE : idEnquete et priorité doivent être des entiers
              titre,statut et lieu doivent être des chaînes de caractères
        POST : Une Enquête a été crée
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
        POST : La preuve a été ajoutée à la liste des preuves de l'enquête
        RAISE : TypeError Si la preuve n'est pas une instance de Preuve
        """
        if not isinstance(preuve, Preuve):
            raise TypeError("La preuve qui est ajoutée doit être une instance de Preuve")
        if preuve not in self.preuves:
            preuve.enqueteAssociee = self
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
            suspect.enqueteAssociee = self
            self.suspects.append(suspect)

    def modifierInformations(self) -> None:
        """
        Modifie les informations de l'enquête.

        PRE :
        POST :
        """
        pass

    def supprimerInformations(self) -> None:
        """
        Supprime les informations de l'enquête.

        PRE :
        POST :
        """

        pass

    def elementsFrise(self) -> List[tuple]:
        """
        Récupère les différents éléments importants pour pouvoir les afficher dans une frise

        PRE : /
        POST : retourne un tableau constitué de tuples avec les différentes informations qui ont été récupérées dans la liste des suspects et la liste des preuves
        """
        elements = []
        elements.append((self.dateDebut, 'Début Enquête', f'Titre : {self.titre}, Lieu : {self.lieu}'))

        for preuve in self.preuves:
                elements.append((preuve.dateDeDecouverte, f'Preuve n° {preuve.idPreuve}', f"Lieu : {preuve.lieu}, Type : {preuve.type}"))
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

    def localiserLieuxPreuves(self) -> str:
        """
        Localise les lieux ou ont été trouvés les preuves liées à l'enquête

        PRE : Encodage du lieux ou a été trouvé la preuve
        POST : Retourne l'addresse des lieux ou on été trouvé la preuve
        """
        pass

    def localiseAddresseSuspects(self) -> str:
        """Localise les différents suspects grâce à leur addresses

        PRE : /
        POST : Retourne l'addresse du suspect

        """
        pass

    def enqueteResolue(self,idCoupable) -> str:
        """
        Change le statut d'une enquête en Classé, supprime l'instance et les données liées à cette enquete seront
        déplacées dans le dictionnaire "dictionnaireEnquetesResolues"

        PRE : Identifiant du suspect qui a été désigné comme étant le coupable
        POST : Ajoute un dictionnaire contenant toutes les informations de l'enquête résolue à dict_global_enquetes_resolues,
               puis supprime cette instance.

        """

        self.statut="Classée/Résolue"
        self.priorite = 0
        coupable =  [s.toDict() for s in self.suspects if s.idSuspect == idCoupable]
        infosEnquete = {
            "idEnquete" : self.idEnquete,
            "titre" : self.titre,
            "dateDebut" : self.dateDebut,
            "statut" : self.statut,
            "lieu" : self.lieu,
            "priorite" : self.priorite,
            "preuves" : [p.toDict() for p in self.preuves],
            "coupable" : coupable,
        }
        Enquete.dictionnaireEnquetesResolues[f'Enquete n° {self.idEnquete}'] = infosEnquete
        retour = f"L'enquête {self.idEnquete} a bien été classée"
        del self
        return retour

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
        Initialise une instance de la classe Preuve


        PRE :    idPreuve, utilisateur doivent être des entiers
                 type, description, lieu ne doivent pas être des chaînes
        POST :   Une Preuve a été crée
        RAISES : ValueError si idPreuve, utilisateur ne sont pas des entiers positifs.
                 ValueError si type, description, lieu sont des chaînes vides.
                 TypeError si dateDecouverte n'est pas une instance de la classe date.
        """

        if idPreuve <= 0 or utilisateur <= 0:
            raise ValueError("idPreuve et utilisateur doivent être des entiers positifs.")

        if not all((type, description, lieu)):
            raise ValueError("type, description, lieu ne doivent pas être des chaînes vides.")

        if not isinstance(dateDecouverte, date):
            raise TypeError("dateDecouverte doit être une instance de la classe date.")

        self.idPreuve = idPreuve
        self.type = type
        self.description = description
        self.lieu = lieu
        self.utilisateur = utilisateur
        self.dateDeDecouverte = dateDecouverte
        self.enqueteAssociee = None

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
            "dateDeDecouverte": self.dateDeDecouverte.isoformat(),
        }
class Personne:
    """
    Classe représentant une Personne soit un enqueteur soit un suspect

    Attributs :
    - idPersonne (int) : l'identifiant de la personne
    - nom (string) : le nom de la personne
    - age (int) : l'age de la personne
    - Type (string): si la personne est un enqueteur ou un suspect
    """

    def __init__(self, idPersonne: int, nom: str, age: int, type: str):
        """
        Crée une instance de la classe Personne

        PRE : idPersonne doit être un entier, une personne doit etre soit suspect soit enqueteur
        POST : Une Personne a été crée
        RAISE :
        """

        self.idPersonne = idPersonne
        self.nom = nom
        self.age = age
        self.type = type

    def modifierPersonne(self) -> None:
        """
        Modifie les informations de la personne.

        PRE : les modifications doivent respecter les formats ci dessus
        POST : modification de la personne
        """
        pass

    def SupprimerPersonne(self) -> None:
        """
        Supprime la Personne.

        PRE : /
        POST : Supprimer la personne
        """

        pass


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

    def __init__(self, idPersonne: int, idSuspect: int, nom: str, dateNaissance: date, age: int, type: str,
                 adresse: str, utilisateur: int, nationalite: str, taille: str, dateIncrimination: date, adn: str):
        super().__init__(idPersonne, nom, age, type)
        self.idSuspect = idSuspect
        self.dateNaissance = dateNaissance
        self.adresse = adresse
        self.utilisateur = utilisateur
        self.nationalite = nationalite
        self.taille = taille
        self.dateIncrimination = dateIncrimination
        self.adn = adn
        self.elementsIncriminants = []
        self.recidive = Suspect.recidive(self)
        self.enqueteAssociee = None

    def toDict(self) -> dict:
        """
        Convertit l'instance de Suspect en un dictionnaire.

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
            "récidive": self.recidive
        }

    def recidive(self) -> bool:
        """
        fonction qui interroge une base de données (fictive/crée pour le programme)
        qui contient le casier judiciaire de la population belge


        POST : renvoie un booléen -> True si la personne a déjà commis une ou des infractions et False si totalement inconnu des services de police

        """
        connection = sqlite3.connect("D:\#5_LILIAN\#2_EPHEC\\2ième\Dev2\PROJET_ENQUETEURPRO\\CasierJudiciareSQlite.db")
        curseur = connection.cursor()

        id = (self.idPersonne,)
        curseur.execute(
            'SELECT description FROM Personnes as P JOIN Crimes as C ON P.idPersonne = C.idPersonne WHERE P.idPersonne == ?',
            id)
        resultat = curseur.fetchall()

        connection.close()

        return bool(resultat)

    def casierJudiciaire(self) -> str:
        """
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
        remplit la liste des différents identifiants de preuves qui incriminent le suspect

        PRE : preuve doit être une instnace de preuve
        POST : tableau contenant les identifiants de preuves
        RAISES : TypeError si preuve n'est pas une instance de Preuve
        """


class Enqueteur(Personne):
    """
    Classe représentant un Enqueteur qui utilise une enquete

    Attributs :
    - attributs hérités de Personne ( nom , age, idPersonne, type )
    - idEnqueteur (int) : l'identifiant de l'enqueteur
    - mdp (int) : mot de passe de l'enquteur pour accèder aux informations

    """

    def __init__(self, idEnqueteur: int, mdp: int, nom: str, idPersonne: int, age: int, type: str):
        """
        Crée une instance de la classe Enquteur

        PRE : idEnquteur doit être un entier, mdp doit etre un entier
        POST : Un enquteur a été crée
        RAISE :
        """
        super().__init__(idPersonne, nom, age, type)
        self.idEnqueteur = idEnqueteur
        self.mdp = mdp

    def modifierEnqueteur(self) -> None:
        """
        Modifie les informations de l'enquteur.

        PRE : les modifications doivent respecter les formats ci dessus
        POST : Les données de l'enqueteur ont été modifié
        """
        pass

    def SupprimerEnquteur(self) -> None:
        """
        Supprime l'enquteur.

        PRE : /
        POST : Supprime l'enquteur
        """

        pass


class FriseChronologiqueApp(App):
    """
    Application kivy pour afficher une frise chronologique liée à une enquête

    Attibuts :
    - enquete (instance de Enquete) : L'instance de la classe Enquete associé à la frise

    """

    def __init__(self, enquete, **kwargs):
        """
        Initialise une instance de la classe FriseChronologiqueApp
        PRE : enquete doit être une instance de la classe Enquete
        POST :  Une instance de la classe FriseChronologiqueApp a été créée.
        """
        super(FriseChronologiqueApp, self).__init__(**kwargs)
        self.enquete = enquete

    def build(self):
        """
        Construit l'interface utilisateur de l'application
        PRE: /
        POST : Retourne un widget représentant l'interface utilisateur
        """
        layout = BoxLayout(orientation='vertical')
        scrollview = ScrollView()

        elementsFrise = self.enquete.elementsFrise()

        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for element in elementsFrise:
            label = Label(text=f"{element[0]}: {element[1]} - {element[2]}", size_hint_y=None, height=40)
            grid.add_widget(label)

        scrollview.add_widget(grid)
        layout.add_widget(scrollview)

        return layout


"""
test Unitaires qu'on peut prévoir : 
- tester tout les raises 
- tester le fait de mettre deux fois la même preuve 
- tester tout les constructeurs 
"""

# enquêteurs
enqueteur1 = Enqueteur(idEnqueteur=1, mdp=123, nom="Sherlock Holmes", idPersonne=40, age=45, type="Enqueteur")
enqueteur2 = Enqueteur(idEnqueteur=2, mdp=456, nom="Hercule Poirot", idPersonne=41, age=55, type="Enqueteur")

# enquêtes
enquete1 = Enquete(idEnquete=1, titre="Affaire du collier", dateDebut=date(2023, 1, 1), lieu="Paris", priorite=1)
enquete2 = Enquete(idEnquete=2, titre="Disparition mystérieuse", dateDebut=date(2023, 2, 1), lieu="Londres", priorite=2)

# preuves
preuve1 = Preuve(idPreuve=1, type="Empreinte digitale", description="Empreinte sur le collier", lieu="Dressing", utilisateur=1, dateDecouverte=date(2023, 1, 5))
preuve2 = Preuve(idPreuve=2, type="ADN", description="ADN sur la scène de crime", lieu="Salon", utilisateur=2, dateDecouverte=date(2023, 1, 7))
preuve3 = Preuve(idPreuve=3, type="Témoignage", description="Témoin de la disparition", lieu="Place publique", utilisateur=1, dateDecouverte=date(2023, 2, 5))

# suspects
suspect1 = Suspect(idPersonne=3, idSuspect=1, nom="Johnson Michael", dateNaissance=date(1980, 5, 10), age=43, type="Suspect",
                   adresse="Rue de la République", utilisateur=1, nationalite="Française", taille="1m75", dateIncrimination=date(2023, 1, 8), adn="Matche avec l'ADN trouvé")
suspect2 = Suspect(idPersonne=4, idSuspect=2, nom="Brown Emily", dateNaissance=date(1990, 8, 15), age=32, type="Suspect",
                   adresse="Baker Street", utilisateur=2, nationalite="Anglaise", taille="1m65", dateIncrimination=date(2023, 2, 8), adn="Aucun élément incriminant")



# Ptits tests

enquete1.associerPreuve(preuve2)
enquete1.associerPreuve(preuve1)

enquete1.associerSuspect(suspect1)
enquete1.creerFriseChrono()

enquete1.enqueteResolue(1)

enquete2.associerPreuve(preuve3)
enquete2.associerSuspect(suspect2)
enquete2.creerFriseChrono()

enquete2.enqueteResolue(2)


print(Enquete.dictionnaireEnquetesResolues)


