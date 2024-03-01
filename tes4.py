import pandas as pd
import numpy as np

# lese die Daten ein
df = pd.read_parquet("output.parquet")
print(df.info())
print(df.head())
print(df.describe())

print(df.groupby('Modell').describe())

df['Modell'] = df['Modell'].replace('mistral', 'eigenes Modell')
df['Modell'] = df['Modell'].replace('gpt', 'GPT-3.5')
df['Modell'] = df['Modell'].replace('mensch', 'menschlicher Autor')
df.rename(columns={'Modell': 'Ersteller'}, inplace=True)

df['Kategorie'] = df['Kategorie'].replace('WORLD', 'International')
df['Kategorie'] = df['Kategorie'].replace('NATION', 'National')
df['Kategorie'] = df['Kategorie'].replace('BUSINESS', 'Wirtschaft')
df['Kategorie'] = df['Kategorie'].replace('TECHNOLOGY', 'Technik')
df['Kategorie'] = df['Kategorie'].replace('ENTERTAINMENT', 'Unterhaltung')
df['Kategorie'] = df['Kategorie'].replace('SPORTS', 'Sport')
df['Kategorie'] = df['Kategorie'].replace('SCIENCE', 'Wissenschaft')
df['Kategorie'] = df['Kategorie'].replace('HEALTH', 'Gesundheit')

# Sortiere die Ersteller, erst GPT-3.5, dann eigenes Modell, dann menschlicher Autor
df['Ersteller'] = pd.Categorical(df['Ersteller'], ['GPT-3.5', 'eigenes Modell', 'menschlicher Autor'])
df = df.sort_values('Ersteller')

# Erstelle Diagramm zur Verteilung der Textlänge in Abhängigkeit von dem Modell und der Kategorie, mit dem Durchschnitt der Textlänge
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")
g = sns.catplot(x="Kategorie", y="Textlänge", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("textlaenge.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Textlänge", hue="Ersteller", data=df, kind="box", height=6, aspect=2, legend_out=False)
g.set(ylim=(0, 2000))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("textlaenge-violin.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Wienersachtextformel", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
g.set(ylim=(4, 14))
plt.show()
g.savefig("wiener.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Flesch-Reading-Ease", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("flesch.png", dpi=300)
# Füge den Durchschnitt der Textlänge, der Wienersachtextformel und des Flesch-Reading-Ease hinzu
print(df.groupby(['Kategorie', 'Ersteller'])['Textlänge'].mean())
print(df.groupby(['Kategorie', 'Ersteller'])['Wienersachtextformel'].mean())
print(df.groupby(['Kategorie', 'Ersteller'])['Flesch-Reading-Ease'].mean())

# Anzahl der Texte in Abhängigkeit von der Kategorie und dem Modell
print(df.groupby(['Kategorie', 'Ersteller']).size())
