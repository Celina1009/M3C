# Milestone 3: Interim Status Report

**Project:** VA Disability Compensation Recipients and Expenditures by County

**Team:** M3C

**Date:** November 19, 2026

## 1. Project Overview

Our project looks at how VA disability compensation recipients and expenditures changed across U.S. counties from FY2023 to FY2025.

Our main research question is:

**How did VA disability compensation recipient counts and expenditures change across U.S. counties from FY2023 to FY2025?**

We are using three datasets: VA Disability Compensation Recipients by County, Geographic Distribution of VA Expenditures (GDX), and VetPop2023 County Data. Our goal is to clean and combine these datasets using county FIPS codes so we can analyze changes across counties and years.

So far, we have completed data collection, most of the cleaning and preparation, and the integration of the three datasets. We are now moving toward the analysis and visualization stage.

## 2. Progress on Project Tasks

The table below summarizes the progress made on the tasks from our original project plan.

| Task                                    | Status                    | Progress                                                                                                                                                      |
| --------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Define the data lifecycle               | [Update needed]           | [Documentation Lead to add progress.]                                                                                                                         |
| Establish data organization and storage | Complete                  | Created folders for raw data, cleaned data, processed data, scripts, and documentation. The large VetPop file is stored in Box.                               |
| Copyright, licensing, and ethics        | [Update needed]           | [Documentation Lead to add progress.]                                                                                                                         |
| Acquire datasets and verify integrity   | Complete                  | Downloaded the VA datasets, preserved the raw files, and verified file integrity using SHA-256 checksums.                                                     |
| Assess data quality before integration  | Complete                  | Checked missing values, duplicates, geographic coverage, and consistency across datasets.                                                                     |
| Clean and harmonize datasets            | Complete                  | Prepared the recipient, GDX, and VetPop datasets for integration. Standardized FIPS codes and aggregated VetPop demographic records into county-level totals. |
| Build geographic crosswalk              | Complete                  | Matched GDX county names to FIPS codes using recipient data and resolved naming differences where possible.                                                   |
| Integrate datasets                      | Complete                  | Combined the recipient, GDX, and VetPop datasets into three county-level datasets for FY2023, FY2024, and FY2025.                                             |
| Assess quality after integration        | Complete                  | Checked duplicate FIPS codes, missing values, row counts, and unmatched counties.                                                                             |
| Analyze and visualize results           | Not started / In progress | The integrated datasets are ready for the Analysis Lead to begin EDA and create visualizations.                                                               |
| Automate workflow and record provenance | In progress               | Created separate scripts for GDX preparation, VetPop preparation, and dataset integration. Full workflow automation is still needed.                          |
| Create metadata and documentation       | In progress               | Data source documentation is available. A complete data dictionary and metadata still need to be created.                                                     |
| Verify reproducibility                  | Pending                   | Dependencies are recorded in `requirements.txt`. The complete workflow still needs to be tested from a fresh repository clone.                                |
| Complete reports and releases           | In progress               | Preparing this interim report. Final documentation and the required GitHub release will be completed later.                                                   |

### Important Repository Files

The main project files are available in our [GitHub repository](https://github.com/Celina1009/M3C).

**Integrated datasets:**

- `data/processed/integrated/Integrated_FY2023.csv`
- `data/processed/integrated/Integrated_FY2024.csv`
- `data/processed/integrated/Integrated_FY2025.csv`

**QA reports:**

- `data/processed/integrated/Integration_QA_Summary.csv`
- `data/processed/integrated/Integration_Unmatched_Geographies.csv`

**Preparation and integration scripts:**

- `scripts/prepare_gdx_integration.py`
- `scripts/prepare_vetpop.py`
- `scripts/integrate_datasets.py`

## 3. Updated Timeline

The following table shows our updated timeline based on our progress so far.

| Task                                | Status                 | Expected completion     |
| ----------------------------------- | ---------------------- | ----------------------- |
| Project setup and data organization | Complete               | Completed               |
| Dataset acquisition                 | Complete               | Completed               |
| Data cleaning and quality checks    | Complete               | Completed               |
| Geographic crosswalk                | Complete               | Completed               |
| Dataset integration and validation  | Complete               | Completed               |
| EDA and visualizations              | Upcoming / In progress | [Add date]              |
| Workflow automation                 | In progress            | [Add date]              |
| Data dictionary and documentation   | In progress            | [Add date]              |
| Reproducibility testing             | Pending                | Before final submission |
| Final report and presentation       | Pending                | Week 6                  |

## 4. Changes to the Project Plan

Our main research question and datasets have not changed. However, we made a few adjustments after examining the actual data.

One change was using FY2023 VetPop data as a baseline for veteran population instead of treating it as updated population data for all three years.

We also found that Connecticut uses different geographic identifiers across the datasets. The FY2023 recipient data uses historical counties, while FY2024 and FY2025 use planning regions. Since these areas do not match directly, we decided not to force a crosswalk.

Puerto Rico was also excluded from our prepared county-level GDX and VetPop datasets because of differences in geographic coverage.

Finally, we identified a change in GDX reporting methodology between FY2023 and FY2024. We will account for this when comparing expenditures across years.

## 5. Challenges and Problems

We encountered a few challenges while preparing and integrating the datasets.

- **Large VetPop file:** The original file exceeded GitHub's 50 MB limit, so we stored it in Box and created a script to retrieve it.
- **Different FIPS formats:** Some datasets did not preserve leading zeros in FIPS codes. We standardized them to five digits before joining.
- **VetPop aggregation:** VetPop contained separate records for four age groups and two sexes. We combined these into one veteran population total per county. We also fixed an issue with commas in population values that affected numeric conversion.
- **Connecticut geography:** The different county and planning-region definitions prevented some records from matching. We kept these records unmatched rather than making inaccurate geographic matches.
- **Puerto Rico:** Puerto Rico appeared in the recipient data but was not included in the prepared county-level GDX and VetPop datasets.
- **GDX methodology:** The reporting method changed between FY2023 and FY2024, which may affect expenditure comparisons.

After integration, our QA checks showed that all three datasets had unique FIPS codes and no missing recipient counts. The remaining missing expenditure and population values correspond to the geographic mismatches described above.

## 6. Individual Team Contributions

### Monika Saravanakumar – Integration Lead

Monika worked on the geographic crosswalk and integration of the three datasets. She prepared the GDX datasets for all three years, aggregated the FY2023 VetPop data into county-level population totals, and validated the recipient datasets. She also created the integration scripts, generated the final FY2023–FY2025 integrated datasets, and performed post-integration quality checks. She documented unmatched geographic records and pushed the completed scripts, datasets, and QA reports to GitHub.

### Celina Saeki – Data Lead

[Celina: Add a short summary of your contributions to data acquisition, cleaning, standardization, and quality checks. Please commit your own contribution.]

### Millie Chu – Analysis Lead

[Millie: Add a short summary of your contributions to data analysis, EDA, statistical comparisons, and visualizations. Please commit your own contribution.]

### Manasa Thangappan – Documentation Lead

[Manasa: Add a short summary of your contributions to the data lifecycle, licensing research, citations, metadata, and documentation. Please commit your own contribution.]

## 7. Next Steps

Our main focus now is to begin analyzing the integrated datasets. We plan to examine changes in recipient counts and Compensation & Pension expenditures across counties, identify geographic patterns, and create visualizations to answer our research question.

We also need to finish the data dictionary, document the complete workflow, test reproducibility, and prepare the final report and presentation.

