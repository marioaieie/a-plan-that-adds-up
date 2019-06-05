import pandas as pd

sources_names = ["Clean coal", "Nuclear", "Tide", "Wave", "Hydro", "Waste", "Pumped heat", "Wood", "Solar HW",
                 "Biofuels", "Photovoltaic", "Wind", "Solar in deserts", ]
sources = pd.DataFrame(index=sources_names)

print(sources.head())
