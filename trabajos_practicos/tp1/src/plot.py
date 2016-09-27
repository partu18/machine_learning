import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid")

df = pd.read_csv(open('../results/scores.csv'))

palette = {'pca-antes':"#5C3908", 'pca-despues':"#0B0D36", 'svd-antes':"#6F625F", 'svd-despues':"#5A1615"}
ax = sns.barplot(x='classifier', y='f1', hue='decomposition', data=df, palette=palette)

ax.set_ylabel('f1 score')

plot_margin = 0.25

x0, x1, y0, y1 = plt.axis()
plt.axis((x0 - plot_margin,
          x1 + plot_margin,
          y0,
          y1 + 2*plot_margin))

for p in ax.patches:
	height = p.get_height()
	ax.text(p.get_x(), height+3, '%1.2f'%(height/10))

plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=3.)
plt.show()