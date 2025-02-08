import pandas as pd

def print_columns(year, df):
    print(f"Year: {year}")
    print("[")
    for col in df.columns:
        print(f"\t{col}")
    print("]")

# Define columns to exclude
exclude_columns = [
    'CASE_NUMBER',
    'REFILE',
    'ORIG_FILE_DATE',
    'ORIG_CASE_NO',
    'SCHD_A_SHEEPHERDER',
    'EMPLOYER_ADDRESS_2',
    'EMPLOYER_POSTAL_CODE',
    'EMPLOYER_PHONE',
    'EMPLOYER_PHONE_EXT',
    'PW_TRACK_NUM',
    'PW_SOC_CODE',
    'PW_SOURCE_NAME_9089',
    'PW_SOURCE_NAME_OTHER_9089',
    'PW_DETERM_DATE',
    'PW_EXPIRE_DATE',
    'JOB_INFO_WORK_POSTAL_CODE',
    'JI_OFFERED_TO_SEC_J_FOREIGN_WORKER',
    'JI_FOREIGN_WORKER_LIVE_ON_PREMISES',
    'JI_LIVE_IN_DOMESTIC_SERVICE',
    'JI_LIVE_IN_DOM_SVC_CONTRACT',
    'RI_COLL_TEACH_PRO_JNL',
    'RECR_INFO_SUNDAY_NEWSPAPER',
    'RI_1ST_AD_NEWSPAPER_NAME',
    'RECR_INFO_FIRST_AD_START',
    'RI_2ND_AD_NEWSPAPER_NAME',
    'RI_2ND_AD_NEWSPAPER_OR_JOURNAL',
    'RECR_INFO_SECOND_AD_START',
    'RECR_INFO_JOB_FAIR_FROM',
    'RECR_INFO_JOB_FAIR_TO',
    'RECR_INFO_ON_CAMPUS_RECR_FROM',
    'RECR_INFO_ON_CAMPUS_RECR_TO',
    'RI_EMPLOYER_WEB_POST_FROM',
    'RI_EMPLOYER_WEB_POST_TO',
    'RECR_INFO_PRO_ORG_ADVERT_FROM',
    'RECR_INFO_PRO_ORG_ADVERT_TO',
    'RI_JOB_SEARCH_WEBSITE_FROM',
    'RI_JOB_SEARCH_WEBSITE_TO',
    'RI_PVT_EMPLOYMENT_FIRM_FROM',
    'RI_PVT_EMPLOYMENT_FIRM_TO',
    'RI_EMPLOYEE_REFERRAL_PROG_FROM',
    'RI_EMPLOYEE_REFERRAL_PROG_TO',
    'RI_CAMPUS_PLACEMENT_FROM',
    'RI_CAMPUS_PLACEMENT_TO',
    'RI_LOCAL_ETHNIC_PAPER_FROM',
    'RI_LOCAL_ETHNIC_PAPER_TO',
    'RECR_INFO_RADIO_TV_AD_FROM',
    'RECR_INFO_RADIO_TV_AD_TO',
    'RECR_INFO_EMPLOYER_REC_PAYMENT',
    'REC_INFO_BARG_REP_NOTIFIED',
    'RI_POSTED_NOTICE_AT_WORKSITE',
    'FW_INFO_POSTAL_CODE',
    'FW_INFO_TRAINING_COMP',
    'FW_INFO_REQ_EXPERIENCE',
    'FW_INFO_ALT_EDU_EXPERIENCE',
    'FW_INFO_REL_OCCUP_EXP'
]

dfs = []
for i in range(15, 25):
    dfs.append(pd.read_csv(
        f"PERM_Disclosure_Data_FY{str(i)}.csv",
        encoding='ISO-8859-1',
        usecols=lambda col: col not in exclude_columns
    ))

accepted_columns = {
    'CASE_STATUS': "",
    'DECISION_DATE': "",
    'COUNTRY_OF_CITIZENSHIP': "",
    'FOREIGN_WORKER_INFO_INST': "FOREIGN_WORKER_INST_OF_ED",
    'FOREIGN_WORKER_INFO_MAJOR': "",
    'FW_INFO_BIRTH_COUNTRY': "FOREIGN_WORKER_BIRTH_COUNTRY",
    'FW_INFO_YR_REL_EDU_COMPLETED': "FOREIGN_WORKER_YRS_ED_COMP",
    'NAICS_US_CODE': "NAICS_CODE",
}

# Process each dataframe
for i in range(len(dfs)):
    rename_dict = {}

    # Build a rename mapping for each DataFrame
    for standard_col, alt_col in accepted_columns.items():
        if standard_col in dfs[i].columns:
            rename_dict[standard_col] = standard_col  # Keep standard name
        elif alt_col and alt_col in dfs[i].columns:
            rename_dict[alt_col] = standard_col  # Rename alternative column

    dfs[i] = dfs[i].rename(columns=rename_dict)  # Rename first
    dfs[i] = dfs[i][list(accepted_columns.keys())]  # Select only renamed columns

    # Filter out rows where 'CASE_STATUS' is invalid or 'Withdrawn'
    dfs[i] = dfs[i][dfs[i]['CASE_STATUS'].notna() & (dfs[i]['CASE_STATUS'] != 'Withdrawn')]

    # Modify 'CASE_STATUS' values
    dfs[i].loc[dfs[i]['CASE_STATUS'].isin(['Certified', 'Certified-Expired']), 'CASE_STATUS'] = 'Y'
    dfs[i].loc[dfs[i]['CASE_STATUS'] == 'Denied', 'CASE_STATUS'] = 'N'

# Concatenate all DataFrames on the final selected columns
merged_df = pd.concat(dfs, ignore_index=True)

# Extract year from DECISION_DATE and FW_INFO_YR_REL_EDU_COMPLETED
merged_df = merged_df.assign(
    DECISION_DATE=merged_df['DECISION_DATE'].astype(str).str.split().str[0]
)
merged_df = merged_df.assign(
    DECISION_YEAR=pd.to_datetime(merged_df['DECISION_DATE'], format='%m/%d/%Y', errors='coerce').dt.year
)
merged_df = merged_df.assign(
    FW_EDU_YEAR=pd.to_numeric(merged_df['FW_INFO_YR_REL_EDU_COMPLETED'], errors='coerce').astype('Int64')
)
merged_df = merged_df.assign(
    YEAR_DIFF=merged_df['DECISION_YEAR'] - merged_df['FW_EDU_YEAR']
)

# Count rows with valid YEAR_DIFF and calculate the mean
valid_year_diff_rows = merged_df['YEAR_DIFF'].dropna()
mean_year_diff = valid_year_diff_rows.mean()

print(f"Number of rows with valid YEAR_DIFF: {len(valid_year_diff_rows)}")
print(f"Mean of YEAR_DIFF: {(mean_year_diff):.2f}")
print(merged_df.head())

merged_df.to_csv("merged.csv", index=True)
