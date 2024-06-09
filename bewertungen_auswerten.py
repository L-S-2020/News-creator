# Zweck: Auswertung der Bewertungen
# Importiere die benötigten Bibliotheken
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# lese die Daten ein
df = pd.read_parquet("bewertungen.parquet")

# berechne generelle Statistiken
print(df.info())
print(df.head())
print(df.describe())

print(df.groupby('richtig').count())
# Erstelle Statistiken in Abhängigkeit von der Kategorie
print(df.groupby('kategorie').describe())

# Erstelle Statistiken in Abhängigkeit von der Kategorie und dem Modell (nur von der Spalte Sterne)
print(df.groupby(['kategorie', 'art'])['Sterne'].describe())

# Erstelle Statistiken in Abhängigkeit von dem Modell
print(df.groupby('art')['Sterne'].describe())

# Berechne die Anzahl der Bewertungen in Abhängigkeit von der Kategorie und dem Modell
print(df.groupby(['Kategorie', 'Ersteller']).size())

# Ersetze interne Namen der Modelle/Ersteller durch Namen für Diagramme
df['art'] = df['art'].replace('mistral', 'eigenes Modell')
df['art'] = df['art'].replace('gpt', 'GPT-3.5')
df['art'] = df['art'].replace('mensch', 'menschlicher Autor')

# Ändere 'kategorie' in Kategorie, 'art' in Ersteller
df.rename(columns={'kategorie': 'Kategorie'}, inplace=True)
df.rename(columns={'art': 'Ersteller'}, inplace=True)

# Balkendiagramm der Verteilung der Sterne in Abhängigkeit von der Kategorie und dem Modell, das Diagramm geht von 0,5 bis 5
sns.set(style="whitegrid")
g = sns.catplot(x="Kategorie", y="Sterne", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen.png", dpi=300)

# Boxdiagramm der Streuung der Sterne in Abhängigkeit von der Kategorie und dem Modell (aus Platzgründen nicht in der schriftlichen Ausarbeitung)
g = sns.catplot(x="Kategorie", y="Sterne", hue="Ersteller", data=df, kind="box", height=6, aspect=2, legend_out=False, medianprops=dict(color="red", alpha=0.7),)
g.set(ylim=(0, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_streuung.png", dpi=300)


my_palette = ["#5975A4", "#cc8963", "#5f9e6e"]
# Erstelle Diagramm der Verteilung der Sterne in Abhängigkeit von dem Modell, das Diagramm geht 0,5 bis 5
g = sns.catplot(x="Ersteller", y="Sterne", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2, palette=my_palette)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_modell.png", dpi=300)

# Violindiagramm der Streuung der Sterne in Abhängigkeit von dem Modell (aus Platzgründen nicht in der schriftlichen Ausarbeitung)
g = sns.catplot(x="Ersteller", y="Sterne", data=df, kind="violin", height=6, aspect=2, legend_out=False)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_modell_streuung.png", dpi=300)

# Kreisdiagramm mit Einschätzungen (in Prozent) (Richtig, Falsch)
df['richtig'] = df['richtig'].astype(int)
df['falsch'] = 1 - df['richtig']
df2 = df.groupby('richtig').count()
df2 = df2['Sterne']
df2.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['blue', 'red'])
plt.ylabel('')
plt.savefig("einschaetzung_kreis.png", dpi=300)
plt.show()

# Balkendiagramm mit Schätzungen, die richtig und falsch waren, in Abhängigkeit von dem Modell
df['richtig'] = df['richtig'].astype(int)
df['falsch'] = 1 - df['richtig']
df['gesamt'] = 1
df2 = df.groupby('Ersteller').sum()
df2['richtig'] = df2['richtig'] / df2['gesamt']
df2['falsch'] = df2['falsch'] / df2['gesamt']
df2 = df2[['richtig', 'falsch']]

df2.plot(kind='bar', stacked=True, figsize=(10,7))

plt.xlabel('Ersteller')
plt.ylabel('Prozent')
plt.xticks(rotation=0)  # Bezeichnungen der x-Achse waagerecht anzeigen
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.savefig("einschaetzung_bar.png", dpi=300)
plt.show()
