#Librerie
import datetime

#Variabili globali
data = None
orario = None
giorno = None
mese = None
anno = None
giorno_sett = None
istanze_cliente = {}
istanze_istruttore = {}
istanze_abbonamento = {}

#Funzioni globali
def definisci_momento():
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

    def __init__(self, nome, elenco_iscritti = [], abbonamenti = {}, corsi = [], aperta = False, istruttori = [], cassa = 0, orari_apertura = {}, planning = {}):
        self.nome = nome
        self.nr_iscritti = len(elenco_iscritti)
        self.elenco_iscritti = []
        self.abbonamenti = abbonamenti
        self.corsi = corsi
        self.aperta = aperta
        self.istruttori = istruttori
        self.cassa = cassa
        self.orari_apertura = orari_apertura
        self.planning = planning
        self.diff = 0

    def apri_chiudi(self):
        self.aperta = not self.aperta
        if self.aperta:
            print("La palestra adesso è aperta")
        else:
            print(f"La palestra adesso è chiusa, oggi la palestra ha incassato {self.diff}, il totale disponibile in cassa è {self.cassa}")
    
    def aggiungi_cliente(self, cliente):
        if self.aperta:
            self.elenco_iscritti.append(cliente.nome)
            self.elenco_iscritti.sort()
            #print(self.elenco_iscritti)
            self.nr_iscritti += 1
            abb = input(f"Scegli l'abbonamento tra i seguenti: {self.abbonamenti}\n> ")
            while not abb in self.abbonamenti.keys():
                abb = input(f"Abbonamento non trovato, riprova: {self.abbonamenti}\n> ")
            prezzo = self.abbonamenti[abb]
            abb = abb.split("_")
            istanze_abbonamento[cliente.nome] = Abbonamento(abb[0], prezzo, nr_ingressi = abb[1])
            abb = "_".join(abb)
            cliente.abbonamento += abb
            self.incasso(self.abbonamenti.get(abb))
            #print(self.elenco_iscritti)
            #print(self.cassa)
        else:
            print("La palestra è chiusa!")
    
    def planner(self):
        if giorno_sett in self.orari_apertura.keys():
            orario_ap = min(self.orari_apertura[giorno_sett])
            orario_chius = max(self.orari_apertura[giorno_sett])
            self.planning[data] = { str(x) : []  for x in range(orario_ap, orario_chius)}
            if giorno_sett == "Monday" or giorno_sett == "Wednesday" or giorno_sett == "Friday":
                self.planning[data]["18"].append("Pilates")
            if giorno_sett == "Monday" or giorno_sett == "Wednesday" or giorno_sett == "Friday":
                self.planning[data]["19"].append("Walking")
            if giorno_sett == "Tuesday" or giorno_sett == "Thursday":
                self.planning[data]["18"].append("Yoga")
            if giorno_sett == "Tuesday" or giorno_sett == "Thursday":
                self.planning[data]["19"].append("Funzionale")
            for istruttore in istanze_istruttore:
                if giorno_sett in istanze_istruttore[istruttore].orari.keys():
                    if min(istanze_istruttore[istruttore].orari[giorno_sett]) <= int(orario[:2]) <= max(istanze_istruttore[istruttore].orari[giorno_sett]):
                        istanze_istruttore[istruttore].inizio_fine_turno()
        else:
            return None

    def incasso(self, importo):
        if self.aperta:
            self.cassa += importo
            self.diff += importo
        else:
            print("La palestra è chiusa!")
    
    def uscita(self, importo):
        if self.aperta:
            self.cassa -= importo
            self.diff -= importo
        else:
            print("La palestra è chiusa!")
    
    def crea_cliente(self):
        global istanze_cliente
        if self.aperta:
            nome = input("Insersci il nome completo del cliente:\n> ")
            cliente = Cliente(nome)
            istanze_cliente[nome] = cliente
            return cliente
        else:
            print("La palestra è chiusa!")
    
    def crea_istruttore(self):
        global istanze_istruttore
        if self.aperta:
            nome = input("Insersci il nome completo dell'istruttore:\n> ")
            attivita = input("Inserisci l'attività dell'istruttore\n> ")
            if not attivita in self.corsi:
                self.corsi.append(attivita)
            stipendio = input("Inserisci stipendio mensile istruttore\n> ")
            orari = {"Monday" : (9,21), "Tuesday" : (9,21), "Wednesday" :(9,21), "Thursday" : (9,21), "Friday" : (9,21), "Saturday" : (10,18)}
            istruttore = Istruttore(nome, attivita, stipendio, orari)
            istanze_istruttore[nome] = istruttore
            self.istruttori.append(istruttore.nome)
            self.planner()
            return istruttore
        else:
            print("La palestra è chiusa!")

    def __repr__(self):
        message = f"La {self.nome} è una palestra con {self.nr_iscritti} iscritti, i suoi corsi sono: {self.corsi}\nGli abbonamenti sono: {self.abbonamenti}\nGli istruttori sono: {self.istruttori}\nIl planning di oggi è: {self.planning}\n" + (f"La palestra è aperta adesso! Gli istruttori di turno sono: {self.di_turno()}" if self.aperta else "La palestra al momento è chiusa!")
        return message

    def cerca_cliente(self):
        if self.aperta:
            nome = input("Inserisci il nome  completo del cliente da cercare\n> ")
            if nome in self.elenco_iscritti:
                return True, nome
            else: 
                print("Nome non presente in sistema")
                return False
        else:
            print("La palestra è chiusa!")

    def di_turno(self):
        global istanze_istruttore
        lst = []
        for nome in istanze_istruttore:
            if istanze_istruttore[nome].di_turno == True:
                lst.append(nome)
        return lst

class Cliente:
    def __init__(self, nome, abbonamento = "", in_struttura = False,):
        self.nome = nome
        self.abbonamento = abbonamento
        self.in_struttura = in_struttura
        
    def __repr__(self):
        message = f"{self.nome} abbonato con {self.abbonamento}\n" + (f"{self.nome} al momento è in struttura" if self.in_struttura else f"{self.nome} al momento non è in struttura")
        return message

    def arrivo_uscita_struttura(self):
        self.in_struttura = not self.in_struttura
    
    def prenotazione(self, palestra):
        orario = input("Seleziona l'orario per la prenotazione:\n> ")
        while not len(palestra.planning[data][str(orario)]) <= 6:
            print("Impossibile prenotare, orario pieno")
            orario = input("Seleziona l'orario per la prenotazione:\n> ")
        palestra.planning[data][str(orario)].append(self.nome)
        

class Istruttore:
    def __init__(self, nome, corso = "", stipendio = 0, orari = {}, schede_allenamento = {}, di_turno = False):
        self.nome = nome
        self.corso = corso
        self.stipendio = stipendio
        self.orari = orari
        self.schede_allenamento = schede_allenamento
        self.di_turno = di_turno
    
    def creazione_scheda(self):
        nome = input("Inserire il nome della persona al quale allegare la scheda d'allenamento:\n> ")
        if nome in self.schede_allenamento:
            answer = input("Questo atleta ha già una scheda, vuoi aggiornarla?(s o n)\n> ")
            if answer == "s":
                self.schede_allenamento[nome] = input("Inserire gli esercizi:\n")
            else:
                return self.creazione_scheda()
        else:
            self.schede_allenamento[nome] = input("Inserire gli esercizi:\n")

    def inizio_fine_turno(self):
        self.di_turno = not self.di_turno

    def __repr__(self):
        message = f"{self.nome} è un istruttore di {self.corso}" + (f" {self.nome} al momento è in palestra!" if self.di_turno else f" {self.nome} al momento non è in palstra")
        return message

#Classe implementata nel processo di refactoring
class Abbonamento:
    def __init__(self, nome, prezzo = 0, inizio = data, scadenza = None, attivo = False, nr_ingressi = 0):
        self.nome = nome
        self.prezzo = prezzo
        self.inizio = inizio
        self.scadenza = scadenza
        self.attivo = attivo
        durate = ["mensile", "trimestrale", "semestrale"]
        self.set_durata()
    
    def set_durata(self):
        pass

    def attiva(self):
        pass
    


#Oggetti
wellness = Palestra("Wellness Club", elenco_iscritti = [], abbonamenti = {"mensile_2v": 35, "trimestrale_2v": 90, "mensile_3v": 40, "trimestrale_3v": 105, "open_6m": 200}, corsi = ["Pilates", "Walking", "Funzionale", "Yoga"], orari_apertura = {"Monday" : (9,11,16,21), "Tuesday" : (9,11,16,21), "Wednesday" : (9,11,16,21), "Thursday" : (9,11,16,21), "Friday" : (9,11,16,21), "Saturday" : (10,11,16,18)}, cassa = 3000)
#wellness2 = Palestra("Wellness Club", elenco_iscritti = ["Prova"], abbonamenti = {"mensile_2v": 35, "trimestrale_2v": 90, "mensile_3v": 40, "trimestrale_3v": 105, "open_6m": 200}, corsi = ["Pilates", "Walking", "Funzionale", "Yoga"], orari_apertura = {"Monday" : (9,21), "Tuesday" : (9,21), "Wednesday" :(9,21), "Thursday" : (9,21), "Friday" : (9,21), "Saturday" : (10,18)})
#wellness2 test apertura orario continuato, con soli 2 orari al posto di 4 nella lista all'interno del dizionario degli orari

#Script
definisci_momento()
if giorno_sett in wellness.orari_apertura.keys() and (wellness.orari_apertura[giorno_sett][0] <= int(orario[:2]) <= wellness.orari_apertura[giorno_sett][1] or wellness.orari_apertura[giorno_sett][2] <= int(orario[:2]) <= wellness.orari_apertura[giorno_sett][3]):
    wellness.aperta = True
else:
    wellness.aperta = False
print(f"Benvenuto in Wellness Manager, cosa vorresti fare?\n1-apertura\n2-aggiungi cliente\n3-prenota un allenamento\n4-cerca cliente\n5-aggiungi istruttore\n6-informazioni palestra\n7-informazioni istruttore\n8-creazione scheda allenamento")
wellness.planner()
master_input = input("> ")
while not master_input == "esci":
    if master_input == "apertura" or master_input == "1":
        wellness.apri_chiudi()
    elif master_input == "aggiungi cliente" or master_input == "2": 
        try:
            cliente = wellness.crea_cliente()
            wellness.aggiungi_cliente(cliente)
            print(cliente)
        except:
            print("Errore!")
    elif master_input == "prenota un allenamento" or master_input == "3":
        #wellness.planner() spostato dopo il primo controllo sull'apertura della palestra per avere a disposizione il planning globalmente
        print(wellness.planning) 
        if wellness.cerca_cliente():
            cliente.prenotazione(wellness)
            print(wellness.planning)
        for h in wellness.planning[data]:
            for name in wellness.planning[data][h]:
                if name in wellness.elenco_iscritti:
                    istanze_cliente[name].arrivo_uscita_struttura()
    elif master_input == "cerca cliente" or master_input == "4":#da implementare o togliere
        try:
            cliente = wellness.cerca_cliente()
            print(istanze_cliente[cliente[1]])
        except:
            print("Non è stato possibile trovare il cliente")
    elif master_input == "aggiungi istruttore" or master_input == "5":
        wellness.crea_istruttore()
    elif master_input == "informazioni palestra" or master_input == "6":
        print(wellness)
    elif master_input == "informazioni istruttore" or master_input == "7":
        nome = input("Nome dell'istruttore:\n> ")
        if nome in istanze_istruttore:
            print(istanze_istruttore[nome])
    elif master_input == "creazione scheda allenamento" or master_input == "8":
        nome = input("Nome dell'istruttore:\n> ")
        if nome in istanze_istruttore:
            istanze_istruttore[nome].creazione_scheda()
        else:
            print("Istruttore non trovato!")
    else:
        print("Input non valido, riprova")
    master_input = input("> ")
    