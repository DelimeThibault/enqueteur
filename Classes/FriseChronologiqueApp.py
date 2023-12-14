class FriseChronologiqueApp(App):
    """
    Application kivy pour afficher une frise chronologique liée à une enquête

    Attibuts :
    - enquete (instance de Enquete) : L'instance de la classe Enquete associé à la frise

    """

    def __init__(self, enquete, **kwargs):
        """
        Auteur : Thibault
        Initialise une instance de la classe FriseChronologiqueApp
        PRE : enquete doit être une instance de la classe Enquete
        POST :  Une instance de la classe FriseChronologiqueApp a été créée.
        """
        super(FriseChronologiqueApp, self).__init__(**kwargs)
        self.enquete = enquete

    def build(self):
        """
        Auteur: Thibault
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
