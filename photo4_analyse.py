import pandas as pd

pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")
df_pm10 = pollution_raw[
    (pollution_raw["측정항목 명(줄임 명칭)"] == "PM10") &
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
]

box_df = df_pm10[["측정소 이름", "평균값"]]

iqr_df = (
    df_pm10.groupby("측정소 이름")["평균값"]
    .quantile([0.75, 0.25])
    .unstack()
    .reset_index()
    .rename(columns={0.75: "Q3", 0.25: "Q1"})
)
iqr_df["IQR"] = iqr_df["Q3"] - iqr_df["Q1"]
top3_iqr = iqr_df.sort_values("IQR", ascending=False).head(3)["측정소 이름"].tolist()

df_pm10 = df_pm10.copy()
df_pm10["is_top3_iqr"] = df_pm10["측정소 이름"].apply(
    lambda x: "Top 3" if x in top3_iqr else "Other"
)

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(14, 6))
sns.boxplot(
    data=df_pm10,
    x="측정소 이름", y="평균값",
    hue="is_top3_iqr",
    palette={"Top 3": "tomato", "Other": "lightgray"},
    dodge=False
)

plt.xticks(rotation=45, ha='right')
plt.ylabel("PM10 concentration (µg/m³)")
plt.yscale("log")
plt.title("Box plot of PM10 concentration fluctuations in different regions from 2018 to 2022")
plt.tight_layout()
plt.show()
