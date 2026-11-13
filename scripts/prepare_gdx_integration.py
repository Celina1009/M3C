#!/usr/bin/env python3
"""Prepare county-level GDX datasets for FY2023-FY2025.

Reads original GDX workbooks and the FY2023 VA recipient file as a
state/county-to-FIPS lookup. FY2023 territory sheets are excluded from
county-level output. Does not modify raw, cleaned, or existing
IntegrationReady files.

FY2023 monetary amounts are in $000s and are converted to USD.
FY2023 veteran population estimates are already counts and are not scaled.
FY2024/FY2025 workbook expenditures are in dollars.
"""

from pathlib import Path
import re
import unicodedata

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "processed"

LOOKUP_FILE = RAW / "FY2023 recipient data.csv"
WORKBOOKS = {
    2023: RAW / "GDX_FY23.xlsx",
    2024: RAW / "GDX_FY24.xlsx",
    2025: RAW / "GDX_FY25.xlsx",
}

STATE_ABBR_TO_NAME = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut",
    "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico", "GU": "Guam",
}


def normalize(value):
    if pd.isna(value):
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^A-Z0-9]+", " ", value.upper().strip())
    return re.sub(r"\s+", " ", value).strip()


def to_number(series):
    return pd.to_numeric(
        series.astype("string")
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip(),
        errors="coerce",
    )


def get_column(frame, expected):
    target = normalize(expected)
    normalized = {normalize(c): c for c in frame.columns}
    if target in normalized:
        return normalized[target]
    for key, original in normalized.items():
        if target in key:
            return original
    raise KeyError(
        f"Missing expected column {expected!r}. Available: {list(frame.columns)}"
    )


def build_fips_lookup():
    data = pd.read_csv(LOOKUP_FILE, dtype=str)
    required = ["FIPS code", "State", "County Name"]
    if any(c not in data.columns for c in required):
        raise ValueError(f"Lookup file must contain {required}")

    data["state_key"] = data["State"].map(normalize)
    data["county_key"] = data["County Name"].map(normalize)
    data["county_fips"] = (
        data["FIPS code"].astype("string").str.strip()
        .str.replace(r"\.0$", "", regex=True).str.zfill(5)
    )

    if data.duplicated(["state_key", "county_key"]).any():
        raise ValueError("Duplicate state/county keys in recipient lookup.")
    if data["county_fips"].duplicated().any():
        raise ValueError("Duplicate FIPS codes in recipient lookup.")

    return {
        (r.state_key, r.county_key): r.county_fips
        for r in data.itertuples(index=False)
    }


def attach_geography(data, state_col, county_col, lookup, fiscal_year):
    out = data.copy()
    out["state_name"] = out[state_col].astype("string").str.strip()
    out["county_name"] = out[county_col].astype("string").str.strip()
    out = out[
        out["state_name"].notna()
        & out["county_name"].notna()
        & (out["state_name"] != "")
        & (out["county_name"] != "")
        & (out["county_name"].str.upper() != "TOTALS")
    ].copy()

    out["state_key"] = out["state_name"].map(normalize)
    out["county_key"] = out["county_name"].map(normalize)
    out["county_fips"] = [
        lookup.get((s, c), pd.NA)
        for s, c in zip(out["state_key"], out["county_key"])
    ]
    out["fiscal_year"] = fiscal_year
    out["join_status"] = out["county_fips"].notna().map(
        {True: "MATCHED_FIPS", False: "UNMATCHED_GEOGRAPHY"}
    )
    return out


def assert_unique_counties(data, label):
    dup = data.duplicated(["state_key", "county_key"], keep=False)
    if dup.any():
        sample = data.loc[dup, ["state_name", "county_name"]].head(15)
        raise ValueError(
            f"{label} has duplicate state/county rows:\n{sample.to_string(index=False)}"
        )


def prepare_2023(lookup):
    path = WORKBOOKS[2023]
    workbook = pd.ExcelFile(path)
    pieces = []

    for sheet in workbook.sheet_names:
        if sheet in {"Data Guide", "State Level Expenditures"}:
            continue
        # The recipient lookup is county-level for the 50 states and DC.
        # FY2023 PR contains municipality rows and GU is a territory aggregate,
        # so neither can be joined consistently to county-level records.
        if sheet in {"PR", "GU"}:
            print(f"FY2023: excluding territory sheet {sheet} from county-level output")
            continue

        state = STATE_ABBR_TO_NAME.get(sheet)
        if state is None:
            print(f"FY2023: skipping unrecognized sheet {sheet!r}")
            continue

        raw = pd.read_excel(path, sheet_name=sheet, header=2)
        county_col = get_column(raw, "County Congressional District")
        population_col = get_column(raw, "Veteran Population")
        total_col = get_column(raw, "Total Expenditure")
        comp_col = get_column(raw, "Compensation Pension")

        data = pd.DataFrame({
            "state_name": state,
            "county_name": raw[county_col],
            "veteran_population_est": to_number(raw[population_col]),
            "total_direct_expenditure_usd": to_number(raw[total_col]) * 1000,
            "compensation_pension_usd": to_number(raw[comp_col]) * 1000,
            "total_indirect_expenditure_usd": pd.NA,
        })

        # State worksheets include subtotal rows such as "ALABAMA (Totals)".
        # These are not counties and must be excluded from county-level output.
        county_labels = data["county_name"].astype("string").str.strip()
        county_labels_upper = county_labels.str.upper()

        # Keep actual county/county-equivalent rows only. FY2023 state worksheets
        # also contain congressional-district summaries, state/territory totals,
        # and explanatory notes below the county table.
        valid_county_row = (
            county_labels.notna()
            & (county_labels != "")
            & ~county_labels_upper.str.contains(r"TOTALS|CONG\.?\s*DIST|^NOTES:?$", na=False)
            & data["total_direct_expenditure_usd"].notna()
            & data["compensation_pension_usd"].notna()
        )
        data = data.loc[valid_county_row].copy()

        # Documented spelling/abbreviation variants between the GDX workbook
        # and the FY2023 recipient county lookup.
        county_aliases = {
            "FAIRBANKS N STAR": "FAIRBANKS NORTH STAR",
            "DE KALB": "DEKALB",
            "SAINT CLAIR": "ST CLAIR",
        }
        data["county_name"] = data["county_name"].map(
            lambda value: county_aliases.get(normalize(value), value)
        )

        data = attach_geography(
            data, "state_name", "county_name", lookup, 2023
        )
        data["source_type"] = sheet
        pieces.append(data)

    if not pieces:
        raise ValueError("No FY2023 state worksheets were processed.")

    result = pd.concat(pieces, ignore_index=True)
    assert_unique_counties(result, "FY2023 GDX")
    return result


def read_2024_2025_sheet(path, sheet_name, fiscal_year, expenditure_kind, lookup):
    raw = pd.read_excel(path, sheet_name=sheet_name, header=2)
    state_col = get_column(raw, "State")
    county_col = get_column(raw, "County")
    total_col = get_column(raw, f"Total {expenditure_kind} Expenditure")

    data = pd.DataFrame({
        "state_name": raw[state_col],
        "county_name": raw[county_col],
        "expenditure_usd": to_number(raw[total_col]),
    })

    if expenditure_kind == "Direct":
        comp_col = get_column(raw, "Compensation Pension")
        data["compensation_pension_usd"] = to_number(raw[comp_col])
    else:
        data["compensation_pension_usd"] = pd.NA

    data = attach_geography(
        data, "state_name", "county_name", lookup, fiscal_year
    )
    assert_unique_counties(data, f"FY{fiscal_year} {expenditure_kind}")
    return data


def prepare_2024_2025(fiscal_year, lookup):
    path = WORKBOOKS[fiscal_year]
    direct = read_2024_2025_sheet(
        path, "County Direct Exp", fiscal_year, "Direct", lookup
    )
    indirect = read_2024_2025_sheet(
        path, "County Indirect Exp", fiscal_year, "Indirect", lookup
    )

    direct = direct.rename(columns={
        "expenditure_usd": "total_direct_expenditure_usd",
        "join_status": "direct_join_status",
    })
    indirect = indirect.rename(columns={
        "state_name": "indirect_state_name",
        "county_name": "indirect_county_name",
        "county_fips": "indirect_county_fips",
        "expenditure_usd": "total_indirect_expenditure_usd",
        "compensation_pension_usd": "indirect_compensation_unused",
        "join_status": "indirect_join_status",
    })

    result = direct.merge(
        indirect[[
            "state_key", "county_key", "indirect_state_name",
            "indirect_county_name", "indirect_county_fips",
            "total_indirect_expenditure_usd", "indirect_join_status",
        ]],
        on=["state_key", "county_key"],
        how="outer",
        validate="one_to_one",
    )

    result["state_name"] = result["state_name"].combine_first(
        result["indirect_state_name"]
    )
    result["county_name"] = result["county_name"].combine_first(
        result["indirect_county_name"]
    )
    result["county_fips"] = result["county_fips"].combine_first(
        result["indirect_county_fips"]
    )
    result["join_status"] = result["county_fips"].notna().map(
        {True: "MATCHED_FIPS", False: "UNMATCHED_GEOGRAPHY"}
    )
    result["fiscal_year"] = fiscal_year
    result["veteran_population_est"] = pd.NA
    result["source_type"] = "County Direct + County Indirect"

    return result[[
        "fiscal_year", "state_name", "county_name", "county_fips",
        "veteran_population_est", "total_direct_expenditure_usd",
        "total_indirect_expenditure_usd", "compensation_pension_usd",
        "source_type", "join_status", "state_key", "county_key",
    ]]


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lookup = build_fips_lookup()
    unmatched = []

    for year in (2023, 2024, 2025):
        print(f"\nPreparing FY{year}...")
        result = (
            prepare_2023(lookup)
            if year == 2023
            else prepare_2024_2025(year, lookup)
        )

        missing = result[result["county_fips"].isna()]
        if not missing.empty:
            unmatched.append(missing[[
                "fiscal_year", "state_name", "county_name", "source_type"
            ]].drop_duplicates())

        output = result.drop(columns=["state_key", "county_key"])
        output_path = OUTPUT / f"Prepared_GDX_FY{year}.csv"
        output.to_csv(output_path, index=False)

        print(f"Rows: {len(result):,}")
        print(f"FIPS matched: {result['county_fips'].notna().sum():,}")
        print(f"Unmatched: {result['county_fips'].isna().sum():,}")
        print(f"Wrote: {output_path.relative_to(ROOT)}")

    unmatched_path = OUTPUT / "GDX_unmatched_geographies.csv"
    if unmatched:
        pd.concat(unmatched, ignore_index=True).to_csv(unmatched_path, index=False)
    else:
        pd.DataFrame(columns=[
            "fiscal_year", "state_name", "county_name", "source_type"
        ]).to_csv(unmatched_path, index=False)

    print(f"\nUnmatched-geography report: {unmatched_path.relative_to(ROOT)}")
    print("Preparation finished. Review outputs and unmatched records before joining.")


if __name__ == "__main__":
    main()
