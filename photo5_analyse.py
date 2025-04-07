import pandas as pd

pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")
df_filtered = pollution_raw[
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]
df_pm25 = df_filtered[df_filtered["측정항목 명(줄임 명칭)"] == "PM2.5"]
df_no2 = df_filtered[df_filtered["측정항목 명(줄임 명칭)"] == "NO2"]


df_pm25 = df_pm25[["측정일시", "측정소 코드", "평균값"]].rename(columns={"평균값": "PM2.5"})
df_no2  = df_no2[["측정일시", "측정소 코드", "평균값"]].rename(columns={"평균값": "NO2"})
df_merged = pd.merge(df_pm25, df_no2, on=["측정일시", "측정소 코드"])

corr = df_merged[["NO2", "PM2.5"]].corr().iloc[0, 1]
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.regplot(
    data=df_merged,
    x="NO2", y="PM2.5",
    scatter_kws={"alpha": 0.3},
    line_kws={"color": "red"},
)

plt.text(
    0.01, 60,
    f"correlation coefficient r = {corr:.2f}",
    fontsize=12, color="blue"
)
plt.xlabel("NO₂ concentration (ppm)")
plt.ylabel("PM2.5 concentration (µg/m³)")
plt.title("PM2.5 vs NO₂ scatter plot")
plt.grid(True)
plt.tight_layout()
plt.show()


