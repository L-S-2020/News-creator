import pandas as pd

# lese die Daten ein
df = pd.read_parquet("bewertungen.parquet")

# berechne Statistiken
print(df.info())
print(df.head())
print(df.describe())

# Erstelle Statistiken in Abhängigkeit von der Kategorie
print(df.groupby('kategorie').describe())

# Erstelle Statistiken in Abhängigkeit von der Kategorie und dem Modell (nur von der Spalte Sterne)
print(df.groupby(['kategorie', 'art'])['Sterne'].describe())

# Erstelle Statistiken in Abhängigkeit von dem Modell
print(df.groupby('art')['Sterne'].describe())

# Ersetze 'mistral' durch 'eigenes Modell'
df['art'] = df['art'].replace('mistral', 'eigenes Modell')
df['art'] = df['art'].replace('gpt', 'GPT-3.5')
df['art'] = df['art'].replace('mensch', 'menschlicher Autor')

# Ändere 'kategorie' in Kategorie
df.rename(columns={'kategorie': 'Kategorie'}, inplace=True)
df.rename(columns={'art': 'Ersteller'}, inplace=True)

# Erstelle Diagramm der Verteilung der Sterne in Abhängigkeit von der Kategorie und dem Modell, sowie der Anzahl der Bewertungen, das Diagramm sollte von 0,5 bis 5 gehen
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")
g = sns.catplot(x="Kategorie", y="Sterne", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen.png", dpi=300)

# Options are 'strip', 'swarm', 'box', 'boxen', 'violin', 'bar', 'count', and 'point'.
# Erstelle Diagramm der Streuung der Sterne in Abhängigkeit von der Kategorie und dem Modell
g = sns.catplot(x="Kategorie", y="Sterne", hue="Ersteller", data=df, kind="violin", height=6, aspect=2, legend_out=False)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_streuung.png", dpi=300)

# Erstelle Diagramm der Verteilung der Sterne in Abhängigkeit von dem Modell, sowie der Anzahl der Bewertungen, das Diagramm sollte von 0,5 bis 5 gehen
g = sns.catplot(x="Ersteller", y="Sterne", data=df, kind="bar", height=6, aspect=2, legend_out=False)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_modell.png", dpi=300)

# Erstelle Diagramm der Streuung der Sterne in Abhängigkeit von dem Modell
g = sns.catplot(x="Ersteller", y="Sterne", data=df, kind="violin", height=6, aspect=2, legend_out=False)
g.set(ylim=(0.5, 5))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("bewertungen_modell_streuung.png", dpi=300)

# Erstelle ein Kreisdiagramm mit Schätzungen (in Prozent) (Richtig, Falsch), Beschriftung: Richtig, Falsch, Richtig: Blau, Falsch: Rot
df['richtig'] = df['richtig'].astype(int)
df['falsch'] = 1 - df['richtig']
df2 = df.groupby('richtig').count()
df2 = df2['Sterne']
df2.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['blue', 'red'])
plt.ylabel('')
plt.savefig("bewertungen_schaetzung.png", dpi=300)
plt.show()

# Erstelle diagramm mit Schätzungen, die richtig und falsch waren (in Prozent) (x: Modell, y: Prozent) (mit gestapelten Balken (richtig, falsch))
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
plt.savefig("bewertungen_schaetzung.png", dpi=300)
plt.show()


# Erstelle ein Kreisdiagramm aus folegenden Daten: Richtig: 664, Falsch: 531, ohne den Datenframe
data = {'Richtig': 664, 'Falsch': 531}
df2 = pd.Series(data)
df2.plot(kind='pie', autopct='%1.1f%%', startangle=90, )
plt.ylabel('')
plt.savefig("bewertungen_schaetzung.png", dpi=300)
plt.show()



