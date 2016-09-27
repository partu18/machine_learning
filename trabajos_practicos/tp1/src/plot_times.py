import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid")

df = pd.read_csv(open('../results/times.csv'))

palette = {'pca-antes':"#5C3908", 'pca-despues':"#0B0D36", 'svd-antes':"#6F625F", 'svd-despues':"#5A1615"}
ax = sns.barplot(x='classifier', y='prediction_time', hue='decomposition', data=df, palette=palette)

ax.set_ylabel('clocks')

plot_margin = 0.25

for p in ax.patches:
	x = p.get_x()
	p.set_width(10)
	height = p.get_height()
	ax.text(x, height+0.1, '%1.2f'%(height/10))

x0, x1, y0, y1 = plt.axis()
plt.axis((x0 - plot_margin,
          x1 + plot_margin,
          y0,
          y1 + 2*plot_margin))

plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=3.)
plt.show()