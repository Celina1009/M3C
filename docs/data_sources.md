# Data Sources and Acquisition

## 1. VA Disability Compensation Recipients by County

- **Source:** U.S. Department of Veterans Affairs (VA), National Center for Veterans Analysis and Statistics.
- **Data:** Annual disability compensation recipient counts by county.
- **Fiscal years:** FY2023, FY2024, FY2025.
- **Format:** CSV.
- **Storage:** `data/raw/`
- **GitHub:** Original files are included in the repository.

**Source pages:**
- [FY2023 Disability Compensation Recipients by County](https://catalog.data.gov/dataset/fy-2023-disability-compensation-recipients-by-county)
- [FY2024 Disability Compensation Recipients by County](https://catalog.data.gov/dataset/fy-2024-disability-compensation-recipients-by-county)
- [FY2025 Disability Compensation Recipients by County](https://catalog.data.gov/dataset/fy-2025-disability-compensation-recipients-by-county)

**Local file timestamp date:** November 13, 2026.

## 2. Geographic Distribution of VA Expenditures (GDX)

- **Source:** U.S. Department of Veterans Affairs.
- **Data:** VA expenditures by geographic area and program.
- **Fiscal years:** FY2023, FY2024, FY2025.
- **Format:** Excel workbooks.
- **Storage:** `data/raw/`
- **GitHub:** Original files are included in the repository.
- **Source page:** [VA Geographic Distribution of Expenditures](https://www.va.gov/vetdata/Expenditures.asp)

**Local file timestamp date:** November 13, 2026.

## 3. VetPop2023 County Data

- **Source:** U.S. Department of Veterans Affairs.
- **Data:** Projected veteran population by county, including demographic categories.
- **Format:** CSV.
- **Original filename:** `VetPop2023 county data.csv`
- **Size:** Approximately 64 MB.
- **Storage:** University of Illinois Box.
- **Source page:** [VetPop2023 County Data](https://catalog.data.gov/dataset/vetpop2023-county-data-9l)

**Local file timestamp date:** November 13, 2026.

### Box Access and Download Instructions

The VetPop dataset is stored in U of I Box because it exceeds the project's 50 MB GitHub storage threshold.

**Box download link:**

https://uofi.box.com/shared/static/claymwl2hzbzxdkp6yc5q6vaee59hsnp.csv

The dataset is not committed to GitHub. Team members can download it into `data/raw/` by running:

```bash
python scripts/download_vetpop.py
```

The download script:
1. Downloads the dataset from Box.
2. Saves it in `data/raw/`.
3. Calculates its SHA-256 checksum.
4. Compares the checksum with the expected value.
5. Accepts the file only if the checksum matches.

**Expected SHA-256 checksum:**

`b0787e318ca6d5abc648c11068f7c9de3997c44a1e3484010701d6472b4c47ed`

The download process has been tested successfully, and the downloaded file matched the expected checksum.

## 4. Data Storage and Reproducibility

The project uses the following folder organization:

- `data/raw/` – Original source datasets.
- `data/cleaned/` – Cleaned datasets.
- `data/processed/` – Processed and integrated datasets.
- `scripts/` – Python scripts for data acquisition, cleaning, and integration.
- `docs/` – Project documentation and data source information.
- `results/` – Analysis outputs and results.

### Data Integrity

SHA-256 checksums are used to verify the integrity of the raw datasets.

The checksum manifest is stored at:

`data/raw/SHA256SUMS.txt`

All seven raw datasets were verified successfully using:

```bash
sha256sum -c data/raw/SHA256SUMS.txt
```

The large VetPop dataset is stored externally in Box and retrieved using the provided Python download script to keep the GitHub repository within the project's file-size requirements.

### Initial Dataset Record Counts

The following CSV record counts were verified, excluding header rows:

| Dataset | Data rows |
|---|---:|
| FY2023 recipient data | 3,147 |
| FY2024 recipient data | 3,148 |
| FY2025 recipient data | 3,148 |
| VetPop2023 county data | 781,200 |

GDX Excel workbook record counts will be documented after inspection.

*Note: Local file timestamps indicate when files were last modified in the Codespace; they do not independently establish the original source retrieval dates. Record counts are initial checks and do not establish data completeness or uniqueness.*

## 5. Project Dependencies

Python dependencies are listed in `requirements.txt`.

To install the required libraries in a Codespace or local Python environment, run:

```bash
python -m pip install -r requirements.txt

## 6. Preliminary Data Quality and Integration Considerations

The following observations were identified during the initial data acquisition and structural review. Further validation is required during the cleaning and integration stages.

- **Geographic coverage:** The datasets contain county-level information, but county and county-equivalent coverage must be checked across sources. The FY2023 GDX workbook uses separate state and territory worksheets, unlike the FY2024 and FY2025 workbooks.
- **Missing and suppressed values:** Missing, suppressed, or unavailable values must be identified and distinguished from actual zero values.
- **Duplicate records:** County-level records must be checked for duplicates before integration.
- **Fiscal-year alignment:** Recipient and GDX datasets are available for FY2023, FY2024, and FY2025. VetPop2023 is intended as the FY2023 veteran population baseline, not a population series for all three years.
- **Expenditure definitions:** GDX contains expenditures across multiple VA programs. The Compensation and Pension category must be distinguished from total VA expenditures. The FY2023-to-FY2024 methodology change must also be considered when comparing expenditure trends.
- **Integration feasibility:** County names and geographic identifiers must be standardized and validated before joining the datasets. A geographic crosswalk may be required to resolve naming differences and unmatched records.

These are preliminary considerations, not completed validation results. Detailed cleaning, duplicate checks, missing-value analysis, and integration validation will be documented in the subsequent project stages.