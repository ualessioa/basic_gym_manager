#Classi
class Palestra:
    def __init__(self, nome, nr_iscritti = 0, abbonamenti = {}, corsi = [], aperta = False, istruttori = []):
        self.nome = nome
        self.nr_iscritti = nr_iscritti
        self.abbonamenti = abbonamenti
        self.corsi = corsi
        self.aperta = aperta
        self.istruttori = istruttori
    
    def apri_chiudi(self):
        self.aperta = not self.aperta
        if self.aperta:
            print("La palestra adesso è aperta")
        else:
            print("La palestra adesso è chiusa")

#Oggetti
wellness = Palestra("Wellness Club")

#Programma Visibile a schermo
print(f"Benvenuto in Wellness Manager, cosa vorresti fare?")
master_input = input("> ")
while not master_input == "esci":
    if master_input == "apertura":
        wellness.apri_chiudi()
    else:
        print("Input non valido, riprova")
    master_input = input("> ")