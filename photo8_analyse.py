import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")


df_pm25 = df[(df["측정항목 명(줄임 명칭)"] == "PM2.5") & (df["측정기 상태"] == 0) & (df["평균값"] >= 0)].copy()


df_pm25["측정일시"] = pd.to_datetime(df_pm25["측정일시"].astype(str), format="%Y%m%d%H")
df_pm25["year"] = df_pm25["측정일시"].dt.year


avg_by_year = df_pm25[df_pm25["year"].isin([2018, 2022])].groupby(["측정소 이름", "year"])["평균값"].mean().unstack()


avg_by_year["difference value"] = avg_by_year[2022] - avg_by_year[2018]
avg_by_year["Improvement ratio"] = (avg_by_year["difference value"] / avg_by_year[2018]) * 100


avg_by_year = avg_by_year.sort_values("Improvement ratio")


plt.figure(figsize=(18, 6))
bars = plt.bar(avg_by_year.index, avg_by_year["difference value"], color="green")


for bar, diff, pct in zip(bars, avg_by_year["difference value"], avg_by_year["Improvement ratio"]):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.1,
             f"{diff:.1f}\n({pct:.1f}%)", ha='center', va='top' if diff < 0 else 'bottom', fontsize=9)

plt.title("Change in PM2.5 Concentration by District (2022 - 2018)\n(Improvement sorted by % drop)", fontsize=14)
plt.xticks(rotation=60)
plt.ylabel("PM2.5 Difference (µg/m³)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
