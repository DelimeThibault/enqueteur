"""MVP permettant de créer une enquête, ajouter un suspect avec différentes informations et de lier
une enquête avec un suspect."""
import json
import cmd


class Enquete:
    """Permet d'initialiser la classe Enquete avec les différents attributs."""
    def __init__(self, nom, lieu, date, suspects=None):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.suspects = suspects if suspects is not None else []

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date": self.date,
            "suspects": [s.to_dict() for s in self.suspects]
        }


class Suspect:
    """Permet d'initialiser la class Suspect avec les différents attributs."""

    def __init__(self, prenom, nom, age, nationalite, taille, description):
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.nationalite = nationalite
        self.taille = taille
        self.description = description

    def to_dict(self):
        """permet d'ajouter suspect dans le dictionnaire"""
        return {
            "prenom": self.prenom,
            "nom": self.nom,
            "age": self.age,
            "nationalite": self.nationalite,
            "taille": self.taille,
            "description": self.description
        }


class GestionSuspect(cmd.Cmd):
    """Permet d'ajouter et de modifier les informations sur les suspects et les enquêtes."""
    intro = "Bienvenue dans le gestionnaire d'enquêtes. Tapez ? pour la liste des commandes.\n"
    prompt = "(MVP) "

    def __init__(self):
        super().__init__()
        self.dict_suspects = {}
        self.dict_enquetes = {}
        self.id_suspect = 1
        self.id_enquete = 1
        self.charger_donnees()

    def sauvegarder_donnees(self):
        """permet de sauvegarder les données dans le fichier json"""
        with open('donnees.json', 'w') as fichier:
            data = {
                "suspects": {id: suspect.to_dict() for id, suspect in self.dict_suspects.items()},
                "enquetes": {id: enquete.to_dict() for id, enquete in self.dict_enquetes.items()}
            }
            json.dump(data, fichier)

    def charger_donnees(self):
        """permet de charger les données dans le fichier json"""
        try:
            with open('donnees.json', 'r') as fichier:
                data = json.load(fichier)
                self.dict_suspects = {int(id): Suspect(**suspect) for id, suspect in data["suspects"].items()}
                self.id_suspect = max(self.dict_suspects.keys(), default=0) + 1

                self.dict_enquetes = {}
                for id, enquete in data["enquetes"].items():
                    # Reconstitution des suspects pour chaque enquête
                    suspects = []
                    for suspect_data in enquete["suspects"]:
                        if isinstance(suspect_data, dict):  # Le suspect est déjà un dictionnaire
                            suspects.append(Suspect(**suspect_data))
                        else:  # Le suspect est référencé par son identifiant
                            suspect_id = int(suspect_data)
                            if suspect_id in self.dict_suspects:
                                suspects.append(self.dict_suspects[suspect_id])

                    self.dict_enquetes[int(id)] = Enquete(enquete["nom"], enquete["lieu"], enquete["date"], suspects)
                self.id_enquete = max(self.dict_enquetes.keys(), default=0) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.dict_suspects = {}
            self.dict_enquetes = {}
            self.id_suspect = 1
            self.id_enquete = 1

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

    @staticmethod
    def do_fermer(_):
        """Fermer le logiciel"""
        return True


if __name__ == "__main__":
    GestionSuspect().cmdloop()
