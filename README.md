# Pingviinit ohtu miniprojekti

[Backlog](https://docs.google.com/spreadsheets/d/108_K1P9uL-86Tu4TdDwMSQYmsihaklVIYrhUz3J1-l8/edit?usp=sharing)

# Definition of done:
<ul>
  <li>Koodin ylläpidettävyyden tulee olla mahdollisimman hyvä: järkevä nimeäminen, selkeä ja perusteltu arkkitehtuuri ja yhtenäinen koodityyli.</li>
  <li>Asiakas pääsee näkemään koko ajan koodien ja testien tilanteen CI-palvelusta.</li>
  <li>User Storyjen hyväksymiskriteerit toteutuvat.</li>
</ul>



![GHA workflow badge](https://github.com/saarapasonen/pingviinit/workflows/CI/badge.svg)

[![codecov](https://codecov.io/github/saarapasonen/pingviinit/graph/badge.svg?token=HV13RSQWRS)](https://codecov.io/github/saarapasonen/pingviinit)

# Asennus- ja käyttöohjeet
1. Kloonaa repositorio omalle koneellesi.
2. Avaa selaimessa (https://aiven.io) ja rekisteröidy/kirjaudu sisään. Luo PostgreSQL-tietokanta ja kopioi saamasi Service URI-linkki kohdasta Connection Information.
3. Luo .env-tiedosto, joka sisältää seuraavan (katso tarkkaan, että urlin alku on muodossa postgresql:// eikä postgres://):
   ```
   DATABASE_URL=postgresql://xxx
   TEST_ENV=true
   SECRET_KEY=satunnainen_merkkijono
   ```
4. Lataa riippuvuudet komennolla
   ```
   poetry install
   ```
5. Mene virtuaaliympäristöön komennolla
   ```
   poetry shell
   ```
6. Ensimmäistä kertaa sovellusta käynnistäessä tulee suorittaa komento
   ```
   python src/db_helper.py
   ```
   Jos tämä ei toimi koneellasi, kokeile
   ```
   python3 src/db_helper.py
   ```
7. Käynnistä sovellus komennolla
   ```
   python src/index.py
   ```
8. Nyt sovellus toimii selaimellasi.

