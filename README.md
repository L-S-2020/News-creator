# News-creator

Diese Repository ist ein Teil meines Jugend Forscht 2024 Projektes "Journalismus in Zeiten künstlicher Intelligenz"

## Programme:
trainingsdatenset_erstellen.py: Erstellt das Trainingsdatenset für das Finetuning des KI-Modells zur Artikelgenerierung

klassifizierung_datenset_erstellen.py: Erstellt das Datenset für das Training des KI-Modells zur Klassifizierung von Artikeln

Artikel_erstellen_hochladen.py: Erstellt Artikel mit beiden Modellen und lädt sie auf die Website hoch

Artikel_datenset_erstellen.py: Erstellt das Datenset für die Auswertung der KI-Modelle

Artikel_datenset_auswerten.py: Wertet das Datenset über die KI-Modelle aus und erstellt die Diagramme

Bewertungen_downloaden.py: Lädt die Bewertungen der Artikel von der Website herunter und speichert sie als Datenset

bewertungen_auswerten.py: Wertet die Bewertungen aus und erstellt die Diagramme

## Datensets:
artikel.parquet: Datenset für die Auswertung der KI-Modelle (von Artikel_datenset_erstellen.py)

bewertungen.parquet: Datenset für die Auswertung der Bewertungen (von Bewertungen_downloaden.py)

classification-dataset.csv: Datenset für das Training des KI-Modells zur Klassifizierung von Artikeln (von klassifizierung_datenset_erstellen.py)
