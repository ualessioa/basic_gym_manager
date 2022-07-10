#Librerie
import datetime

#Funzioni globali
def crea_cliente(palestra):#definire meglio lo scopo di questa funzione, al momento globale
    if palestra.aperta:
        nome = input("Insersci il nome completo del cliente:\n> ")
        cliente = Cliente(nome)
        return cliente
    else:
        print("La palestra è chiusa!")

data = None
orario = None
giorno = None
mese = None
anno = None
giorno_sett = None

def definisci_momento():#da implementare ulteriormente
    global data, orario, giorno, mese, anno, giorno_sett
    now = datetime.datetime.now()
    giorno = now.strftime("%d")
    mese = now.strftime("%m")
    anno = now.strftime("%Y")
    data = f"{giorno}/{mese}/{anno}"
    giorno_sett = now.strftime("%A")
    #print(data)
    orario = now.strftime("%X")
    #print(int(orario[:2]))


#Classi
class Palestra:
    def __init__(self, nome, nr_iscritti = 0, elenco_iscritti = [], abbonamenti = {}, corsi = [], aperta = False, istruttori = [], cassa = 0, orari_apertura = {}):
        self.nome = nome
        self.nr_iscritti = nr_iscritti
        self.elenco_iscritti = []
        self.abbonamenti = abbonamenti
        self.corsi = corsi
        self.aperta = aperta
        self.istruttori = istruttori
        self.cassa = cassa
        self.orari_apertura = orari_apertura
    
    def apri_chiudi(self):
        self.aperta = not self.aperta
        if self.aperta:
            print("La palestra adesso è aperta")
        else:
            print("La palestra adesso è chiusa")
    
    def aggiungi_cliente(self, cliente):
        self.elenco_iscritti.append(cliente.nome)
        self.elenco_iscritti.sort()
        #print(self.elenco_iscritti)
        self.nr_iscritti += 1
        abb = input("Scegli l'abbonamento tra i seguenti: mensile_2v : 35, trimestrale_2v : 90, mensile_3v : 40, trimestrale_3v : 105, open_6m : 200\n> ")
        while not abb in self.abbonamenti.keys():
            abb = input("Abbonamento non trovato, riprova: mensile_2v : 35, trimestrale_2v : 90, mensile_3v : 40, trimestrale_3v : 105, open_6m : 200\n> ") 
        cliente.abbonamento += abb
        self.incasso(self.abbonamenti.get(abb))
        print(self.cassa)
    

    def incasso(self, importo):
        if self.aperta:
            self.cassa += importo
        else:
            print("La palestra è chiusa!")
    
    def uscita(self, importo):
        if self.aperta:
            self.cassa -= importo
        else:
            print("La palestra è chiusa!")

class Cliente:
    def __init__(self, nome, abbonamento = "", in_struttura = False):
        self.nome = nome
        self.abbonamento = abbonamento
        
    def __repr__(self):
        return f"{self.nome} abbonato con {self.abbonamento}"

#Oggetti
wellness = Palestra("Wellness Club", elenco_iscritti = ["Prova"], abbonamenti = {"mensile_2v": 35, "trimestrale_2v": 90, "mensile_3v": 40, "trimestrale_3v": 105, "open_6m": 200}, corsi = ["Pilates", "Walking", "Funzionale", "Yoga"], orari_apertura = {"Monday" : (9,11,16,21), "Tuesday" : (9,11,16,21), "Wednesday" : (9,11,16,21), "Thursday" : (9,11,16,21), "Friday" : (9,11,16,21), "Saturday" : (10,11,16,18)})
#wellness2 = Palestra("Wellness Club", elenco_iscritti = ["Prova"], abbonamenti = {"mensile_2v": 35, "trimestrale_2v": 90, "mensile_3v": 40, "trimestrale_3v": 105, "open_6m": 200}, corsi = ["Pilates", "Walking", "Funzionale", "Yoga"], orari_apertura = {"Monday" : (9,21), "Tuesday" : (9,21), "Wednesday" :(9,21), "Thursday" : (9,21), "Friday" : (9,21), "Saturday" : (10,18)})
#wellness2 test apertura orario continuato, con soli 2 orari al posto di 4 nella lista all'interno del dizionario degli orari

#Script
definisci_momento()
if giorno_sett in wellness.orari_apertura.keys() and (wellness.orari_apertura[giorno_sett][0] <= int(orario[:2]) <= wellness.orari_apertura[giorno_sett][1] or wellness.orari_apertura[giorno_sett][2] <= int(orario[:2]) <= wellness.orari_apertura[giorno_sett][3]):
    wellness.aperta = True
else:
    wellness.aperta = False
print(f"Benvenuto in Wellness Manager, cosa vorresti fare?\n1-apertura\n2-aggiungi cliente")
master_input = input("> ")
while not master_input == "esci":
    if master_input == "apertura" or master_input == "1":
        wellness.apri_chiudi()
    elif master_input == "aggiungi cliente" or master_input == "2": 
        try:
            cliente = crea_cliente(wellness)
            wellness.aggiungi_cliente(cliente)
            print(cliente)
        except:
            print("Errore!")
        
    else:
        print("Input non valido, riprova")
    master_input = input("> ")
    