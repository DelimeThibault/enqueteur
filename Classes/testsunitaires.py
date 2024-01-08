import unittest
from datetime import datetime
from preuve import Preuve
from enqueteur import Enqueteur
from suspect import Suspect
from personne import Personne
from enquete import Enquete

# test git

class TestPreuve(unittest.TestCase):

    def test___init__(self):
        date_test = datetime.now()
        # Tests valides
        preuve_valide = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        self.assertEqual(preuve_valide.idPreuve, 1, "__init__ : idPreuve valide")
        self.assertEqual(preuve_valide.type, "ADN", "__init__ : Type valide")
        self.assertEqual(preuve_valide.description, "Description", "__init__ : Description valide")
        self.assertEqual(preuve_valide.lieu, "Lieu", "__init__ : Lieu valide")
        self.assertEqual(preuve_valide.utilisateur, 123, "__init__ : utilisateur valide")
        self.assertEqual(preuve_valide.dateDecouverte, date_test, "__init__ : DateDecouverte valide")

        # Test avec une date passé
        date_past = datetime(2020, 5, 17)
        preuve_past = Preuve(2, "Empreinte", "Description passée", "Lieu passé", 456, date_past)
        self.assertEqual(preuve_past.dateDecouverte, date_past, "__init__ : Date de découverte passée")

        # Test avec une date futur (erreur)
        datefutur = datetime(2025, 12, 31)
        self.assertRaises(ValueError, Preuve, 3, "couteau", "Description future", "Lieu futur", 789, datefutur)

        # Test avec id invalide
        self.assertRaises(ValueError, Preuve, -1, "ADN", "Description", "Lieu", 123, date_test)
        self.assertRaises(ValueError, Preuve, 0, "ADN", "Description", "Lieu", 123, date_test)

        # Test avec utilisateur invalide
        self.assertRaises(ValueError, Preuve, 1, "ADN", "Description", "Lieu", -123, date_test)

        # Test avec type, description, lieu vides
        self.assertRaises(ValueError, Preuve, 1, "", "", "", 123, date_test)

        # Test avec dateDeDecouverte invalide
        self.assertRaises(TypeError, Preuve, 1, "ADN", "Description", "Lieu", 123, "date")

    def test_modifierPreuve(self):
        date_test = datetime.now()

        nouvelle_date = datetime(2022, 7, 14)
        # Test valide
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve.modifierPreuve("Empreinte", "Nouvelle description", "Nouveau lieu", 456, date_test)
        self.assertEqual(preuve.type, "Empreinte", "modifierPreuve : Type modifié")
        self.assertEqual(preuve.description, "Nouvelle description", "modifierPreuve : Description modifiée")
        self.assertEqual(preuve.lieu, "Nouveau lieu", "modifierPreuve : Lieu modifié")
        self.assertEqual(preuve.utilisateur, 456, "modifierPreuve : utilisateur modifié")
        self.assertEqual(preuve.dateDecouverte, date_test, "modifierPreuve : DateDecouverte modifiée")

        preuve1 = Preuve(4, "Sang", "Description initiale", "Lieu initial", 1213, date_test)
        preuve1.modifierPreuve("Cheveux", "Description modifiée", "Nouveau lieu", 1011, nouvelle_date)
        self.assertEqual(preuve1.type, "Cheveux", "modifierPreuve : Type modifié")
        self.assertEqual(preuve1.description, "Description modifiée", "modifierPreuve : Description modifiée")
        self.assertEqual(preuve1.lieu, "Nouveau lieu", "modifierPreuve : Lieu modifié")
        self.assertEqual(preuve1.utilisateur, 1011, "modifierPreuve : utilisateur modifié")
        self.assertEqual(preuve1.dateDecouverte, nouvelle_date, "modifierPreuve : Date de découverte modifiée")

        # Test modification avec type, description, lieu vides
        self.assertRaises(ValueError, preuve.modifierPreuve, "", "", "", 45, date_test)

        # Test modification avec utilisateur invalide
        self.assertRaises(ValueError, preuve.modifierPreuve, "Empreinte", "Nouvelle description", "Nouveau lieu", -45,
                          date_test)
        # Test modification avec taille négative
        self.assertRaises(ValueError, preuve.modifierPreuve, "Empreinte", "Description", "Lieu", -180, date_test)

        # Test modification avec une date dans le futur
        datefutur = datetime(2050, 1, 1)
        self.assertRaises(ValueError, Preuve, 3, "Fibre", "Description future", "Lieu futur", 789, datefutur)

    def test_supprimerPreuve(self):
        date_test = datetime.now()
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve.supprimerPreuve()
        self.assertTrue(preuve.supprime, "supprimerPreuve : Preuve supprimée")

        # Modification d'une preuve supprimé
        preuve1 = Preuve(2, "couteau", "Description", "Lieu", 12, date_test)
        preuve1.supprimerPreuve()
        with self.assertRaises(Exception):
            preuve1.modifierPreuve("Empreinte", "Nouvelle Description", "Nouveau Lieu", 456, datetime.now())

    def test_toDict(self):
        date_test = datetime.now()
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve_dict = preuve.toDict()

        self.assertEqual(preuve_dict["idPreuve"], 1, "toDict : idPreuve")
        self.assertEqual(preuve_dict["type"], "ADN", "toDict : type")
        self.assertEqual(preuve_dict["description"], "Description", "toDict : description")
        self.assertEqual(preuve_dict["lieu"], "Lieu", "toDict : lieu")
        self.assertEqual(preuve_dict["utilisateur"], 123, "toDict : utilisateur")
        self.assertEqual(preuve_dict["dateDecouverte"], date_test, "toDict : dateDecouverte")

        # test en associant une enquete
        date_test = datetime(2020, 1, 1)
        preuve1 = Preuve(2, "Empreinte", "Autre Description", "Autre Lieu", 456, date_test)
        enquete = Enquete(10, "Enquête Test", date_test, "Lieu Fictif", 5)
        preuve1.enqueteAssociee = enquete

        preuve_dict = preuve1.toDict()
        self.assertEqual(preuve_dict["idPreuve"], 2, "toDict : idPreuve")
        self.assertEqual(preuve_dict["type"], "Empreinte", "toDict : type")
        self.assertEqual(preuve_dict["description"], "Autre Description", "toDict : description")
        self.assertEqual(preuve_dict["lieu"], "Autre Lieu", "toDict : lieu")
        self.assertEqual(preuve_dict["utilisateur"], 456, "toDict : utilisateur")
        self.assertEqual(preuve_dict["dateDecouverte"], date_test, "toDict : dateDecouverte")
        self.assertEqual(preuve_dict["enqueteAssociee"], 10, "toDict : enqueteAssociee")


class TestSuspect(unittest.TestCase):

    def test___init__(self):
        date_test = datetime.now()
        # Test avec valeurs valides
        suspect_valide = Suspect(1, 1, "Devroye", "Lilian", date_test, 30, "suspect", "Rue de coquerie", 123, "Belge",
                                 "180cm", date_test, "ADN 1")
        self.assertEqual(suspect_valide.idPersonne, 1, "__init__ : idPersonne valide")
        self.assertEqual(suspect_valide.idSuspect, 1, "__init__ : idSuspect valide")
        self.assertEqual(suspect_valide.age, 30, "__init__ : idSuspect valide")
        self.assertEqual(suspect_valide.nom, "Devroye", "__init__ : Nom valide")
        self.assertEqual(suspect_valide.prenom, "Lilian", "__init__ : Prénom valide")
        self.assertEqual(suspect_valide.fonction, "suspect", "__init__ : fonction valide")
        self.assertEqual(suspect_valide.adresse, "Rue de coquerie")
        self.assertEqual(suspect_valide.utilisateur, 123, "__init__ : utilisateur valide")
        self.assertEqual(suspect_valide.nationalite, "Belge", "__init__ : nationalité valide")
        self.assertEqual(suspect_valide.taille, "180cm", "__init__ : taille valide")
        self.assertEqual(suspect_valide.dateNaissance, date_test, "__init__ : dateNaissance valide")
        self.assertEqual(suspect_valide.dateIncrimination, date_test, "__init__ : dateIncrimation valide")
        self.assertEqual(suspect_valide.adn, "ADN 1", "__init__ : adn valide")
        self.assertEqual(suspect_valide.enqueteAssociee, None, "__init__ : enqueteAssociee valide")

        # Test avec age invalide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, -30, "suspect", "Adresse", 123, "Nationalité", "180cm", date_test,
                    "ADN")

        # Test avec adresse vide
        with self.assertRaises(ValueError):
            Suspect(1, 3, "Nom", "Prénom", date_test, 30, "suspect", "", 123, "Nationalité", "180cm", date_test, "ADN")

        # Test avec dateNaissance invalide
        with self.assertRaises(TypeError):
            Suspect(1, 4, "Nom", "Prénom", "date invalide", 30, "suspect", "Adresse", 123, "Nationalité", "180cm",
                    date_test, "ADN")

        # Test avec idPersonne invalide
        with self.assertRaises(ValueError):
            Suspect(-1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "180cm",
                    date_test, "ADN")

            # Test avec idSuspect invalide
        with self.assertRaises(ValueError):
            Suspect(1, -1, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "180cm",
                    date_test, "ADN")

            # Test avec nom vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "180cm", date_test,
                    "ADN")

            # Test avec prénom vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "180cm", date_test,
                    "ADN")

        # Test avec utilisateur invalide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", -123, "Nationalité", "180cm",
                    date_test, "ADN")

        # Test avec nationalité vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "", "180cm", date_test, "ADN")

        # Test avec taille vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "", date_test,
                    "ADN")

            # Test avec adn vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "180cm",
                    date_test, "")

    def test_to_dict(self):
        # Conversion de l'instance en dictionnaire
        self.date_naissance = datetime(1980, 1, 1)
        self.date_incrimination = datetime.now()
        self.suspect = Suspect(1, 1, "Nom", "Prénom", self.date_naissance, 40, "suspect", "Adresse", 123,
                               "Nationalité", "180cm", self.date_incrimination, "ADN")
        suspect_dict = self.suspect.to_dict()

        # Vérification de la présence des clés et de la correspondance des valeurs
        self.assertEqual(suspect_dict["idSuspect"], self.suspect.idSuspect, "to_dict : idSuspect")
        self.assertEqual(suspect_dict["nom"], self.suspect.nom, "to_dict : nom")
        self.assertEqual(suspect_dict["prenom"], self.suspect.prenom, "to_dict : prenom")
        self.assertEqual(suspect_dict["dateNaissance"], self.suspect.dateNaissance, "to_dict : dateNaissance")
        self.assertEqual(suspect_dict["adresse"], self.suspect.adresse, "to_dict : adresse")
        self.assertEqual(suspect_dict["utilisateur"], self.suspect.utilisateur, "to_dict : utilisateur")
        self.assertEqual(suspect_dict["nationalite"], self.suspect.nationalite, "to_dict : nationalite")
        self.assertEqual(suspect_dict["taille"], self.suspect.taille, "to_dict : taille")
        self.assertEqual(suspect_dict["dateIncrimination"], self.suspect.dateIncrimination,
                         "to_dict : dateIncrimination")
        self.assertEqual(suspect_dict["adn"], self.suspect.adn, "to_dict : adn")

    def test_modifier_suspect(self):
        # Création d'un suspect pour le test
        date_naissance = datetime(1980, 1, 1)
        date_incrimination = datetime.now()
        suspect = Suspect(1, 1, "Nom", "Prénom", date_naissance, 40, "suspect", "Adresse", 123, "Nationalité", "180cm",
                          date_incrimination, "ADN")

        # Test modification valide
        nouvelle_date_naissance = "1981-02-02"
        nouvelle_date_incrimination = "2022-07-14"
        suspect.modifier_suspect("Nouveau Nom", "Nouveau Prénom", 41, nouvelle_date_naissance, "Nouvelle Adresse",
                                 "Nouvelle Nationalité", "185cm", "Nouvel ADN", 456, nouvelle_date_incrimination)

        self.assertEqual(suspect.idSuspect, 1, "modifier_suspect : idSupect inchangé")
        self.assertEqual(suspect.idPersonne, 1, "modifier_suspect : idPersonne inchangé")


        self.assertEqual(suspect.nom, "Nouveau Nom", "modifier_suspect : Nom modifié")
        self.assertEqual(suspect.prenom, "Nouveau Prénom", "modifier_suspect : Prénom modifié")
        self.assertEqual(suspect.age, 41, "modifier_suspect : Age modifié")
        self.assertEqual(suspect.dateNaissance, datetime.strptime(nouvelle_date_naissance, "%Y-%m-%d"),
                         "modifier_suspect : Date de naissance modifiée")
        self.assertEqual(suspect.adresse, "Nouvelle Adresse", "modifier_suspect : Adresse modifiée")
        self.assertEqual(suspect.nationalite, "Nouvelle Nationalité", "modifier_suspect : Nationalité modifiée")
        self.assertEqual(suspect.taille, "185cm", "modifier_suspect : Taille modifiée")
        self.assertEqual(suspect.adn, "Nouvel ADN", "modifier_suspect : ADN modifié")
        self.assertEqual(suspect.utilisateur, 456, "modifier_suspect : Utilisateur modifié")
        self.assertEqual(suspect.dateIncrimination, datetime.strptime(nouvelle_date_incrimination, "%Y-%m-%d"),
                         "modifier_suspect : Date d'incrimination modifiée")

        # Test modification avec valeurs invalides
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("", "", 0, "date invalide", "", "", "", "", -1, "date invalide")

    def test_modification_suspect_supprimee(self):
        # Création et suppression d'un suspect
        date_test = datetime.now()
        suspect = Suspect(1, 1, "Nom", "Prénom", date_test, 40, "suspect", "Adresse", 123, "Nationalité", "180cm",
                          date_test, "ADN")
        suspect.supprimer()
        self.assertTrue(suspect.supprimer, "supprimer : Suspect correctement supprimé")


        # Test de modification d'un Suspect supprimé !
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("", "Prénom Valide", 30, "1980-01-01", "Adresse Valide", "Nationalité Valide",
                                 "180cm", "ADN Valide", 123, "2022-07-14")

    def test_modifier_suspect_valeurs_invalides(self):
        date_naissance = datetime(1980, 1, 1)
        date_incrimination = datetime.now()
        suspect = Suspect(1, 1, "Nom", "Prénom", date_naissance, 40, "suspect", "Adresse", 123, "Nationalité", "180cm",
                          date_incrimination, "ADN")

        # Test modification avec âge négatif
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", -30, "1980-01-01", "Adresse Valide",
                                     "Nationalité Valide", "180cm", "ADN Valide", 123, "2022-07-14")

        """
        # Test modification avec une date de naissance dans le futur

        date_future = datetime(2025, 12, 31)
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", 30, date_future, "Adresse Valide",
                                     "Nationalité Valide", "180cm", "ADN Valide", 123, "2022-07-14")
        """

        # Test modification avec nom vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("", "Prénom Valide", 30, "1980-01-01", "Adresse Valide", "Nationalité Valide",
                                     "180cm", "ADN Valide", 123, "2022-07-14")

        # Test modification avec prénom vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "", 30, "1980-01-01", "Adresse Valide", "Nationalité Valide",
                                     "180cm", "ADN Valide", 123, "2022-07-14")

        # Test modification avec adresse vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", 30, "1980-01-01", "", "Nationalité Valide", "180cm",
                                     "ADN Valide", 123, "2022-07-14")

        # Test modification avec nationalité vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", 30, "1980-01-01", "Adresse Valide", "", "180cm",
                                     "ADN Valide", 123, "2022-07-14")

        # Test modification avec taille vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", 30, "1980-01-01", "Adresse Valide",
                                     "Nationalité Valide", "", "ADN Valide", 123, "2022-07-14")

        # Test modification avec ADN vide
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("Nom Valide", "Prénom Valide", 30, "1980-01-01", "Adresse Valide",
                                     "Nationalité Valide", "180cm", "", 123, "2022-07-14")



class TestEnqueteur(unittest.TestCase):

    def test___init__(self):
        # Test avec valeurs valides
        enqueteur_valide = Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")
        self.assertEqual(enqueteur_valide.idPersonne, 1, "__init__ : idPersonne valide")
        self.assertEqual(enqueteur_valide.nom, "NomEnqueteur", "__init__ : Nom valide")
        self.assertEqual(enqueteur_valide.prenom, "PrénomEnqueteur", "__init__ : Prénom valide")
        self.assertEqual(enqueteur_valide.age, 40, "__init__ : Age valide")
        self.assertEqual(enqueteur_valide.idEnqueteur, 100, "__init__ : idEnqueteur valide")
        self.assertEqual(enqueteur_valide.grade, "GradeEnqueteur", "__init__ : Grade valide")
        self.assertEqual(enqueteur_valide.fonction, "enquêteur", "__init__ : Fonction valide")

        # Test avec idPersonne invalide
        with self.assertRaises(ValueError):
            Enqueteur(-1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec idEnqueteur invalide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, -100, "GradeEnqueteur", "enquêteur")

        # Test avec nom vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec prénom vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec age invalide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", -1, 100, "GradeEnqueteur", "enquêteur")

        # Test avec grade vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "", "enquêteur")

        # Test avec fonction vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "")


    def test_to_dict(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        result = enqueteur.to_dict()
        expected_keys = ['idPersonne', 'nom', 'prenom', 'age', 'fonction', 'idEnqueteur', 'grade']
        self.assertTrue(all(key in result for key in expected_keys),
                        "Les clés attendues ne sont pas toutes présentes dans le dictionnaire")

    def test_assignerEnquete(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enquete = Enquete(1, 'Enquête Test', datetime.now(), 'Paris', 1)
        enqueteur.assignerEnquete(enquete)
        self.assertIn(enquete, enqueteur.enquetesAssignees, "L'enquête n'a pas été correctement assignée")

    def test_modifierEnqueteur(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enqueteur.modifierEnqueteur('Martin', 'Paul', 45, 'Capitaine')
        self.assertEqual(enqueteur.nom, 'Martin')
        self.assertEqual(enqueteur.prenom, 'Paul')
        self.assertEqual(enqueteur.age, 45)
        self.assertEqual(enqueteur.grade, 'Capitaine')
        self.assertEqual(enqueteur.fonction, 'enquêteur')

    def test_supprimerEnqueteur(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enqueteur.supprimerEnqueteur()
        self.assertTrue(enqueteur.estSupprime, "L'enquêteur n'a pas été marqué comme supprimé")


class TestPersonne (unittest.TestCase):
    def testInitNormal(self):
        personne = Personne(1, "Dupont", "Jean", 30, "suspect")
        self.assertEqual(personne.idPersonne, 1)
        self.assertEqual(personne.nom, "Dupont")
        self.assertEqual(personne.prenom, "Jean")
        self.assertEqual(personne.age, 30)
        self.assertEqual(personne.fonction, "suspect")
        self.assertIsInstance(personne.idPersonne, int)
        self.assertIsInstance(personne.nom, str)
        self.assertIsInstance(personne.prenom, str)
        self.assertIsInstance(personne.age, int)
        self.assertIsInstance(personne.fonction, str)

    def testLimites(self):
        personne = Personne(1000000, "Dupont", "Jean", 30, "enquêteur")
        self.assertEqual(personne.idPersonne, 1000000)
        personne2 = Personne(2, "Dupont", "Jean", 120, "enquêteur")
        self.assertEqual(personne2.age, 120)
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 0, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", -1, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 30, "ishfdsjhkgjd")
        with self.assertRaises(ValueError):
            Personne(-1, "Dupont", "Jean", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "", "Jean", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(-1, "Dupont", "Jean", 30, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(0, "Dupont", "Jean", 30, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 30, "ishfdsjhkgjd")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 30, "autreFonction")

    def testToDict(self):
        personnne = Personne(1, "Dupont", "Jean", 30, "suspect")
        dictionnaireAttendu = {
            "idPersonne": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "age": 30,
            "fonction": "suspect"
        }
        self.assertEqual(personnne.to_dict(), dictionnaireAttendu)
        self.assertIsInstance(personnne.to_dict(), dict)


class TestEnquete (unittest.TestCase):
    def setUp(self):
        self.date_Debut = datetime.now()
        self.enquete = Enquete(1, "Enquête Test", self.date_Debut, "Lieu Fictif", 5)

    def testInit(self):
        date_test = datetime.now()

        # Test valide
        enquete_valide = Enquete(1, "Enquête Test", date_test, "Lieu Test", 5, "en cours")
        self.assertEqual(enquete_valide.idEnquete, 1, "__init__ : idEnquete valide")
        self.assertEqual(enquete_valide.titre, "Enquête Test", "__init__ : Titre valide")
        self.assertEqual(enquete_valide.dateDebut, date_test, "__init__ : DateDebut valide")
        self.assertEqual(enquete_valide.lieu, "Lieu Test", "__init__ : Lieu valide")
        self.assertEqual(enquete_valide.priorite, 5, "__init__ : Priorite valide")
        self.assertEqual(enquete_valide.statut, "en cours", "__init__ : Statut valide")

        # Test avec une date passée
        date_past = datetime(2020, 5, 17)
        enquete_past = Enquete(2, "Enquête Passée", date_past, "Lieu Passé", 3, "en cours")
        self.assertEqual(enquete_past.dateDebut, date_past, "__init__ : DateDebut passée")

        # Test avec date dans le future
        date_futur = datetime(2025, 12, 31)
        self.assertRaises(ValueError, Enquete, 1, "Enquête Test", date_futur, "Lieu Test", 5)

        # Test avec id invalide
        self.assertRaises(ValueError, Enquete, -1, "Enquête Test", date_test, "Lieu Test", 5, "en cours")
        self.assertRaises(ValueError, Enquete, 0, "Enquête Test", date_test, "Lieu Test", 5, "en cours")

        # Test avec titre ou lieu vide
        self.assertRaises(ValueError, Enquete, 1, "", date_test, "Lieu Test", 5, "en cours")
        self.assertRaises(ValueError, Enquete, 1, "Enquête Test", date_test, "", 5, "en cours")

        # Test avec priorité invalide
        self.assertRaises(ValueError, Enquete, 1, "Enquête Test", date_test, "Lieu Test", -1, "en cours")
        self.assertRaises(ValueError, Enquete, 1, "Enquête Test", date_test, "Lieu Test", 0, "en cours")

    def testErreurs(self):
        with self.assertRaises(ValueError):
            Enquete(0, "Enquête Test", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(-1, "Enquête Test", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", 0)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", -4)
        with self.assertRaises(ValueError):
            Enquete(1, "", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", 5, statut="")
        with self.assertRaises(TypeError):
            Enquete(1, "Enquête Test", "1998/20/12", "Lieu Fictif", 5)

    def test_to_dict(self):
        enqueteDict = self.enquete.to_dict()
        self.assertEqual(enqueteDict['idEnquete'], 1)
        self.assertEqual(enqueteDict['titre'], "Enquête Test")
        self.assertEqual(enqueteDict['dateDebut'], self.date_Debut)
        self.assertEqual(enqueteDict['lieu'], "Lieu Fictif")
        self.assertEqual(enqueteDict['statut'], "En cours")
        self.assertEqual(enqueteDict['priorite'], 5)
        self.assertEqual(enqueteDict['preuves'], [])
        self.assertEqual(enqueteDict['suspects'], [])
        self.assertEqual(enqueteDict['enqueteurs'], [])

    def test_ajouter_preuve(self):
        preuve = Preuve(1, "Type", "Sang", "Lieu", 4, datetime.now())
        self.enquete.ajouter_preuve(preuve)
        self.assertIn(preuve, self.enquete.preuves)



    def test_modifer_informations(self):
        self.enquete.modifierInformations()
        self.assertEqual(self.enquete.titre, "Enquête Test")
        nouvelle_date = datetime.now()
        self.enquete.modifierInformations(titre="nOUVEAu Titre", dateDebut=nouvelle_date, statut="Résolu", lieu="Nouveau Lieu", priorite=10)
        self.assertEqual(self.enquete.titre, "nOUVEAu Titre")
        self.assertEqual(self.enquete.dateDebut, nouvelle_date)
        self.assertEqual(self.enquete.statut, "Résolu")
        self.assertEqual(self.enquete.lieu, "Nouveau Lieu")
        self.assertEqual(self.enquete.priorite, 10)

    def test_supprimer_informations(self):
        self.enquete.supprimerInformations()
        self.assertIsNone(self.enquete.idEnquete)
        self.assertIsNone(self.enquete.titre)
        self.assertIsNone(self.enquete.dateDebut)
        self.assertIsNone(self.enquete.statut)
        self.assertIsNone(self.enquete.lieu)
        self.assertIsNone(self.enquete.priorite)
        self.assertEqual(self.enquete.preuves, [])
        self.assertEqual(self.enquete.suspects, [])

    def test_classer_enquete(self):
        self.enquete.classer_enquete()
        self.assertEqual(self.enquete.statut, "Classé")

    def test_enquete_resolue(self):
        self.enquete.classer_enquete()
        self.assertEqual(self.enquete.statut, "Classé")
        self.assertEqual(self.enquete.priorite, 5)






if __name__ == '__main__':
    unittest.main()
