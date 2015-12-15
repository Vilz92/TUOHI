<h1>PowerLan ilmoittautumissivusto</h1>

Tämä projekti palvelee kahta eri käyttötarkoitusta: saada pelitapahtumalle
elektroninen ilmoittautumistapa ja tehdä Turvallisen ohjelmoinnin kurssille
harjoitustyö.

<h2>Käytetty alusta ja ohjelmistot</h2>

Sivustoa pyöritetään DigitalOceanin tarjoamalla virtuaaliprivaattiserverillä,
jossa pyörii Ubuntu 14.04 ja mm. seuraavat ohjelmat uusimmilla versioilla:
<ul>
   <li>Gunicorn (WSGI HTTP Server)</li>
   <li>Django (Web-framework)</li>
   <li>UFW (Palomuuri)</li>
   <li>PostgreSQL (Tietokanta)</li>
</ul>

<h2> Ohjelman ajaminen </h2>
Jos haluat ajaa ohjelmaa omalla koneellasi, käytä esim. Virtualboxia pyörittääksesi
Ubuntu 14.04:ää ja asenna siihen Django, sekä Crispy Forms 
(http://django-crispy-forms.readthedocs.org/en/latest/) <br>
Virtualenv (https://virtualenv.readthedocs.org/en/latest/installation.html) on hyvä
työkalu python-kirjastojen hallinnointiin. 

Kun haluat päästä nopeasti pyörittämään softaa ilman PostgreSQL:n asentelua ja konffaamista,
aseta Lanit/Lanit/settings.py:stä DEBUG = True, jolloin tietokanta pyörii SQLitessä suoraan.
Käskytä Lanit/manage.py:tä seuraavasti: <br>
./manage.py makemigrations <br>
./manage.py migrate <br>
./manage.py runserver <br>
Tällöin serveri pyörii komentokehoitteen kertomassa osoitteessa.

Lisäksi jos haluat aktivoida admin-sivut, aja manage.py:lle seuraava:
./manage.py createsuperuser <br>