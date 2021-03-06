import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import math

sns.set(style="darkgrid")

df = pd.read_csv(open('../results/times.csv'))

palette = {'pca-antes':"#5C3908", 'pca-despues':"#0B0D36", 'svd-antes':"#6F625F", 'svd-despues':"#5A1615"}
ax = sns.barplot(x='classifier', y='prediction_time', hue='decomposition', data=df, palette=palette)
ax.set(yscale="log")
ax.set_xlabel('Classifier')
ax.set_ylabel('Prediction time (seconds)')

plot_margin = 0.5

for p in ax.patches:
	x = p.get_x()
	height = p.get_height()
	ax.text(x + 0.05, 3.5*height, '%1.2f'%(height), rotation='vertical')

x0, x1, y0, y1 = plt.axis()
plt.axis((x0 - plot_margin,
          x1 + plot_margin,
          y0,
          y1 + 2*plot_margin))

plt.legend(loc=1)
plt.show()