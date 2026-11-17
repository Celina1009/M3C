import pandas as pd
from pathlib import Path

CLEANED = Path("data/cleaned")
PROCESSED = Path("data/processed")
OUTPUT = PROCESSED / "integrated"

OUTPUT.mkdir(parents=True, exist_ok=True)

def normalize_fips(df):
    df = df.copy()
    df["county_fips"] = (
        df["county_fips"]
        .astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(5)
    )
    return df

# Load FY2023 VetPop baseline
vetpop = pd.read_csv(
    PROCESSED / "Prepared_VetPop_FY2023.csv",
    dtype={"county_fips": str}
)
vetpop = normalize_fips(vetpop)

if vetpop["county_fips"].duplicated().any():
    raise ValueError("Duplicate FIPS found in VetPop.")

vetpop = vetpop[
    ["county_fips", "veteran_population_fy2023"]
]

qa_summary = []
unmatched_records = []

for year in [2023, 2024, 2025]:
    print(f"\nIntegrating FY{year}...")

    # Load recipient data and retain county-level records
    recipients = pd.read_csv(
        CLEANED / f"IntegrationReady_FY{year}_VA_Disability_Recipients.csv",
        dtype={"county_fips": str}
    )
    recipients = recipients[
        recipients["geo_level"] == "county"
    ].copy()
    recipients = normalize_fips(recipients)

    # Load prepared GDX data
    gdx = pd.read_csv(
        PROCESSED / f"Prepared_GDX_FY{year}.csv",
        dtype={"county_fips": str}
    )
    gdx = normalize_fips(gdx)

    if recipients["county_fips"].duplicated().any():
        raise ValueError(f"Duplicate recipient FIPS in FY{year}.")

    if gdx["county_fips"].duplicated().any():
        raise ValueError(f"Duplicate GDX FIPS in FY{year}.")

    # Keep relevant GDX expenditure measures
    gdx_columns = [
        "county_fips",
        "total_direct_expenditure_usd",
        "compensation_pension_usd",
        "total_indirect_expenditure_usd"
    ]
    gdx = gdx[gdx_columns]

    # Join recipients to GDX and FY2023 VetPop baseline
    integrated = recipients.merge(
        gdx,
        on="county_fips",
        how="left",
        validate="one_to_one",
        indicator="gdx_match"
    )

    integrated = integrated.merge(
        vetpop,
        on="county_fips",
        how="left",
        validate="one_to_one",
        indicator="vetpop_match"
    )

    integrated["gdx_match"] = integrated["gdx_match"].map({
        "both": "MATCHED",
        "left_only": "NO_GDX_MATCH"
    })

    integrated["vetpop_match"] = integrated["vetpop_match"].map({
        "both": "MATCHED",
        "left_only": "NO_VETPOP_MATCH"
    })

    # Save integrated dataset
    output_file = OUTPUT / f"Integrated_FY{year}.csv"
    integrated.to_csv(output_file, index=False)

    # Record QA results
    gdx_unmatched = (integrated["gdx_match"] == "NO_GDX_MATCH").sum()
    vetpop_unmatched = (integrated["vetpop_match"] == "NO_VETPOP_MATCH").sum()

    qa_summary.append({
        "fiscal_year": year,
        "recipient_counties": len(recipients),
        "integrated_rows": len(integrated),
        "unique_fips": integrated["county_fips"].nunique(),
        "gdx_matched": len(integrated) - gdx_unmatched,
        "gdx_unmatched": gdx_unmatched,
        "vetpop_matched": len(integrated) - vetpop_unmatched,
        "vetpop_unmatched": vetpop_unmatched,
        "missing_compensation_pension": integrated["compensation_pension_usd"].isna().sum(),
        "missing_vetpop_baseline": integrated["veteran_population_fy2023"].isna().sum()
    })

    unmatched = integrated[
        (integrated["gdx_match"] == "NO_GDX_MATCH") |
        (integrated["vetpop_match"] == "NO_VETPOP_MATCH")
    ][[
        "fiscal_year",
        "county_fips",
        "state_name",
        "gdx_match",
        "vetpop_match"
    ]]

    unmatched_records.append(unmatched)

    print("Output:", output_file)
    print("Rows:", len(integrated))
    print("GDX unmatched:", gdx_unmatched)
    print("VetPop unmatched:", vetpop_unmatched)

# Save QA reports
qa = pd.DataFrame(qa_summary)
qa.to_csv(OUTPUT / "Integration_QA_Summary.csv", index=False)

unmatched_all = pd.concat(unmatched_records, ignore_index=True)
unmatched_all.to_csv(
    OUTPUT / "Integration_Unmatched_Geographies.csv",
    index=False
)

print("\nIntegration complete.")
print("\nQA Summary:")
print(qa.to_string(index=False))
print("\nOutput folder:", OUTPUT)
