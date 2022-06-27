print("*************************************************")

#_______________________________________________________________________________________________________________#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kde

#Read csv as pandas dataframe
ss13hil_df = pd.read_csv('ss13hil.csv')
# make 2 by 2 subplots having size 16 and 12
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (16,12))
fig.suptitle('Sample Output',fontsize=16, fontweight="bold")

#For making the pie chart below data is extracted from the dataframe
HHL_df= ss13hil_df[['HHL']]
HHL_count = (HHL_df.value_counts()).to_numpy()
HHL_names = ['English only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other language']
# print('\n')
# Plot the Pie chart
Col, texts = ax1.pie(HHL_count, startangle=-120.5)
ax1.legend(Col, HHL_names, loc='upper left', bbox_to_anchor=(-0.23,1), frameon=True)
ax1.set_title('Household Languages',fontweight="bold")
ax1.set_ylabel('HHL',fontweight="bold")

#For plotting the bar graph follwoing is the process
vehicle_df = ss13hil_df['VEH']
vehicle_df = vehicle_df.dropna()
vehicle_count = (ss13hil_df.groupby('VEH')['WGTP'].sum()).to_numpy()
y_axis = vehicle_count/1000
x_axis = [i for i,x in enumerate(y_axis)]
# Plotting bar graph
ax3.bar(x_axis, y_axis, color='red')
ax3.set_title('Vehicles Available in Households',fontweight="bold")
ax3.set_ylabel('Thousands of Households',fontweight="bold")
ax3.set_xlabel('# of Vehicles',fontweight="bold")


# For making the histogram below procedure is adopt
HINCP_df = ss13hil_df['HINCP']
HINCP_df = pd.DataFrame(HINCP_df)
HINCP_df = HINCP_df.assign(HINCP = HINCP_df['HINCP'].fillna(1))
HINCP_df['HINCP'][HINCP_df['HINCP']<=1] = 1
HINCP_values = HINCP_df['HINCP'].values
Histbin = np.logspace(1,7,num=100)
ax2.hist(HINCP_values, bins=Histbin, facecolor='g', density='True', alpha=0.5, histtype='bar', range=(0, len(HINCP_values)))
ax2.set_xscale('log')
ax2.ticklabel_format(style='plain', axis='y')
density=kde.gaussian_kde(ss13hil_df['HINCP'].dropna())
ax2.plot(Histbin, density(Histbin), color='k', ls='dashed')
ax2.set_title('Distribution of Household Income',fontweight="bold")
ax2.set_ylabel('Density',fontweight="bold")
ax2.set_xlabel('Household Income($)- Log Scaled',fontweight="bold")


# Last graph is the scatter plot following data is for scatter plot
ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(1, 0)
ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(2, 1)
for i in range(3,23):
    ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(i, (i-2)*50)
for i in range(23,63):
    ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(i, (i-12)*100)
ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(63, 5500)
for i in range(64,69):
    ss13hil_df['TAXP'] = ss13hil_df['TAXP'].replace(i, (i-58)*1000)
scatter_Plot = ax4.scatter(ss13hil_df['VALP'], ss13hil_df['TAXP'], marker='o', s=ss13hil_df['WGTP']/2, c=ss13hil_df['MRGP'], cmap='bwr', alpha=0.5)
Bar_line=plt.colorbar(scatter_Plot)
Bar_line.set_label('First Mortgage Payment (Monthly $)', fontweight="bold")
ax4.set_xlim(0, 1200000)
ax4.ticklabel_format(style='plain')
ax4.set_title('Property Taxes vs Property Values', fontweight="bold")
ax4.set_ylabel('Taxes($)', fontweight="bold")
ax4.set_xlabel('Property Value($)', fontweight="bold")

# Save all sub-Plots as Png Picture

fig.savefig('pums.png')
