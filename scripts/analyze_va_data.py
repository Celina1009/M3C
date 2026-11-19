import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Project root (M3C folder)
project_root = Path(__file__).resolve().parent.parent

data_dir = project_root / "data" / "processed" / "integrated"
output_dir = project_root / "results" / "analysis"

output_dir.mkdir(parents=True, exist_ok=True)

# Load integrated datasets
df23 = pd.read_csv(data_dir / "Integrated_FY2023.csv")
df24 = pd.read_csv(data_dir / "Integrated_FY2024.csv")
df25 = pd.read_csv(data_dir / "Integrated_FY2025.csv")

print("FY2023:", df23.shape)
print("FY2024:", df24.shape)
print("FY2025:", df25.shape)

# Combine all three fiscal years
df = pd.concat([df23, df24, df25], ignore_index=True)

# Preserve FIPS codes as five-character strings
df["county_fips"] = df["county_fips"].astype(str).str.zfill(5)

# Sort by county and fiscal year
df = df.sort_values(
    ["county_fips", "fiscal_year"]
).reset_index(drop=True)

print("Combined dataset shape:", df.shape)
print("\nRecords by fiscal year:")
print(df["fiscal_year"].value_counts().sort_index())

# Nationwide Analysis
recipients_wide = pd.pivot(df,values='total_recipients', index='county_fips', columns='fiscal_year')

# Absolute change in recipients
recipients_wide['abs_recp'] = recipients_wide[2025] - recipients_wide[2023]

# Percentage change in recipients
recipients_wide['perc_recp'] = (recipients_wide[2025] - recipients_wide[2023])/recipients_wide[2023] * 100

expenditures_wide = pd.pivot(df,values='compensation_pension_usd', index='county_fips', columns='fiscal_year')
# Absolute change in expenditures
expenditures_wide['abs_exp'] = expenditures_wide[2025] - expenditures_wide[2023]
expenditures_wide['perc_exp'] = (expenditures_wide[2025] - expenditures_wide[2023])/expenditures_wide[2023] * 100

# Check for infinite values
print(np.isinf(recipients_wide["perc_recp"]).sum())
print(np.isinf(expenditures_wide["perc_exp"]).sum())

# Check for missing values
print(recipients_wide["perc_recp"].isna().sum())
print(expenditures_wide["perc_exp"].isna().sum())

# Replace infinite values with NaN
recipients_wide["perc_recp"] = recipients_wide["perc_recp"].replace(
    [np.inf, -np.inf], np.nan
)
expenditures_wide["perc_exp"] = expenditures_wide["perc_exp"].replace(
    [np.inf, -np.inf], np.nan
)

# Descriptive statistics
print("Recipient percentage change:")
print(recipients_wide["perc_recp"].describe())

print("\nExpenditure percentage change:")
print(expenditures_wide["perc_exp"].describe())

# Number of counties with increases, decreases, or no change
print("\nRecipient changes:")
print("Increased:", (recipients_wide["abs_recp"] > 0).sum())
print("Decreased:", (recipients_wide["abs_recp"] < 0).sum())
print("Unchanged:", (recipients_wide["abs_recp"] == 0).sum())

print("\nExpenditure changes:")
print("Increased:", (expenditures_wide["abs_exp"] > 0).sum())
print("Decreased:", (expenditures_wide["abs_exp"] < 0).sum())
print("Unchanged:", (expenditures_wide["abs_exp"] == 0).sum())

# Distribution of county-level recipient changes
plt.figure()  # Added: start a separate figure for this histogram
plt.hist(recipients_wide["perc_recp"], bins=40)
plt.axvline(0, color="red", linestyle="--")

plt.xlim(-100, 100)
plt.xlabel("Recipient Change (%)")
plt.ylabel("Number of Counties")
plt.title("Distribution of County-Level Recipient Changes (FY2023–FY2025)")

plt.tight_layout()
plt.savefig(output_dir / "county_recipient_growth_histogram.png", dpi=300, bbox_inches="tight")
plt.close()

# Distribution of county-level expenditure changes
plt.figure()  # Added: start a separate figure for this histogram
plt.hist(expenditures_wide['perc_exp'], bins=40)
plt.axvline(0, color="red", linestyle="--")

plt.xlim(-100, 100)
plt.xlabel("Expenditure Change (%)")
plt.ylabel("Number of Counties")
plt.title("Distribution of County-Level Expenditure Changes (FY2023–FY2025)")

plt.tight_layout()
plt.savefig(output_dir / "county_expenditure_growth_histogram.png", dpi=300, bbox_inches="tight")
plt.close()

# Do counties experiencing greater increases in VA disability compensation recipients also experience greater increases in compensation and pension expenditures?
county_changes = pd.concat([recipients_wide['perc_recp'], expenditures_wide['perc_exp']], axis=1)
county_changes.to_csv(output_dir / "county_growth.csv")

plt.figure(figsize=(8, 6))

plt.scatter(
    county_changes["perc_recp"],
    county_changes["perc_exp"],
    alpha=0.2,
    s=10
)

plt.xlabel("Recipient Change (%)")
plt.ylabel("Compensation & Pension Expenditure Change (%)")
plt.title("County-Level Recipient vs. Expenditure Growth (FY2023–FY2025)")

plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)

plt.tight_layout()
plt.savefig(output_dir / "county_growth_scatterplot.png", dpi=300, bbox_inches="tight")
plt.close()

# State level analysis
state_summary = (
    df.groupby(["state_name", "fiscal_year"], as_index=False)[
        ["total_recipients", "compensation_pension_usd"]
    ].sum()
)

state_recipients_wide = state_summary.pivot(
    index="state_name",
    columns="fiscal_year",
    values="total_recipients"
)
state_recipients_wide['growth_perc'] = (state_recipients_wide[2025] - state_recipients_wide[2023])/state_recipients_wide[2023] *100

state_cp_usd_wide = state_summary.pivot(
    index="state_name",
    columns="fiscal_year",
    values="compensation_pension_usd"
)
state_cp_usd_wide['growth_perc'] = (state_cp_usd_wide[2025] - state_cp_usd_wide[2023])/state_cp_usd_wide[2023] *100

state_growth = pd.concat(
    [
        state_recipients_wide["growth_perc"].rename("recipient_growth"),
        state_cp_usd_wide["growth_perc"].rename("expenditure_growth")
    ],
    axis=1
).dropna()

state_growth = state_growth.sort_values("recipient_growth")
state_growth.to_csv(output_dir / "state_growth.csv")

selected_states = pd.concat([
    state_growth.head(5),
    state_growth.tail(5)
])

ax = selected_states.plot(
    kind="barh",
    figsize=(11, 7),
    width=0.75
)

ax.set_xlabel("Percentage Change (%)")
ax.set_ylabel("")
ax.set_title("Change in VA Recipients and Compensation/Pension Expenditures (FY2023–FY2025)")
ax.legend(["Recipients", "Expenditures"])
ax.axhline(y=4.5, color="gray", linestyle="--", linewidth=1)

plt.tight_layout()
plt.savefig(output_dir / "state_growth_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
