from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from datetime import date
from typing import List

class Enquete:
    """
    Classe représentant une enquête.

    Auteurs : 2TL2 - 2
    Date : Novembre 2023

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

    def __init__(self, idEnquete: int, titre: str,dateDebut: date ,lieu: str,priorite :int ,statut: str ='En cours') -> None:
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



    def ajouterPreuve(self, preuve) -> None :
        """
        Ajoute des Preuves liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : La preuve a été ajoutée à la liste des preuves de l'enquête
        RAISE : TypeError Si la preuve n'est pas une instance de Preuve
        """
        if not isinstance(preuve, Preuve):
            raise TypeError("La preuve qui est ajoutée doit être une instance de Preuve")
        if preuve not in self.preuves :
            preuve.enqueteAssociee = self
            self.preuves.append(preuve)


    def ajouterSuspect(self,suspect)-> None:
        """
        Ajoute des Suspects liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : Le suspect a été ajoutée à la liste des suspects de l'enquête
        RAISE : TypeError Si le suspect n'est pas une instance de Suspect
               """

        if not isinstance(suspect, Suspect):
            raise TypeError("Le suspect qui est ajouté doit être une instance de Suspect")
        if suspect not in self.suspects :
            suspect.enqueteAssociee = self
            self.preuves.append(suspect)

    def modifierInformations(self) -> None :
        """
        Modifie les informations de l'enquête.

        PRE :
        POST :
        """
        pass
    def supprimerInformations(self)-> None :
        """
        Supprime les informations de l'enquête.

        PRE :
        POST :
        """

        pass
    def elementsFrise(self)->List[tuple]:
        """
        Récupère les différents éléments importants pour pouvoir les afficher dans une frise
        """
        elements = []
        for preuve in self.preuves:
            elements.append((preuve.dateDeDecouverte,'Preuve',f"Lieu : {preuve.lieu}, Type : {preuve.type}"))
        for suspect in self.suspects:
            elements.append((suspect.dateIncrimination,'Suspect', f"Nom : {suspect.nom}, Adresse : {suspect.adresse}"))



    def creerFriseChrono(self) -> None:
        """
        Crée une frise chronologique pour l'enquête avec les différents éléments
        repertoriés au cours du temps ( découverte d'une preuve, nouveau suspect, etc...)

        PRE :
        POST :
        """
        FriseChronologiqueApp(enquete=self).run()

        pass
    def localiserLieuxPreuves(self)-> str :
        """
        Localise les lieux ou ont été trouvés les preuves liées à l'enquête

        PRE :
        POST :
        """
        pass

    def localiseAddresseSuspects(self) -> str:
        """Localise les différents suspects grâce à leur addresses

        PRE :
        POST :

        """
        pass


    def enqueteResolue(self,idEnquete) -> str :
        """
        Change le statut d'une enquête en Classé, les données liées à cette enquete seront
        déplacées autre part

        PRE : l'identifiant de l'enquête qui est résolue
        POST : supprime cette instance

        """

class Preuve () :
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
    def __init__(self,idPreuve:int , type: str, description: str,lieu: str, utilisateur: int, dateDecouverte: date):
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


class Suspect:
    """
    Classe représentant un suspect qui est lié a une enquête en cours

    Attributs :
    - idSuspect (int) : l'identifiant du suspect
    - nom (string) : le nom du suspect
    - dateNaissance (date): la date de naissance du suspect
    - adresse (string) : l'adresse du suspect
    - utilisateur (int) : l'enquêteur qui a découvert le pot aux roses
    - nationalite (string) : la nationalité du suspect
    - taille (int) : la taille du suspect
    - enqueteAssociee (int) : l'enquete pour la quelle le suspect est suspecté
    - dateIncrimination (date) : date à la quelle l'humain est devenu suspect
    - adn (string) :
    - elementsIncriminants (list(instance de Preuve -> l'id d'une preuve)) : la ou les preuves qui incrimine ce suspect


    """

    def __init__(self, idSuspect: int, nom: str, dateNaissance: date, adresse: str, utilisateur: int, nationalité: str,
                 taille: str, dateIncrimination: date, adn: str):
        """
        Crée une instance de la classe Suspect

        PRE :
        POST : Un Suspect a été crée
        RAISE :
        """

        self.enqueteAssociee = None
        self.idSuspect = idSuspect
        self.nom = nom
        self.dateNaissance = dateNaissance
        self.adresse = adresse
        self.utilisateur = utilisateur
        self.nationalité = nationalité
        self.taille = taille
        self.dateIncrimination = dateIncrimination
        self.adn = adn
        self.elementsIncriminants = []

class FriseChronologiqueApp(App):
    def __init__(self,enquete, **kwargs):
        super(FriseChronologiqueApp, self).__init__(**kwargs)
        self.enquete = enquete

    def build(self):
        layout = BoxLayout(orientation='vertical')
        elementsFrise = self.enquete.elementsFrise()

        for element in elementsFrise :
            label = Label(text=f'{element[0]} : {element[1]} - {element[2]}')
            layout.add_widget(label)
        return layout



# rem:  j'ai ajouté dans preuve deux attributs enqueteAssociee, dateDecouverte
# rem : j'ai ajouté dans enquête un attribut preuve qui est une liste
# rem : j'ai ajouté une méthode enqueteRésolue dans la classe enquete
# rem : j'ai changé ajouterInformations en ajouterPreuves et ajouterSuspects
# rem : j'ai changé localiserlieux en localiserlieuxPreuves et localiserAddressesSuspects
"""
test Unitaires qu'on peut prévoir : 
- tester tout les raises 
- tester le fait de mettre deux fois la même preuve 
- tester tout les constructeurs 
"""


# à faire -> ajouter un attribut enquête associée a suspect et aussi un attribut elementsAcharge et éventuellement ADN, empreintes digitales,etc (tout se qui pourrait incriminer un suspect)

# Petit Exemple D'utilisation

enquete1 = Enquete ( idEnquete=1, titre="Enquête A", lieu="Ville A", dateDebut=date(2023,1,1), priorite=15)
preuve1 = Preuve ( idPreuve= 1 , type='Sang/ADN', description='Sang Retrouvé sur la scène de crime', lieu='Scène de Crime', dateDecouverte = date(2023,1,1) ,utilisateur=5)
preuve2 = Preuve ( idPreuve= 5 , type='Mobile', description='Témoignage qui dit que la victime et le suspect n° 4 ne se kiffaient pas de ouf' , lieu='Voisinage Du suspect', dateDecouverte=date(2023,4,3),utilisateur=5 )

enquete1.ajouterPreuve(preuve1)
enquete1.ajouterPreuve(preuve2)


for i in enquete1.preuves:
    print(f'{i.idPreuve} : {i.type} : {i.description} : {i.lieu}')
