#! /usr/bin/env python

import random
import sys


LISTA_INFO = (
"""
    LISTA POMIESZCZEN
Polecenie wypisze liste pomieszczen znajdujacych sie w domu
""",
"""
    IDZ DO
Polecenie sluzy, aby przeniesc sie do wybranego pomieszczenia
w domu.

*** Aby przeniesc sie do pomieszczenia wpisz:
"1 [pomieszczenie]", gdzie "pomieszczenie" -jedno, wybrane
pomieszczenie z listy pomieszczen.
""",
"""
    STAN POMIESZCZENIA
Polecenie wypisze przedmioty znajdujace sie w pomieszczeniu.
""",
"""
    OTWORZ
Polecenie spowoduje otworzenie wybranego mebla, w celu
sprawdzenia jego zawartosci.

*** Aby otworzyc mebel wpisz:
"3" [mebel], gdzie "mebel" - mebel znajdujacy sie
w pomieszczeniu.
*** Aby sprawdzic jakie meble znajduja sie w pomieszczeniu
wpisz: "2".
""",
"""
    MOJE PRZEDMIOTY
Polecenie wypisze liste przedmiotow, ktore posiada Twoja postac
wraz z opisem jak i do czego mozesz ich uzyc.
""",
"""
    UZYJ
Polecenie spowoduje uzycie wybranego przedmiotu z wyposazenia.

*** Aby uzyc przedmiotu wpisz:
"5 [przedmiot]", gdzie "przedmiot" -przedmiot z wyposazenia,
ktory chcesz uzyc w danej chwili.
*** Aby sprawdzic jakie masz przedmioty, wpisz: "4"
""",
"""
    STAN ZDROWIA
Polecenie wypisze ilosc punktow zdrowia Twojej postaci w danej
chwili.

*** Mozesz zwiekszyc punkty zdrowia znajdujac w pomieszczeniach
jedzenie i nastepnie je zjadajac [komenda "uzyj"].
Musisz jednak uwazac, gdyz niektore jedzenie odejmie Ci punkty.
""",
"""
    WYJSCIE Z GRY
Polecenie spowoduje wyjscie z gry.
"""
)

POLECENIA_START = (
"""
Witaj %s w magicznym swiecie Salmandia!
Za chwile utworzysz swoja postac, ktora bedzie poruszala sie
po domu. """,
"""
Wpisz "0" jezeli chcesz byc Magiem lub
"1" jezeli chcesz byc Wrozka: """,
"""
Wpisz "tak" jesli chcesz, aby Twoja wrozka potrafila latac lub
"nie" jesli nie chcesz, aby Twoja postac posiadala taka umiejetnosc: """,
"\n" + "~"*50 + """
Mozesz teraz rozpoczac gre!
Pomieszczenie, w ktorym sie znajdujesz to:""",
"""Oto lista komend, za pomoca ktorych poruszasz sie po domu:
""",
"""
Wpisz odpowiednia cyfre, jesli chcesz przejsc do danej komendy
lub wpisz "info [cyfra]", aby dowiedziec sie wiecej na temat danego
polecenia. """
)
CZARY = {
"swiatlo":"""Czar powoduje rozswietlenie tajemniczej komnaty, dzieki czemu
mozesz zobaczyc znajdujace sie w niej przedmioty.""",
"otworz":"""Czar sluzy do otwarcia skrzyni. Musisz miec 30 punktow zdrowia,
aby moc go uzyc.

*** Wiecej na temat punktow zdrowia mozesz dowiedziec sie wpisujac:
info 7"""
}

MEBLE = (
"szafa",
"komoda",
"szuflada",
"biurko",
"kufer",
)


# BOHATEROWIE

class Bohater(object):
    def __init__(self, imie, punkty_zdr=20):
        self.imie = imie
        self.punkty_zdr = punkty_zdr
        self.zaklecia = []
        self.wyposazenie = []
        self.uzyte_czary = []

    def wypisz(self):
        print """
Imie: %s
Punkty zdrowia: %d""" % (self.imie, self.punkty_zdr)


class Mag(Bohater):
    def __init__(self, imie):
        super(Mag, self).__init__(imie)
        self.poziom_umiejetnosci = random.randint(1, 4)

    def wypisz(self):
        super(Mag, self).wypisz()
        print "Poziom umiejetnosci: ", self.poziom_umiejetnosci


class Wrozka(Bohater):
    def __init__(self, imie, um_latania):
        super(Wrozka, self).__init__(imie)
        self.um_latania = um_latania

    def wypisz(self):
        super(Wrozka, self).wypisz()
        print "Umiejetnosc latania:", self.um_latania


# POMIESZCZENIA


class Pomieszczenie(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.zawartosc = []


# MEBLE


class Mebel(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.zawartosc = []


# PRZEDMIOTY


class Przedmiot(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa


class Rozdzka(Przedmiot):
    def __init__(self, nazwa, czar):
        super(Rozdzka, self).__init__(nazwa)
        self.czar = czar

    def opis(self):
        print "\nJest to rozdzka:", self.nazwa
        print "Za pomoca niej mozesz uzyc czaru:", self.czar
        for i,k in CZARY.items():
            if i == self.czar:
                print "\nOpis czaru:", k


class Jedzenie(Przedmiot):
    def __init__(self, nazwa, punkty_zdrowia):
        super(Jedzenie, self).__init__(nazwa)
        self.punkty_zdrowia = punkty_zdrowia

    def opis(self):
        print "\nJest to jedzenie:", self.nazwa
        print """Aby zjesc wybierz opcje "uzyj".
! Pamietaj, ze niektore jedzenie moze odjac Ci punkty zdrowia!"""


class Diament(Przedmiot):
    def __init__(self, nazwa):
        super(Diament, self).__init__(nazwa)

    def opis(self):
        print """\nZnalazles %s!
Jestes zwyciezca! Bedziesz diamentem!
Koniec gry!""" % self.nazwa


PRZEDMIOTY = (
Jedzenie("Ciastko Niezdo", -5),
Jedzenie("Owoc Klisto", -5),
Jedzenie("Lijko", 5),
Jedzenie("Owoc Derbo", 5),
Jedzenie("Rebem", 5),
Jedzenie("Slodycz Wilcesa", -5),
Jedzenie("Medoro", 5),
Jedzenie("Segio", -5),
)
# DOM


class Dom(object):
    def __init__(self):
        self.pomieszczenia = [
            Pomieszczenie('kuchnia'),
            Pomieszczenie('sypialnia'),
            Pomieszczenie('tajemnicza komnata'),
            Pomieszczenie('lazienka'),
            Pomieszczenie('salon')]
        self.aktualne_pomieszczenie = random.choice(
            [pom for pom in self.pomieszczenia
                if pom.nazwa != 'tajemnicza komnata'])
        self.aktualny_przedmiot = []
        self.aktualny_mebel = []
        self.komendy = [
            "[0] lista pomieszczen",
            "[1] idz do",
            "[2] stan pomieszczenia",
            "[3] otworz",
            "[4] moje przedmioty",
            "[5] uzyj",
            "[6] stan zdrowia",
            "[7] wyjscie z gry"]
            # dodanie mebli
        for pomieszczenie in self.pomieszczenia:
            if pomieszczenie.nazwa != 'tajemnicza komnata':
                pomieszczenie.zawartosc = [
                    Mebel(nazwa) for nazwa in random.sample(MEBLE, 2)]
            # dodanie przedmiotow do mebli
        meble = []
        for elem in self.pomieszczenia:
            meble += elem.zawartosc
            # dodanie rozdzek
        k = random.randint(0, len(meble)-1)
        meble[k].zawartosc = [Rozdzka("Swietlik", "swiatlo")]
        meble.remove(meble[k])

        k = random.randint(0, len(meble)-1)
        meble[k].zawartosc = [Rozdzka("Openidus", "otworz")]
        meble.remove(meble[k])
            # reszta mebli
        for mebel in meble:
            mebel.zawartosc = [random.choice(PRZEDMIOTY)]
            # tajemnicza komnata
        for komnata in self.pomieszczenia:
            if komnata.nazwa == 'tajemnicza komnata':
                skrzynka = Mebel("skrzynia")
                komnata.zawartosc = [skrzynka]
                skrzynka.zawartosc = [Diament("Diament")]

    def info(self, polecenie):
        if (polecenie.isdigit() and int(polecenie) in range(len(LISTA_INFO))):
            polecenie = int(polecenie)
            print LISTA_INFO[polecenie]
            print '\n'.join(self.komendy)
        else:
            print "Nie ma takiej komendy, wybierz polecenie z listy:"
            print '\n'.join(self.komendy)

    def lista_pomieszczen(self):
        print "W domu jest: "
        print "*", '\n* '.join([pomieszczenie.nazwa
                    for pomieszczenie in self.pomieszczenia])
        print "Ty znajdujesz sie obecnie w:", self.aktualne_pomieszczenie.nazwa

    def idz_do(self, pomieszczenie):
        pom = None
        for pokoj in self.pomieszczenia:
            if pokoj.nazwa == pomieszczenie:
                pom = pokoj
        if pom is not None:
            self.aktualne_pomieszczenie = pom
            print "\nJestes w:", self.aktualne_pomieszczenie.nazwa.upper()
            print "\n", '\n'.join(self.komendy)
        else:
            print """Nie ma takiego pomieszczenia!
Wybierz pomieszczenie z listy:"""
            self.lista_pomieszczen()

    def stan_pomieszczenia(self):
        if self.aktualne_pomieszczenie.nazwa == "tajemnicza komnata":
            for przedmiot in self.postac.wyposazenie:
                if przedmiot.nazwa == "Swietlik":
                    for czar in self.postac.uzyte_czary:
                        if czar == "swiatlo":
                            print ', '.join(
            [mebel.nazwa for mebel in self.aktualne_pomieszczenie.zawartosc])
                            return
                    print """Uzyj czaru "swiatlo", aby zobaczyc zawartosc
pomieszczenia!"""
        else:
            print ', '.join(
            [mebel.nazwa for mebel in self.aktualne_pomieszczenie.zawartosc])

    def stan_mebla(self, mebel):
        for przedmiot in self.aktualne_pomieszczenie.zawartosc:
            if przedmiot.nazwa == mebel:
                if not przedmiot.zawartosc:
                    print "Brak przedmiotu w tym meblu."
                    print "\n", '\n'.join(self.komendy)
                    return
                self.aktualny_przedmiot = [przedmiot.zawartosc[0]]
                przedmiot.zawartosc[0].opis()
                print """\nCzy chcesz podniesc dany przedmiot i dodac go do
swojego wyposazenia? [tak/nie]"""
                pol = ''
                while (pol != 'tak' and pol != 'nie'):
                    pol = raw_input().strip()
                    if pol == 'tak':
                      self.podnies()
                      przedmiot.zawartosc = []
                    elif pol == 'nie':
                        break
                    else:
                        print "!!! Wpisz tak lub nie!"

    def otworz(self, rzecz):
        for elem in self.aktualne_pomieszczenie.zawartosc:
            if elem.nazwa == rzecz:
                if rzecz == 'skrzynia':
                    self.otworz_skrzynie(rzecz)
                    return
                else:
                    self.stan_mebla(rzecz)
                    return
        print "Nie ma takiego mebla! Wybierz jeden z listy:"
        print ', '.join(
            [me.nazwa for me in self.aktualne_pomieszczenie.zawartosc])

    def otworz_skrzynie(self, rzecz):
        for przedmiot in self.postac.wyposazenie:
                if przedmiot.nazwa == "Openidus":
                    for czar in self.postac.uzyte_czary:
                        if czar == "otworz":
                            for przedmiot in self.aktualne_pomieszczenie.zawartosc:
                                if przedmiot.nazwa == rzecz:
                                    przedmiot.zawartosc[0].opis()
                                    sys.exit()
                    print "Rzuc czar z rozdzki Openidus! [komenda uzyj]"
                    print "\n", '\n'.join(self.komendy)
                    return
        print """Nie masz rozdzki Openidus, ktora jest niezbedna do
otwarcia skrzyni."""
        print "\n", '\n'.join(self.komendy)

    def idz_do_taj_komnata(self, pom):
        for przedmiot in self.postac.wyposazenie:
            if przedmiot.nazwa == "Swietlik":
                self.idz_do(pom)
                return True
        print """\n! Aby tu wejsc musisz miec rozdzke Swietlik!
Wybierz inne pomieszczenie!"""
        print "\n", self.lista_pomieszczen()

    def podnies(self):
        self.postac.wyposazenie += self.aktualny_przedmiot
        print "Do wyposazenia zostal dodany:",self.aktualny_przedmiot[0].nazwa
        self.aktualny_przedmiot = []

    def uzyj(self, przedmiot):
        for przed in self.postac.wyposazenie:
            if przed.nazwa == przedmiot:
                for rzecz in PRZEDMIOTY:
                    if rzecz.nazwa == przedmiot:
                        self.postac.punkty_zdr += rzecz.punkty_zdrowia
                        print "Ulegly zmianie Twoje punkty zdrowia."
                        self.postac.wyposazenie.remove(rzecz)
                        print "\n", '\n'.join(self.komendy)
                        return
                if przed.nazwa == "Swietlik":
                    if self.aktualne_pomieszczenie.nazwa == "tajemnicza komnata":
                        self.postac.uzyte_czary += [przed.czar]
                        print "Wlasnie uzyles czaru: ", przed.czar
                        print "\n", '\n'.join(self.komendy)
                        return
                    else:
                        print """Musisz byc w tajemniczej komnacie, aby moc
uzyc ten czar!"""
                        return
                        print "\n", '\n'.join(self.komendy)
                if przed.nazwa == "Openidus":
                    if self.postac.punkty_zdr < 30:
                        print """\n! Masz za malo punktow zdrowia aby tu wejsc!
Musisz miec conajmniej 30. Znajdz i zjedz cos [komenda uzyj],
aby zwiekszyc punkty.
Wiecej na temat punktow zdrowia dowiesz sie wpisujac: info 6"""
                        print "\n", '\n'.join(self.komendy)
                        return
                    for cz in self.postac.uzyte_czary:
                        if cz == "swiatlo":
                            self.postac.uzyte_czary += [przed.czar]
                            print "Wlasnie uzyles czaru: ", przed.czar
                            return
                            print "\n", '\n'.join(self.komendy)
                        else:
                            print """Musisz uzyc wpierw czaru "swiatlo"!"""
                            return
                            print "\n", '\n'.join(self.komendy)
        print "! Nie masz takiego przedmiotu."
        print "\n", '\n'.join(self.komendy)

    # START

    def start(self):
        gracz = raw_input("Podaj swoje imie: ").strip()
        print POLECENIA_START[0] % gracz
        ### tworzenie postaci
            # dane
        bohater = ''
        print POLECENIA_START[1]
        while (bohater != '0' and bohater != '1'):
            bohater = raw_input().strip()
            if (bohater != '0' and bohater != '1'):
                print """!!! Wybierz "0" lub "1"! """
        imie = raw_input("\nWpisz imie swojej postaci: ").strip()
        um_latania = ''
        if bohater == '1':
            print POLECENIA_START[2]
            while (um_latania != 'nie' and um_latania != 'tak'):
                um_latania = raw_input().strip()
                if (um_latania != 'nie' and um_latania != 'tak'):
                    print """!!! Wpisz "tak" lub "nie"! """
            # postac
        if bohater == '0':
            self.postac = Mag(imie)
            print """\n~~~~~~~~~~~~~~~~~~\nDane Twojego Maga:"""
            self.postac.wypisz()
        elif bohater == '1':
            self.postac = Wrozka(imie, um_latania)
            print "\n~~~~~~~~~~~~~~~~~~~\nDane Twojej Wrozki:"
            self.postac.wypisz()
        ### rozpoczecie gry
        print
        print POLECENIA_START[3], self.aktualne_pomieszczenie.nazwa.upper()
        print POLECENIA_START[4], "\n", '\n'.join(self.komendy)
        print POLECENIA_START[5]
        while True:
            polecenie = raw_input("\n> ").strip().split(" ", 1)
            if polecenie[0] == "info":
                if len(polecenie) < 2:
                    cyfra = raw_input("Podaj cyfre polecenia: ").strip()
                    self.info(cyfra)
                else:
                    self.info(polecenie[1])
            elif polecenie[0] == '0':
                self.lista_pomieszczen()
                print "\n",'\n'.join(self.komendy)
            elif polecenie[0] == '1':
                if len(polecenie) < 2:
                    self.lista_pomieszczen()
                    pom = 'tajemnicza komnata'
                    while pom == 'tajemnicza komnata':
                        pom = raw_input("Podaj nazwe pomieszczenia: ").strip()
                        if pom == 'tajemnicza komnata':
                            if self.idz_do_taj_komnata(pom):
                                break
                        else:
                            self.idz_do(pom)
                else:
                    if polecenie[1] == 'tajemnicza komnata':
                        self.idz_do_taj_komnata(polecenie[1])
                    else:
                        self.idz_do(polecenie[1])
            elif polecenie[0] == '2':
                self.stan_pomieszczenia()
            elif polecenie[0] == '3':
                if len(polecenie) < 2:
                    self.stan_pomieszczenia()
                    rzecz = raw_input(
                        "Podaj mebel, ktory chcesz otworzyc: ").strip()
                    self.otworz(rzecz)
                else:
                    self.otworz(polecenie[1])
            elif polecenie[0] == '4':
                if not self.postac.wyposazenie:
                    print "Aktualnie nie posiadasz zadnego przedmiotu."
                    print "\n",'\n'.join(self.komendy)
                else:
                    print "Posiadasz:\n", '\n'.join(
                        [przed.nazwa for przed in self.postac.wyposazenie])
                    print "\n",'\n'.join(self.komendy)
            elif polecenie[0] == '5':
                if len(polecenie) < 2:
                    print "Wyposazenie:\n",'\n'.join(
                        [przed.nazwa for przed in self.postac.wyposazenie])
                    przedmiot = raw_input(
                        "\nPodaj przedmiot, ktory chcesz uzyc: ").strip()
                    self.uzyj(przedmiot)
                else:
                    self.uzyj(polecenie[1])
            elif polecenie[0] == '6':
                print "Punkty zdrowia:", self.postac.punkty_zdr
                print """Wiecej na temat punktow zdrowia dowiesz sie wpisujac:
info 6"""
                # wyjscie
            elif polecenie[0] == '7':
                wyjscie = ''
                while (wyjscie != 'tak' and wyjscie != 'nie'):
                    wyjscie = raw_input(
                        "Czy na pewno chcesz wyjsc?[tak/nie] ").strip()
                    if wyjscie == 'tak':
                        sys.exit()
                    elif wyjscie == 'nie':
                        print "\n", '\n'.join(self.komendy)
                    else:
                        print """!!! Wpisz "tak" lub "nie"! """

Dom().start()
