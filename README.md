## Kommuunisovellus

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

## Tilanne välipalautus 2
- Suurin osa toiminnallisuudesta toteutettu
- Huomasin bugin, jossa eventin lisäys ei aina onnistun ensimmäisellä kerralla klikkauksella, se tulee korjata
- Virheiden parempaa selvittämistä tulevaisuudessa
- Events listaukset epäselviä äänestyksessä ja muutenkin. Tämän kehittäminen sekä hakutoiminto.
- Sovellus aiemmin kehitetty englanniksi, jos kieli tulee muuttaa, sen tekeminen

## Tilanne välipalautus 2
- Olin aiemmin tehnyt sovelluksen käyttäen ei-sallittuja teknologioista Postgres sql sekä käyttänyt flask wtf ja bootstrap. Tällä viikolla refaktoroin koodin ja otin nämä pois käytöstä
- Suurin osa toiminnallisuudesta toteutettu
- Hakutoiminnallisuus puuttuu vielä
- CSS parantelua seuraavaksi
- Ilmoitusten parantamista sovelluksessa


# Commune App

Welcome to the **Commune App**, a collaborative platform designed to manage events, votes, scoring, and tasks (todos) among multiple user accounts. This README provides an overview of how to set up and use the app’s core features.

---

## Table of Contents

1. [Set-up](#setup)
1. [Overview](#overview)  
2. [Account Management](#account-management)  
3. [Score Table](#score-table)  
4. [Events and Voting](#events-and-voting)  
5. [Todos](#todos)  

---

## Overview

The Commune App is all about creating a communal environment where members can propose events that assign or modify scores for themselves or others. These events go through a voting procedure—if the half or more of the votes are in favor, the credit (score) is awarded. In addition to events, users can also create todos. When a user completes a todo and it’s verified, scores are assigned accordingly. In short, the app revolves around collaboration, community decisions, and shared responsibility.

## Setup

# Setup Instructions (English)

1. **Clone this repository** to your local machine and navigate to its root directory.**

2. **Activate a virtual environment** and install the dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install flask
   ```
3. **Set up a secret key into a .env file. The file should look like this**
   ```bash
   SECRET_KEY='<your_secret_key>'
   ```


4. **Set up the database schema**:
   ```bash
   sqlite3 database.db < db_schema.sql
   ```
   
5. **Add example entries**:
   ```bash
   sqlite3 database.db <db_example_entries.sql
   ```

6. **Run the application**:
   ```bash
   flask run
   ```

---

## Account Management

### Sign Up (Create an Account)
1. Go to the [**Create a new user**](http://127.0.0.1:8000/users/new_user) page.
2. Enter your desired username, email, and password.
3. Submit the form to create your account.

### Or use a testing account from example entries
   * Username: Testaaja
   * Password: testaaja

### Sign In
1. Navigate to the [**Log In**](http://127.0.0.1:8000/users/) page.
2. Provide your credentials (username and password).

Only logged-in users can access the Commune App’s features such as viewing scores, creating events, voting, and managing todos.

---

## User summary

Once logged in, you’ll land on the [**Home**](http://127.0.0.1:8000/) page. Here you will see summary information about the logged in user. You can also go and see the summary of another user through user search functionality which can be found in the navigation bar.

When you are looking into your own summary, at the bottom of the page you will find events that you can vote on. 

---

## Events

### Creating an Event
1. Navigate to the [**Events**](http://127.0.0.1:8000/events/) section.
2. Click [**Add New Event**](http://127.0.0.1:8000/events/new_event).
3. Fill out the details of the event, including:
   - **Applied for**: Which user(s) should get this score change?
   - **Title/Description** of the event.
   - **Score Change**: How many points are awarded or deducted? (Can be yourself or someone else.)
4. Submit the event.

**Note**: Once you create an event, an automatic **pass vote** (in favor) from you is recorded.

### Score Application
- When an event is **passed**, the recipient(s) automatically get the specified score adjustment (positive or negative).
- The total scores are updated, and these changes will be reflected in the **Score Graph** on the Home page.

---

## Todos

The Commune App also includes a **Todo** feature where users can create tasks, assign themselves or be assigned by others, and complete them for score changes.

### Creating a Todo
1. Navigate to the [**Todos**](http://127.0.0.1:8000/todos/) section.
2. Click [**Create Todo**](http://127.0.0.1:8000/todos/new_todo).
3. Fill in:
   - **Title** and **Description** of the task.
   - **Score** to be associated with completing the todo.
4. Submit the todo.

### Assigning and Completing a Todo
1. Any user can **assign themselves** to the todo (unless it’s already assigned).
2. Once the assigned person finishes the task, they **mark it completed**.
3. The creator of the todo can **verify** it after.
   
### Verification and Scoring
- When the **creator** verifies that the todo has been completed:
  - The **negative score** is added to the account that created the todo (as some cost or accountability for creating tasks).
  - The **positive score** is awarded to the user who completed it.
 
### Updating and deleting a todo
- When you are the creator of the todo, an there is no one assigned to it yet, you will have the option to delete it or update it. Theses operations are not possible after so they can't me misused. 

This ensures fairness, where creating a todo has a cost (negative score for the creator), but it’s offset by the benefit the assigned user gets upon completion (positive score).
