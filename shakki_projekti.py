"""
Tekij�: Juliusz Kotelba

T�m� ohjelma on Shakki. T�t� peli� voi pelata kahdestaan tai yksin.
Logiikkana on listan luonti, jossa on kahdeksan listaa sis�ll�. Jokainen lista listassa
vastaa siis yht� vaakarivi� laudalla. Sen avulla ohjelma rakentaa grafiikan. Listaa
p�ivitet��n aina kun nappulaa siirret��n.

Ohjelma osaa reagoida laittomiin siirtoihin sek� erikoissiirtoihin. Ainoa mit� ohjelma
ei osaa on sotilaan korotus ja shakin tunnistaminen. Olen tietysti yritt�nyt tehd� molempia,
mutta yritykset eiv�t tuottaneet mit��n toimivaa.

Ohjelmassa on my�s integroidu siirron peruutus, uuden pelin aloittaminen valikosta sek�
lyhyehk� s��nt�kirja.

    Ohjeet:
Peli� pelataan painamalla ensin nappulaa, jota haluaa liikuttaa. Sitten painamalla
ruutua, johon haluaa liikkua. Tai painamalla ruutua, jossa on vastustajan nappula,
sy�d�kseen se. Sen j�lkeen onkin vastustajan vuoro. Ohjelma osaa tunnistaa jos pelaaja pelaa
vastustajan nappuloilla. Ohjelma osaa neuvoa kenen vuoro on ja mit� pit�� painaa seuraavaksi.
N�m� tiedot l�ytyv�t laudan oikealta puolelta.

Peliss� ei erikseen tule ilmoitus pelin p��ttymisest�, koska:
a) sen tekiminen veisi j�rjett�m�n paljon aikaa
b) k�yt�nn�ss� peli useimmiten p��ttyy luovutukseen tai sovittuun tasapeliin

Jos haluaa aloittaa pelin uudestaan, voi sen teh� p��valikosta.

Jos sinulla tulee lis�kysymyksi� ohjelmastani voit ottaa yhteytt� osoitteeseen:
juliusz.kotelba(at)tuni.fi
"""
from tkinter import *


class Shakki:
    """
    P��silmukka jossa k�sitell��n koko peli ja kentt�
    """

    def __init__(self):
        """
        Luodaan paaikkuna, sek� menubar, ett� tarvittavat
        muuttujat peli� varten.

        -> L�hetet��n pyynt� shakkilaudan luomiseen
        """
        # Luodaan paaikkuna
        self.__paaikkuna = Tk()
        self.__paaikkuna.geometry("850x610")
        self.__paaikkuna.title('Shakki')

        # Luodaan menu
        self.__menubar = Menu(self.__paaikkuna)

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
        self.__helpmenu.add_command(label="S��nn�t", command=info)
        self.__menubar.add_cascade(label="Apua", menu=self.__helpmenu)

        # Konfiguroitaan menu
        self.__paaikkuna.config(menu=self.__menubar)

        # Luodaan kuva oliot
        self.__ruudukko = None
        self.__images = None
        self.__varit = []
        self.luodaan_nappulat()

        # Luodaan tarvittavat attribuutit
        self.__mista = False
        self.__mista_x = None
        self.__mista_y = None
        self.__mihin_x = None
        self.__mihin_y = None
        self.__siirtoHistoria = []

        # Luodaan kirjaimet ja numerot laudan sivuille
        # Ensin kirjaimet
        kirjaimet = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for index, text in enumerate(kirjaimet):
            Label(self.__paaikkuna, text=text).grid(row=8, column=index)

        # Sitten numerot
        numerot = ["8", "7", "6", "5", "4", "3", "2", "1"]
        for index, text in enumerate(numerot):
            Label(self.__paaikkuna, text=text).grid(row=index, column=8)

        # Tulostetaan kenen vuoro on kyseess�
        self.__vuoroTeksti = StringVar()
        self.__vuoroTeksti.set("Valkoisen vuoro")
        Label(self.__paaikkuna, textvariable=self.__vuoroTeksti, background="azure").grid(row=3, column=9, columnspan=2)

        # Tulostetaan ohje mit� painaa
        self.__painaTeksti = StringVar()
        self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")
        Label(self.__paaikkuna, textvariable=self.__painaTeksti, background="azure").grid(row=4, column=9, columnspan=2)

        # Virhe teksti
        self.__virheTeksti = StringVar()
        self.__virheTeksti.set(" ")
        Label(self.__paaikkuna, textvariable=self.__virheTeksti, background="red").grid(row=5, column=9, columnspan=2)

        # K�ynnistet��n k�ytt�liittym�
        self.__paaikkuna.mainloop()

    def luodaan_nappulat(self):
        """
        Luodaan kuvat sen j�lkeen luodaan painikkeet.
        Asetellaan painikkeet kentt��n. Lis�t��n laudan
        sivuille kordinaatti kirjaimet ja yt.
        N�ytet��n kenen vuoro on kyseess�, mit� pit��
        seuraavaksi painaa sek� luodaan mahdollinen virheilmoitus.
        """
        self.__images = {"TM": "", "HM": "", "LM": "", "QM": "", "KM": "", "SM": "",
                         "TV": "", "HV": "", "LV": "", "QV": "", "KV": "", "SV": "", "tyhja": ""}
        for nimi in self.__images:
            self.__images[nimi] = PhotoImage(file="kuvat/" + nimi + ".png")

        self.__ruudukko = [["TM", "HM", "LM", "QM", "KM", "LM", "HM", "TM"],
                           ["SM", "SM", "SM", "SM", "SM", "SM", "SM", "SM"],
                           ["tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja"],
                           ["tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja"],
                           ["tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja"],
                           ["tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja", "tyhja"],
                           ["SV", "SV", "SV", "SV", "SV", "SV", "SV", "SV"],
                           ["TV", "HV", "LV", "QV", "KV", "LV", "HV", "TV"]]

        white = False
        for i in range(0, 8):
            if white:
                white = False
            else:
                white = True

            rivi = []

            for j in range(0, 8):
                if white:
                    vari = "white"
                    white = False
                else:
                    vari = "grey39"
                    white = True

                Button(self.__paaikkuna, image=self.__images[self.__ruudukko[i][j]], background=vari,
                       command=lambda x=i, y=j: self.tallenna_koordinaatti(x, y)).grid(row=i, column=j)

                rivi.append(vari)

            self.__varit.append(rivi)

    def tallenna_koordinaatti(self, x, y):
        """
        Tallennetaan l�ht�- ja loppukordinaatit.
        Jos molemmat ovat tallennettuja; l�hetet��n pyynt�
        siirt�� nappulat ja nollata l�hd�- ja loppukordinaatit.
        """
        # Poistetaan mahdollinen virhe ilmoitus
        self.__virheTeksti.set("")

        # Tallennetaan l�ht�kordinaatti, jos tyhj�.
        if not self.__mista:
            self.__mista_x = x
            self.__mista_y = y
            # Tarkistetaanko pelaako pelaaja omilla nappuloilla
            if self.oma_nappula(self.__ruudukko[x][y]):
                self.__mista = True
                self.__painaTeksti.set("Paina ruutua johon haluat siirt�� nappula!")

        # Tallennetaan loppukordinaatti, jos tyhj�.
        else:
            self.__mihin_x = x
            self.__mihin_y = y
            self.__mista = False
            self.siirra()

    def oma_nappula(self, nappulan_nimi):
        """
        - Tarkistetaan pelaako pelaaja omilla nappuloilla siis pelaako musta
            tai valkoinen omalla vuorollaan omilla nappuloilla.
        - Tarkistetaan onko ruutu tyhj�, jos on -> tulostetaan virheilmoitus.
        :return self.__tarkistettava_nappula = True or False
        """
        # Tallennetaan kenen vuoro
        kuka_pelaa = self.__vuoroTeksti.get()
        if kuka_pelaa == "Mustan vuoro":
            kuka_pelaa = "M"
        elif kuka_pelaa == "Valkoisen vuoro":
            kuka_pelaa = "V"

        # Tarkistetaan toteutuuko ehto
        if nappulan_nimi[1:2] == kuka_pelaa:
            return True

        # Jos ei toteudu niin tarkistetaan onko ruutu
        # kenties tyhja.
        elif nappulan_nimi == "tyhja":
            self.__virheTeksti.set("Ei mit��n siirrett�v��!")
            return False

        # Muulloin ruudussa sijaitsee vastustajan nappula
        else:
            self.__virheTeksti.set("�l� pelaa vastustajan puolesta!")
            return False

    def siirra(self):
        """
        Toteutetaan siirto:
        Ensin muutetaan kirjain numeroksi sek� numero oikeaksi numeroksi.
        Sen j�lkeen haetaan kentt� lista ja tarkistetaan nappula. Sen
        j�lkeen tarkistetaan onko siirto laininen. Jos siirto on laillinen
        tallennetaan uudet sijainnit
        """
        if self.__mista_x == self.__mihin_x and self.__mista_y == self.__mihin_y:
            self.__virheTeksti.set("Et siirt�nyt nappulaa!")
            self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")

        elif self.laillinen_siirto():
            # Tallennetaan koordinaatit mahdollista perumista varten
            self.__siirtoHistoria.append([self.__mista_x, self.__mista_y, self.__mihin_x, self.__mihin_y,
                                          self.__ruudukko[self.__mihin_x][self.__mihin_y]])

            # Tallennetaan uudet sijainnit
            self.__ruudukko[self.__mihin_x][self.__mihin_y] = self.__ruudukko[self.__mista_x][self.__mista_y]
            self.__ruudukko[self.__mista_x][self.__mista_y] = "tyhja"

            # P�ivitet��n GUI
            for coords in [[self.__mista_x, self.__mista_y], [self.__mihin_x, self.__mihin_y]]:
                i = coords[0]
                j = coords[1]
                Button(self.__paaikkuna, image=self.__images[self.__ruudukko[i][j]], background=self.__varit[i][j],
                       command=lambda x=i, y=j: self.tallenna_koordinaatti(x, y)).grid(row=i, column=j)

            # Vaihdetaan tekstit
            self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")
            if self.__vuoroTeksti.get() == "Mustan vuoro":
                self.__vuoroTeksti.set("Valkoisen vuoro")
            else:
                self.__vuoroTeksti.set("Mustan vuoro")

        else:
            self.__virheTeksti.set("Laiton siirto")
            self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")

    def laillinen_siirto(self):
        """
        Ohjataan kyseisen nappulan liikkeen laillisuustarkastukseen
        TAI tulostetaan virhe, jos jonkin takia sit� ei huomattu aiemmin.
        """
        pelattava_nappula = self.__ruudukko[self.__mista_x][self.__mista_y][:1]
        if pelattava_nappula == "S":
            return self.sotilas()
        elif pelattava_nappula == "T":
            return self.torni()
        elif pelattava_nappula == "H":
            return self.hevonen()
        elif pelattava_nappula == "L":
            return self.lahetti()
        elif pelattava_nappula == "Q":
            return self.kuningatar()
        elif pelattava_nappula == "K":
            return self.kuningas()
        else:
            return False

    def sotilas(self):
        """
        Tutkitaan sotilaan siirron laillisuutta
        - Lasketaan mahdolliset lailliset liikkeet
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit.
        - Palautetaan virhe tai "liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan tarvittavat tiedot
        pelattava_nappula = self.__ruudukko[self.__mista_x][self.__mista_y][1:]

        # Jos sotilas on valkoinen
        if pelattava_nappula == "V":
            # Muodostetaan tutkittavat sijainnit
            yksi_ruutu_siirto = self.__mista_x - 1
            kaksi_ruutu_siirto = self.__mista_x - 2
            lyonti_vasemmalle = self.__mista_y - 1
            lyonti_oikealle = self.__mista_y + 1
            # Muodostetaan uudet tarvittavat muuttujat
            lahtoruutu = 6
            vastustaja = "M"

        # Jos sotilas on musta
        else:
            # Muodostetaan tutkittavat sijainnit
            yksi_ruutu_siirto = self.__mista_x + 1
            kaksi_ruutu_siirto = self.__mista_x + 2
            lyonti_vasemmalle = self.__mista_y + 1
            lyonti_oikealle = self.__mista_y - 1
            # Muodostetaan uudet tarvittavat muuttujat
            lahtoruutu = 1
            vastustaja = "V"

        # Tarkistetaan ly�t�v�t sijainnit
        lyotava = self.__ruudukko[self.__mihin_x][self.__mihin_y]

        # Kaksi ruutua eteenp�in jos sotilas sijaitsee lahtoruudussa
        if self.__mista_x == lahtoruutu and kaksi_ruutu_siirto == self.__mihin_x and \
                self.__mista_y == self.__mihin_y and lyotava == "tyhja":
            return True

        # Ly�nti vasemmalle
        elif yksi_ruutu_siirto == self.__mihin_x and lyonti_vasemmalle == self.__mihin_y and lyotava[1:] == vastustaja:
            return True

        # Ly�nti oikealle
        elif yksi_ruutu_siirto == self.__mihin_x and lyonti_oikealle == self.__mihin_y and lyotava[1:] == vastustaja:
            return True

        # Liike eteenp�in
        elif yksi_ruutu_siirto == self.__mihin_x and self.__mista_y == self.__mihin_y and lyotava == "tyhja":
            return True

        else:
            return False

    def torni(self):
        """
        Tutkitaan tornin siirron laillisuutta
        - Tarkistetaan onko "mihin" kordinaatit samat kuin l�ht�kordinaatit
            T�m� toteutetaan "nelj�ss�" silmukassa tutkittaen jokaisen suunnan.
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        laskutoimitus = 0
        mihin_testi = 0
        mihin = 0
        sivuille = False

        # Pelaajan tiedot:
        if self.__ruudukko[self.__mista_x][self.__mista_y][1:] == "V":
            vastustaja = "M"
        else:
            vastustaja = "V"

        # Sivuille
        if (self.__mista_y - self.__mihin_y) != 0:
            sivuille = True
            mihin = self.__mihin_y
            mihin_testi = self.__mista_y
            if (self.__mista_y - self.__mihin_y) > 0:
                laskutoimitus = -1
            else:
                laskutoimitus = 1
        # Ylos_alas
        if (self.__mista_x - self.__mihin_x) != 0:
            mihin = self.__mihin_x
            mihin_testi = self.__mista_x
            if (self.__mista_x - self.__mihin_x) > 0:
                laskutoimitus = -1
            else:
                laskutoimitus = 1

        # Testi joko kattoo jokaisen ruudun kerrallaan
        for i in range(0, 7):
            mihin_testi += laskutoimitus
            if sivuille:
                lyotava = self.__ruudukko[self.__mista_x][mihin_testi]
            else:
                lyotava = self.__ruudukko[self.__mista_x][mihin_testi]

            # Listan ulkopuolella
            if mihin_testi == -1 or mihin_testi == 8:
                return False

            # Jos testi on yht�suuri kuin m��r�np��
            if mihin_testi == mihin:
                # Tarkistetaan mik� sijaitsee m��r�np��ss�
                # Jos vastustaja -> ly�nti
                if lyotava == "KM" or lyotava == "KV":
                    return False
                elif lyotava[1:2] == vastustaja:
                    return True
                # Jos tyhj� -> laillinen
                elif lyotava == "tyhja":
                    return True
                # Muulloin on ruudussa oma nappula -> Laiton siirto
                else:
                    return False

            # Tarkistetaan onko joku nappula tiell�
            if lyotava == "tyhja":
                pass
            else:
                return False

    def hevonen(self):
        """
        Tutkitaan hevosen siirron laillisuutta
        - Lasketaan mahdolliset lailliset liikkeet -> kahdeksan mahdollisuutta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Pelaajan tiedot:
        if self.__ruudukko[self.__mista_x][self.__mista_y][1:] == "V":
            vastustaja = "M"
        else:
            vastustaja = "V"

        lyotava = self.__ruudukko[self.__mihin_x][self.__mihin_y][1:]
        x_index = 0
        y_index = 1
        for sijainti in [[1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]:
            if self.__mihin_y == (self.__mista_y + sijainti[y_index]) and \
                    self.__mihin_x == (self.__mista_x + sijainti[x_index]) and \
                    (lyotava == vastustaja or lyotava == "yhja"):
                return True

        return False

    def lahetti(self):
        """
        Tutkitaan lahetin siirron laillisuutta
        - Tutkitaan silmukalla jokainen nelj�st� suunnasta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        mihin_y_laskutoimitus = -1
        mihin_x_laskutoimitus = -1

        # Pelaajan tiedot:
        if self.__ruudukko[self.__mista_x][self.__mista_y][1:] == "V":
            vastustaja = "M"
        else:
            vastustaja = "V"

        # Katotaan silmukalla onko lahetin liike laillinen
        # Ensin oikealle, sitten vasemmalla
        for a in range(0, 2):
            if mihin_y_laskutoimitus == -1:
                mihin_y_laskutoimitus = 1
            else:
                mihin_y_laskutoimitus = -1

            # Ensin yl�s, sitten alas
            for b in range(0, 2):
                if mihin_x_laskutoimitus == -1:
                    mihin_x_laskutoimitus = 1
                else:
                    mihin_x_laskutoimitus = -1

                # Muodostetaan testi muuttujat
                mihin_y_testi = self.__mista_y
                mihin_x_testi = self.__mista_x

                # Jokainen ruutu kyseiseen suuntaan kerralla
                for c in range(0, 8):
                    # Testi joko kattoo jokaisen ruudun kerrallaan
                    mihin_x_testi += mihin_x_laskutoimitus
                    mihin_y_testi += mihin_y_laskutoimitus

                    # Kent�n ulkopuolella
                    if mihin_x_testi < 0 or mihin_x_testi > 7 or mihin_y_testi < 0 or mihin_y_testi > 7:
                        break

                    # Haetaan lyotava
                    lyotava = self.__ruudukko[mihin_x_testi][mihin_y_testi]

                    # Jos testi on yht� suuri kuin m��r�np��
                    if mihin_x_testi == self.__mihin_x and mihin_y_testi == self.__mihin_y:
                        # Tarkistetaan mik� sijaitsee m��r�np��ss�
                        # Jos vastustaja -> ly�nti
                        if lyotava == "KM" or lyotava == "KV":
                            return False
                        elif lyotava[1:2] == vastustaja:
                            return True
                        # Jos tyhj� -> laillinen
                        elif lyotava == "tyhja":
                            return True
                        # Muulloin on ruudussa oma nappula -> Laiton siirto
                        else:
                            return False

                    # Tarkistetaan onko joku nappula tiell�
                    if lyotava != "tyhja":
                        break
        return False

    def kuningatar(self):
        """
        Tutkitaan onko kunigattaren liike laillinen.
        Koska kuningattaren liikkeet ovat samanlaiset kuin tornin
        tai l�hetin tutkitaan tornin ja l�hetin silmukat. Jos jompikumpi
        palauttaa paluuarvona totuuden kuningatar voi liikkua. Jos molemmat
        palauttavat paluuarvona tarua kuningatar ei liiku.
        :return: virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        if self.torni() or self.lahetti():
            return True
        else:
            return False

    def kuningas(self):
        """
        Tutkitaan kuninkaan siirron laillisuutta
        - Lasketaan mahdolliset lailliset liikkeet -> kahdeksan mahdollisuutta.
        - Tarkistetaan onko "mihin" kordinaatit samat kuin lasketut mihinkordinaatit
        - Palautetaan virhe tai "Liike laillinen = totta"
        :return virhe = "Laiton siirto!" TAI liike_laillinen = True
        """
        # Haetaan muuttujat
        lyotava = self.__ruudukko[self.__mihin_x][self.__mihin_y][1:]

        # Pelaajan tiedot:
        if self.__ruudukko[self.__mista_x][self.__mista_y][1:] == "V":
            koti_linja = 7
            vastustaja = "M"
        else:
            koti_linja = 0
            vastustaja = "V"

        x_index = 0
        y_index = 1
        for sijainti in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
            if self.__mihin_y == (self.__mista_y + sijainti[y_index]) \
                    and self.__mihin_x == (self.__mista_x + sijainti[x_index])\
                    and (lyotava == vastustaja or lyotava == "yhja"):
                return True

        # Linnoitus vasemmalle
        ruudukko = self.__ruudukko
        if ruudukko[koti_linja][1] == "tyhja" and ruudukko[koti_linja][2] == "tyhja" \
                and ruudukko[koti_linja][3] == "tyhja" and self.__mihin_y == 1 \
                and ruudukko[koti_linja][0][:1] == "T":
            return True

        # Linnoitus oikealle
        if ruudukko[koti_linja][5] == "tyhja" and ruudukko[koti_linja][6] == "tyhja" \
                and self.__mihin_y == 6 and ruudukko[koti_linja][7][:1] == "T":

            return True

        return False

    # ------------TASTA ALASPAIN ON MENU BAR FUNKTIOT-----------------
    def uusi_peli(self):
        """
        Suljetaan vanha peli ja avataan uusi
        """
        self.__siirtoHistoria = []
        self.__vuoroTeksti.set("Valkoisen vuoro")
        self.__mista = False
        self.__virheTeksti.set("")
        self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")
        self.luodaan_nappulat()

    def peruuta_siirto(self):
        """
        Perutetaan siirto, tallennettujen siirtojen perusteella
        """
        try:
            siirto = self.__siirtoHistoria.pop()
        except IndexError:
            self.__virheTeksti.set("Ei mit��n peruutettavaa siirtoa")
            return

        self.__ruudukko[siirto[0]][siirto[1]] = self.__ruudukko[siirto[2]][siirto[3]]
        self.__ruudukko[siirto[2]][siirto[3]] = siirto[4]

        # P�ivitet��n GUI
        for coords in [[siirto[0], siirto[1]], [siirto[2], siirto[3]]]:
            i = coords[0]
            j = coords[1]
            Button(self.__paaikkuna, image=self.__images[self.__ruudukko[i][j]], background=self.__varit[i][j],
                   command=lambda x=i, y=j: self.tallenna_koordinaatti(x, y)).grid(row=i, column=j)

        # Vaihdetaan tekstit
        self.__mista = False
        self.__painaTeksti.set("Paina nappulaa jota haluat siirt��!")
        if self.__vuoroTeksti.get() == "Mustan vuoro":
            self.__vuoroTeksti.set("Valkoisen vuoro")
        else:
            self.__vuoroTeksti.set("Mustan vuoro")

    def lopeta(self):
        """
        Komponentti, joka sulkee k�ytt�liittym�n
        """
        self.__paaikkuna.destroy()


class info:
    """
    T�m� komponentti pystyy n�ytt�m��n ohjeita kuvien avulla.
    K�ytt�j� voi valita mink� ohjeen haluaa lukea menusta.
    Kaikkien tekstien ja kuvien l�hde on wikipedia.
    """

    def __init__(self):
        self.__yleis_info = None
        self.__menubar = None
        self.__erikoissiirrot = None
        self.__liikkeet_kuva = None

        self.__infoikkuna = Tk()
        self.__infoikkuna.title('Ohjeet')

        self.__kuva = PhotoImage(file="kuvat/yleiset_ohjeet.png", master=self.__infoikkuna)
        self.__liikkeet = PhotoImage(file="kuvat/wiki.png", master=self.__infoikkuna)

        # Luodaan menu
        self.__menubar = None
        self.__nappulamenu = None

        self.saannot()

        self.__infoikkuna.mainloop()

    def saannot(self):
        # Luodaan nappuloiden s��nn�t menu
        self.__menubar = Menu(self.__infoikkuna)
        self.__nappulamenu = Menu(self.__menubar, tearoff=0)
        sivut = ["Yleiset", "Sotilas", "Lahetti", "Ratsu", "Torni", "Kuningatar", "Kuningas"]
        for sivu in sivut:
            self.__nappulamenu.add_command(label=sivu, command=lambda nimi=sivu: self.uusi_kuva(nimi))
        self.__nappulamenu.add_separator()
        self.__nappulamenu.add_command(label="Poistu", command=self.lopeta)
        self.__menubar.add_cascade(label="Nappuloiden s��nn�t", menu=self.__nappulamenu)

        # Luodaan erikoissiirrot menu
        self.__erikoissiirrot = Menu(self.__menubar, tearoff=0)
        self.__erikoissiirrot.add_command(label="Ohestaly�nti", command=lambda: self.uusi_kuva("ohesta"))
        self.__erikoissiirrot.add_command(label="Tornitus", command=lambda: self.uusi_kuva("tornitus"))
        self.__menubar.add_cascade(label="Erikoisiirtojen s��nn�t", menu=self.__erikoissiirrot)

        # Konfiguroitaan menu
        self.__infoikkuna.config(menu=self.__menubar)

        # Luodaan yleiset ohjeet ja nappuloiden merkinta selitys
        self.__yleis_info = Label(self.__infoikkuna, image=self.__kuva)
        self.__liikkeet_kuva = Label(self.__infoikkuna, image=self.__liikkeet)
        self.__yleis_info.grid(row=0, column=0)
        self.__liikkeet_kuva.grid(row=0, column=1)

    def uusi_kuva(self, nimi):
        # P�ivitet��n kuvat
        if nimi.lower() == "yleiset":
            self.__kuva = PhotoImage(file=f"kuvat/yleiset_ohjeet.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file="kuvat/wiki.png", master=self.__infoikkuna)
        else:
            self.__kuva = PhotoImage(file=f"kuvat/{nimi.lower()}_saannot.png", master=self.__infoikkuna)
            self.__liikkeet = PhotoImage(file=f"kuvat/{nimi.lower()}_siirrot.png", master=self.__infoikkuna)
        self.saannot()

    def lopeta(self):
        """
            Komponentti, joka sulkee k�ytt�liittym�n
            """
        self.__infoikkuna.destroy()


def main():
    # Kutsutaan shakki peli
    Shakki()


if __name__ == '__main__':
    main()
