Overview:
This project investigates geographic and temporal changes in Department of Veterans Affairs (VA) disability compensation recipients and expenditures across U.S. counties from Fiscal Year 2023 through Fiscal Year 2025. By examining recipient counts, VA expenditures, and estimated veteran population, we aim to understand how disability compensation distribution changes across counties.
To execute the project, we will build an automated data curation pipeline that retrieves, cleans, validates, and integrates these datasets using compatible geographic identifiers, such as county FIPS codes.
Our workflow follows five stages:
1.	Acquisition and Integrity: Download raw files from data.va.gov and va.gov and verify them with SHA-256 checksums.
2.	Quality Profiling: Assess accuracy, completeness, timeliness, and consistency.
3.	Cleaning and Harmonization: Standardize formats, units, and county identifiers across datasets and years, and handle missing values.
4.	Integration: Join the cleaned datasets on county FIPS code and fiscal year.
5.	Analysis: Measure county-level changes in recipients and expenditures, and visualize the results.
We will document data limitations, including differences in expenditure reporting methods and the use of projected veteran population figures, to support reproducible analysis.


Research Questions:
How did VA disability compensation recipient counts and expenditures change across U.S. counties from FY2023 to FY2025?

Datasets:
Dataset	Source & format	What it provides	Key fields	How we will use it
VA Disability Compensation Recipients by County (FY2023, FY2024, FY2025)	VA NCVAS; CSV; CC0	Number of veterans receiving disability compensation in each county at the end of each fiscal year 	FIPS code, county name, total recipients	Track changes in recipient counts over time
Geographic Distribution of VA Expenditures (GDX) (FY2023–FY2025)	VA NCVAS; Excel	VA spending by county and program, including Compensation & Pension 	State, county name, C&P expenditures	Compare spending patterns with changes in recipient counts
VetPop2023 County Data
VA NCVAS; CSV; CC0	Estimated and projected veteran population by county, age group, and sex	FIPS, date, veterans	Provide population context for recipient counts

How the datasets relate: All three are linked by the 5-digit county FIPS code and fiscal year. The recipient files and VetPop2023 include FIPS codes. GDX lists only state and county names, so we will build a crosswalk from the recipient files, which contain both names and FIPS codes, to attach FIPS codes to GDX.




