from main import Enquete,Preuve,Enqueteur,Suspect,Personne
import cmd
import json
from datetime import date


class Enregistrer(cmd.Cmd):
    """Permet d'ajouter et de modifier les informations"""

    class Gestion(cmd.Cmd):
        """Permet d'ajouter et de modifier les informations"""

        def __init__(self):
            super().__init__()
            self.dict_suspects = {}
            self.dict_enquetes = {}
            self.dict_preuves = {}
            self.dict_enqueteurs = {}
            self.id_suspect = 1
            self.id_enquete = 1
            self.id_preuve = 1
            self.id_enqueteur = 1
            self.charger_donnees()

        def sauvegarder_donnees(self):
            """permet de sauvegarder les données dans le fichier json"""
            with open('donnees.json', 'w') as fichier:
                data = {
                    "suspects": {id: suspect.to_dict() for id, suspect in self.dict_suspects.items()},
                    "enquetes": {id: enquete.to_dict() for id, enquete in self.dict_enquetes.items()},
                    "preuves": {id: preuve.to_dict() for id, preuve in self.dict_preuves.items()},
                    "enqueteurs": {id: enqueteur.to_dict() for id, enqueteur in self.dict_enqueteurs.items()}
                }
                json.dump(data, fichier)

        def charger_donnees(self):
            """permet de charger les données depuis le fichier json"""
            try:
                with open('donnees.json', 'r') as fichier:
                    data = json.load(fichier)
                    # Charger les suspects
                    self.dict_suspects = {int(id): Suspect(**suspect) for id, suspect in
                                          data.get("suspects", {}).items()}
                    self.id_suspect = max(self.dict_suspects.keys(), default=0) + 1
                    # Charger les enquetes
                    self.dict_enquetes = {int(id): Enquete(**enquete) for id, enquete in
                                          data.get("enquetes", {}).items()}
                    self.id_enquete = max(self.dict_enquetes.keys(), default=0) + 1
                    # Charger les preuves
                    self.dict_preuves = {int(id): Preuve(**preuve) for id, preuve in data.get("preuves", {}).items()}
                    self.id_preuve = max(self.dict_preuves.keys(), default=0) + 1
                    # Charger les enqueteurs
                    self.dict_enqueteurs = {int(id): Enqueteur(**enqueteur) for id, enqueteur in
                                            data.get("enqueteurs", {}).items()}
                    self.id_enqueteur = max(self.dict_enqueteurs.keys(), default=0) + 1
            except (FileNotFoundError, json.JSONDecodeError):
                self.dict_suspects = {}
                self.dict_enquetes = {}
                self.dict_preuves = {}
                self.dict_enqueteurs = {}
                self.id_suspect = 1
                self.id_enquete = 1
                self.id_preuve = 1
                self.id_enqueteur = 1

    def do_ajouter_suspect(self, _):
        """Ajouter un suspect"""
        prenom = input("Prénom du suspect: ")
        nom = input("Nom du suspect: ")
        age = input("Âge du suspect: ")
        nationalite = input("Nationalité du suspect: ")
        taille = input("Taille du suspect (en cm): ")
        description = input("Description du suspect: ")

        try:
            age = int(age)
            taille = float(taille)
        except ValueError:
            print("Erreur : L'âge et la taille doivent être des nombres valides.")
            return

        self.dict_suspects[self.id_suspect] = Suspect(prenom, nom, age, nationalite, taille, description)
        print(f"Suspect ajouté avec succès. ID du suspect : {self.id_suspect}")
        self.id_suspect += 1
        self.sauvegarder_donnees()

    def do_ajouter_enquete(self, _):
        """Ajouter une enquête"""
        nom = input("Nom de l'enquête: ")
        lieu = input("Lieu de l'enquête: ")
        date = input("Date de l'enquête: ")

        self.dict_enquetes[self.id_enquete] = Enquete(nom, lieu, date)
        print(f"Enquête ajoutée avec succès. ID de l'enquête : {self.id_enquete}")
        self.id_enquete += 1
        self.sauvegarder_donnees()

    def do_ajouter_suspect_enquete(self, _):
        """Ajouter un suspect à une enquête"""
        id_enquete = int(input("ID de l'enquête : "))
        id_suspect = int(input("ID du suspect à ajouter à l'enquête : "))

        if id_enquete in self.dict_enquetes and id_suspect in self.dict_suspects:
            enquete = self.dict_enquetes[id_enquete]
            suspect = self.dict_suspects[id_suspect]
            enquete.suspects.append(suspect)
            print(f"Suspect ajouté à l'enquête '{enquete.nom}' avec succès.")
            self.sauvegarder_donnees()
        else:
            print("ID d'enquête ou de suspect invalide.")

    def do_afficher_enquetes(self, _):
        """Afficher la liste des enquêtes"""
        if not self.dict_enquetes:
            print("Aucune enquête enregistrée.")
        else:
            for identifiant, enquete in self.dict_enquetes.items():
                print("----------------------------")
                print(f"ID : {identifiant}")
                print(f"Nom : {enquete.nom}")
                print(f"Lieu : {enquete.lieu}")
                print(f"Date : {enquete.date}")
                if enquete.suspects:
                    print("Suspects:")
                    for suspect in enquete.suspects:
                        print(f"  - {suspect.prenom} {suspect.nom}")
                else:
                    print("Aucun suspect associé à cette enquête.")
                print("----------------------------")

    def do_afficher_suspects(self, _):
        """Afficher la liste des suspects"""
        if not self.dict_suspects:
            print("Aucun suspect enregistré.")
        else:
            for identifiant, suspect in self.dict_suspects.items():
                print("----------------------------")
                print(f"ID : {identifiant}")
                print(f"Prénom : {suspect.prenom}")
                print(f"Nom : {suspect.nom}")
                print(f"Âge : {suspect.age}")
                print(f"Nationalité : {suspect.nationalite}")
                print(f"Taille : {suspect.taille} cm")
                print(f"Description : {suspect.description}")
                print("----------------------------")

    def do_ajouter_preuve(self, _):
        """Ajouter une preuve"""
        type_preuve = input("Type de la preuve (empreinte, ADN, etc.): ")
        description = input("Description de la preuve: ")
        lieu = input("Lieu de découverte: ")
        id_utilisateur = input("Identifiant de l'enquêteur ayant découvert la preuve: ")
        date_de_decouverte = input("Date de découverte (format AAAA-MM-JJ): ")

        try:
            id_utilisateur = int(id_utilisateur)
            # Validation de la date
            annee, mois, jour = map(int, date_de_decouverte.split('-'))
            date_de_decouverte = date(annee, mois, jour)
        except ValueError:
            print("Erreur : Format de date incorrect ou l'identifiant de l'utilisateur n'est pas valide.")
            return

        # Création et ajout de la preuve
        self.dict_preuves[self.id_preuve] = Preuve(self.id_preuve, type_preuve, description, lieu, id_utilisateur,
                                                   date_de_decouverte)
        print(f"Preuve ajoutée avec succès. ID de la preuve : {self.id_preuve}")
        self.id_preuve += 1
        self.sauvegarder_donnees()

    def do_afficher_preuves(self, _):
        """Afficher la liste des preuves"""
        if not self.dict_preuves:
            print("Aucune preuve enregistrée.")
        else:
            for identifiant, preuve in self.dict_preuves.items():
                print("----------------------------")
                print(f"ID : {identifiant}")
                print(f"Type : {preuve.type}")
                print(f"Description : {preuve.description}")
                print(f"Lieu : {preuve.lieu}")
                print(f"Utilisateur : {preuve.utilisateur}")
                print(f"Date de Découverte : {preuve.dateDecouverte.strftime('%Y-%m-%d')}")
                if preuve.enqueteAssociee:
                    print(f"Enquête Associée : {preuve.enqueteAssociee}")
                else:
                    print("Enquête Associée : Aucune")
                print("----------------------------")

    def do_ajouter_personne(self, _):
        """Ajouter une personne"""
        nom = input("Nom de la personne : ")
        age = input("Âge de la personne : ")
        fonction = input("Fonction de la personne : ")

        try:
            age = int(age)
        except ValueError:
            print("Erreur : L'âge doit être un nombre valide.")
            return

        # Création et ajout de la personne
        nouvelle_personne = Personne(self.id_personne, nom, age, fonction)
        self.dict_personnes[self.id_personne] = nouvelle_personne
        print(f"Personne ajoutée avec succès. ID de la personne : {self.id_personne}")
        self.id_personne += 1
        self.sauvegarder_donnees()

    def do_afficher_personnes(self, _):
        """Afficher la liste des personnes"""
        if not self.dict_personnes:
            print("Aucune personne enregistrée.")
        else:
            for identifiant, personne in self.dict_personnes.items():
                print("----------------------------")
                print(f"ID : {identifiant}")
                print(f"Nom : {personne.nom}")
                print(f"Âge : {personne.age}")
                print(f"Fonction : {personne.fonction}")
                print("----------------------------")

    def do_ajouter_enqueteur(self, _):
        """Ajouter un enquêteur"""
        nom = input("Nom de l'enquêteur: ")
        age = input("Âge de l'enquêteur: ")
        id_personne = self.id_personne  # Générer un nouvel ID pour la personne
        id_enqueteur = self.id_enqueteur
        grade = input("Grade de l'enquêteur: ")
        fonction = input("Fonction de l'enquêteur: ")

        try:
            age = int(age)
        except ValueError:
            print("Erreur : L'âge doit être un nombre valide.")
            return

        # Création et ajout de l'enquêteur
        nouvel_enqueteur = Enqueteur(id_personne, nom, age, self.id_enqueteur, grade, fonction)
        self.dict_enqueteurs[self.id_enqueteur] = nouvel_enqueteur
        self.id_enqueteur += 1
        self.id_personne += 1  # Augmenter aussi l'ID de la personne
        print(f"Enquêteur ajouté avec succès. ID de l'enquêteur : {self.id_enqueteur - 1}")
        self.sauvegarder_donnees()

    def do_afficher_enqueteurs(self, _):
        """Afficher la liste des enquêteurs"""
        if not self.dict_enqueteurs:
            print("Aucun enquêteur enregistré.")
        else:
            for identifiant, enqueteur in self.dict_enqueteurs.items():
                print("----------------------------")
                print(f"ID Enquêteur : {identifiant}")
                print(f"Nom : {enqueteur.nom}")
                print(f"Âge : {enqueteur.age}")
                print(f"Grade : {enqueteur.grade}")
                print(f"Fonction : {enqueteur.fonction}")
                print("----------------------------")

    @staticmethod
    def do_fermer(_):
        """Fermer le logiciel"""
        return True


if __name__ == "__main__":
    Enregistrer().cmdloop()