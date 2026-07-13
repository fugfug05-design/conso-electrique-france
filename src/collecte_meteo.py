
import time
import requests
import pandas as pd

URL = "https://archive-api.open-meteo.com/v1/archive"

VILLES = { "paris": (48.85, 2.35), "lyon": (45.76, 4.84), "marseille": (43.30, 5.37),
    "toulouse": (43.60, 1.44), "lille": (50.63, 3.07), "bordeaux": (44.84, -0.58),
    "nantes": (47.22, -1.55), "strasbourg": (48.57, 7.75), }


temperatures = {}

for nom, (lat, lon) in VILLES.items():

    print(f"Téléchargement {nom}...")

    reponse=requests.get(URL,params={"latitude": lat,
    "longitude": lon,
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "hourly": "temperature_2m",
    "timezone": "UTC",})

    if reponse.status_code != 200:                                  
        print(f"Erreur pour {nom} : code {reponse.status_code}")      
        exit()                                                        

    donnees=reponse.json()

    temperatures[nom]=donnees["hourly"]["temperature_2m"]
    temperatures["date_heure"] = donnees["hourly"]["time"]

    time.sleep(1)

df = pd.DataFrame(temperatures)

df["temp_france"] = df[list(VILLES.keys())].mean(axis=1)

df.to_csv("data/meteo_2023_2024.csv", index=False)

print(df["temp_france"].describe())