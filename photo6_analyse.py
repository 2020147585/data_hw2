import pandas as pd


pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")


df_pm25 = pollution_raw[
    (pollution_raw["측정항목 명(줄임 명칭)"] == "PM2.5") &
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
].copy()


df_pm25["측정일시"] = pd.to_datetime(df_pm25["측정일시"].astype(str), format="%Y%m%d%H")


df_pm25["hour"] = df_pm25["측정일시"].dt.hour


hourly_avg = df_pm25.groupby("hour")["평균값"].mean().reset_index()


from adjustText import adjust_text
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(hourly_avg["hour"], hourly_avg["평균값"], marker='o')


texts = []
for i, row in hourly_avg.iterrows():
    texts.append(
        plt.text(row["hour"], row["평균값"], f"{row['평균값']:.1f}", fontsize=9)
    )


adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))


plt.xticks(range(0, 24))
plt.xlabel("hour")
plt.ylabel("Average PM2.5 concentration (µg/m³)")
plt.title("Daily trend of PM2.5 concentration")
plt.grid(True)
plt.tight_layout()
plt.show()

