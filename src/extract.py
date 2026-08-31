from datetime import datetime, timedelta
import os
import sys
import time
import pandas as pd
import requests

FINAL_MASTER_CSV = "master_lagos_hydrological_zone_with_flood_features.csv"
DEFAULT_START_DATE = "2012-05-01"
WEATHER_API_URL = "https://archive-api.open-meteo.com/v1/archive"
FLOOD_API_URL = "https://flood-api.open-meteo.com/v1/flood"

HYDROLOGICAL_ZONE_LGAS = [
    # Lagos State
    {"name": "Alimosho", "lat": 6.6015, "lon": 3.2938, "state": "Lagos"},
    {"name": "Ikeja", "lat": 6.6018, "lon": 3.3515, "state": "Lagos"},
    {"name": "Kosofe", "lat": 6.5574, "lon": 3.3854, "state": "Lagos"},
    {"name": "Mushin", "lat": 6.5299, "lon": 3.3504, "state": "Lagos"},
    {"name": "Oshodi-Isolo", "lat": 6.5362, "lon": 3.3254, "state": "Lagos"},
    {"name": "Somolu", "lat": 6.5284, "lon": 3.3764, "state": "Lagos"},
    {"name": "Surulere", "lat": 6.4994, "lon": 3.3578, "state": "Lagos"},
    {"name": "Agege", "lat": 6.6175, "lon": 3.3204, "state": "Lagos"},
    {"name": "Ifako-Ijaiye", "lat": 6.6661, "lon": 3.3082, "state": "Lagos"},
    {"name": "Lagos Mainland", "lat": 6.4869, "lon": 3.3742, "state": "Lagos"},
    {"name": "Ajeromi-Ifelodun", "lat": 6.4527, "lon": 3.3283, "state": "Lagos"},
    {"name": "Amuwo-Odofin", "lat": 6.4281, "lon": 3.2504, "state": "Lagos"},
    {"name": "Ojo", "lat": 6.4589, "lon": 3.1794, "state": "Lagos"},
    {"name": "Badagry", "lat": 6.4311, "lon": 2.8818, "state": "Lagos"},
    {"name": "Ikorodu", "lat": 6.6174, "lon": 3.5104, "state": "Lagos"},
    {"name": "Epe", "lat": 6.5833, "lon": 3.9833, "state": "Lagos"},
    {"name": "Eti-Osa", "lat": 6.4344, "lon": 3.4831, "state": "Lagos"},
    {"name": "Lagos Island", "lat": 6.4549, "lon": 3.3958, "state": "Lagos"},
    {"name": "Apapa", "lat": 6.4449, "lon": 3.3638, "state": "Lagos"},
    {"name": "Ibeju-Lekki", "lat": 6.4258, "lon": 3.6194, "state": "Lagos"},
    # Ogun State
    {"name": "Abeokuta South", "lat": 7.1457, "lon": 3.3484, "state": "Ogun"},
    {"name": "Abeokuta North", "lat": 7.1982, "lon": 3.3134, "state": "Ogun"},
    {"name": "Ifo", "lat": 6.8149, "lon": 3.1952, "state": "Ogun"},
    {"name": "Obafemi Owode", "lat": 6.9461, "lon": 3.5042, "state": "Ogun"},
    {"name": "Odeda", "lat": 7.2327, "lon": 3.5244, "state": "Ogun"},
    {"name": "Ado-Odo Ota", "lat": 6.6853, "lon": 3.0125, "state": "Ogun"},
    {"name": "Sagamu", "lat": 6.8319, "lon": 3.6498, "state": "Ogun"},
    {"name": "Ijebu Ode", "lat": 6.8194, "lon": 3.9174, "state": "Ogun"},
    # Oyo & Ondo
    {"name": "Ibadan Southwest", "lat": 7.3529, "lon": 3.8647, "state": "Oyo"},
    {"name": "Ondo West", "lat": 7.1000, "lon": 4.8333, "state": "Ondo"},
]

DAILY_METRICS = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "apparent_temperature_mean",
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "shortwave_radiation_sum",
    "et0_fao_evapotranspiration",
]

HOURLY_METRICS = [
    "soil_moisture_0_to_7cm",
    "soil_moisture_7_to_28cm",
    "soil_moisture_28_to_100cm",
    "soil_temperature_0_to_7cm",
    "soil_temperature_7_to_28cm",
    "soil_temperature_28_to_100cm",
]


def extract_hydrological_data(csv_path: str = FINAL_MASTER_CSV) -> bool:
  """Fetches weather and river discharge data from Open-Meteo.

  Returns True if new data was fetched and saved, False if already up to date.
  """
  target_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

  existing_df = None
  completed_lgas = set()
  start_date_to_fetch = DEFAULT_START_DATE
  pending_lgas = HYDROLOGICAL_ZONE_LGAS.copy()

  # Check existing CSV to avoid fetching redundant data
  if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path)

    if "LGA_Location" in existing_df.columns and "Date" in existing_df.columns:
      completed_lgas = set(existing_df["LGA_Location"].unique())
      existing_df["Date_Parsed"] = pd.to_datetime(existing_df["Date"])
      max_date_in_file = (
          existing_df["Date_Parsed"].max().strftime("%Y-%m-%d")
      )
      existing_df.drop(columns=["Date_Parsed"], inplace=True)

      print(
          f"Found dataset with {len(completed_lgas)}/{len(HYDROLOGICAL_ZONE_LGAS)} LGAs."
      )
      print(f"Latest Date in CSV: {max_date_in_file}")

      if len(completed_lgas) == len(HYDROLOGICAL_ZONE_LGAS):
        if max_date_in_file >= target_end_date:
          print(f"Dataset already up to date through {target_end_date}.")
          return False
        else:
          next_day = datetime.strptime(
              max_date_in_file, "%Y-%m-%d"
          ) + timedelta(days=1)
          start_date_to_fetch = next_day.strftime("%Y-%m-%d")
          print(
              f"Fetching updates from {start_date_to_fetch} to"
              f" {target_end_date}..."
          )
      else:
        pending_lgas = [
            lga
            for lga in HYDROLOGICAL_ZONE_LGAS
            if lga["name"] not in completed_lgas
        ]
        print(f"Remaining LGAs to fetch: {len(pending_lgas)}")

  print(
      f"\nStarting API extraction ({start_date_to_fetch} to"
      f" {target_end_date})...\n"
  )

  batch_size = 4
  master_frames = []

  for i in range(0, len(pending_lgas), batch_size):
    batch = pending_lgas[i : i + batch_size]
    lats = [str(lga["lat"]) for lga in batch]
    lons = [str(lga["lon"]) for lga in batch]
    names = ", ".join([lga["name"] for lga in batch])

    weather_params = {
        "latitude": ",".join(lats),
        "longitude": ",".join(lons),
        "start_date": start_date_to_fetch,
        "end_date": target_end_date,
        "daily": ",".join(DAILY_METRICS),
        "hourly": ",".join(HOURLY_METRICS),
        "timezone": "Africa/Lagos",
    }

    flood_params = {
        "latitude": ",".join(lats),
        "longitude": ",".join(lons),
        "start_date": start_date_to_fetch,
        "end_date": target_end_date,
        "daily": "river_discharge",
    }

    success = False
    while not success:
      try:
        res_weather = requests.get(WEATHER_API_URL, params=weather_params)
        data_weather = res_weather.json()

        if "error" in data_weather:
          reason = data_weather.get("reason", "")
          if "Minutely API request limit exceeded" in reason:
            print(f"Rate limit hit on [{names}]. Backing off for 65s...")
            time.sleep(65)
            continue
          elif "Hourly API request limit exceeded" in reason:
            raise RuntimeError("Hourly API limit hit. Wait or change IP.")

        res_flood = requests.get(FLOOD_API_URL, params=flood_params)
        data_flood = res_flood.json()

        weather_resp = (
            data_weather if isinstance(data_weather, list) else [data_weather]
        )
        flood_resp = (
            data_flood if isinstance(data_flood, list) else [data_flood]
        )

        for idx, w_loc in enumerate(weather_resp):
          lga = batch[idx]
          f_loc = flood_resp[idx]

          df_daily = pd.DataFrame(w_loc["daily"])
          df_daily["Date"] = pd.to_datetime(
              df_daily["time"], format="ISO8601"
          ).dt.strftime("%Y-%m-%d")
          df_daily.drop(columns=["time"], inplace=True)

          # Aggregate hourly soil data into daily averages
          df_hourly = pd.DataFrame(w_loc["hourly"])
          df_hourly["Timestamp"] = pd.to_datetime(df_hourly["time"])
          df_hourly_avg = (
              df_hourly.groupby(df_hourly["Timestamp"].dt.date)[HOURLY_METRICS]
              .mean()
              .reset_index()
          )
          df_hourly_avg.rename(columns={"Timestamp": "Date"}, inplace=True)
          df_hourly_avg["Date"] = pd.to_datetime(
              df_hourly_avg["Date"]
          ).dt.strftime("%Y-%m-%d")

          df_flood = pd.DataFrame(f_loc["daily"])
          df_flood["Date"] = pd.to_datetime(
              df_flood["time"], format="ISO8601"
          ).dt.strftime("%Y-%m-%d")
          df_flood.drop(columns=["time"], inplace=True)

          # Combine daily, hourly soil averages, and discharge data
          lga_df = pd.merge(df_daily, df_hourly_avg, on="Date", how="inner")
          lga_df = pd.merge(lga_df, df_flood, on="Date", how="inner")

          lga_df.insert(1, "State", lga["state"])
          lga_df.insert(2, "LGA_Location", lga["name"])

          master_frames.append(lga_df)
          print(f"Done: {lga['name']} ({lga['state']})")

        success = True

      except Exception as e:
        print(f"Error processing batch [{names}]: {e}")
        break

    time.sleep(12)

  # Merge with existing file if available and save locally
  if master_frames:
    new_df = pd.concat(master_frames, ignore_index=True)

    if existing_df is not None:
      final_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
      final_df = new_df

    final_df.drop_duplicates(subset=["Date", "LGA_Location"], inplace=True)
    final_df.sort_values(by=["LGA_Location", "Date"], inplace=True)

    final_df.to_csv(csv_path, index=False)
    print(f"\nExtraction finished. Saved to '{csv_path}'.")
    print(
        f"Total rows: {final_df.shape[0]} across"
        f" {len(final_df['LGA_Location'].unique())} LGAs"
    )
    return True

  return False
