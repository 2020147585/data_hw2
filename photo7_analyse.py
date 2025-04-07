import pandas as pd


pollution_raw = pd.read_csv("pollution_merged.csv", encoding="utf-8-sig")
df_valid = pollution_raw[
    (pollution_raw["측정기 상태"] == 0) &
    (pollution_raw["평균값"] >= 0)
].copy()


df_valid["측정일시"] = pd.to_datetime(df_valid["측정일시"].astype(str), format="%Y%m%d%H")


df_valid["hour"] = df_valid["측정일시"].dt.hour
hourly_pollutants = df_valid.groupby(["hour", "측정항목 명(줄임 명칭)"])["평균값"].mean().reset_index()
pivot_table = hourly_pollutants.pivot(index="hour", columns="측정항목 명(줄임 명칭)", values="평균값").fillna(0)

import matplotlib.pyplot as plt


fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)


colors_top = {"PM2.5": "#FDB462", "PM10": "#80B1D3"}
colors_bottom = {"CO": "#FB8072", "NO2": "#B3DE69", "O3": "#BC80BD", "SO2": "#CCEBC5"}


pivot_table[["PM2.5", "PM10"]].plot.area(
    stacked=True,
    ax=axs[0],
    color=[colors_top["PM2.5"], colors_top["PM10"]]
)
axs[0].set_title("Hourly Variation of PM2.5 and PM10")
axs[0].set_ylabel("Concentration (µg/m³)")
axs[0].grid(True)
axs[0].legend(title="Pollutant")


pivot_table[["CO", "NO2", "O3", "SO2"]].plot.area(
    stacked=True,
    ax=axs[1],
    color=[colors_bottom["CO"], colors_bottom["NO2"],
           colors_bottom["O3"], colors_bottom["SO2"]]
)
axs[1].set_title("Hourly Variation of Gaseous Pollutants")
axs[1].set_xlabel("Hour of Day")
axs[1].set_xticks(range(0, 24)) 
axs[1].set_ylabel("Concentration (ppm or ppb)")
axs[1].grid(True)
axs[1].legend(title="Pollutant")

plt.tight_layout()
plt.show()


