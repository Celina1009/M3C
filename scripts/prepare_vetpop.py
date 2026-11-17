import pandas as pd
from pathlib import Path

input_file = Path("data/raw/VetPop2023 county data.csv")
output_file = Path("data/processed/Prepared_VetPop_FY2023.csv")

print("Loading VetPop data...")
df = pd.read_csv(input_file, dtype={"FIPS": str})

# Keep September 30, 2023 projection
df = df[df["Date"] == "2023 Sep 30 12:00:00 AM"].copy()

# Normalize FIPS and exclude non-county aggregates
df["FIPS"] = df["FIPS"].str.strip().str.zfill(5)
excluded_fips = {"72000", "90060", "90066", "90069", "90078", "99000"}
df = df[~df["FIPS"].isin(excluded_fips)].copy()

# Remove thousands separators before numeric conversion
df["Veterans"] = pd.to_numeric(
    df["Veterans"].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

if df["Veterans"].isna().any():
    raise ValueError("Missing or invalid Veterans values found.")

# Aggregate all 8 age/sex categories per county
prepared = (
    df.groupby(["FIPS", "County, State", "State"], as_index=False)
      ["Veterans"].sum()
)

prepared = prepared.rename(columns={
    "FIPS": "county_fips",
    "County, State": "county_state",
    "State": "state_name",
    "Veterans": "veteran_population_fy2023"
})

prepared["veteran_population_fy2023"] = (
    prepared["veteran_population_fy2023"].astype("Int64")
)

output_file.parent.mkdir(parents=True, exist_ok=True)
prepared.to_csv(output_file, index=False)

print("\nVetPop preparation complete.")
print("Output:", output_file)
print("County records:", len(prepared))
print("Unique FIPS:", prepared["county_fips"].nunique())
print("Duplicate FIPS:", prepared["county_fips"].duplicated().sum())
print("Missing population:", prepared["veteran_population_fy2023"].isna().sum())
print("Total veteran population:", prepared["veteran_population_fy2023"].sum())

autauga = prepared[prepared["county_fips"] == "01001"]
print("\nAutauga population:", autauga["veteran_population_fy2023"].iloc[0])
