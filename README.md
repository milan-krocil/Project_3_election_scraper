# Project_3_election_scraper

POPIS PROJEKTU:

Tento projekt slouzi k extrahovani vysledku voleb z roku 2017. Odkaz na vysledky voleb je https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Po vyberu uzemniho celku program(script) vycrapuje vysledky hlasovani pro vsechny obce do csv souboru.

INSTALACE KNIHOVEN:

Knihovny, ktere jsou pouzity v kodu, jsou ulozene v souboru requirements.txt. 
Pro instalaci doporucuji pouzit nove virtualni prostredi a naistalovanym managerem spustit nasledovne:

pip install -r requirements.txt

SPUSTENI PROGRAMU:

Program se spousti pres prikazovy radek, do ktereho je nutne zadat 2 povinne argumenty.
Instrukce pro spusteni:
1. Zadej prikaz python
2. Zapis nazev souboru election_scraper.py
3. Zadej url link na vybrany uzemni celek (nutne v uvozovkach). Napr uzemni celek Sumperk "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105"
4. Zapis nazev vysledneho csv souboru. Napr vysledky_sumperk.csv

Zapis do prikazoveho radku pro uvedeny priklad bude tedy vypadat nasledovne:
python election_scraper "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105" vysledky_sumperk.csv






