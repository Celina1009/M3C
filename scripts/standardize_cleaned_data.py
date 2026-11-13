import pandas as pd
import numpy as np

# ==============================================================================
# 1. STANDARDIZE VA DISABILITY RECIPIENTS (FY2023 - FY2025)
# ==============================================================================
rec_specs = [
    ('Cleaned_FY2023_VA Disability Compensation Recipients by County.csv', 2023, 'IntegrationReady_FY2023_VA_Disability_Recipients.csv'),
    ('Cleaned_FY2024_VA Disability Compensation Recipients by County.csv', 2024, 'IntegrationReady_FY2024_VA_Disability_Recipients.csv'),
    ('Cleaned_FY2025_VA Disability Compensation Recipients by County.csv', 2025, 'IntegrationReady_FY2025_VA_Disability_Recipients.csv'),
]

col_rename_map = {
    'fips_code': 'county_fips',
    'state': 'state_name',
    'county_name': 'county_name_raw',
    'total:_disability_compensation_recipients': 'total_recipients',
    'scd_rating:_0%_to_20%': 'scd_rating_0_to_20_pct',
    'scd_rating:_30%_to_40%': 'scd_rating_30_to_40_pct',
    'scd_rating:_50%_to_60%': 'scd_rating_50_to_60_pct',
    'scd_rating:_70%_to_90%': 'scd_rating_70_to_90_pct',
    'scd_rating:_100%': 'scd_rating_100_pct',
    'age:_17-44': 'age_17_to_44',
    'age:_45-64': 'age_45_to_64',
    'age:_65_or_older': 'age_65_plus',
    'male': 'male_recipients',
    'female': 'female_recipients'
}

metric_cols = [
    'total_recipients', 'scd_rating_0_to_20_pct', 'scd_rating_30_to_40_pct',
    'scd_rating_50_to_60_pct', 'scd_rating_70_to_90_pct', 'scd_rating_100_pct',
    'age_17_to_44', 'age_45_to_64', 'age_65_plus', 'male_recipients', 'female_recipients'
]

for src, fy, out_name in rec_specs:
    df = pd.read_csv(src, dtype=str).rename(columns=col_rename_map)
    df.insert(0, 'fiscal_year', fy)

    # Zero-pad county FIPS codes to 5-digit strings (e.g., 1001.0 -> '01001')
    df['county_fips'] = (
        df['county_fips']
        .str.replace(r'\.0$', '', regex=True)
        .str.strip()
        .str.zfill(5)
    )

    # Flag non-county aggregate records (US Territories, Foreign, Unknown)
    non_county_mask = df['county_fips'].isin(['00000', '88888']) | df['state_name'].isin([
        'US TERRITORIES (EXCLUDING PUERTO RICO)', 'OTHER FOREIGN COUNTRIES', 'UNKNOWN'
    ])
    df['geo_level'] = np.where(non_county_mask, 'non_county_aggregate', 'county')

    # Convert recipient counts from float strings to nullable integers (Int64)
    for c in metric_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').round().astype('Int64')

    ordered_cols = ['fiscal_year', 'county_fips', 'state_name', 'geo_level'] + metric_cols
    df[ordered_cols].to_csv(out_name, index=False)


# ==============================================================================
# 2. STANDARDIZE GDX EXPENDITURES (FY2023 - FY2025)
# ==============================================================================

# --- GDX FY2023 ---
gdx23 = pd.read_csv('Cleaned_GDX_FY23.csv', dtype=str)
gdx23 = gdx23[gdx23['sheet_source'] != 'Data Guide'].copy()

num_cols_23 = [
    c for c in gdx23.columns
    if c not in ['unnamed:_0', 'sheet_source', 'fy23_summary_of_expenditures_by_state']
]
for c in num_cols_23:
    gdx23[c] = pd.to_numeric(gdx23[c], errors='coerce').fillna(0.0)

# Drop all-zero header/blank rows
gdx23 = gdx23[(gdx23[num_cols_23] != 0.0).any(axis=1)].copy()

# Normalize FY23 expenditures from thousands of dollars to exact USD
dollar_cols_23 = [
    'unnamed:_1', 'unnamed:_2', 'unnamed:_3', 'unnamed:_4',
    'unnamed:_5', 'unnamed:_6', 'unnamed:_7', 'unnamed:_8', 'unnamed:_9'
]
for c in dollar_cols_23:
    gdx23[c] = (gdx23[c] * 1000.0).round(2)
gdx23['unnamed:_10'] = gdx23['unnamed:_10'].round().astype('Int64')

gdx23_clean = pd.DataFrame({
    'fiscal_year': 2023,
    'geo_level': np.where(gdx23['sheet_source'] == 'State Level Expenditures', 'state', 'county'),
    'state_abbr': np.where(gdx23['sheet_source'] == 'State Level Expenditures', 'ALL', gdx23['sheet_source']),
    'veteran_population_est': gdx23['unnamed:_1'].round().astype('Int64'),
    'total_expenditure_usd': gdx23['unnamed:_2'],
    'compensation_pension_usd': gdx23['unnamed:_3'],
    'construction_usd': gdx23['unnamed:_4'],
    'education_voc_rehab_usd': gdx23['unnamed:_5'],
    'loan_guaranty_usd': gdx23['unnamed:_6'],
    'general_operating_usd': gdx23['unnamed:_7'],
    'insurance_indemnities_usd': gdx23['unnamed:_8'],
    'medical_care_usd': gdx23['unnamed:_9'],
    'unique_patients': gdx23['unnamed:_10'],
    'join_status': 'BLOCKED_MISSING_COUNTY_FIPS_IN_SOURCE_CSV'
})
gdx23_clean.to_csv('IntegrationReady_GDX_FY2023.csv', index=False)

# --- GDX FY2024 ---
gdx24 = pd.read_csv('Cleaned_GDX_FY24.csv', dtype=str)
gdx24 = gdx24[gdx24['sheet_source'] != 'Data Guide'].copy()

num_cols_24 = [c for c in gdx24.columns if c not in ['unnamed:_0', 'unnamed:_1', 'sheet_source']]
for c in num_cols_24:
    gdx24[c] = pd.to_numeric(gdx24[c], errors='coerce').fillna(0.0)
gdx24 = gdx24[(gdx24[num_cols_24] != 0.0).any(axis=1)].copy()

# Normalize FY24 State sheets from thousands of dollars to exact USD
state_mask_24 = gdx24['sheet_source'].isin(['State Direct Exp', 'State_Indirect_Exp'])
exp_cols_24 = ['unnamed:_3', 'unnamed:_4', 'unnamed:_5', 'unnamed:_6', 'unnamed:_7', 'unnamed:_8']
for c in exp_cols_24:
    gdx24.loc[state_mask_24, c] = gdx24.loc[state_mask_24, c] * 1000.0
    gdx24[c] = gdx24[c].round(2)

gdx24_clean = pd.DataFrame({
    'fiscal_year': 2024,
    'sheet_category': gdx24['sheet_source'].str.replace('_', ' '),
    'geo_level': gdx24['sheet_source'].map({
        'State Direct Exp': 'state', 'State_Indirect_Exp': 'state',
        'County Direct Exp': 'county', 'County Indirect Exp': 'county',
        'CD Direct Exp': 'congressional_district', 'CD Indirect Exp': 'congressional_district'
    }),
    'expenditure_type': np.where(gdx24['sheet_source'].str.contains('Indirect'), 'indirect', 'direct'),
    'state_fips_if_available': (
        pd.to_numeric(gdx24['unnamed:_2'], errors='coerce')
        .round().astype('Int64').astype(str).str.zfill(2)
        .replace({'00': np.nan, '<NA>': np.nan})
    ),
    'total_expenditure_usd': gdx24['unnamed:_3'],
    'category_1_usd': gdx24['unnamed:_4'],
    'category_2_usd': gdx24['unnamed:_5'],
    'category_3_usd': gdx24['unnamed:_6'],
    'category_4_usd': gdx24['unnamed:_7'],
    'category_5_usd': gdx24['unnamed:_8'],
    'join_status': 'BLOCKED_MISSING_COUNTY_FIPS_IN_SOURCE_CSV'
})
gdx24_clean.to_csv('IntegrationReady_GDX_FY2024.csv', index=False)

# --- GDX FY2025 ---
gdx25 = pd.read_csv('Cleaned_GDX_FY25.csv', dtype=str)
gdx25 = gdx25[gdx25['sheet_source'].str.strip() != 'Data  Guide'].copy()

num_cols_25 = [c for c in gdx25.columns if c not in ['unnamed:_0', 'unnamed:_1', 'unnamed:_2', 'sheet_source']]
for c in num_cols_25:
    gdx25[c] = pd.to_numeric(gdx25[c], errors='coerce').fillna(0.0)
gdx25 = gdx25[(gdx25[num_cols_25] != 0.0).any(axis=1)].copy()

state_fips_25 = (
    pd.to_numeric(
        gdx25['fy25_summary_of_direct_benefit_expenditures_by_state'].where(
            gdx25['fy25_summary_of_direct_benefit_expenditures_by_state'] != 0.0,
            gdx25['fy25_summary_of_indirect_benefit_expenditures_by_state']
        ),
        errors='coerce'
    )
    .round().astype('Int64').astype(str).str.zfill(2)
    .replace({'00': np.nan, '<NA>': np.nan})
)

exp_cols_25 = [
    'unnamed:_3', 'unnamed:_4', 'unnamed:_5', 'unnamed:_6',
    'unnamed:_7', 'unnamed:_8', 'unnamed:_9', 'unnamed:_10', 'unnamed:_11'
]
for c in exp_cols_25:
    gdx25[c] = gdx25[c].round(2)

gdx25_clean = pd.DataFrame({
    'fiscal_year': 2025,
    'sheet_category': gdx25['sheet_source'].str.strip(),
    'geo_level': gdx25['sheet_source'].str.strip().map({
        'State Direct Exp': 'state', 'State Indirect Exp': 'state',
        'County Direct Exp': 'county', 'County Indirect Exp': 'county',
        'CD Direct Exp': 'congressional_district', 'CD Indirect Exp': 'congressional_district'
    }),
    'expenditure_type': np.where(gdx25['sheet_source'].str.contains('Indirect'), 'indirect', 'direct'),
    'state_fips_if_available': state_fips_25,
    'total_expenditure_usd': gdx25['unnamed:_3'],
    'category_1_usd': gdx25['unnamed:_4'],
    'category_2_usd': gdx25['unnamed:_5'],
    'category_3_usd': gdx25['unnamed:_6'],
    'category_4_usd': gdx25['unnamed:_7'],
    'category_5_usd': gdx25['unnamed:_8'],
    'category_6_usd': gdx25['unnamed:_9'],
    'category_7_usd': gdx25['unnamed:_10'],
    'category_8_usd': gdx25['unnamed:_11'],
    'join_status': 'BLOCKED_MISSING_COUNTY_FIPS_IN_SOURCE_CSV'
})
gdx25_clean.to_csv('IntegrationReady_GDX_FY2025.csv', index=False)


# ==============================================================================
# 3. STANDARDIZE VETPOP2023 COUNTY PROJECTIONS
# ==============================================================================
vp = pd.read_csv('Cleaned_VetPop2023 County Data.csv', dtype=str)

vp_clean = pd.DataFrame({
    'county_fips': vp['fips'].str.strip().str.zfill(5),
    'state_name': vp['state'].str.strip(),
    'geo_level': np.where(vp['fips'].str.strip().isin(['99000']), 'non_county_aggregate', 'county'),
    'projection_block_index': vp.index // 25200,  # 31 projection year blocks (25,200 rows per block)
    'demographic_cell_index': vp.index % 8,      # 8 age/sex cells per county per block
    'veterans': pd.to_numeric(vp['veterans'], errors='coerce').round().astype('Int64'),
    'join_status': 'PARTIAL_DATE_AGE_SEX_OVERWRITTEN_AS_0_IN_SOURCE_CSV'
})
vp_clean.to_csv('IntegrationReady_VetPop2023_County.csv', index=False)