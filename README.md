# AI News - Jugend Forscht project (scripts)
In this repo you can find the client code for my AI news research project for the german science competition Jugend Forscht.

## The project

This repo is a part of my project for the german science competition Jugend Forscht about the question "how well can ai be used to create news articles that are objective and have no halluzinations in it?". The project consists of a fined-tuned version of Mistral-7b to write news articles,a classification modell to categorize the articles, a system to collect halluzinations (based on GPT-3.5) and a website to collect user reviews.
#### Links:
- The scientific paper for my project: [Paper](https://cloud.stegle.eu/d/b8d916998f2448d3a003/)
- The website for user feedback collection: [News-server](https://github.com/L-S-2020/News-server)
- The project on the official site of Jugend Forscht: [Jugend Forscht BW](https://www.jugend-forscht-bw.de/projekt/journalismus-in-zeiten-kuenstlicher-intelligenz/) 
- News articles about the project: [GSG Waldkirch](https://www.gsg-waldkirch.de/aktuelles/jugend-forscht-leonard-stegle-gewinnt-1-preis-beim-regionalwettbewerb.html) [Badische Zeitung](https://www.badische-zeitung.de/waldkircher-gewinnt-regional-entscheid-mit-projekt-zu-kuenstlicher-intelligenz)

## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
3. Fill in the credentials in .env

## Programs:
trainingsdatenset_erstellen.py: Creates the training dataset for the fine-tuning of the AI model for article generation

klassifizierung_datenset_erstellen.py: Creates the data set for training the AI model for classifying articles

Artikel_erstellen_hochladen.py: Creates articles with both models and uploads them to the website

Artikel_datenset_erstellen.py: Creates the dataset for the evaluation of the AI models

Artikel_datenset_auswerten.py: Evaluates the dataset via the AI models and creates the diagrams

Bewertungen_downloaden.py: Downloads the ratings of the articles from the website and saves them as a dataset

bewertungen_auswerten.py: Evaluates the ratings and creates the diagrams

## Data sets:
artikel.parquet: Dataset for the evaluation of the AI models (from Artikel_datenset_erstellen.py)

bewertungen.parquet: Dataset for evaluating the ratings (from Bewertungen_downloaden.py)

classification-dataset.csv: Dataset for training the AI model for classifying articles (from classification_datenset_create.py)
