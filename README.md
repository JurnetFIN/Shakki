# Shakki

Tämä ohjelma on Shakki. Tätä peliä voi pelata kahdestaan tai yksin.
Logiikkana on listan luonti, jossa on kahdeksan listaa sisällä. Jokainen lista listassa
vastaa siis yhtä vaakariviä laudalla. Sen avulla ohjelma rakentaa grafiikan. Listaa
päivitetään aina kun nappulaa siirretään.

Ohjelma osaa reagoida laittomiin siirtoihin sekä erikoissiirtoihin. Ainoa mitä ohjelma
ei osaa on sotilaan korotus ja shakin tunnistaminen. Olen tietysti yrittänyt tehdä molempia,
mutta yritykset eivät tuottaneet mitään toimivaa.

Ohjelmassa on myös integroidu siirron peruutus, uuden pelin aloittaminen valikosta sekä
lyhyehkö sääntökirja. Sääntökirja on siis luokka luokassa ja sen periaate on näyttää
wikipediasta otetut näyttökuvat kyseisestä aiheesta.

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

Jos haluaa aloittaa pelin uudestaan, voi sen tehä päävalikosta.


Jos sinulla tulee lisäkysymyksiä ohjelmastani voit ottaa yhteyttä osoitteeseen:
juliusz.kotelba(at)tuni.fi
