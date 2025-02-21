# Project_3_election_scraper

POPIS PROJEKTU:

Tento projekt slouzi k extrahovani vysledku voleb z roku 2017. Odkaz na vysledky voleb je https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Po vyberu uzemniho celku program(script) vycrapuje vysledky hlasovani pro vsechny obce do csv souboru. 

![image](https://github.com/user-attachments/assets/417c4301-4f8d-44f4-8bb7-6a28a43febdd)

Vyber uzemniho celku se provadi kliknutim na kod obce nebo "krizku" u vyberu obce.



INSTALACE KNIHOVEN:

Knihovny, ktere jsou pouzity v kodu, jsou ulozene v souboru requirements.txt. 
Pro instalaci doporucuji pouzit nove virtualni prostredi a naistalovanym managerem spustit nasledovne:

pip install -r requirements.txt

SPUSTENI PROGRAMU:

Program se spousti pres prikazovy radek, do ktereho je nutne zadat 2 povinne argumenty.
Instrukce pro spusteni:
1. Zadej prikaz python
2. Zapis nazev souboru election_scraper.py
3. Zadej 1 argument (= url link) na vybrany uzemni celek (nutne v uvozovkach). Napr uzemni celek Sumperk "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105"
4. Zapis 2 argument (= nazev vysledneho csv souboru). Napr vysledky_sumperk.csv

Zapis do prikazoveho radku pro uvedeny priklad bude tedy vypadat nasledovne:

python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105" vysledky_sumperk.csv

Pokud dojde k neuplnemu nebo spatnemu zadani, tak program na chybu upozorni.
Napr:![image](https://github.com/user-attachments/assets/6f737ec4-2e56-4b38-a903-538b6b0924e0)



CASTECNY VYSTUP (ukazka csv souboru):
![image](https://github.com/user-attachments/assets/b552dc21-dff8-4699-98dd-4436c4047344)











