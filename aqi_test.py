import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('AQI and Lat Long of Countries.csv')
df.info()
print(df)
print("We look for duplicate rows.  The shape of the dataframe of duplicate elements is:")
print(df[df.duplicated()].shape)
print("There are no duplicate rows.")
# What do the empty country rows look like?
print(df[df.Country.isna()])
# We will try to do this another way as well, which would catch missing entries in other columns as well (if there were any)
print("Does this work?")
print(df[df.isna().any(axis=1)])
# For fun, let's find all those rows where the entries in one column (PM2.5 value) are the same as in another (AQI value)
print(df[df['PM2.5 AQI Value']==df['AQI Value']])

# We can also group entries by country and consider all the entries for a single nation. 
grouped_df =df.groupby('Country')
print(grouped_df.get_group('Slovakia'))
# The following would be helpful if we want to see each country seperately.
"""
for key, item in grouped_df:
    print(grouped_df.get_group(key), "\n\n")
"""
# Let us look at those entries with unhealthy AQI values.
print(df[df['AQI Value']>100])

# Let's make a dataframe containing the average AQI by country.
# Note that we also sort the countries alphabetically here.
nationalaqi_df = pd.DataFrame(df['Country'].sort_values().unique())
print(nationalaqi_df)
# Let's drop the NaN entry (there were cities whose countries were not listed).
nationalaqi_df.dropna(inplace=True)
print(nationalaqi_df)
# Let's label the column correctly.
nationalaqi_df.rename(columns={0: "Country"}, inplace=True)
print(nationalaqi_df)
# We would like the average value for each country.
print(grouped_df.get_group('Slovakia'))
print("The average AQI value for Slovakia is",grouped_df.get_group('Slovakia')['AQI Value'].mean())

# We will add a column to our country-based dataframe nationalaqi_df which tracks the average AQI value.
nationalaqi_df['AQI Value'] = [grouped_df.get_group(key)['AQI Value'].mean().round(0).astype(int) for key in nationalaqi_df['Country']]
print(nationalaqi_df)
# Testing to see that nothing went terribly wrong.
print(df[df['AQI Value']<0])
# Then we categorize (according to airnow.gov) by binning these average AQI Values.
print(df.sort_values('AQI Value'))

nationalaqi_df['AQI Category'] = pd.cut(x=nationalaqi_df['AQI Value'], 
                             bins=[0,50,100,150,200,300,600], 
                             labels=['Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'],
                             ordered=True,
                             right=True,
                             include_lowest=True)
                             

# We can take a peek to see whether this worked
print(nationalaqi_df)
print(df.columns)
# Now we repeat for different values.

# For CO: ######################################################
nationalaqi_df['CO AQI Value'] = [grouped_df.get_group(key)['CO AQI Value'].mean().round(0).astype(int) for key in nationalaqi_df['Country']]
# Then we categorize by binning these.
print(df.sort_values('CO AQI Value'))

nationalaqi_df['CO AQI Category'] = pd.cut(x=nationalaqi_df['CO AQI Value'], 
                             bins=[0,50,100,150,200,300,600], 
                             labels=['Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'],
                             ordered=True,
                             right=True,
                             include_lowest=True)

# For Ozone #####################################################
nationalaqi_df['Ozone AQI Value'] = [grouped_df.get_group(key)['Ozone AQI Value'].mean().round(0).astype(int) for key in nationalaqi_df['Country']]
# Then we categorize by binning these.
print(df.sort_values('Ozone AQI Value'))

nationalaqi_df['Ozone AQI Category'] = pd.cut(x=nationalaqi_df['Ozone AQI Value'], 
                             bins=[0,50,100,150,200,300,600], 
                             labels=['Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'],
                             ordered=True,
                             right=True,
                             include_lowest=True)

# For NO2 ############################################################
nationalaqi_df['NO2 AQI Value'] = [grouped_df.get_group(key)['NO2 AQI Value'].mean().round(0).astype(int) for key in nationalaqi_df['Country']]
# Then we categorize by binning these.
print(df.sort_values('NO2 AQI Value'))

nationalaqi_df['NO2 AQI Category'] = pd.cut(x=nationalaqi_df['NO2 AQI Value'], 
                             bins=[0,50,100,150,200,300,600], 
                             labels=['Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'],
                             ordered=True,
                             right=True,
                             include_lowest=True)

# For PM2.5 ############################################################
nationalaqi_df['PM2.5 AQI Value'] = [grouped_df.get_group(key)['PM2.5 AQI Value'].mean().round(0).astype(int) for key in nationalaqi_df['Country']]
# Then we categorize by binning these.
print(df.sort_values('PM2.5 AQI Value'))

nationalaqi_df['PM2.5 AQI Category'] = pd.cut(x=nationalaqi_df['PM2.5 AQI Value'], 
                             bins=[0,50,100,150,200,300,600], 
                             labels=['Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'],
                             ordered=True,
                             right=True,
                             include_lowest=True)

nationalaqi_df.info()
print(nationalaqi_df[['Country','AQI Value','AQI Category']])
print(nationalaqi_df[['Country','CO AQI Value','CO AQI Category']])
print(nationalaqi_df[['Country','Ozone AQI Value','Ozone AQI Category']])
print(nationalaqi_df[['Country','NO2 AQI Value','NO2 AQI Category']])
print(nationalaqi_df[['Country','PM2.5 AQI Value','PM2.5 AQI Category']])


print(nationalaqi_df.corr(numeric_only=True))


print(df[['Country','NO2 AQI Value','NO2 AQI Category']].sort_values('NO2 AQI Value'))
print(nationalaqi_df)


# Let's compare how countries rank!
# First we add the country and value columns.
country_rank = pd.DataFrame(nationalaqi_df[['Country', 'AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value']])
# Note we omit PM2.5 since it behaves very similarly to the AQI value.
print(country_rank)


country_rank.sort_values('AQI Value', inplace=True)
country_rank['AQI Rank']= country_rank.reset_index().index+1
print(country_rank)
# This worked, so let's do it three more times and then select only those columns.

country_rank.sort_values('CO AQI Value', inplace=True)
country_rank['CO AQI Rank']= country_rank.reset_index().index+1

country_rank.sort_values('Ozone AQI Value', inplace=True)
country_rank['Ozone AQI Rank']= country_rank.reset_index().index+1

country_rank.sort_values('NO2 AQI Value', inplace=True)
country_rank['NO2 AQI Rank']= country_rank.reset_index().index+1


country_rank.sort_values('Country', inplace=True)
country_rank=country_rank.iloc[:,[0,5,6,7,8]]
print(country_rank)
print("Testing!")
print(country_rank.iloc[:,1:])
country_rank['Average Rank'] = country_rank.iloc[:,1:].mean(axis=1)
print(country_rank)
# Let's also add a count for the number of tests per country.
country_rank['Test count'] = [df['Country'].value_counts()[country]  for country in country_rank['Country']]
print(country_rank.sort_values('Average Rank'))

# Let's check that value count stuff.
print(df['Country'].value_counts())
df['Country'].value_counts().head(20).plot(kind='bar')
plt.tight_layout()
plt.show()
# This came out strange because of the presence of the especially long: 'United Kingdom of Great Britain and Northern Ireland'
# Let's just clean this up.
most_counts=df['Country'].value_counts().head(30)
print(most_counts)
most_counts=most_counts.rename({'United States of America': 'USA', 
                                'United Kingdom of Great Britain and Northern Ireland':'UK',
                                'Russian Federation':'Russia'})
print(most_counts)
most_counts.plot(kind='bar')
plt.title("Nations with the most tests")
plt.ylabel('Total tests')
plt.tight_layout()
plt.show()
print("What are the Australian locations?")
print(df[df['Country']=='Australia'])

# If we want to only use countries with a decent number of tests, we could do the following.
country_rank= country_rank[country_rank['Test count']>9]
country_rank.info()

country_rank.sort_values('AQI Rank', inplace=True)
print(country_rank)
country_rank['AQI Rank']= country_rank.reset_index().index+1
print(country_rank)

country_rank.sort_values('CO AQI Rank', inplace=True)
country_rank['CO AQI Rank']= country_rank.reset_index().index+1

country_rank.sort_values('Ozone AQI Rank', inplace=True)
country_rank['Ozone AQI Rank']= country_rank.reset_index().index+1

country_rank.sort_values('NO2 AQI Rank', inplace=True)
country_rank['NO2 AQI Rank']= country_rank.reset_index().index+1

country_rank['Average Rank'] = country_rank.iloc[:,1:4].mean(axis=1)

country_rank.sort_values('Country', inplace=True)
print(country_rank.sort_values('Average Rank'))