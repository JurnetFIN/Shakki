"""
COMP.CS.100 13.10 Projekti: Graafinen kayttoliittyma: Shakki
Tekijä: Juliusz Kotelba
Opiskelijanumero: 150586775

Tämä ohjelma on Shakki. Tätä peliä voi pelata kahdestaan tai yksin.
Logiikkana on listan luonti, jossa on kahdeksan listaa. Jokainen lista listassa
vastaa siis yhtä vaakariviä laudalla. Sen avulla ohjelma rakentaa grafiikan. Listaa
päivitetään aina kun nappulaa siirretään.

Ohjelma osaa reagoida laittomiin siirtoihin sekä erikoissiirtoihin. Ainoa mitä ohjelma
ei osaa on sotilaan korotus ja shakin tunnistaminen. Olen tietysti yrittänyt tehdö molempia,
mutta yritykset eivät tuottaneet mitään toimivaa.

Ohjelmassa on myös integroidu siirron peruutus, uuden pelin aloittaminen valikosta sekä
lyhyehkö sääntökirja. Sööntökirja on siis luokka luokassa ja sen periaate on näyttää
wikipediasta otettut näyttökuvat kyseisestä aiheesta.

Pyydän tätä arvosteltavaksi kehittyneenä käyttäliittymänä, koska olen tutustunut
itsenäisesti valikkoon ja soveltanut sitä kahdessa paikassa sekä käyttänyt tähän
projektiin tosi poljon vapaa-aikaani.


    Ohjeet:
Peliä pelataan painamalla ensin nappulaa, jota haluaa liikuttaa. Sitten painamalla
ruutua, johon haluaa liikkua. Tai painamalla ruutua, jossa on vastustajan nappula,
syödäkseen se. Sen jälkeen onkin vastustajan vuoro, joka liikkuu samalla tavalla,
mutta liikuttaa omia nappuloita. Ohjelma osaa tunnistaa jos pelaaja pelaa vastustajan
nappuloilla. Ohjelma osaa neuvoa kenen vuoro on ja mitä pitää painaa nytten. Nämä
tiedot löytyvät laudan oikealta puolelta.

Pelissä ei erikseen tule ilmoitus pelin päättymisestä, koska:
a) sen tekiminen veisi järjettömän paljon aikaa
b) käytännössä peli useimmiten päättyy luovutukseen tai sovittuun tasapeliin

Jos haluaa aloittaa pelin uudestaan, voi sen tehö päävalikosta.

Jos sinulla tulee lisäkysymyksiä ohjelmastani voit ottaa yhteyttä osoitteeseen:
juliusz.kotelba(at)tuni.fi
"""
from tkinter import *

class Shakki():
    """
    Pääsilmukka jossa käsitellään koko peli ja kenttä
    """
    def __init__(self):
        """
        Luodaan pääikkuna, sekä menubar, että tarvittavat
        muuttujat peliä varten.

        -> Lähetetään pyyntö shakkilaudan luomiseen
        """
        # Luodaan pääikkuna
        self.__pääikkuna = Tk()

        # Luodaan otsikko
        self.__pääikkuna.title('Shakki')

        # Luodaan menu
        self.__menubar = Menu(self.__pääikkuna)

        # Luodaan asetukset menu
        self.__filemenu = Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Uusi peli", command=self.uusi_peli)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Poistu", command=self.lopeta)
        self.__menubar.add_cascade(label="Asetukset", menu=self.__filemenu)

        # Luodaan apua menu
        self.__helpmenu = Menu(self.__menubar, tearoff=0)
        self.__helpmenu.add_command(label="Peruuta siirto", command=self.peruuta_siirto)
        self.__helpmenu.add_separator()
        self.__helpmenu.add_command(label="Säännöt", command=self.info)
        self.__menubar.add_cascade(label="Apua", menu=self.__helpmenu)

        # Konfiguroitaan menu
        self.__pääikkuna.config(menu=self.__menubar)

        # Luodaan virhe muuttuja
        self.__virhe = None

        # Luodaan tarvittavat nappula muuttujat
        self.__kaksi_ruutu_siirto = None

        # Luodaan kenttä
        self.__kentta = [["TM.png", "HM.png", "LM.png", "QM.png", "KM.png", "LM.png", "HM.png", "TM.png"],
                         ["SM.png", "SM.png", "SM.png", "SM.png", "SM.png", "SM.png", "SM.png", "SM.png"],
                         ["tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png"],
                         ["tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png"],
                         ["tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png"],
                         ["tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png", "tyhja.png"],
                         ["SV.png", "SV.png", "SV.png", "SV.png", "SV.png", "SV.png", "SV.png", "SV.png"],
                         ["TV.png", "HV.png", "LV.png", "QV.png", "KV.png", "LV.png", "HV.png", "TV.png"],
                         # Tämä on silmukoita varten jos silmukan testit menee kentan ulkopuolelle
                         ["tyhja.png"]]

        # Luodaan vari ja vuoro muuttujat
        self.__color = "grey39"
        self.__vuoro = "Valkoisen vuoro"
        self.__paina = "Paina nappulaa jota haluat siirtää!"

        # Luodaan tarvittavat muuttujat
        self.__mista_totta = 0
        self.__mihin_totta = 0

        # Lähetetään pyyntö kentän luomiseen
        self.luo_kenttä()

        # Käynnistetään köyttöliittymä
        self.__pääikkuna.mainloop()

    def luo_kenttä(self):
        """
        Luodaan kuvat sen jälkeen luodaan painikkeet.
        Asetellaan painikkeet kenttään. Lisätään laudan
        sivuille kordinaatti kirjaimet ja numerot.
        Näytetään kenen vuoro on kyseessä, mitä pitää
        nytten painaa sekä luodaan mahdollinen virheilmoitus.
        """

        # Haetaan tarvittavat muuttujat
        vuoro = self.__vuoro

        # Tallennetaan ruudukko
        ruudukko = self.__kentta

        # LUODAAN/PÄIVITETÄÄN KUVAT
        self.__kuvaA8 = PhotoImage(file=ruudukko[0][0])
        self.__kuvaA7 = PhotoImage(file=ruudukko[1][0])
        self.__kuvaA6 = PhotoImage(file=ruudukko[2][0])
        self.__kuvaA5 = PhotoImage(file=ruudukko[3][0])
        self.__kuvaA4 = PhotoImage(file=ruudukko[4][0])
        self.__kuvaA3 = PhotoImage(file=ruudukko[5][0])
        self.__kuvaA2 = PhotoImage(file=ruudukko[6][0])
        self.__kuvaA1 = PhotoImage(file=ruudukko[7][0])
        self.__kuvaB8 = PhotoImage(file=ruudukko[0][1])
        self.__kuvaB7 = PhotoImage(file=ruudukko[1][1])
        self.__kuvaB6 = PhotoImage(file=ruudukko[2][1])
        self.__kuvaB5 = PhotoImage(file=ruudukko[3][1])
        self.__kuvaB4 = PhotoImage(file=ruudukko[4][1])
        self.__kuvaB3 = PhotoImage(file=ruudukko[5][1])
        self.__kuvaB2 = PhotoImage(file=ruudukko[6][1])
        self.__kuvaB1 = PhotoImage(file=ruudukko[7][1])
        self.__kuvaC8 = PhotoImage(file=ruudukko[0][2])
        self.__kuvaC7 = PhotoImage(file=ruudukko[1][2])
        self.__kuvaC6 = PhotoImage(file=ruudukko[2][2])
        self.__kuvaC5 = PhotoImage(file=ruudukko[3][2])
        self.__kuvaC4 = PhotoImage(file=ruudukko[4][2])
        self.__kuvaC3 = PhotoImage(file=ruudukko[5][2])
        self.__kuvaC2 = PhotoImage(file=ruudukko[6][2])
        self.__kuvaC1 = PhotoImage(file=ruudukko[7][2])
        self.__kuvaD8 = PhotoImage(file=ruudukko[0][3])
        self.__kuvaD7 = PhotoImage(file=ruudukko[1][3])
        self.__kuvaD6 = PhotoImage(file=ruudukko[2][3])
        self.__kuvaD5 = PhotoImage(file=ruudukko[3][3])
        self.__kuvaD4 = PhotoImage(file=ruudukko[4][3])
        self.__kuvaD3 = PhotoImage(file=ruudukko[5][3])
        self.__kuvaD2 = PhotoImage(file=ruudukko[6][3])
        self.__kuvaD1 = PhotoImage(file=ruudukko[7][3])
        self.__kuvaE8 = PhotoImage(file=ruudukko[0][4])
        self.__kuvaE7 = PhotoImage(file=ruudukko[1][4])
        self.__kuvaE6 = PhotoImage(file=ruudukko[2][4])
        self.__kuvaE5 = PhotoImage(file=ruudukko[3][4])
        self.__kuvaE4 = PhotoImage(file=ruudukko[4][4])
        self.__kuvaE3 = PhotoImage(file=ruudukko[5][4])
        self.__kuvaE2 = PhotoImage(file=ruudukko[6][4])
        self.__kuvaE1 = PhotoImage(file=ruudukko[7][4])
        self.__kuvaF8 = PhotoImage(file=ruudukko[0][5])
        self.__kuvaF7 = PhotoImage(file=ruudukko[1][5])
        self.__kuvaF6 = PhotoImage(file=ruudukko[2][5])
        self.__kuvaF5 = PhotoImage(file=ruudukko[3][5])
        self.__kuvaF4 = PhotoImage(file=ruudukko[4][5])
        self.__kuvaF3 = PhotoImage(file=ruudukko[5][5])
        self.__kuvaF2 = PhotoImage(file=ruudukko[6][5])
        self.__kuvaF1 = PhotoImage(file=ruudukko[7][5])
        self.__kuvaG8 = PhotoImage(file=ruudukko[0][6])
        self.__kuvaG7 = PhotoImage(file=ruudukko[1][6])
        self.__kuvaG6 = PhotoImage(file=ruudukko[2][6])
        self.__kuvaG5 = PhotoImage(file=ruudukko[3][6])
        self.__kuvaG4 = PhotoImage(file=ruudukko[4][6])
        self.__kuvaG3 = PhotoImage(file=ruudukko[5][6])
        self.__kuvaG2 = PhotoImage(file=ruudukko[6][6])
        self.__kuvaG1 = PhotoImage(file=ruudukko[7][6])
        self.__kuvaH8 = PhotoImage(file=ruudukko[0][7])
        self.__kuvaH7 = PhotoImage(file=ruudukko[1][7])
        self.__kuvaH6 = PhotoImage(file=ruudukko[2][7])
        self.__kuvaH5 = PhotoImage(file=ruudukko[3][7])
        self.__kuvaH4 = PhotoImage(file=ruudukko[4][7])
        self.__kuvaH3 = PhotoImage(file=ruudukko[5][7])
        self.__kuvaH2 = PhotoImage(file=ruudukko[6][7])
        self.__kuvaH1 = PhotoImage(file=ruudukko[7][7])

        # LUODAAN PAINIKKEET ESITIETOJEN AVULLA
        self.__A8 = Button(self.__pääikkuna, image=self.__kuvaA8, background="white", command=self.A8)
        self.__A7 = Button(self.__pääikkuna, image=self.__kuvaA7, background="grey39", command=self.A7)
        self.__A6 = Button(self.__pääikkuna, image=self.__kuvaA6, background="white", command=self.A6)
        self.__A5 = Button(self.__pääikkuna, image=self.__kuvaA5, background="grey39", command=self.A5)
        self.__A4 = Button(self.__pääikkuna, image=self.__kuvaA4, background="white", command=self.A4)
        self.__A3 = Button(self.__pääikkuna, image=self.__kuvaA3, background="grey39", command=self.A3)
        self.__A2 = Button(self.__pääikkuna, image=self.__kuvaA2, background="white", command=self.A2)
        self.__A1 = Button(self.__pääikkuna, image=self.__kuvaA1, background="grey39", command=self.A1)
        self.__B8 = Button(self.__pääikkuna, image=self.__kuvaB8, background="grey39", command=self.B8)
        self.__B7 = Button(self.__pääikkuna, image=self.__kuvaB7, background="white", command=self.B7)
        self.__B6 = Button(self.__pääikkuna, image=self.__kuvaB6, background="grey39", command=self.B6)
        self.__B5 = Button(self.__pääikkuna, image=self.__kuvaB5, background="white", command=self.B5)
        self.__B4 = Button(self.__pääikkuna, image=self.__kuvaB4, background="grey39", command=self.B4)
        self.__B3 = Button(self.__pääikkuna, image=self.__kuvaB3, background="white", command=self.B3)
        self.__B2 = Button(self.__pääikkuna, image=self.__kuvaB2, background="grey39", command=self.B2)
        self.__B1 = Button(self.__pääikkuna, image=self.__kuvaB1, background="white", command=self.B1)
        self.__C8 = Button(self.__pääikkuna, image=self.__kuvaC8, background="white", command=self.C8)
        self.__C7 = Button(self.__pääikkuna, image=self.__kuvaC7, background="grey39", command=self.C7)
        self.__C6 = Button(self.__pääikkuna, image=self.__kuvaC6, background="white", command=self.C6)
        self.__C5 = Button(self.__pääikkuna, image=self.__kuvaC5, background="grey39", command=self.C5)
        self.__C4 = Button(self.__pääikkuna, image=self.__kuvaC4, background="white", command=self.C4)
        self.__C3 = Button(self.__pääikkuna, image=self.__kuvaC3, background="grey39", command=self.C3)
        self.__C2 = Button(self.__pääikkuna, image=self.__kuvaC2, background="white", command=self.C2)
        self.__C1 = Button(self.__pääikkuna, image=self.__kuvaC1, background="grey39", command=self.C1)
        self.__D8 = Button(self.__pääikkuna, image=self.__kuvaD8, background="grey39", command=self.D8)
        self.__D7 = Button(self.__pääikkuna, image=self.__kuvaD7, background="white", command=self.D7)
        self.__D6 = Button(self.__pääikkuna, image=self.__kuvaD6, background="grey39", command=self.D6)
        self.__D5 = Button(self.__pääikkuna, image=self.__kuvaD5, background="white", command=self.D5)
        self.__D4 = Button(self.__pääikkuna, image=self.__kuvaD4, background="grey39", command=self.D4)
        self.__D3 = Button(self.__pääikkuna, image=self.__kuvaD3, background="white", command=self.D3)
        self.__D2 = Button(self.__pääikkuna, image=self.__kuvaD2, background="grey39", command=self.D2)
        self.__D1 = Button(self.__pääikkuna, image=self.__kuvaD1, background="white", command=self.D1)
        self.__E8 = Button(self.__pääikkuna, image=self.__kuvaE8, background="white", command=self.E8)
        self.__E7 = Button(self.__pääikkuna, image=self.__kuvaE7, background="grey39", command=self.E7)
        self.__E6 = Button(self.__pääikkuna, image=self.__kuvaE6, background="white", command=self.E6)
        self.__E5 = Button(self.__pääikkuna, image=self.__kuvaE5, background="grey39", command=self.E5)
        self.__E4 = Button(self.__pääikkuna, image=self.__kuvaE4, background="white", command=self.E4)
        self.__E3 = Button(self.__pääikkuna, image=self.__kuvaE3, background="grey39", command=self.E3)
        self.__E2 = Button(self.__pääikkuna, image=self.__kuvaE2, background="white", command=self.E2)
        self.__E1 = Button(self.__pääikkuna, image=self.__kuvaE1, background="grey39", command=self.E1)
        self.__F8 = Button(self.__pääikkuna, image=self.__kuvaF8, background="grey39", command=self.F8)
        self.__F7 = Button(self.__pääikkuna, image=self.__kuvaF7, background="white", command=self.F7)
        self.__F6 = Button(self.__pääikkuna, image=self.__kuvaF6, background="grey39", command=self.F6)
        self.__F5 = Button(self.__pääikkuna, image=self.__kuvaF5, background="white", command=self.F5)
        self.__F4 = Button(self.__pääikkuna, image=self.__kuvaF4, background="grey39", command=self.F4)
        self.__F3 = Button(self.__pääikkuna, image=self.__kuvaF3, background="white", command=self.F3)
        self.__F2 = Button(self.__pääikkuna, image=self.__kuvaF2, background="grey39", command=self.F2)
        self.__F1 = Button(self.__pääikkuna, image=self.__kuvaF1, background="white", command=self.F1)
        self.__G8 = Button(self.__pääikkuna, image=self.__kuvaG8, background="white", command=self.G8)
        self.__G7 = Button(self.__pääikkuna, image=self.__kuvaG7, background="grey39", command=self.G7)
        self.__G6 = Button(self.__pääikkuna, image=self.__kuvaG6, background="white", command=self.G6)
        self.__G5 = Button(self.__pääikkuna, image=self.__kuvaG5, background="grey39", command=self.G5)
        self.__G4 = Button(self.__pääikkuna, image=self.__kuvaG4, background="white", command=self.G4)
        self.__G3 = Button(self.__pääikkuna, image=self.__kuvaG3, background="grey39", command=self.G3)
        self.__G2 = Button(self.__pääikkuna, image=self.__kuvaG2, background="white", command=self.G2)
        self.__G1 = Button(self.__pääikkuna, image=self.__kuvaG1, background="grey39", command=self.G1)
        self.__H8 = Button(self.__pääikkuna, image=self.__kuvaH8, background="grey39", command=self.H8)
        self.__H7 = Button(self.__pääikkuna, image=self.__kuvaH7, background="white", command=self.H7)
        self.__H6 = Button(self.__pääikkuna, image=self.__kuvaH6, background="grey39", command=self.H6)
        self.__H5 = Button(self.__pääikkuna, image=self.__kuvaH5, background="white", command=self.H5)
        self.__H4 = Button(self.__pääikkuna, image=self.__kuvaH4, background="grey39", command=self.H4)
        self.__H3 = Button(self.__pääikkuna, image=self.__kuvaH3, background="white", command=self.H3)
        self.__H2 = Button(self.__pääikkuna, image=self.__kuvaH2, background="grey39", command=self.H2)
        self.__H1 = Button(self.__pääikkuna, image=self.__kuvaH1, background="white", command=self.H1)

        # Sijoitellaan painikkeet oikeille paikoille
        self.__A8.grid(row=0, column=0)
        self.__A7.grid(row=1, column=0)
        self.__A6.grid(row=2, column=0)
        self.__A5.grid(row=3, column=0)
        self.__A4.grid(row=4, column=0)
        self.__A3.grid(row=5, column=0)
        self.__A2.grid(row=6, column=0)
        self.__A1.grid(row=7, column=0)
        self.__B8.grid(row=0, column=1)
        self.__B7.grid(row=1, column=1)
        self.__B6.grid(row=2, column=1)
        self.__B5.grid(row=3, column=1)
        self.__B4.grid(row=4, column=1)
        self.__B3.grid(row=5, column=1)
        self.__B2.grid(row=6, column=1)
        self.__B1.grid(row=7, column=1)
        self.__C8.grid(row=0, column=2)
        self.__C7.grid(row=1, column=2)
        self.__C6.grid(row=2, column=2)
        self.__C5.grid(row=3, column=2)
        self.__C4.grid(row=4, column=2)
        self.__C3.grid(row=5, column=2)
        self.__C2.grid(row=6, column=2)
        self.__C1.grid(row=7, column=2)
        self.__D8.grid(row=0, column=3)
        self.__D7.grid(row=1, column=3)
        self.__D6.grid(row=2, column=3)
        self.__D5.grid(row=3, column=3)
        self.__D4.grid(row=4, column=3)
        self.__D3.grid(row=5, column=3)
        self.__D2.grid(row=6, column=3)
        self.__D1.grid(row=7, column=3)
        self.__E8.grid(row=0, column=4)
        self.__E7.grid(row=1, column=4)
        self.__E6.grid(row=2, column=4)
        self.__E5.grid(row=3, column=4)
        self.__E4.grid(row=4, column=4)
        self.__E3.grid(row=5, column=4)
        self.__E2.grid(row=6, column=4)
        self.__E1.grid(row=7, column=4)
        self.__F8.grid(row=0, column=5)
        self.__F7.grid(row=1, column=5)
        self.__F6.grid(row=2, column=5)
        self.__F5.grid(row=3, column=5)
        self.__F4.grid(row=4, column=5)
        self.__F3.grid(row=5, column=5)
        self.__F2.grid(row=6, column=5)
        self.__F1.grid(row=7, column=5)
        self.__G8.grid(row=0, column=6)
        self.__G7.grid(row=1, column=6)
        self.__G6.grid(row=2, column=6)
        self.__G5.grid(row=3, column=6)
        self.__G4.grid(row=4, column=6)
        self.__G3.grid(row=5, column=6)
        self.__G2.grid(row=6, column=6)
        self.__G1.grid(row=7, column=6)
        self.__H8.grid(row=0, column=7)
        self.__H7.grid(row=1, column=7)
        self.__H6.grid(row=2, column=7)
        self.__H5.grid(row=3, column=7)
        self.__H4.grid(row=4, column=7)
        self.__H3.grid(row=5, column=7)
        self.__H2.grid(row=6, column=7)
        self.__H1.grid(row=7, column=7)

        # Luodaan kirjaimet ja numerot laudan sivuille
        # Ensin kirjaimet
        kirjaimet = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for a in range(0, 8):
            self.__kirjain = Label(self.__pääikkuna, text=kirjaimet[a])
            self.__kirjain.grid(row=8, column=a)

        # Sitten numerot
        numerot = ["8", "7", "6", "5", "4", "3", "2", "1"]
        for a in range(0, 8):
            self.__numerot = Label(self.__pääikkuna, text=numerot[a])
            self.__numerot.grid(row=a, column=8)

        # Yliviivataan kenen vuoro
        ei_mitaan = " " * 75
        self.__yliviiva_vuoro = Label(self.__pääikkuna, text=ei_mitaan)
        self.__yliviiva_vuoro.grid(row=3, column=9, columnspan=2)

        # Yliviivataan mita painaa
        self.__yliviiva_mita_painaa = Label(self.__pääikkuna, text=ei_mitaan)
        self.__yliviiva_mita_painaa.grid(row=4, column=9, columnspan=2)

        # Yliviivataan mahdollinen virheilmoitus
        # Tämä siksi, että voi olla esimerkiki kaksi virhettä
        # peräkkäin jolloin pitää yliviivata aiempi.
        self.__yliviiva_virhe = Label(self.__pääikkuna, text=ei_mitaan)
        self.__yliviiva_virhe.grid(row=5, column=9, columnspan=2)

        # Tulostetaan kenen vuoro on kyseessä
        self.__teksti1 = Label(self.__pääikkuna, text=vuoro, background="azure")
        self.__teksti1.grid(row=3, column=9, columnspan=2)

        # Tulostetaan ohje mitä painaa
        self.__teksti2 = Label(self.__pääikkuna, text=self.__paina, background="azure")
        self.__teksti2.grid(row=4, column=9, columnspan=2)

        # Tulostetaan mahdollinen virheilmoitus
        if self.__virhe == None:
            pass
        else:
            self.__virhe_tulostus = Label(self.__pääikkuna, text=self.__virhe, background="red")
            self.__virhe_tulostus.grid(row=5, column=9, columnspan=2)

    # KAIKKI ALLA OLEVAT (def [kirjain][numero](self):)
    # LÄHETTÄVÄT TIEDON OMASTA KORDINAATISTAAN
    def A8(self):
        self.__sana = "A8"
        self.sana()
    def A7(self):
        self.__sana = "A7"
        self.sana()
    def A6(self):
        self.__sana = "A6"
        self.sana()
    def A5(self):
        self.__sana = "A5"
        self.sana()
    def A4(self):
        self.__sana = "A4"
        self.sana()
    def A3(self):
        self.__sana = "A3"
        self.sana()
    def A2(self):
        self.__sana = "A2"
        self.sana()
    def A1(self):
        self.__sana = "A1"
        self.sana()
    def B8(self):
        self.__sana = "B8"
        self.sana()
    def B7(self):
        self.__sana = "B7"
        self.sana()
    def B6(self):
        self.__sana = "B6"
        self.sana()
    def B5(self):
        self.__sana = "B5"
        self.sana()
    def B4(self):
        self.__sana = "B4"
        self.sana()
    def B3(self):
        self.__sana = "B3"
        self.sana()
    def B2(self):
        self.__sana = "B2"
        self.sana()
    def B1(self):
        self.__sana = "B1"
        self.sana()
    def C8(self):
        self.__sana = "C8"
        self.sana()
    def C7(self):
        self.__sana = "C7"
        self.sana()
    def C6(self):
        self.__sana = "C6"
        self.sana()
    def C5(self):
        self.__sana = "C5"
        self.sana()
    def C4(self):
        self.__sana = "C4"
        self.sana()
    def C3(self):
        self.__sana = "C3"
        self.sana()
    def C2(self):
        self.__sana = "C2"
        self.sana()
    def C1(self):
        self.__sana = "C1"
        self.sana()
    def D8(self):
        self.__sana = "D8"
        self.sana()
    def D7(self):
        self.__sana = "D7"
        self.sana()
    def D6(self):
        self.__sana = "D6"
        self.sana()
    def D5(self):
        self.__sana = "D5"
        self.sana()
    def D4(self):
        self.__sana = "D4"
        self.sana()
    def D3(self):
        self.__sana = "D3"
        self.sana()
    def D2(self):
        self.__sana = "D2"
        self.sana()
    def D1(self):
        self.__sana = "D1"
        self.sana()
    def E8(self):
        self.__sana = "E8"
        self.sana()
    def E7(self):
        self.__sana = "E7"
        self.sana()
    def E6(self):
        self.__sana = "E6"
        self.sana()
    def E5(self):
        self.__sana = "E5"
        self.sana()
    def E4(self):
        self.__sana = "E4"
        self.sana()
    def E3(self):
        self.__sana = "E3"
        self.sana()
    def E2(self):
        self.__sana = "E2"
        self.sana()
    def E1(self):
        self.__sana = "E1"
        self.sana()
    def F8(self):
        self.__sana = "F8"
        self.sana()
    def F7(self):
        self.__sana = "F7"
        self.sana()
    def F6(self):
        self.__sana = "F6"
        self.sana()
    def F5(self):
        self.__sana = "F5"
        self.sana()
    def F4(self):
        self.__sana = "F4"
        self.sana()
    def F3(self):
        self.__sana = "F3"
        self.sana()
    def F2(self):
        self.__sana = "F2"
        self.sana()
    def F1(self):
        self.__sana = "F1"
        self.sana()
    def G8(self):
        self.__sana = "G8"
        self.sana()
    def G7(self):
        self.__sana = "G7"
        self.sana()
    def G6(self):
        self.__sana = "G6"
        self.sana()
    def G5(self):
        self.__sana = "G5"
        self.sana()
    def G4(self):
        self.__sana = "G4"
        self.sana()
    def G3(self):
        self.__sana = "G3"
        self.sana()
    def G2(self):
        self.__sana = "G2"
        self.sana()
    def G1(self):
        self.__sana = "G1"
        self.sana()
    def H8(self):
        self.__sana = "H8"
        self.sana()
    def H7(self):
        self.__sana = "H7"
        self.sana()
    def H6(self):
        self.__sana = "H6"
        self.sana()
    def H5(self):
        self.__sana = "H5"
        self.sana()
    def H4(self):
        self.__sana = "H4"
        self.sana()
    def H3(self):
        self.__sana = "H3"
        self.sana()
    def H2(self):
        self.__sana = "H2"
        self.sana()
    def H1(self):
        self.__sana = "H1"
        self.sana()


    def sana(self):
        """
        Tallennetaan lähtö- ja loppukordinaatit.

        Jos molemmat ovat tallennettuja; lähetetään pyyntö
        siirtää nappulat ja nollata lähdö- ja loppukordinaatit.
        """
        # Tallennetaan lähtökordinaatti, jos tyhjä.
        if self.__mista_totta == 0:
            self.__mista = self.__sana
            self.__mista_totta = 1
            self.mita_painaa()

        # Tallennetaan loppukordinaatti, jos tyhjä.
        elif self.__mihin_totta == 0:
            self.__mihin = self.__sana
            self.__mihin_totta = 1
            self.mita_painaa()

        # Jos molemmat lähtö- ja loppukordinaatit ovat
        # täytettyjä, lähetään siirto pyyntö.
        if self.__mista_totta == 1 and self.__mihin_totta == 1:
            self.__mista_totta = 0
            self.__mihin_totta = 0
            self.siirra()

    def siirra(self):
        """
        Toteutetaan siirto:
        Ensin muutetaan kirjain numeroksi sekä numero oikeaksi numeroksi.
        Sen jälkeen haetaan kenttä lista ja tarkistetaan nappula. Sen
        jälkeen tarkistetaan onko siirto laininen. Jos siirto on laillinen
        tallennetaan uudet sijainnit
        """
        # Tehdään lista, jonka avulla voimme vaihtaa kirjaimet numeroksi
        kirjaimet   = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numerot     = ["8", "7", "6", "5", "4", "3", "2", "1"]

        # Eritellään kirjaimet ja numerot toisistaan
        mista = self.__mista
        mihin = self.__mihin
        mista_kirjain = mista[:1]
        mista_numero = mista[1:]
        mihin_kirjain = mihin[:1]
        mihin_numero = mihin[1:]

        # Vaihdetaan kirjaimet ja numerot tarvittavaan muotoon
        # Vaihdetaan lähtökirjain numeroksi
        for i in range(0, 8):
            if mista_kirjain == kirjaimet[i]:
                mista_kirjain = i
                break

        # Vaihdetaan maalikirjain numeroksi
        for i in range(0, 8):
            if mihin_kirjain == kirjaimet[i]:
                mihin_kirjain = i
                break

        # Vaihdetaan lähtönumero oikeaan numeroon
        for i in range(0, 8):
            if mista_numero == numerot[i]:
                mista_numero = i
                break

        # Vaihdetaan maalinumero oikeaan numeroon
        for i in range(0, 8):
            if mihin_numero == numerot[i]:
                mihin_numero = i
                break

        # Haetaan kentta
        ruudukko = self.__kentta
        self.__nappula = ruudukko[mista_numero][mista_kirjain]

        # Tallennetaan muuttujat liikkeen toteuttamista ja mahdollista perumista varten
        self.__mista_numero     = mista_numero
        self.__mista_kirjain    = mista_kirjain
        self.__mihin_numero     = mihin_numero
        self.__mihin_kirjain    = mihin_kirjain
        self.__mista_nappula    = ruudukko[mista_numero][mista_kirjain]
        self.__mihin_nappula    = ruudukko[mihin_numero][mihin_kirjain]

        # Tarkistetaan pelaako pelaaja omilla nappuloilla
        self.__tarkistettava_nappula = self.__nappula
        self.tarkista_nappula()

        # Tarkistetaan onko liike laillinen
        # Tämä silmukka toteutuu vain jos on mitä tarkistaa vrt. aiempi rivi.
        self.__liike_laillinen = False
        if self.__tarkistettava_nappula == True:
            self.__tarkistettava_liike = self.__nappula
            self.tarkista_laillisuus()

        #self.__shakissa = False
        #if self.__liike_laillinen == True:
        #    pass

        # Tallennetaan uudet sijainnit jos aiemmat ehdot töyttyvät.
        # Tämä silmukka toteutuu vain jos liike on laillinen.
        if self.__liike_laillinen == True:
            ruudukko[mista_numero][mista_kirjain] = "tyhja.png"
            ruudukko[mihin_numero][mihin_kirjain] = self.__nappula
            self.__kentta = ruudukko
            self.kenen_vuoro()

            # Tarkistus mielisesti
            self.__virhe = None

        # Lopuksi päivitetään kenttä
        self.luo_kenttä()

    def mita_painaa(self):
        """
        Päivitetään ohjeet mitä pitää painaa sekä
        poistetaan mahdollinen aiempi virheilmoitus.
        """
        if self.__paina == "Paina nappulaa jota haluat siirtää!":
            self.__paina = "Paina ruutua johon haluat siirtää nappula!"
            self.__virhe = None

        elif self.__paina == "Paina ruutua johon haluat siirtää nappula!":
            self.__paina = "Paina nappulaa jota haluat siirtää!"

        self.luo_kenttä()

    def kenen_vuoro(self):
        """
        Selvitetaan kenen vuoro on kyseessa.

        :return self.__vuoro = Valkoinen TAI Musta
        """
        if self.__vuoro == "Valkoisen vuoro":
            self.__vuoro = "Mustan vuoro"
        elif self.__vuoro == "Mustan vuoro":
            self.__vuoro = "Valkoisen vuoro"

    def tarkista_nappula(self):
        """
        - Tarkistetaan pelaako pelaaja omilla nappuloilla siis pelaako musta
            tai valkoinen omalla vuorollaan omilla nappuloilla.
        - Tarkistetaan onko ruutu tyhjä, jos on -> tulostetaan virheilmoitus.

        :return self.__tarkistettava_nappula = True or False
        """
        # Tallennetaan kenen vuoro
        kuka_pelaa = self.__vuoro
        if kuka_pelaa == "Mustan vuoro":
            kuka_pelaa = "M"
        elif kuka_pelaa == "Valkoisen vuoro":
            kuka_pelaa = "V"

        # Tarkistetaan toteutuuko ehto
        if self.__tarkistettava_nappula[1:2] == kuka_pelaa:
            self.__tarkistettava_nappula = True

        # Jos ei toteudu niin tarkistetaan onko ruutu
        # kenties tyhja.
        elif self.__tarkistettava_nappula == "tyhja.png":
            self.__virhe = "Ei mitään siirrettävää!"
            self.__tarkistettava_nappula = False

        # Muulloin ruudussa sijaitsee vastustajan nappula
        else:
            self.__virhe = "Älä pelaa vastustajan puolesta!"
            self.__tarkistettava_nappula = False

    def tarkista_laillisuus(self):
        """
        Ohjataan kyseisen nappulan liikkeen laillisuustarkastukseen
        TAI tulostetaan virhe, jos jonkin takia sitö ei huomattu aiemmin.
        """
        pelattava_liike = self.__tarkistettava_liike[:1]
        if pelattava_liike == "S":
            self.sotilas()
        elif pelattava_liike == "T":
            self.torni()
        elif pelattava_liike == "H":
            self.hevonen()
        elif pelattava_liike == "L":
            self.lahetti()
        elif pelattava_liike == "Q":
            self.kuningatar()
        elif pelattava_liike == "K":
            self.kuningas()
        else:
            self.__virhe = "Tunnistamaton nappula..."

    def sotilas(self):
        """
        Tutkitaan sotilaan siirron laillisuutta

        - Lasketaan mahdolliset lailliset liikkeet
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit.
        - Palautetaan virhe tai "liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan tarvittavat tiedot
        mista_kirjain = self.__mista_kirjain
        mista_numero = self.__mista_numero
        mihin_kirjain = self.__mihin_kirjain
        mihin_numero = self.__mihin_numero

        # Jos sotilas on valkoinen
        if self.__tarkistettava_liike[1:2] == "V":
            # Muodostetaan tutkittavat sijainnit
            yksi_ruutu_siirto = mista_numero - 1
            kaksi_ruutu_siirto = mista_numero - 2
            lyonti_vasemmalle = mista_kirjain - 1
            lyonti_oikealle = mista_kirjain + 1
            # Muodostetaan uudet tarvittavat muuttujat
            lahtoruutu = 6
            vastustaja = "M.png"
            kaksois_siirto = 3
            paaty = 0

        # Jos sotilas on musta
        elif self.__tarkistettava_liike[1:2] == "M":
            # Muodostetaan tutkittavat sijainnit
            yksi_ruutu_siirto = mista_numero + 1
            kaksi_ruutu_siirto = mista_numero + 2
            lyonti_vasemmalle = mista_kirjain + 1
            lyonti_oikealle = mista_kirjain - 1
            # Muodostetaan uudet tarvittavat muuttujat
            lahtoruutu = 1
            vastustaja = "V.png"
            kaksois_siirto = 4
            paaty = 7

        # Tarkistetaan lyötävät sijainnit
        ruudukko = self.__kentta
        lyotava = ruudukko[mihin_numero][mihin_kirjain]
        edessa = lyotava

        # Kaksi ruutua eteenpäin jos sotilas sijaitsee lahtoruudussa
        if mista_numero == lahtoruutu and kaksi_ruutu_siirto == mihin_numero and\
                mista_kirjain == mihin_kirjain and edessa == "tyhja.png":
            self.__liike_laillinen = True
            self.__kaksi_ruutu_siirto = True

        # Lyönti vasemmalle
        elif yksi_ruutu_siirto == mihin_numero and lyonti_vasemmalle == \
                mihin_kirjain and lyotava[1:] == vastustaja:
            self.__liike_laillinen = True

        # Lyönti oikealle
        elif yksi_ruutu_siirto == mihin_numero and lyonti_oikealle == mihin_kirjain\
                and lyotava[1:] == vastustaja:
            self.__liike_laillinen = True

        # Liike eteenpäin
        elif yksi_ruutu_siirto == mihin_numero and mista_kirjain == mihin_kirjain\
                and edessa == "tyhja.png":
            self.__liike_laillinen = True

        # Jos kyseessä on ohestalyönti
        elif self.__kaksi_ruutu_siirto == True:
            # Haetaan lyötävä nappula
            lyotava = ruudukko[kaksois_siirto][mihin_kirjain]

            # Vasemmalle
            if mista_numero == kaksois_siirto and lyonti_vasemmalle == mihin_kirjain\
                and lyotava[1:] == vastustaja and lyotava[:1] == "S":
                self.__liike_laillinen = True

            # Oikealle
            elif mista_numero == kaksois_siirto and lyonti_oikealle == mihin_kirjain\
                and lyotava[1:] == vastustaja and lyotava[:1] == "S":
                self.__liike_laillinen = True

            # Tallenetaan tämä mahdollista siirron perumista varten
            if self.__liike_laillinen == True:
                ruudukko[kaksois_siirto][mihin_kirjain] = lyotava
                self.__mihin_nappula = ruudukko[kaksois_siirto][mihin_kirjain]
                ruudukko[kaksois_siirto][mihin_kirjain] = "tyhja.png"
                self.__kentta = ruudukko

            # Nollataan kaksi ruutu siirto
            self.__kaksi_ruutu_siirto = False

        # Muulloin -> Laiton siirto -> Virhetulostus
        else:
            self.__virhe = "Laiton siirto!"

        # Jos pelaaja ei liikuttanut nappulaa
        if mista_numero == mihin_numero and mista_kirjain == mihin_kirjain:
            self.__virhe = "Et siirtänyt nappulaa!"


    def torni(self):
        """
        Tutkitaan tornin siirron laillisuutta

        - Tarkistetaan onko "mihin" kordinaatit samat kuin lähtökordinaatit
            Tämä toteutetaan "neljässä" silmukassa tutkittaen jokaisen suunnan.
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        mista_kirjain = int(self.__mista_kirjain)
        mista_numero = int(self.__mista_numero)
        mihin_kirjain = int(self.__mihin_kirjain)
        mihin_numero = int(self.__mihin_numero)
        ruudukko = self.__kentta

        # Pelaajan tiedot:
        if self.__tarkistettava_liike[1:2] == "V":
            omat = "V"
            vastustaja = "M"
        elif self.__tarkistettava_liike[1:2] == "M":
            omat = "M"
            vastustaja = "V"

        # Lasketaan laskut
        sivuille = mista_kirjain - mihin_kirjain
        ylos_alas = mista_numero - mihin_numero

        # Vasemmalle
        if sivuille > 0:
            sivuille = True
            laskutoimitus = -1
        # Oikealle
        elif sivuille < 0:
            sivuille = True
            laskutoimitus = +1
        # Muulloin liike ei ole sivuille
        else:
            sivuille = False

        # Ylos
        if ylos_alas > 0:
            ylos_alas = True
            laskutoimitus = -1
        # Alas
        elif ylos_alas < 0:
            ylos_alas = True
            laskutoimitus = +1
        # Muulloin liike ei ole ylos tai alas.
        else:
            ylos_alas = False

        # Muodostetaan testi muuttujat
        mihin_kirjain_testi = mista_kirjain
        mihin_numero_testi = mista_numero

        # Sivuille
        if sivuille == True:
            for i in range(0, 7):
                # Testi joko kattoo jokaisen ruudun kerrallaan
                mihin_kirjain_testi = mihin_kirjain_testi + laskutoimitus
                lyotava = ruudukko[mista_numero][mihin_kirjain_testi]

                # Listan ulkopuolella
                if mihin_kirjain_testi == -1 or mihin_kirjain_testi == 8:
                    self.__virhe = "Laiton siirto!"
                    break

                # Jos testi on yhtäsuuri kuin määränpää
                if mihin_kirjain_testi == mihin_kirjain:
                    # Tarkistetaan mikä sijaitsee määränpäässä
                    # Jos vastustaja -> lyönti
                    if lyotava == "KM.png" or lyotava == "KV.png":
                        self.__liike_laillinen = False
                    elif lyotava[1:2] == vastustaja:
                        self.__liike_laillinen = True
                    # Jos tyhjä -> laillinen
                    elif lyotava == "tyhja.png":
                        self.__liike_laillinen = True
                    # Muulloin on ruudussa oma nappula -> Laiton siirto
                    else:
                        self.__virhe = "Laiton siirto!"
                    break

                # Tarkistetaan onko joku nappula tiellä
                if lyotava == "tyhja.png":
                    pass
                else:
                    self.__virhe = "Laiton siirto!"
                    break

        # Ylos tai alas
        elif ylos_alas == True:
            for i in range(0, 7):
                # Testi joko kattoo jokaisen ruudun kerrallaan
                mihin_numero_testi = mihin_numero_testi + laskutoimitus
                lyotava = ruudukko[mihin_numero_testi][mista_kirjain]

                # Kentän ulkopuolella
                if mihin_numero_testi == -1 or mihin_numero_testi == 8:
                    self.__virhe = "Laiton siirto!"
                    break

                # Jos testi on yhtä suuri kuin määränpää
                if mihin_numero_testi == mihin_numero:
                    # Tarkistetaan mikä sijaitsee määränpäässä
                    # Jos vastustaja -> lyönti
                    if lyotava == "KM.png" or lyotava == "KV.png":
                        self.__liike_laillinen = False
                    elif lyotava[1:2] == vastustaja:
                        self.__liike_laillinen = True
                    # Jos tyhjä -> laillinen
                    elif lyotava == "tyhja.png":
                        self.__liike_laillinen = True
                    # Muulloin on ruudussa oma nappula -> Laiton siirto
                    else:
                        self.__virhe = "Laiton siirto!"
                    break

                # Tarkistetaan onko joku nappula tiellä
                if lyotava == "tyhja.png":
                    pass
                else:
                    self.__virhe = "Laiton siirto!"
                    self.__liike_laillinen = False
                    break

        # Jos pelaaja ei liikuttanut nappulaa
        else:
            self.__virhe = "Et siirtänyt nappulaa!"

    def hevonen(self):
        """
        Tutkitaan hevosen siirron laillisuutta

        - Lasketaan mahdolliset lailliset liikkeet -> kahdeksan mahdollisuutta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan muuttujat
        mista_kirjain = int(self.__mista_kirjain)
        mista_numero = int(self.__mista_numero)
        mihin_kirjain = int(self.__mihin_kirjain)
        mihin_numero = int(self.__mihin_numero)
        ruudukko = self.__kentta
        lyotava = None

        # Pelaajan tiedot:
        if self.__tarkistettava_liike[1:2] == "V":
            vastustaja = "M.png"
        elif self.__tarkistettava_liike[1:2] == "M":
            vastustaja = "V.png"

        # Pohjois-koillinen
        nne_mihin_kirjain = mista_kirjain + 1
        nne_mihin_numero = mista_numero - 2
        if nne_mihin_kirjain == mihin_kirjain and nne_mihin_numero == mihin_numero:
            lyotava = ruudukko[nne_mihin_numero][nne_mihin_kirjain][1:]

        # Itä-koillinen
        ene_mihin_kirjain = mista_kirjain + 2
        ene_mihin_numero = mista_numero - 1
        if ene_mihin_kirjain == mihin_kirjain and ene_mihin_numero == mihin_numero:
            lyotava = ruudukko[ene_mihin_numero][ene_mihin_kirjain][1:]

        # Itä-kaakko
        ese_mihin_kirjain = mista_kirjain + 2
        ese_mihin_numero = mista_numero + 1
        if ese_mihin_kirjain == mihin_kirjain and ese_mihin_numero == mihin_numero:
            lyotava = ruudukko[ese_mihin_numero][ese_mihin_kirjain][1:]

        # Etelä-kaakko
        sse_mihin_kirjain = mista_kirjain + 1
        sse_mihin_numero = mista_numero + 2
        if sse_mihin_kirjain == mihin_kirjain and sse_mihin_numero == mihin_numero:
            lyotava = ruudukko[sse_mihin_numero][sse_mihin_kirjain][1:]

        # Etelä-lounas
        ssw_mihin_kirjain = mista_kirjain - 1
        ssw_mihin_numero = mista_numero + 2
        if ssw_mihin_kirjain == mihin_kirjain and ssw_mihin_numero == mihin_numero:
            lyotava = ruudukko[ssw_mihin_numero][ssw_mihin_kirjain][1:]

        # Länsi-lounas
        wew_mihin_kirjain = mista_kirjain - 2
        wew_mihin_numero = mista_numero + 1
        if wew_mihin_kirjain == mihin_kirjain and wew_mihin_numero == mihin_numero:
            lyotava = ruudukko[wew_mihin_numero][wew_mihin_kirjain][1:]

        # Länsi-luode
        wnw_mihin_kirjain = mista_kirjain - 2
        wnw_mihin_numero = mista_numero -1
        if wnw_mihin_kirjain == mihin_kirjain and wnw_mihin_numero == mihin_numero:
            lyotava = ruudukko[wnw_mihin_numero][wnw_mihin_kirjain][1:]

        # Pohjoinen-luode
        nnw_mihin_kirjain = mista_kirjain - 1
        nnw_mihin_numero = mista_numero - 2
        if nnw_mihin_kirjain == mihin_kirjain and nnw_mihin_numero == mihin_numero:
            lyotava = ruudukko[nnw_mihin_numero][nnw_mihin_kirjain][1:]

        # Tarkistetaan onko liike laillinen
        if lyotava == "yhja.png":
            self.__liike_laillinen = True
        elif lyotava == "KM.png" or lyotava == "KV.png":
            self.__liike_laillinen = False
        elif lyotava == vastustaja:
            self.__liike_laillinen = True
        # Jos pelaaja ei liikuttanut nappulaa
        elif mista_numero == mihin_numero and mista_kirjain == mihin_kirjain:
            self.__virhe = "Et siirtänyt nappulaa!"
        else:
            self.__virhe = "Laiton siirto!"

    def lahetti(self):
        """
        Tutkitaan lahetin siirron laillisuutta

        - Tutkitaan silmukalla jokainen neljästä suunnasta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan muuttujat
        mista_kirjain = int(self.__mista_kirjain)
        mista_numero = int(self.__mista_numero)
        mihin_kirjain = int(self.__mihin_kirjain)
        mihin_numero = int(self.__mihin_numero)
        ruudukko = self.__kentta
        lyotava = None
        mihin_kirjain_laskutoimitus = 1
        mihin_numero_laskutoimitus = 1

        # Pelaajan tiedot:
        if self.__tarkistettava_liike[1:2] == "V":
            vastustaja = "M"
        elif self.__tarkistettava_liike[1:2] == "M":
            vastustaja = "V"

        # Katotaan silmukalla onko lahetin liike laillinen
        # Ensin oikealle, sitten vasemmalla
        for a in range(0, 2):
                if mihin_kirjain_laskutoimitus == -1:
                    mihin_kirjain_laskutoimitus = 1
                else:
                    mihin_kirjain_laskutoimitus = -1

                # Ensin ylös, sitten alas
                for b in range(0, 2):
                    if mihin_numero_laskutoimitus == -1:
                        mihin_numero_laskutoimitus = 1
                    else:
                        mihin_numero_laskutoimitus = -1

                    # Muodostetaan testi muuttujat
                    mihin_kirjain_testi = mista_kirjain
                    mihin_numero_testi = mista_numero

                    # Jokainen ruutu kyseiseen suuntaan kerralla
                    for c in range(0, 8):
                        # Testi joko kattoo jokaisen ruudun kerrallaan
                        mihin_numero_testi = mihin_numero_testi + mihin_numero_laskutoimitus
                        mihin_kirjain_testi = mihin_kirjain_testi + mihin_kirjain_laskutoimitus

                        # Jos siirto on löydetty aiemmassa silmukassa ja on laillinen
                        if self.__liike_laillinen == True:
                            break

                        # Kentän ulkopuolella
                        if mihin_numero_testi < 0 or mihin_numero_testi > 7 or\
                                mihin_kirjain_testi < 0 or mihin_kirjain_testi > 7:
                            self.__virhe = "Laiton siirto!"
                            mihin_numero_testi = 8
                            mihin_kirjain_testi = 0
                            pass

                        # Haetaan lyotava
                        lyotava = ruudukko[mihin_numero_testi][mihin_kirjain_testi]

                        # Jos testi on yhtä suuri kuin määränpää
                        if mihin_numero_testi == mihin_numero and mihin_kirjain_testi == mihin_kirjain:
                            # Tarkistetaan mikä sijaitsee määränpäässä
                            # Jos vastustaja -> lyönti
                            if lyotava == "KM.png" or lyotava == "KV.png":
                                self.__liike_laillinen = False
                            elif lyotava[1:2] == vastustaja:
                                self.__liike_laillinen = True
                            # Jos tyhjä -> laillinen
                            elif lyotava == "tyhja.png":
                                self.__liike_laillinen = True
                            # Muulloin on ruudussa oma nappula -> Laiton siirto
                            else:
                                self.__virhe = "Laiton siirto!"

                        # Tarkistetaan onko joku nappula tiellä
                        if lyotava == "tyhja.png":
                            pass
                        else:
                            self.__virhe = "Laiton siirto!"
                            break

        # Jos pelaaja ei ole liikuttanut nappulaa
        if mista_numero == mihin_numero and mista_kirjain == mihin_kirjain:
            self.__virhe = "Et siirtänyt nappulaa!"

    def kuningatar(self):
        """
        Tutkitaan onko kunigattaren liike laillinen.

        Koska kuningattaren liikkeet ovat samanlaiset kuin tornin
        tai lähetin tutkitaan tornin ja lähetin silmukat. Jos jompikumpi
        palauttaa paluuarvona totuuden kuningatar voi liikkua. Jos molemmat
        palauttavat paluuarvona tarua kuningatar ei liiku.
        :return: virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        self.torni()
        self.lahetti()

    def kuningas(self):
        """
        Tutkitaan kuninkaan siirron laillisuutta

        - Lasketaan mahdolliset lailliset liikkeet -> kahdeksan mahdollisuutta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan muuttujat
        mista_kirjain = int(self.__mista_kirjain)
        mista_numero = int(self.__mista_numero)
        mihin_kirjain = int(self.__mihin_kirjain)
        mihin_numero = int(self.__mihin_numero)
        ruudukko = self.__kentta
        lyotava = None
        linnoitus = False

        # Pelaajan tiedot:
        if self.__tarkistettava_liike[1:2] == "V":
            vastustaja = "M.png"
            koti_linja = 7
            oma_torni = "TV.png"
        elif self.__tarkistettava_liike[1:2] == "M":
            vastustaja = "V.png"
            koti_linja = 0
            oma_torni = "TM.png"

        # Pohjoinen
        p_mihin_kirjain = mista_kirjain
        p_mihin_numero = mista_numero - 1
        if p_mihin_kirjain == mihin_kirjain and p_mihin_numero == mihin_numero:
            lyotava = ruudukko[p_mihin_numero][mihin_kirjain][1:]

        # Koillinen
        ko_mihin_kirjain = mista_kirjain + 1
        ko_mihin_numero = mista_numero - 1
        if ko_mihin_kirjain == mihin_kirjain and ko_mihin_numero == mihin_numero:
            lyotava = ruudukko[ko_mihin_numero][ko_mihin_kirjain][1:]

        # Itä
        i_mihin_kirjain = mista_kirjain + 1
        i_mihin_numero = mista_numero
        if i_mihin_kirjain == mihin_kirjain and i_mihin_numero == mihin_numero:
            lyotava = ruudukko[i_mihin_numero][i_mihin_kirjain][1:]

        # Kaakko
        ka_mihin_kirjain = mista_kirjain + 1
        ka_mihin_numero = mista_numero + 1
        if ka_mihin_kirjain == mihin_kirjain and ka_mihin_numero == mihin_numero:
            lyotava = ruudukko[ka_mihin_numero][ka_mihin_kirjain][1:]

        # Etelä
        e_mihin_kirjain = mista_kirjain
        e_mihin_numero = mista_numero + 1
        if e_mihin_kirjain == mihin_kirjain and e_mihin_numero == mihin_numero:
            lyotava = ruudukko[e_mihin_numero][e_mihin_kirjain][1:]

        # Lounas
        lo_mihin_kirjain = mista_kirjain - 1
        lo_mihin_numero = mista_numero + 1
        if lo_mihin_kirjain == mihin_kirjain and lo_mihin_numero == mihin_numero:
            lyotava = ruudukko[lo_mihin_numero][lo_mihin_kirjain][1:]

        # Länsi
        la_mihin_kirjain = mista_kirjain - 1
        la_mihin_numero = mista_numero
        if la_mihin_kirjain == mihin_kirjain and la_mihin_numero == mihin_numero:
            lyotava = ruudukko[la_mihin_numero][la_mihin_kirjain][1:]

        # Luode
        lu_mihin_kirjain = mista_kirjain - 1
        lu_mihin_numero = mista_numero - 1
        if lu_mihin_kirjain == mihin_kirjain and lu_mihin_numero == mihin_numero:
            lyotava = ruudukko[lu_mihin_numero][lu_mihin_kirjain][1:]

        # Linnoitus vasemmalle
        if ruudukko[koti_linja][1] == "tyhja.png" and ruudukko[koti_linja][2] == "tyhja.png"\
                and ruudukko[koti_linja][3] == "tyhja.png" and mihin_kirjain == 1\
                and ruudukko[koti_linja][0][:1] == "T" :
            ruudukko[koti_linja][0] = "tyhja.png"
            ruudukko[koti_linja][2] = oma_torni
            self.__kentta = ruudukko
            linnoitus = True

        # Linnoitus oikealle
        if ruudukko[koti_linja][5] == "tyhja.png" and ruudukko[koti_linja][6] == "tyhja.png" \
                and mihin_kirjain == 6 and ruudukko[koti_linja][7][:1] == "T":
            ruudukko[koti_linja][7] = "tyhja.png"
            ruudukko[koti_linja][5] = oma_torni
            self.__kentta = ruudukko
            linnoitus = True

        # Tarkistetaan onko liike laillinen
        if lyotava == "yhja.png":
            self.__liike_laillinen = True
        elif lyotava == vastustaja:
            self.__liike_laillinen = True
        elif linnoitus == True:
            self.__liike_laillinen = True
        # Jos pelaaja ei liikuttanut nappulaa
        elif mista_numero == mihin_numero and mista_kirjain == mihin_kirjain:
            self.__virhe = "Et siirtänyt nappulaa!"
        else:
            self.__virhe = "Laiton siirto!"


#   ------------TASTA ALASPAIN ON MENU BAR FUNKTIOT-----------------
    def uusi_peli(self):
        """
        Suljetaan vanha peli ja avataan uusi
        """
        self.__pääikkuna.destroy()
        Shakki()

    def peruuta_siirto(self):
        """
        Perutetaan siirto, tallennettujen siirtojen perusteella
        """
        ruudukko = self.__kentta

        # Jos perutettiin jo kerran ei pystyä peruuttamaan
        if ruudukko[self.__mista_numero][self.__mista_kirjain] == self.__mista_nappula:
            self.__virhe = "Et voi peruuttaa siirtoasi kaksi kertaa"

        # Perutetaan siirto
        else:
            ruudukko[self.__mista_numero][self.__mista_kirjain] = self.__mista_nappula
            ruudukko[self.__mihin_numero][self.__mihin_kirjain] = self.__mihin_nappula
            self.__kentta = ruudukko
            self.kenen_vuoro()

        # Luodaan kentta uudelleen
        self.luo_kenttä()

    def lopeta(self):
        """
        Komponentti, joka sulkee käyttöliittymän
        """
        self.__pääikkuna.destroy()

    #-----------TASTA ALASPAIN OVAT SAANNOT---------------
    class info():
        """
        Tämä komponentti pystyy näyttämään ohjeita kuvien avulla.
        Käyttäjä voi valita minkä ohjeen haluaa lukea menusta.
        Kaikkien tekstien ja kuvien lähde on wikipedia.
        """
        def __init__(self):
            self.__infoikkuna = Tk()

            self.__kuva = PhotoImage(file="yleis_ohjeet.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="wiki.png", master=self.__infoikkuna)
            self.saannot()

            self.__infoikkuna.mainloop()

        def saannot(self):
            self.__infoikkuna.title('Ohjeet')

            # Luodaan menu
            self.__menubar = Menu(self.__infoikkuna)

            # Luodaan nappuloiden säännöt menu
            self.__nappulamenu = Menu(self.__menubar, tearoff=0)
            self.__nappulamenu.add_command(label="Ohjeet", command=self.yleiset)
            self.__nappulamenu.add_command(label="Sotilas", command=self.sotilas_kuva)
            self.__nappulamenu.add_command(label="Lähetti", command=self.lahetti_kuva)
            self.__nappulamenu.add_command(label="Ratsu", command=self.ratsu_kuva)
            self.__nappulamenu.add_command(label="Torni", command=self.torni_kuva)
            self.__nappulamenu.add_command(label="Kuningatar", command=self.kuningatar_kuva)
            self.__nappulamenu.add_command(label="Kuningas", command=self.kuningas_kuva)
            self.__nappulamenu.add_separator()
            self.__nappulamenu.add_command(label="Poistu", command=self.lopeta)
            self.__menubar.add_cascade(label="Nappuloiden säännöt", menu=self.__nappulamenu)

            # Luodaan erikoissiirrot menu
            self.__erikoissiirrot = Menu(self.__menubar, tearoff=0)
            self.__erikoissiirrot.add_command(label="Ohestalyönti", command=self.ohestalyonti)
            self.__erikoissiirrot.add_command(label="Tornitus", command=self.tornitus)
            self.__menubar.add_cascade(label="Erikoisiirtojen säännöt", menu=self.__erikoissiirrot)

            # Konfiguroitaan menu
            self.__infoikkuna.config(menu=self.__menubar)

            # Luodaan yleiset ohjeet ja nappuloiden merkinta selitys
            self.__yleis_info = Label(self.__infoikkuna, image=self.__kuva)
            self.__liikkeet_kuva = Label(self.__infoikkuna, image=self.__liikkeet)
            self.__yleis_info.grid(row=0, column=0)
            self.__liikkeet_kuva.grid(row=0, column=1)

        def donothing(self):
            pass

        def yleiset(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="yleis_ohjeet.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="wiki.png", master=self.__infoikkuna)
            self.saannot()

        def sotilas_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="sotilas_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="sotilas_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def ratsu_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="hevonen_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="hevonen_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def lahetti_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="lahetti_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="lahetti_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def torni_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="torni_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="torni_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def kuningatar_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="kuningatar_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="kuningatar_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def kuningas_kuva(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="kuningas_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="kuningas_siirrot.png", master=self.__infoikkuna)
            self.saannot()

        def ohestalyonti(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="ohestalyonti.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="tyhja.png", master=self.__infoikkuna)
            self.saannot()

        def tornitus(self):
            # Päivitetään kuvat
            self.__kuva = PhotoImage(file="tornitus_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="tyhja.png", master=self.__infoikkuna)
            self.saannot()

        def lopeta(self):
            """
            Komponentti, joka sulkee käyttöliittymän
            """
            self.__infoikkuna.destroy()

def main():
    # Kutsutaan shakki peli
    Shakki()

if __name__ == '__main__':
    main()