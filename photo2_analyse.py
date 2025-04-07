import pandas as pd

pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")

pollution_raw["측정일시"] = pd.to_datetime(pollution_raw["측정일시"].astype(str), format="%Y%m%d%H")
pollution_raw["year"] = pollution_raw["측정일시"].dt.year
pollution_raw["month"] = pollution_raw["측정일시"].dt.month
pollution_raw["day"] = pollution_raw["측정일시"].dt.day
pollution_raw["hour"] = pollution_raw["측정일시"].dt.hour
pollution_raw["ym"] = pollution_raw["측정일시"].dt.to_period("M")

df_valid = pollution_raw[
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]
monthly_pollutants = (
    df_valid.groupby(["측정항목 명(줄임 명칭)", "month"])["평균값"]
    .mean()
    .reset_index()
)

heatmap_data = monthly_pollutants.pivot(
    index="측정항목 명(줄임 명칭)", columns="month", values="평균값"
)
heatmap_data = heatmap_data.loc[~(heatmap_data == 0).all(axis=1)]

import matplotlib.pyplot as plt
import seaborn as sns


high_pollutants = ["PM10", "PM2.5", "CO"]
low_pollutants = ["NO2", "O3", "SO2"]

fig, axes = plt.subplots(2, 1, figsize=(12, 8))


sns.heatmap(
    heatmap_data.loc[high_pollutants],
    annot=True, fmt=".2f", cmap="YlOrRd", ax=axes[0],
    cbar_kws={'label': 'Average concentration (high concentration level)'}
)
axes[0].set_title("Major Pollutants (Monthly mean concentration)")
axes[0].set_xlabel("month")
axes[0].set_ylabel("pollutant")

sns.heatmap(
    heatmap_data.loc[low_pollutants],
    annot=True, fmt=".3f", cmap="YlGnBu", ax=axes[1],
    cbar_kws={'label': 'Average concentration (low concentration level)'},
    vmin=0, vmax=0.05
)
axes[1].set_title("Trace gas Pollutants (Monthly mean concentration)")
axes[1].set_xlabel("month")
axes[1].set_ylabel("pollutant")

plt.tight_layout()
plt.show()

"""""
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".3f", cmap="YlOrRd", cbar_kws={'label': 'mean concentration'})
plt.title("Average concentration heat maps of different pollutants in different months(5 years)")
plt.xlabel("month")
plt.ylabel("pollutant")
plt.tight_layout()
plt.show()
"""

