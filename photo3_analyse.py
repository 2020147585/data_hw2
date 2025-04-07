import pandas as pd

pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")
df_pm25 = pollution_raw[
    (pollution_raw["측정항목 명(줄임 명칭)"] == "PM2.5") &
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]


station_avg = (
    df_pm25.groupby("측정소 이름")["평균값"]
    .mean()
    .reset_index()
    .sort_values(by="평균값", ascending=False)
)

max_idx = station_avg["평균값"].idxmax()
min_idx = station_avg["평균값"].idxmin()

colors = []
for idx in station_avg.index:
    if idx == max_idx:
        colors.append('tomato')
    elif idx == min_idx:
        colors.append('mediumseagreen')
    else:
        colors.append('lightgray')


import matplotlib.pyplot as plt
import matplotlib

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


plt.figure(figsize=(12, 6))
bars = plt.bar(station_avg["측정소 이름"], station_avg["평균값"], color=colors)
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.1f}",
        ha='center', va='bottom', fontsize=9
    )
plt.xticks(rotation=45, ha='right')
plt.ylabel("Average PM2.5 concentration (µg/m³)")
plt.title("Comparison of average PM2.5 concentration at different stations from 2018 to 2022")
plt.tight_layout()
plt.show()
