import requests

URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/exports/csv"

params = {
    "select": "date_heure,consommation,nucleaire,eolien,solaire,hydraulique,gaz,charbon,fioul,bioenergies,ech_physiques,taux_co2",
    "where": "date_heure >= date'2023-01-01' AND date_heure < date'2025-01-01'",
    "order_by": "date_heure",
}

print("Téléchargement en cours...")


reponse=requests.get(URL,params=params)


reponse.status_code

if reponse.status_code != 200:
    print(f"Erreur : le serveur a répondu {reponse.status_code}")
    exit()

with open("data/eco2mix_2023_2024.csv", "w", encoding="utf-8") as f:
    f.write(reponse.text)

nb_lignes = len(reponse.text.split("\n"))
print(f"{nb_lignes} lignes téléchargées dans data/eco2mix_2023_2024.csv")
