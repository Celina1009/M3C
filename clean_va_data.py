import pandas as pd
import numpy as np
import re

# -------------------------------------------------------------------
# 1. Helper Functions for Standardization
# -------------------------------------------------------------------


def clean_fips(val):
    """Formats FIPS codes as 5-digit strings with leading zeros."""
    if pd.isna(val) or val is None or str(val).strip() == '':
        return np.nan
    val_str = str(val).split('.')[0].strip()
    # Remove non-alphanumeric characters
    val_str = re.sub(r'[^0-9]', '', val_str)
    if not val_str:
        return np.nan
    return val_str.zfill(5)


def clean_county_name(name):
    """Standardizes county names (uppercase, stripped whitespace)."""
    if pd.isna(name) or name is None:
        return np.nan
    name = str(name).strip().upper()
    name = re.sub(r'\s+', ' ', name)  # normalize spaces
    return name


def clean_currency(val):
    """Converts currency/numeric text into clean numeric values (in USD)."""
    if pd.isna(val) or val is None:
        return np.nan
    val_str = str(val).replace('$', '').replace(',', '').strip()
    try:
        return float(val_str)
    except ValueError:
        return np.nan


# -------------------------------------------------------------------
# 2. Process VA Disability Compensation Files (FY23, FY24, FY25)
# -------------------------------------------------------------------
va_files = {
    "FY2023": "FY2023_VA Disability Compensation Recipients by County.csv",
    "FY24": "FY2024_VA Disability Compensation Recipients by County.csv",
    "FY25": "FY2025_VA Disability Compensation Recipients by County.csv",
}

for year, filename in va_files.items():
    try:
        df = pd.read_csv(filename)

        # Standardize Column Names
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

        # Standardize Identifiers
        if 'fips' in df.columns:
            df['fips'] = df['fips'].apply(clean_fips)
        if 'county' in df.columns:
            df['county'] = df['county'].apply(clean_county_name)
        if 'state' in df.columns:
            df['state'] = df['state'].astype(str).str.strip().str.upper()

        # Handle Missing Values & Numeric Formatting
        numeric_cols = df.select_dtypes(include=[np.number, 'object']).columns
        for col in numeric_cols:
            if col not in ['fips', 'county', 'state']:
                df[col] = df[col].apply(clean_currency)
                df[col] = df[col].fillna(0)  # Fill missing numeric metrics with 0

        # Save Cleaned CSV
        out_name = f"Cleaned_{filename}"
        df.to_csv(out_name, index=False)
        print(f"Successfully processed: {out_name}")
    except Exception as e:
        print(f"Could not process {filename}: {e}")

# -------------------------------------------------------------------
# 3. Process GDX Files (FY23, FY24, FY25 Excel Workbook sheets)
# -------------------------------------------------------------------
gdx_files = {
    "FY23": "GDX_FY23.xlsx",
    "FY24": "GDX_FY24.xlsx",
    "FY25": "GDX_FY25.xlsx",
}

for year, filename in gdx_files.items():
    try:
        xls = pd.ExcelFile(filename)
        all_sheets = []

        for sheet_name in xls.sheet_names:
            sheet_df = pd.read_excel(xls, sheet_name=sheet_name)
            sheet_df.columns = [c.strip().lower().replace(' ', '_') for c in sheet_df.columns]

            # Identify and Clean County/FIPS Identifiers
            if 'fips' in sheet_df.columns:
                sheet_df['fips'] = sheet_df['fips'].apply(clean_fips)
            if 'county' in sheet_df.columns:
                sheet_df['county'] = sheet_df['county'].apply(clean_county_name)
            if 'state' in sheet_df.columns:
                sheet_df['state'] = sheet_df['state'].astype(str).str.strip().str.upper()

            # Clean Numeric Fields ($ values, counts)
            for col in sheet_df.columns:
                if col not in ['fips', 'county', 'state']:
                    sheet_df[col] = sheet_df[col].apply(clean_currency)
                    sheet_df[col] = sheet_df[col].fillna(0)

            sheet_df['sheet_source'] = sheet_name
            all_sheets.append(sheet_df)

        combined_gdx = pd.concat(all_sheets, ignore_index=True)
        out_name = f"Cleaned_{filename.replace('.xlsx', '.csv')}"
        combined_gdx.to_csv(out_name, index=False)
        print(f"Successfully processed: {out_name}")
    except Exception as e:
        print(f"Could not process {filename}: {e}")

# -------------------------------------------------------------------
# 4. Process VetPop2023 County Data
# -------------------------------------------------------------------
try:
    vetpop_filename = "VetPop2023 County Data.csv"
    df_vetpop = pd.read_csv(vetpop_filename)

    df_vetpop.columns = [c.strip().lower().replace(' ', '_') for c in df_vetpop.columns]

    if 'fips' in df_vetpop.columns:
        df_vetpop['fips'] = df_vetpop['fips'].apply(clean_fips)
    if 'county' in df_vetpop.columns:
        df_vetpop['county'] = df_vetpop['county'].apply(clean_county_name)
    if 'state' in df_vetpop.columns:
        df_vetpop['state'] = df_vetpop['state'].astype(str).str.strip().str.upper()

    # Fill missing population estimates with 0 or forward fill where applicable
    num_cols = df_vetpop.select_dtypes(include=[np.number, 'object']).columns
    for col in num_cols:
        if col not in ['fips', 'county', 'state']:
            df_vetpop[col] = df_vetpop[col].apply(clean_currency)
            df_vetpop[col] = df_vetpop[col].fillna(0)

    out_name = f"Cleaned_{vetpop_filename}"
    df_vetpop.to_csv(out_name, index=False)
    print(f"Successfully processed: {out_name}")
except Exception as e:
    print(f"Could not process VetPop dataset: {e}")