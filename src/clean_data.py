import pandas as pd
import numpy as np
import zipfile

df = pd.read_csv('data/publicJuly2020.csv')
df.set_index('caseid2019', inplace=True)

# recoding values
yn_col = ['xd1i', 'CV4_a', 'CV4_b', 'CV4_c', 'CV4_d', 'CV4_e',
          'CV12', 'CV12A', 'CV13A', 'CV14', 'CV15']
for col in yn_col:
    df[col] = df[col].map({'Yes': 1, 'No': 0, 'Refused': -1})

df['ppincimp'] = df['ppincimp'].map({'Less than $5,000': 0,
                                     '$5,000 to $7,499': 1,
                                     '$7,500 to $9,999': 2,
                                     '$10,000 to $12,499': 3,
                                     '$12,500 to $14,999': 4,
                                     '$15,000 to $19,999': 5,
                                     '$20,000 to $24,999': 6,
                                     '$25,000 to $29,999': 7,
                                     '$30,000 to $34,999': 8,
                                     '$35,000 to $39,999': 9,
                                     '$40,000 to $49,999': 10,
                                     '$50,000 to $59,999': 11,
                                     '$60,000 to $74,999': 12,
                                     '$75,000 to $84,999': 13,
                                     '$85,000 to $99,999': 14,
                                     '$100,000 to $124,999': 15,
                                     '$125,000 to $149,999': 16,
                                     '$150,000 to $174,999': 17,
                                     '$175,000 to $199,999': 18,
                                     '$200,000 to $249,999': 19,
                                     '$250,000 or more': 20})

df['Applied SNAP but not received'] = df['CV16_b'].map({'Received': 0, 
                                                        'Applied for but not received': 1,
                                                        'Did not apply for and did not receive': 0})

df['CV16_b'] = df['CV16_b'].map({'Received': 1, 
                                 'Applied for but not received': 1,
                                 'Did not apply for and did not receive': 0})

                  
df['CV1'] = df['CV1'].map({'Employed': 'Employed',
                           'Not employed and not looking for a job': 'Not Employed',
                           'Not working, but being paid my normal wages': 'Not Employed',
                           'Not employed, but looking for a job': 'Unemployed',
                           'Self-employed': 'Employed',
                           'CV1_Temporarily laid off or furloughed': 'Unemployed'
                          })
df['ppgender'] = df['ppgender'].map({'Female': 0, 'Male': 1})
df['ppmsacat'] = df['ppmsacat'].map({'Metro': 1, 'Non-Metro': 0})

columns = df.columns
cv = []
for col in columns:
    if ("CV" in col) or ("EF" in col):
        cv.append(col)
cv.remove('CV16_b')
cv.remove('CV1')
drop_these = ['Duration', 'weight', 'weight_pop', 'DeviceType2', 'PPREG4', 'pphhhead', 'B2', 'ppeducat', 'ppwork', 'ppagecat', 'ppagect4', 'xgh1']
drop_these += cv
for col in drop_these:
    df.pop(col)


df = pd.get_dummies(df)
df.dropna(inplace=True)

columns = df.columns
new_col_names = ['Retired',
                 'Applied for SNAP',
                 'Age',
                 'Male',
                 'Household Size',
                 'Household Income',
                 'Metro',
                 'Household Members (age 0-1)',
                 'Household Members (age 13-17)',
                 'Household Members (age 18+)',
                 'Household Members (age 2-5)',
                 'Household Members (age 6-12)',
                 'Applied SNAP but not received',
                 'Employed',
                 'Not Employed',
                 'Unemployed',
                 'Did not borrow from retirement',
                 'Refused to answer (borrow from retirement)',
                 'Borrowed money from retirement',
                 'Borrowed and cashed out from retirement',
                 'Cashed out from retirement',
                 'Highest Degree (10th grade)',
                 'Highest Degree (11th grade)',
                 'Highest Degree (12th grade)',
                 'Highest Degree (4th grade)',
                 'Highest Degree (6th grade)',
                 'Highest Degree (8th grade)',
                 'Highest Degree (9th grade)',
                 'Highest Degree (Associate degree)',
                 'Highest Degree (Bachelors degree)',
                 'Highest Degree (High School/GED)',
                 'Highest Degree (Masters degree)',
                 'Highest Degree (none)',
                 'Highest Degree (Professional/PhD)',
                 'Highest Degree (Some college no degree)',
                 'Race: 2+',
                 'Race: Black, Non-Hispanic',
                 'Race: Hispanic',
                 'Race: Other, Non-Hispanic',
                 'Race: White, Non-Hispanic',
                 'Housing Type (Apartment)',
                 'Housing Type (Mobile home)',
                 'Housing Type (One-family house attached)',
                 'Housing Type (One-family house detached)',
                 'Housing Type (Boat, RV, van)',
                 'Divorced',
                 'Living with partner',
                 'Married',
                 'Never married',
                 'Separated',
                 'Widowed',
                 'East-North Central',
                 'East-South Central',
                 'Mid-Atlantic',
                 'Mountain',
                 'New England',
                 'Pacific',
                 'South Atlantic',
                 'West-North Central',
                 'West-South Central',
                 'Ownership Status of Living Quarters (Occupied without payment)',
                 'Ownership Status of Living Quarters (Owned)',
                 'Ownership Status of Living Quarters (Rent)',   
                ]
states = []
for col in columns:
    if 'ppstaten' in col:
        state = col.replace('ppstaten_','').upper()
        states.append(state)
        
new_col_names += states

df.columns = new_col_names

df.to_csv('data/food_insecurity.csv')