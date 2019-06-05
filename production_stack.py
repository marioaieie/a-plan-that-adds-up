import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# sources_names = ["Clean coal", "Nuclear", "Tide", "Wave", "Hydro", "Waste", "Pumped heat", "Wood", "Solar HW",
#                  "Biofuels", "Photovoltaic", "Wind", "Solar in deserts", ]
sources = pd.read_csv('sources.csv')
sources.sort_values('source', inplace=True)

sources['area'] = 44
sources['power'] = sources['power_density'] * sources['area'] / 1000. * 24

# sources['power'] = 20
# sources['area'] = sources['power'] / sources['power_density'] * 1000 / 24.

sources['cumulative_power'] = sources['power'].cumsum()

print(sources)
print(sources['power'].sum())

# plt.stackplot([0, 1], np.array([sources['power'], sources['power']]).T, alpha=0.4, labels=sources['source'])
# plt.legend()

# plt.bar(0, height=sources['power'],
#         bottom=sources['cumulative_power'] - sources['power'], color='C' + sources.index.astype(str))

for idx, item in sources.iterrows():
    plt.bar(0, height=item['power'],
            bottom=item['cumulative_power']-item['power'], alpha=0.4)
    plt.text(0, item['cumulative_power'] - item['power']/2.,
             '{name}: {pow:0.1f} kWh/d'.format(name=item['source'], pow=item['power']),
             horizontalalignment='center', verticalalignment='center')

plt.show()

