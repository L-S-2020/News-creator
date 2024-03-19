import pandas as pd

df = pd.read_parquet("halluzinationen.parquet")

print(df.info())
print(df.head())
print(df.describe())

# Bestimme Prozentzahl der halluzinierten Informationen
df = df[(df['Modell'] == 'gpt') | (df['Modell'] == 'mistral')]
df['Halluziniert'] = df['Halluziniert'].str.extract('(\d+)').fillna(0).astype(int)
df['Ursprünglich'] = df['Ursprünglich'].str.extract('(\d+)').fillna(0).astype(int)
df['Gesamt'] = df['Gesamt'].str.extract('(\d+)').fillna(0).astype(int)
df['Prozent'] = df['Halluziniert'] / df['Gesamt'] * 100
print(df.describe())


df['Modell'] = df['Modell'].replace('mistral', 'eigenes Modell')
df['Modell'] = df['Modell'].replace('gpt', 'GPT-3.5')
df['Modell'] = df['Modell'].replace('mensch', 'menschlicher Autor')
df['Kategorie'] = df['Kategorie'].replace('WORLD', 'International')
df['Kategorie'] = df['Kategorie'].replace('NATION', 'National')
df['Kategorie'] = df['Kategorie'].replace('BUSINESS', 'Wirtschaft')
df['Kategorie'] = df['Kategorie'].replace('TECHNOLOGY', 'Technik')
df['Kategorie'] = df['Kategorie'].replace('ENTERTAINMENT', 'Unterhaltung')
df['Kategorie'] = df['Kategorie'].replace('SPORTS', 'Sport')
df['Kategorie'] = df['Kategorie'].replace('SCIENCE', 'Wissenschaft')
df['Kategorie'] = df['Kategorie'].replace('HEALTH', 'Gesundheit')

# Erstelle Diagramm für Halluzinationen in Abhängigkeit vom Modell
import seaborn as sns
import matplotlib.pyplot as plt
my_palette = ["#5975A4", "#cc8963", "#5f9e6e"]
sns.set(style="whitegrid")
g = sns.catplot(x="Modell", y="Prozent", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2, palette=my_palette)
g.set(ylim=(0, 100))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("halluzinationen.png", dpi=300)

# Erstelle Diagramm für Halluzinationen in Abhängigkeit von der Kategorie und dem Modell
g = sns.catplot(x="Kategorie", y="Prozent", hue="Modell", data=df, kind="bar", height=6, aspect=2, legend_out=False, capsize=0.2)
g.set(ylim=(0, 100))
plt.legend(loc='upper center', fancybox=True, shadow=False, ncol=5)
plt.show()
g.savefig("halluzinationen_kategorie.png", dpi=300)