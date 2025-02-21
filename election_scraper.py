"""
projekt_3_elections_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Milan Krocil
email: milan.krocil@email.cz
       mr.milan.krocil@gmail.com
"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv
import sys
import re

def kontrola_zadani_systemovych_argumentu():
       if len(sys.argv) != 3:
              print(f"Pro spusteni programu nejsou zadany vsechny argumenty")
              sys.exit(1)
       link = sys.argv[1]
       jmeno_csv = sys.argv[2]
       if not link.startswith('https:'):
              print(f"Prvni argument neni zadany ve spravnem tvaru url link. Bylo zadano: {link}")
              sys.exit(1)
       elif not jmeno_csv.endswith('.csv'):
              print(f"Druhy argument neobsahu nazev souboru s priponou csv. Bylo zadano: {jmeno_csv}")
              sys.exit(1)

kontrola = kontrola_zadani_systemovych_argumentu()   

def ziskani_cisla_kraje(url_adresa_cislo_kraje):
    """ Ze zadaneho url zjisti cislo kraje, ktere vrati k dalsimu pouziti
    """
    url_adresa_cislo_kraje = sys.argv[1]
    if "xkraj=" in url_adresa_cislo_kraje:
        prvni_index_kraj = url_adresa_cislo_kraje.find("xkraj=") + len("xkraj=")
        posledni_index_kraj = url_adresa_cislo_kraje.find("&",prvni_index_kraj)
        if posledni_index_kraj == -1:
            cislo_kraje = url_adresa_cislo_kraje[prvni_index_kraj:]
        else:
            cislo_kraje = url_adresa_cislo_kraje[prvni_index_kraj:posledni_index_kraj]
    return cislo_kraje

def ziskani_cisla_regionu(url_adresa_cislo_regionu):
       """ Ze zadaneho url zjisti cislo regionu, ktere vrati k dalsimu pouziti
       """
       url_adresa_cislo_regionu=sys.argv[1] 
       if "xnumnuts=" in url_adresa_cislo_regionu:
              prvni_index_region = url_adresa_cislo_regionu.find("xnumnuts=") + len("xnumnuts=")
              posledni_index_region = url_adresa_cislo_regionu.find("&",prvni_index_region)
              if posledni_index_region == -1:
                     cislo_regionu = url_adresa_cislo_regionu[prvni_index_region:]
              else:
                     cislo_regionu = url_adresa_cislo_regionu[prvni_index_region:posledni_index_region]
       return cislo_regionu

def ziskani_url_obsahu():
    """ Nacte url link ze zadaneho argumentu a vypise jeho cely obsah v HTML, tento obsah vrati na dalsi zpracovani
    """
    url=sys.argv[1]
    # url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105"
    odezva = requests.get(url)
    print(odezva)
    return odezva

def ziskani_parsovane_odezvy(): 
    """ Rozdeli/Parsuje HTML vyctene z odkazu 
    """
    url_adresa_k_parsovani = ziskani_url_obsahu()
    rozdelena_odezva = BeautifulSoup(url_adresa_k_parsovani.text,features="html.parser")
    return rozdelena_odezva

def najde_data_se_seznamem_obci():
    """  Vytvori seznam vsech kodu obci a ulozi je do slovniku
    """
    seznam_obci = ziskani_parsovane_odezvy()
    kody_s_obci = seznam_obci.find("div",{"id":"inner"})
    seznam_href = kody_s_obci.find_all("a")
    
    list_obci = []

    for data in seznam_href:
       href=data.get("href","")
       if "xobec=" in href:
            prvni_index = href.find("xobec=") + len("xobec=")
            posledni_index = href.find("&",prvni_index)
            if posledni_index == -1:
                cislo_obce = href[prvni_index:]
            else:
                cislo_obce = href[prvni_index:posledni_index]  
                list_obci.append(cislo_obce)
    return list_obci

def vytvoreni_slovniku_kod_obce_url():
    """ Vytvori slovnik, kde klice jsou kody obci a hodnotami jsou jejich URL
    """ 
    slovnik_obci_a_jejich_url_link ={} 
    zvoleny_kraj = ziskani_cisla_kraje(ziskani_url_obsahu())
    zvoleny_region = ziskani_cisla_regionu(ziskani_url_obsahu())
    seznam_obci = najde_data_se_seznamem_obci()

    for zvolena_obec in seznam_obci:
       url_link_vybranych_obci = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={zvoleny_kraj}&xobec={zvolena_obec}&xvyber={zvoleny_region}" 
       slovnik_obci_a_jejich_url_link[zvolena_obec] = url_link_vybranych_obci
    return slovnik_obci_a_jejich_url_link   

def ziskani_url_obce (url_obce):
    """ Nacte url obce a vypise cely obsah v HTML.
    """
    adresa = url_obce
    odpoved = requests.get(adresa)
    return odpoved


def ziskani_parsovane_odezvy2(url_adresa_k_parsovani):
    """ Parsuje HTML vyctene z odkazu 
    """
    rozdelena_odezva = BeautifulSoup(url_adresa_k_parsovani.text,features="html.parser")
    return rozdelena_odezva

def ziskani_volici_v_seznamu_vydane_obalky_platne_hlasy(rozdelena_odpoved):
    """ Ziskani pocty volicu, poctu vydanych obalek, pocet platnych znaku. 
    """
    tabulka_s_daty = rozdelena_odpoved.find("table",{"id":"ps311_t1"})
    vsechny_tr = tabulka_s_daty.find_all("tr")
    vyber_td_s_daty = vsechny_tr[2]
    td_na_radku = vyber_td_s_daty.find_all("td")
    return  {
        "Volici v seznamu": re.sub(r'\s+', '', td_na_radku[3].text),
        "Vydane obalky": re.sub(r'\s+', '', td_na_radku[4].text),
        "Platne hlasy": re.sub(r'\s+', '', td_na_radku[7].text)
       }
      
def vyhledani_nazvu_obce(rozdelena_odpoved_k_obcim):
    """ Vyhledani nazvu obce
    """
    tabulka_s_obci = rozdelena_odpoved_k_obcim.find("div",{"class":"topline"})
    obec = tabulka_s_obci.find_all("h3")
    vybrana_obec = obec[2].get_text().split(" ",1)
    vybrana_obec_nazev = vybrana_obec[1].strip()
    return {"Nazev obce":vybrana_obec_nazev}

def strany_a_jejich_pocet_hlasu(rozdelena_odpoved_ke_stranam):
    """ Ziskani nazvu strany a jeji pocet hlasu. Vystupem je slovnik, ktery je osetren o data se zadnym klicem a zaroven hodnotou.
    """
    vystupy = []
    slovnik_strany ={}
    osetreny_slovnik_strany={}

    tabulka_se_stranami = rozdelena_odpoved_ke_stranam.find("div",{"id":"inner"})
    strany = tabulka_se_stranami.find_all("td")
    for strana in strany:
        vystup = strana.get_text()
        vystupy.append(vystup)

    for vysledky_stran in range(1,len(vystupy) - 1,5):
        slovnik_strany[vystupy[vysledky_stran]] = vystupy[vysledky_stran+1]
    for k,h in slovnik_strany.items():
        if not (k=="-" and h=="-"):
            osetreny_slovnik_strany[k]=h
    return osetreny_slovnik_strany             
                   
          
def konsolidace_dat_vybrane_obce(kod_obce_a_url):
    """ Slouceni vsech hledanych parametru jedne obce 
    """
    data_obci_ve_slovniku = {}
    kod_obce = list(kod_obce_a_url.keys())[0]
    url_link = list(kod_obce_a_url.values())[0]
    url_obce = ziskani_url_obce(url_link)
    odezva_z_url = ziskani_parsovane_odezvy2(url_obce)
    nazev_obce = vyhledani_nazvu_obce(odezva_z_url)
    volici_obalky_platne_hlasy = ziskani_volici_v_seznamu_vydane_obalky_platne_hlasy(odezva_z_url)
    strany_a_pocty_hlasu = strany_a_jejich_pocet_hlasu(odezva_z_url)
    data_obci_ve_slovniku = {"Kod obce":kod_obce, **nazev_obce,**volici_obalky_platne_hlasy,**strany_a_pocty_hlasu}
    return data_obci_ve_slovniku

def konsolidace_vsech_vybranych_obci(kody_s_obcemi_a_jejich_url):
    """ Vytvori seznam vsech obci s hledanymi udaji
    """
    seznam_s_hledanymi_daty =[]
    for key,value in kody_s_obcemi_a_jejich_url.items():
        data_obce = konsolidace_dat_vybrane_obce({key:value})
        seznam_s_hledanymi_daty.append(data_obce)

    return seznam_s_hledanymi_daty
 

def vytvoreni_a_zapis_do_csv(slovnik_s_daty):
    """ Vytvoreni csv souboru ze scrapovanych dat s nazvem, ktery byl zadan pred spustenim souboru uzivatelem
    """
    nazev_csv_souboru = sys.argv[2]
    with open (nazev_csv_souboru, mode="w", encoding ="UTF-8", newline="") as novy_csv:
        zahlavi=slovnik_s_daty[0].keys()
        zapisovac=csv.DictWriter(novy_csv,fieldnames=zahlavi, quoting=csv.QUOTE_NONE, escapechar='\\')
        zapisovac.writeheader()
        for zapis_do_csv in slovnik_s_daty:
              zapisovac.writerow(zapis_do_csv)
    return nazev_csv_souboru

if __name__ == "__main__":
    vysledek = vytvoreni_a_zapis_do_csv(konsolidace_vsech_vybranych_obci(vytvoreni_slovniku_kod_obce_url()))  







