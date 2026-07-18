# Consommation électrique française : analyse et prévision

**Qu'est-ce qui détermine la consommation électrique de la France, et peut-on la prévoir ?**
Analyse de deux ans de données réelles du réseau électrique français (éco2mix, RTE),
de la collecte par API jusqu'à un duel contre les prévisions officielles de RTE.

![Podium des prévisions](figures/podium_mae.png)

## Résultats clés

- **Thermosensibilité mesurée : -2 066 MW par degré** en dessous de 15°C (R² = 0,79),
  cohérente avec les ~2 400 MW/°C communiqués par RTE. Chaque degré de froid
  équivaut à environ deux réacteurs nucléaires supplémentaires.
- **Modèle de prévision J+1 : 1 126 MW d'erreur moyenne** (2,2% de la consommation),
  soit **-51% par rapport à la prévision naïve**, avec une simple régression linéaire
  à 5 variables construites par analyses d'erreur successives.
- **Duel contre RTE : les pros restent 1,7× meilleurs** (647 MW d'erreur corrigée).
  Un écart honnête pour 5 features linéaires face à des équipes dédiées.
- **Découverte d'un biais de mesure de +1 139 MW** entre les prévisions RTE et les
  données consolidées : sans sa correction, on aurait conclu à tort "battre" RTE.

![Thermosensibilité](figures/thermosensibilite.png)

## Les données

| Source | Contenu | Période | Granularité |
|--------|---------|---------|-------------|
| [éco2mix (RTE / ODRE)](https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/) | Consommation, production par filière, prévisions officielles | 2023-2024 | 30 min |
| [Open-Meteo](https://open-meteo.com/) | Températures horaires de 8 grandes villes, moyennées | 2023-2024 | 1 h |

Les données sont collectées par API via les scripts de `src/` (~70 000 mesures).

## La démarche

| Notebook | Contenu |
|----------|---------|
| `01-collecte-api` | Exploration de l'API ODRE avant l'écriture des scripts |
| `02-exploration` | Les rythmes de la consommation : journée, semaine, saisons |
| `03-thermosensibilite` | Fusion conso-météo, régression sur les jours froids |
| `04-prevision` | Baseline naïve, modèle linéaire, analyses d'erreur, itération |
| `05-duel-rte` | Découverte du biais de mesure et comparaison aux prévisions RTE |

Le fil conducteur : chaque modèle est jugé contre une baseline, chaque erreur est
décomposée (par jour, par mois) pour guider l'amélioration suivante. C'est l'analyse
d'erreur qui a révélé le poids des jours fériés (le mois de mai était le plus
imprévisible !) et inspiré les features de la v2.

## Reproduire

    git clone https://github.com/VOTRE-COMPTE/conso-electrique-france.git
    cd conso-electrique-france
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python src/collecte_eco2mix.py
    python src/collecte_meteo.py
    jupyter notebook

## Limites assumées et pistes

- Température "France" approximée par 8 villes non pondérées par la population
- Le modèle utilise la température **réalisée** (un vrai prévisionniste n'aurait que la prévue)
- Pas de gestion des ponts (le vendredi de l'Ascension...) ni de distinction samedi/dimanche
- Pistes : features "degrés de chauffe" max(0, 15-T), passage au pas horaire, modèles non linéaires

## Stack

Python, pandas, matplotlib, scipy, scikit-learn, requests, Jupyter. Données 100% open data.