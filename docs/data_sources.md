# Data Sources and Acquisition

## 1. VA Disability Compensation Recipients by County

- **Source:** U.S. Department of Veterans Affairs (VA), National Center for Veterans Analysis and Statistics.
- **Data:** Annual disability compensation recipient counts by county.
- **Fiscal years:** FY2023, FY2024, FY2025.
- **Format:** CSV.
- **Storage:** `data/raw/`
- **GitHub:** Original files are included in the repository.
- **Source page:** [VA FY2025 Disability Compensation Recipients by County](https://catalog.data.gov/dataset/fy-2025-disability-compensation-recipients-by-county)

## 2. Geographic Distribution of VA Expenditures (GDX)

- **Source:** U.S. Department of Veterans Affairs.
- **Source page:** [VA Geographic Distribution of Expenditures](https://www.va.gov/vetdata/Expenditures.asp)
- **Data:** VA expenditures by geographic area and program.
- **Fiscal years:** FY2023, FY2024, FY2025.
- **Format:** Excel workbooks.
- **Storage:** `data/raw/`
- **GitHub:** Original files are included in the repository.

## 3. VetPop2023 County Data

- **Source:** U.S. Department of Veterans Affairs.
- **Source page:** [VetPop2023 County Data](https://catalog.data.gov/dataset/vetpop2023-county-data-9l)
- **Data:** Projected veteran population by county, including demographic categories.
- **Format:** CSV.
- **Original filename:** `VetPop2023 county data.csv`
- **Size:** Approximately 64 MB.
- **Storage:** University of Illinois Box.

### Box Access and Download Instructions

The VetPop dataset is stored in U of I Box because it exceeds the project's 50 MB GitHub storage threshold.

**Box download link:**

https://uofi.box.com/shared/static/claymwl2hzbzxdkp6yc5q6vaee59hsnp.csv

The dataset is not committed to GitHub. Team members can download it into `data/raw/` by running:

```bash
python scripts/download_vetpop.py
```

The download script automatically:
1. Downloads the dataset from Box.
2. Saves it in `data/raw/`.
3. Calculates its SHA-256 checksum.
4. Compares the checksum with the expected value.
5. Accepts the file only if the checksum matches.

**Expected SHA-256 checksum:**

`b0787e318ca6d5abc648c11068f7c9de3997c44a1e3484010701d6472b4c47ed`

The download process has been tested successfully, and the downloaded file matched the original checksum.

## 4. Data Storage and Reproducibility

The project uses the following folder organization:

- `data/raw/` – Original source datasets.
- `data/cleaned/` – Cleaned datasets.
- `data/processed/` – Processed and integrated datasets.
- `scripts/` – Python scripts for data acquisition, cleaning, and integration.
- `docs/` – Project documentation and data source information.
- `results/` – Analysis outputs and results.

SHA-256 checksums are used to verify data integrity. The large VetPop dataset is stored externally in Box and retrieved using the provided Python download script to keep the GitHub repository within the project's file-size requirements.