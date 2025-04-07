import pandas as pd
import os
from glob import glob


file_paths = glob("AIR_HOUR_*.csv")


pollution_dfs = [pd.read_csv(fp, encoding='utf-8') for fp in file_paths]
pollution_raw = pd.concat(pollution_dfs, ignore_index=True)




station_info = pd.read_csv("station_info.csv", encoding='cp949')

pollution_raw = pollution_raw.merge(station_info, on="측정소 코드", how="left")


item_info = pd.read_csv("item_info.csv", encoding='cp949')

print(item_info.columns)
pollution_raw = pollution_raw.merge(
    item_info,
    left_on="측정항목",
    right_on="측정항목 코드",
    how="left"
)

pollution_raw.to_csv("pollution_merged.csv", index=False, encoding="utf-8-sig")
