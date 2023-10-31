"""MVP permettant d'ajouter un suspect avec différentes informations sur celui-ci."""
import cmd


class Suspect:
    """Permet d'initialiser la class Suspect avec les différents attributs."""
    def __init__(self, prenom, nom, age, nationalite, taille, description):
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.nationalite = nationalite
        self.taille = taille
        self.description = description


class GestionSuspect(cmd.Cmd):
    """Permet d'ajouter et de modifier les informations sur la class Suspect"""
    intro = "Bienvenue dans le gestionnaire d'enquêtes. Tapez ? pour la liste des commandes.\n"
    prompt = "(MVP) "

    def __init__(self):
        super().__init__()
        self.dict_suspects = {}
        self.id = 1

    def do_ajouter(self, _):
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

        self.dict_suspects[self.id] = Suspect(prenom, nom, age, nationalite, taille, description)
        print(f"Suspect ajouté avec succès. ID du suspect : {self.id}")
        self.id += 1


    def do_afficher(self, _):
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
