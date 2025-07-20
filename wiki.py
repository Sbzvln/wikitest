import streamlit as st
import requests
import datetime

# Functie om feiten op te halen
def fetch_facts(month: int, day: int):
    mm = f"{month:02d}"
    dd = f"{day:02d}"
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{mm}/{dd}"
    headers = {"User-Agent": "FeitjesApp/2.0 (jij@example.com)"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    return resp.json()

# Functie om mogelijke afbeelding op te halen via zoek-API
def fetch_image(search_title: str):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": search_title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 200
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    data = r.json().get("query", {}).get("pages", {})
    for page in data.values():
        if "thumbnail" in page:
            return page["thumbnail"]["source"]
    return None

# Streamlit-appconfig
st.set_page_config(page_title="📅 Feitjes van Vandaag", layout="wide")
st.title("📅 Feitjes van Vandaag inclusief afbeeldingen & datumkiezer")

# Datumkiezer component
chosen_date = st.date_input("Kies een datum:", value=datetime.date.today())
month, day = chosen_date.month, chosen_date.day

# Ophalen van data
data = fetch_facts(month, day)
if not data:
    st.error("Kon geen data ophalen — controleer je internetverbinding.")
    st.stop()

# 10 items per categorie
NUM = 10
categories = [("events", "📌 Historische gebeurtenissen"),
              ("births", "🎂 Geboren op deze dag"),
              ("deaths", "🪦 Overleden op deze dag")]

for key, title in categories:
    st.subheader(title)
    items = data.get(key, [])[:NUM]
    for item in items:
        year = item.get("year")
        text = item.get("text")
        st.write(f"**{year}**: {text}")

        # Optioneel: afbeelding zoeken op basis van de hoofdpersoon of onderwerp
        # Gebruik gewoon het stukje vóór '(' als zoekterm
        search_title = text.split('(')[0][:50]  # eerste deel
        img_url = fetch_image(search_title)
        if img_url:
            st.image(img_url, caption=search_title, width=200)