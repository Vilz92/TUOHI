# -*- coding: utf-8 -*-
# Ääkköset toimimaan

from django.db import models
from datetime import *

# Rekisteroitavan asiakkaan tiedot
class Lanittaja(models.Model):
    kokonimi = models.CharField(max_length=200)
    sahkoposti = models.EmailField() # EmailField tekee automaattisesti tarkastukset
    puhnumero = models.CharField(max_length=20)
    osoite = models.CharField(max_length=200)

    # Django ei tykkää ääkkösistä joten laitetaan errorin kaappaaja
    def __str__(self):
        return self.kokonimi.encode('ascii', errors='replace')


# Yksittainen istumapaikka
class Istumapaikka(models.Model):
            
    # Paikalla kaksi tietoa. Millä rivillä ollaan ja millä paikalla
    rivi = models.CharField(max_length=1) # A, B, C tai D
    paikkanumero = models.IntegerField() # 1-14

    # Aika, jolloin paikka on varattu. Muutetaan aina silloin, kun paikkaa
    # muokataan
    varausaika = models.DateTimeField(default=datetime.now)
    
    # Jos paikka on varattu, mutta ei maksettu
    varattu = models.BooleanField(default=False)
    # Jos paikka on maksettu
    maksettu = models.BooleanField(default=False)

    # Henkilo, joka varasi ja kaiketi maksoi paikan
    # Jos lanittaja poistetaan, nullataan tämä foreignkey. Istumapaikkaa
    # luodessa omistajaa ei myöskään ole
    omistaja = models.ForeignKey(Lanittaja, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    
    def __str__(self):
        if self.varattu and not self.maksettu:
            varaustilanne = "Varattu " + str(self.varausaika)
        elif self.maksettu:
            varaustilanne = "Varattu & maksettu."
        else:
            varaustilanne = "Vapaa."

        return str(self.rivi) + str(self.paikkanumero)