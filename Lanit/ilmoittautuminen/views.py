# -*- coding: utf-8 -*-
# Ääkköset toimimaan

from django.shortcuts import render
from .forms import Ilmolomake  # PaikkavalintaLomake
from .models import Lanittaja, Istumapaikka
from django.core.mail import send_mail
from django.conf import settings  # Emailia varten
from django.contrib import messages

# Yhden lanipaikan hinta
HINTA_PER_PAIKKA = 20


# Rekisteriselostesivun tekevä funktio
def rekisteriseloste(request):
    sisalto = {}
    return render(request, 'rekisteriseloste/rekisteriseloste.html', sisalto)


# Etusivun tekevä funktio
def index(request):
    sisalto = {}
    return render(request, 'index/index.html', sisalto)


def ilmoittautuminen(request):
    # renderoidaan ilmoittautumissivu tietokannasta haetuista tiedoista
    # yhdistämällä ne templateen, eli ilmoittautuminen.html:ään

    # Haetaan kannasta paikat, jotka on varattu. Tällä tietorakenteella
    # voidaan värjätä salikuvasta paikat, jotka on jo viety.
    # Varatut paikat on lista, jossa on tuplena (x, y)
    varatut_paikka_objektit = Istumapaikka.objects.filter(varattu=True)

    # Tehdään näistä dictionary, jota käytetään ruksien tulostamiseen
    varatut_paikat = koordinaatit(varatut_paikka_objektit)
    print(varatut_paikat)

    # Jos ollaan laitettu formiin tavaraa ja lähetetään tiedot palvelimelle
    if request.method == 'POST':
        # Tehdään ilmoittautumislomake, jossa on annetut tavarat
        formi = Ilmolomake(request.POST)

        # Tehdään tarkistukset forms.py:ssä
        if formi.is_valid():

            # Haetaan varatut paikat
            paikat_str = formi.cleaned_data.get("Paikat")
            paikat_lista = parsi_paikka_str(paikat_str)

            # Katsotaan, onko jo näitä paikkoja varattu. Jos on, annetaan virhe
            # Tarkistetaan myös varmuudeksi onko paikka ylipäätään olemassa tietokannassa
            if onko_varattu(paikat_lista):
                messages.error(request, "Valitsemasi paikka oli jo varattu tai sitä ei ole olemassa!")

            else:
                # Haetaan ilmoittautujan yhteystiedot
                kokonimi = formi.cleaned_data.get("Kokonimi")
                puhnumero = formi.cleaned_data.get("Puhelinnumero")
                osoite = formi.cleaned_data.get("Osoite")
                kohdeosoite = formi.cleaned_data.get("Sahkoposti")

                # Laitetaan kama tietokantaan
                aseta_tietokantaan(paikat_lista, kokonimi, puhnumero, osoite, kohdeosoite)

                # Lähetetään vahvistusviesti + lasku
                lahetaposti(paikat_str, paikat_lista, kohdeosoite)

                # Annetaan kiitos-ilmoitus
                messages.success(request, "Isot kiitokset varauksestasi!")


    # Jos taas ollaan vasta lataamassa sivua, annetaan tyhjä formi
    else:
        formi = Ilmolomake()

    # Tiedot, jotka menevät sivun rakentamiseen templatesta
    sisalto = {
        'paikat':varatut_paikat,
        "formi": formi
    }
    return render(request, 'ilmoittautuminen/ilmoittautuminen.html', sisalto)


# Tämä parsii paikkastr:n. Tarkistukset on jo tehty formissa, joten datan
# pitäisi olla oikeanlaista
def parsi_paikka_str(paikat):
    # Talletetaan tuplelistaan rivi ja paikkanumero
    paikkalista = []

    # Paikat annetaan muodossa A1,B11,C4...
    paikka_alkiot = paikat.split(",")

    # Käydään jokainen paikka läpi
    for alkio in paikka_alkiot:
        # Rivin kirjain on ekana alkiona
        rivi = str(alkio[0])

        # Jos numero on 1-9
        if len(alkio) == 2:
            paikkanumero = int(alkio[1])
        else:
            paikkanumero = int(alkio[1:])

        paikkalista.append((rivi, paikkanumero))

    return paikkalista


# Katsotaan tietokannasta, onko paikat_listassa olevat paikat vielä varattuja.
# Palauttaa True, jos on, False jos ei
def onko_varattu(paikat_lista):
    for paikka in paikat_lista:
        rivi = paikka[0]
        numero = paikka[1]

        # Haetaan kyseinen istumapaikka ja katsotaan onko se varattu
        # Tehdään samalla tarkastelu siltä varalta, että paikkaa ei
        # löydykään tietokannasta
        try:
            kyseinen_paikka = Istumapaikka.objects.get(rivi=rivi, paikkanumero=numero)
        except Istumapaikka.DoesNotExist:
            return True

        if kyseinen_paikka.varattu:
            return True

    # Käytiin kaikki paikat läpi ja mikään ei ollut varattu
    return False


# Funktio asettaa paikan varatuksi ja tekee uuden käyttäjän tietokantaan, sekä
# tekee foreignkeyn istumapaikkaan
def aseta_tietokantaan(paikat_lista, kokonimi, puhnumero, osoite, kohdeosoite):
    # Tehdään uusi monikko Lanittaja-tauluun
    uusi_lanittaja = Lanittaja(kokonimi=kokonimi, puhnumero=puhnumero, osoite=osoite,
                               sahkoposti=kohdeosoite)
    uusi_lanittaja.save()

    # Käydään kaikki paikat läpi
    for alkio in paikat_lista:
        # Muokataan istumapaikkaa. Haetaan se ensin tietokannasta. Sitten päivitetään
        # omistaja ja asetetaan paikka varatuksi.
        paikka = Istumapaikka.objects.get(rivi=alkio[0], paikkanumero=alkio[1])
        paikka.varattu = True
        paikka.omistaja = uusi_lanittaja

        # Lopuksi talletetaan homma tietokantaan
        paikka.save()


def lahetaposti(paikat_str, paikat_lista, kohdeosoite):
    # Lasketaan varattujen paikkojen määrän perusteella lasku
    lasku = len(paikat_lista) * HINTA_PER_PAIKKA

    # Lähetetään vahvistusviesti, jossa on myös lasku
    aihe = "PowerLan 2015 ilmoittautuminen"
    viesti = """
    Tervetuloa PowerLan 2015 -lanitapahtumaan!

    Varasit paikat: {}

    Kustannukset ovat yhteensä: {}€


    Ystävällisin terveisin,
    PowerLan-tiimi
    """.format(paikat_str, lasku)

    # Lähettäjäksi sama, mikä on määritelty asetuksissa
    lahetysosoite = settings.EMAIL_HOST_USER

    # Lähetetään meili
    send_mail(aihe, viesti, lahetysosoite, [kohdeosoite], fail_silently=False)


# Funktio ottaa parametrinaan listan paikkaobjekteista, jotka ovat varattuja
# ottaa niistä koordinaatit ja palauttaa ne listana jossa on tupleina
# (x, y)
def koordinaatit(varatut_paikka_objektit):

    koordinaattilista = []

    rivit_numeroina = {"A": 200, "B": 360, "C": 530, "D": 690}

    # Tämä vakio kertoo, paljonko pitää siirtyä koordinaateissa oikealle,
    # kun paikkana pöydässä on yli 7
    SIIRTYMA_X = 50

    # Tämä vakio kertoo, millä kertoimella hypätään seuraavaan paikkaan
    # y-akselilla
    SIIRTYMA_Y = 40

    # Tämä vakio kertoo, mistä kohtaa alkaa kuvassa pöydät kun mennään ylhäältä
    # alas
    Y_ALOITUS = -200

    for alkio in varatut_paikka_objektit:
        rivi = alkio.rivi
        numero = alkio.paikkanumero
        print(rivi)
        print(numero)

        # Jos paikkanumero on 1-7, on rivin koordinaati se mikä on
        # annettu rivit_numeroina -sanakirjassa, muuten se on se + 100 pikseliä
        if numero < 8:
            x = rivit_numeroina[rivi]
        else:
            x = rivit_numeroina[rivi] + SIIRTYMA_X

        # Paikka-akseli aloitetaan kuvasta nähden kohdasta Y_ALOITUS
        #
        if numero < 8:
            y = Y_ALOITUS + numero * SIIRTYMA_Y
        else:
            y = Y_ALOITUS + (numero - 7) * SIIRTYMA_Y

        koordinaattilista.append((x, y))

    return koordinaattilista