import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

df = pd.read_csv('data/publicJuly2020.csv')
df.set_index('caseid2019', inplace=True)

df['Applied SNAP'] = df['CV16_b'].map({'Received': 1, 
                                       'Applied for but not received': 1,
                                       'Did not apply for and did not receive': 0})
                                
print(f"Proportion of sample that are food insecure: {df['Applied SNAP'].mean()}")

snap = df[df['Applied SNAP']==1]
nosnap = df[df['Applied SNAP']==0]

income_cat = {'Less than $5,000': 0,
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
              '$250,000 or more': 20}

inc_cat_prop_snap = {}
inc_cat_prop_nosnap = {}
for i in list(income_cat.keys()):
    inc_cat_prop_snap[i] = len(snap[snap['ppincimp'] == i])/len(snap)
    inc_cat_prop_nosnap[i] = len(nosnap[nosnap['ppincimp'] == i])/len(nosnap)

N = len(num_nosnap_cat)
snap_prop = list(num_snap_cat.values())
nosnap_prop = list(num_nosnap_cat.values())

ind = np.arange(N) 
width = 0.35       
plt.barh(ind, snap_prop, width, label='Food Insecure')
plt.barh(ind + width, nosnap_prop, width,
    label='Not Food Insecure')

plt.xlabel('Proportion')
plt.title('Proportion of Group in Income Category')

plt.yticks(ind + width / 2, list(num_snap_cat.keys()))
plt.legend(loc='best')
plt.show()
plt.savefig('images/prop_incomecat.png', bbox_inches = "tight")