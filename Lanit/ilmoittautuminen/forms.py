# -*- coding: utf-8 -*-
# Ääkköset toimimaan

from django import forms

# Rivejä näillä laneilla on A-D
SALLITUT_RIVIT = "ABCD"


# Ilmoittautujan tiedot ottava lomake. Lomake ottaa tiedon, mitkä istumapaikat
# halutaan, sekä ilmoittatujan yhteystiedot. Nämä tallennetaan onnistuessa
# modeliin views.py:ssä
class Ilmolomake(forms.Form):
    Paikat = forms.CharField(max_length=200)
    Kokonimi = forms.CharField(max_length=200)
    Sahkoposti = forms.EmailField()
    Puhelinnumero = forms.CharField(max_length=200)
    Osoite = forms.CharField(max_length=200)

    # Tarkastelua kokonimelle, ettei esim. numeroita, on etu- ja sukunimi yms.
    def clean_Kokonimi(self):
        kokonimi = self.cleaned_data.get("Kokonimi")
        alkiot = kokonimi.split(" ")

        # Jos ei ole välilyöntiä etu- ja sukunimen välissä
        if len(alkiot) != 2:
            raise forms.ValidationError("Anna sekä etu- että sukunimi!")

        return kokonimi


    # Funktio parsii annetun paikkastringin
    def clean_Paikat(self):
        paikat = self.cleaned_data.get("Paikat")

        # Paikat annetaan muodossa A1,B11,C4...
        paikka_alkiot = paikat.split(",")

        # Käydään jokainen paikka läpi
        for alkio in paikka_alkiot:
            # Sallittu paikka saa olla 2-3 merkkiä pitkä riippuen paikan
            # numerosta
            if len(alkio) < 2 or len(alkio) > 3:
                raise forms.ValidationError("Vääränmuotoinen paikka!")

            # Rivin kirjain on ekana alkiona
            rivi = str(alkio[0])
            # Rivi oltava A, B, C tai D
            if rivi not in SALLITUT_RIVIT:
                raise forms.ValidationError("Vääränmuotoinen paikka!")

            # Katsotaan, onko numero todellakin numero
            try:
                # Jos numero on 1-9
                if len(alkio) == 2:
                    paikkanumero = int(alkio[1])

                    # Tarkistetaan vielä, että numero on oikea
                    if paikkanumero < 1 or paikkanumero > 9:
                        raise ValueError
                # Jos numero onkin 11-14
                else:
                    paikkanumero = int(alkio[1:])

                    # Tarkistetaan vielä, että numero on oikea
                    if paikkanumero < 10 or paikkanumero > 14:
                        raise ValueError

            except ValueError:
                raise forms.ValidationError("Vääränmuotoinen paikka!")

            # Katsotaan vielä, ettei samaa paikkaa ole annetu monta kertaa
            if paikka_alkiot.count(alkio) > 1:
                raise forms.ValidationError("Annoit saman paikan monta kertaa!")

        return paikat