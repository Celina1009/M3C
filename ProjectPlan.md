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


Constraints:
•	Data Availability: Some datasets may have missing values or information that is not available for every county. We will identify these issues and handle missing data carefully.
•	Data Consistency: The datasets may use different column names, formats, or geographic identifiers. We will standardize the data before combining it.
•	Data Integration: We need to make sure the datasets refer to the same counties and compatible fiscal years. We will check that county identifiers match before integrating the data.
•	Expenditure Comparisons: VA expenditure data may include multiple programs, and reporting methods may differ between years. These differences could affect comparisons with recipient counts.
•	Population Estimates: VetPop2023 includes projected population figures for years after FY2023. We will use FY2023 as our baseline when comparing recipient counts with veteran population.
•	Reproducibility: The datasets may require different steps to download and prepare. We will document our process and use scripts and file integrity checks to help ensure that the workflow can be repeated since data reproducibility is very crucial. 

How the datasets relate: All three are linked by the 5-digit county FIPS code and fiscal year. The recipient files and VetPop2023 include FIPS codes. GDX lists only state and county names, so we will build a crosswalk from the recipient files, which contain both names and FIPS codes, to attach FIPS codes to GDX.


Timeline and Team members 
The following timeline outlines the tasks required to investigate county-level changes in VA disability compensation recipients and expenditures from FY2023 through FY2025. Week 1 refers to the first week after submitting the project plan. Responsibilities are listed by proposed role and will be assigned to individual team members. 

Each line of the timeline will be structured by task, description, target completion, and responsible member.

Define the data lifecycle	Relate the project to a lifecycle model discussed in class, explaining how acquisition, quality assessment, cleaning, integration, analysis, documentation, and preservation connect.	Week 1	Documentation lead

Establish data organization and storage	Document the CSV and Excel formats and relevant data types. Establish folders for raw data, cleaned data, scripts, documentation, and results, with consistent naming conventions. Check file sizes and arrange Box storage and retrieval for files exceeding the assignment’s 50 MB threshold.	Week 1	Data lead

Determine copyright, licensing, and ethical requirements	Verify reuse and redistribution terms for all three sources, particularly GDX. Document required citations and establish how suppressed recipient counts will be handled without compromising privacy.	Week 1	Documentation lead

Acquire datasets and verify integrity	Write scripts to retrieve the recipient, GDX, and VetPop2023 datasets from official VA sources. Preserve original files, record source URLs and retrieval dates, verify integrity using SHA-256 checksums, and confirm each dataset meets the minimum record requirement.	Week 2	Data lead

Assess quality before integration	Evaluate accuracy, completeness, timeliness, and consistency for each dataset. Examine missing and suppressed values, duplicates, geographic coverage, fiscal-year alignment, and expenditure definitions. Document whether the proposed county-and-year linkage is feasible.	Week 2	Data lead and integration lead

Clean and harmonize datasets	Use reproducible scripts to address identified quality issues. Standardize column names, data types, five-digit FIPS codes, and expenditure units; flag suppressed values rather than treating them as zero. Prepare county-level veteran population totals without double-counting demographic groups. Determine whether FY2023 expenditures require separate analysis.	Week 3	Data lead

Build and validate the geographic crosswalk	Use state and county names from the recipient files to assign FIPS codes to GDX records. Resolve spelling differences, independent cities, and geographic boundary changes. Document ambiguous or unmatched records and decisions about their treatment.	Week 3	Integration lead

Integrate the cleaned datasets	Join the three sources using validated county FIPS codes and compatible fiscal years. Document join types and expected relationships between records. Preserve FY2023 veteran population as the baseline where appropriate.	Week 4	Integration lead

Assess quality after integration	Reassess accuracy, completeness, timeliness, and consistency. Check unmatched counties, duplicate county-year records, unexpected row losses, and changes in totals. Correct identified problems and document evidence that the integration succeeded.	Week 4	Integration lead and analysis lead

Analyze and visualize results	Calculate county-level changes in recipient counts and comparable expenditures. Use veteran population to contextualize results and create at least one visualization. Explain limitations arising from suppression, projected populations, and differences in expenditure coverage.	Week 5	Analysis lead

Automate the workflow and record provenance	Connect separate, single-purpose scripts with Snakemake or a run-all script, covering acquisition through analysis. Record each stage’s inputs, outputs, and transformations so results can be traced to their sources.	Develop throughout; complete Week 5	Integration lead

Create metadata and documentation	Develop a data dictionary describing variables, units, missing-value codes, and derived measures. Produce machine-readable metadata using a standard such as Schema.org, DataCite, or DCAT, and document sources, licenses, and processing decisions.	Begin Week 2; finalize Week 5	Documentation lead

Verify reproducibility	Declare software dependencies and package versions, use relative paths, and provide exact execution instructions. Test the complete workflow from a fresh repository clone and resolve errors or undocumented manual steps.	Week 6, before final submission	All members

Complete reports and releases	Submit the interim status report with task updates, challenges, revised plans, and individual contributions. Complete the final README with all required sections and links to artifacts, review the submission checklist, and create the required GitHub releases. Each member will commit their own contributions.	Interim report: Canvas deadline; final report: Week 6, by Canvas deadline	All members

