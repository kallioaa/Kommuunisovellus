# Kommuunisovellus

Sovelluksen tarkoituksena on luoda leikkimielinen pistesysteemi kanssa-asujien kanssa käytettäväksi. Jokaisella käyttäjällä on oma pistepankki. Pisteitä voi saada kahdella eri tavalla.

1. Events: käyttäjät voivat hakea pisteitä luomalla tapahtumia, joko itselleen tai muille. Nämä tapahtumat menevät tämän jälkeen äänestysprosessin läpi, ja puolet äänistä takaa tapahtuman läpimenemisen.
   - Esimerkki: Aatu hakee 50 pistettä aatulle, koska tiskasi.
2. Todos: toinen vaihtoehto saada pisteitä on askareiden avulla. Käyttäjä voi luoda askareen, ja muut käyttäjät voivat ilmoittautua tapahtuman tekijäksi. Kun tekijä on merkannut tapahtuman suoritetuksi, niin askareen luojan tulee hyväksyä tapahtuma tehdyksi. Tässä tapauksessa pisteet otetaan tapahtuman luojan balanssista ja annetaan tapahtuman tekiijälle.
   - Esimerkki: Aatu luo 200 pisteen askareen ikkunoiden pesemisestä, jonka tekijäksi ilmoittautuu Mikko. Mikon pestyä ikkunat, Aatu varmistaa puhtaa lopputuloksen ja Aatun balanssista siirtyy Mikolle 200 pistettä.
  
Tarkempi selostus toiminallisuudesta:
- Käyttäjä voi kirjautua sovellukseen
- Käyttäjä näkee muiden sekä omat pisteet
- Käyttäjä voi luoda tapahtuman "Eventin" itselle tai toiselle.
- Käyttäjä näkyy kaikki äänestyksen läpäisseet tapahtumat, ja voi hakea niistä
- Käyttäjä voin äänestää kyllä tai ei muiden luomiin tapahtumiin
- Käyttäjä voi tarkastella ja hakea "Todos" askareita
- Käyttäjä voi ilmoittautua askareen tekijäksi
- Käyttäjä voi merkitä suoritetun askareen tehdyksi
- Käyttäjä voi luoda oman askareen
- Käyttäjä voi poistaa tai muokata askaretta ennen kuin siihen on ilmoittautunut tekijä
- Käyttäjä voi varmistaa oman askareen tehdyksi

