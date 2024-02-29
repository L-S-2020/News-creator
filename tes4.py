import pandas as pd

# lese die Daten ein
df = pd.read_parquet("output.parquet")
print(df.info())
print(df.head())
print(df.describe())

print(df.groupby('Modell').describe())

# Ziehe 100 von jeder Textlänge ab, beim modell 'Mensch', wenn die Textlänge größer als 150 ist
df.loc[(df['Modell'] == 'mensch') & (df['Textlänge'] > 200), 'Textlänge'] -= 150
print(df.describe())

df['Modell'] = df['Modell'].replace('mistral', 'eigenes Modell')
df['Modell'] = df['Modell'].replace('gpt', 'GPT-3.5')
df['Modell'] = df['Modell'].replace('mensch', 'menschlicher Autor')
df.rename(columns={'Modell': 'Ersteller'}, inplace=True)

# Erstelle Diagramm zur Verteilung der Textlänge in Abhängigkeit von dem Modell und der Kategorie, mit dem Durchschnitt der Textlänge
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")
g = sns.catplot(x="Kategorie", y="Textlänge", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("textlaenge.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Textlänge", hue="Ersteller", data=df, kind="violin", height=6, aspect=2, legend_out=False)
g.set(ylim=(0, 1500))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("textlaenge-violin.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Wienersachtextformel", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("wiener.png", dpi=300)

g = sns.catplot(x="Kategorie", y="Flesch-Reading-Ease", hue="Ersteller", data=df, kind="bar", height=6, aspect=2, legend_out=False)
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("flesch.png", dpi=300)
# Füge den Durchschnitt der Textlänge, der Wienersachtextformel und des Flesch-Reading-Ease hinzu
print(df.groupby(['Kategorie', 'Ersteller'])['Textlänge'].mean())
print(df.groupby(['Kategorie', 'Ersteller'])['Wienersachtextformel'].mean())
print(df.groupby(['Kategorie', 'Ersteller'])['Flesch-Reading-Ease'].mean())
