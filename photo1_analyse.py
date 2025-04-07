import pandas as pd
pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")

pollution_raw["측정일시"] = pd.to_datetime(pollution_raw["측정일시"].astype(str), format="%Y%m%d%H")
pollution_raw["year"] = pollution_raw["측정일시"].dt.year
pollution_raw["month"] = pollution_raw["측정일시"].dt.month
pollution_raw["day"] = pollution_raw["측정일시"].dt.day
pollution_raw["hour"] = pollution_raw["측정일시"].dt.hour
pollution_raw["ym"] = pollution_raw["측정일시"].dt.to_period("M")



df_pm25 = pollution_raw[
    (pollution_raw["측정항목 명(줄임 명칭)"] == "PM2.5") &
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]


monthly_avg = df_pm25.groupby(["year", "month"])["평균값"].mean().reset_index()




import matplotlib.pyplot as plt


years = sorted(monthly_avg["year"].unique())

fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(10, 14), sharex=True)

for i, y in enumerate(years):
    ax = axes[i]
    df_year = monthly_avg[monthly_avg["year"] == y]


    ax.plot(df_year["month"], df_year["평균값"], marker='o', label=f"{y}year")


    for x, yval in zip(df_year["month"], df_year["평균값"]):
        ax.text(x, yval + 0.5, f"{yval:.1f}", ha='center', va='bottom', fontsize=12)

    ax.set_title(f"{y} Seoul Monthly average PM2.5", fontsize=11)
    ax.set_ylabel("average(µg/m³)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_ylim(0, monthly_avg["평균값"].max() + 5)


axes[-1].set_xticks(range(1, 13))
axes[-1].set_xticklabels([f"{m}" for m in range(1, 13)])
axes[-1].set_xlabel("month")

plt.tight_layout()
plt.show()



df_pm25 = pollution_raw[
    (pollution_raw["측정항목 명(줄임 명칭)"] == "PM2.5") &
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]

filtered = df_pm25[df_pm25["month"].isin([1, 8])]


monthly_avg = (
    filtered.groupby(["year", "month"])["평균값"]
    .mean()
    .reset_index()
)
pivot = monthly_avg.pivot(index="month", columns="year", values="평균값")
pivot = pivot.loc[[1, 8]]
print(pivot)

import matplotlib.pyplot as plt
import numpy as np


labels = ["january", "august"]
years = pivot.columns.tolist()
x = np.arange(len(labels))
width = 0.15


plt.figure(figsize=(10, 6))
for i, year in enumerate(years):
    plt.bar(x + i*width, pivot[year], width=width, label=str(year))


plt.xticks(x + width*2, labels)
plt.ylabel("PM2.5 average (µg/m³)")
plt.title("January and August PM2.5 average(2018–2022)")
plt.legend(title="year")
plt.tight_layout()
plt.show()
