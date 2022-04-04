import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/hellwig.csv')

#Ranking
fig, ax = plt.subplots(figsize=(14,6))
sns.barplot(x='Player', y='Rank', data=data,palette='rocket_r')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title("Top 5 players - Hellwig rank", fontsize=20)
plt.show()

#npXG and Goals
visData = data[['Player','G-PK','npxG']]
tidy = visData.melt(id_vars='Player')

fig, ax = plt.subplots(figsize=(14,6))
sns.set_style('whitegrid')
sns.barplot(x='Player', y='value', hue='variable', data=tidy, palette='rocket_r')
plt.legend(title='', loc='upper left', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title("Non-penalty goals and non-penalty expected goals", fontsize=20)
plt.show()

#Assists and expected assists
visData = data[['Player','Ast','xA']]
tidy = visData.melt(id_vars='Player')

fig, ax = plt.subplots(figsize=(14,6))
sns.set_style('whitegrid')
sns.barplot(x='Player', y='value', hue='variable', data=tidy, palette='rocket_r')
plt.legend(title='', loc='upper right', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title("Assists and expected assists", fontsize=20)
plt.show()