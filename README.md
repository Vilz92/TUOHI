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
   <li>Fail2Ban (IP ban)</li>
   <li>Tripwire (IDS)</li>
   <li>Chroot (Tietokannan isolaatio)</li>
</ul>

<h2>Päivitysprosessi palvelimelle</h2>

Palvelin pyörii osoitteessa 188.226.189.212. Koodari-käyttäjään otetaan yhteyttä SSH:lla
ja pullataan kansioon "gitkansio" uudet kamat. Nämä kopioidaan PowerLanit-kansioon komennolla
sudo cp -r . ~/PowerLanit/, kun ollaan ~/gitkansio/Lanit/Lanit -polussa. Tämän jälkeen restartataan
gunicorn ja nginx komennoilla:
sudo service gunicorn restart
sudo service nginx restart
Päivitetään lisäksi Djangon modelit yms. komennoilla ~/PowerLanit -polussa:
./manage.py makemigrations
./manage.py migrate