import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap 

# We will plot AQI values on a world map.
####################################################

# First we read the CSV.
df=pd.read_csv('AQI and Lat Long of Countries.csv')
df.info()
# Although a number of countries aren't given, that won't interefere with our plotting, since we plot using 
# latitude and longitude.

# We look for duplicate rows.
print("The length of the dataframe of duplicate elements is {}".format(df[df.duplicated()].shape[0]))
# From this result we know there are no duplicate rows.

print("The minimum and maximum AQI values are {} and {}, respectively.".format(
    df['AQI Value'].min(), df['AQI Value'].max()))

# We will plot a world map with AQI values included by latitude and longitude.
norm = plt.Normalize(df['AQI Value'].min(), df['AQI Value'].max())
# We create a colormap which matches AQI values to the categories and colors defined here:
# https://www.airnow.gov/aqi/aqi-basics/
######################################################################################################
colormap = LinearSegmentedColormap.from_list('custom',
                                             [(0,'green'),
                                              (norm(25), 'green'),
                                              (norm(75), 'yellow'),
                                              (norm(125), 'orange'),
                                              (norm(175), 'red'),
                                              (norm(225), 'purple'),
                                              (norm(275), 'purple'),
                                              (norm(325), 'maroon'),
                                              (1, 'maroon')],
                                              N=(326))
# The following scalar mappable is needed to create a color bar.
sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)

# We use geopandas to read information on a global map (contained in the folder global_geodata)
countries = gpd.read_file(r'global_geodata\ne_110m_admin_0_countries.shp')


########################################################################
# We can now plot the map, and then the AQI values using a scatterplot.
# This sets the size of the plot.
plt.figure(figsize=(16,6))

# This plots the map in the background in grey.
countries.plot(color='lightgrey',ax=plt.gca())

# This plots the AQI values.
sns.scatterplot(data=df, x='lng', y='lat', hue='AQI Value', palette=colormap)


cbar = plt.gca().figure.colorbar(sm, ax=plt.gca(),ticks=[25,75,125,175,250,350])
cbar.ax.set_yticklabels(['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Air Quality Index Levels')
plt.gca().get_legend().remove()
# This lets me set the name of the window!
plt.get_current_fig_manager().set_window_title('AQI with Seaborn')
plt.show(block=False)
###########################################################################################

# Let's see if we can make the colorbar slightly nicer.
plt.figure(figsize=(16,6))
countries.plot(color='lightgrey',ax=plt.gca())
sns.scatterplot(data=df, x='lng', y='lat', hue='AQI Value', palette=colormap)

cmap2 = LinearSegmentedColormap.from_list('custom',
                                             [(0,'green'),
                                              (.2, 'yellow'),
                                              (.4, 'orange'),
                                              (.6, 'red'),
                                              (.8, 'purple'),
                                              (1, 'maroon')],
                                              N=300)
sm2= plt.cm.ScalarMappable(cmap=cmap2)
cbar = plt.gca().figure.colorbar(sm2, ticks=[0,.2,.4,.6,.8,1])
cbar.ax.set_yticklabels(['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Air Quality Index Levels')
plt.gca().get_legend().remove()
# This lets me set the name of the window!
plt.get_current_fig_manager().set_window_title('AQI with Seaborn take 2')
plt.savefig('AQI_Levels.png', dpi=300)
plt.show()





############################################################################################
print(df.sort_values('AQI Value'))
print(df.corr(numeric_only=True))
# Looking at the correlation, AQI and PM2.5 are very closely correlated. 
# We wouldn't learn that much by considering them separately. Let's consider what plotting the Ozone value looks like.
print("The max Ozone AQI in the dataset is {}.  The minimum Ozone AQI is {}".format(
    df['Ozone AQI Value'].max(), df['Ozone AQI Value'].min()))
# Using the above information we build the plot.
norm = plt.Normalize(0, 225)
colormap = LinearSegmentedColormap.from_list('custom',
                                             [(0,'green'),
                                              (norm(25), 'green'),
                                              (norm(75), 'yellow'),
                                              (norm(125), 'orange'),
                                              (norm(175), 'red'),
                                              (norm(225), 'purple')],
                                              N=(225))
sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
plt.figure(figsize=(16,6))
countries.plot(color='lightgrey',ax=plt.gca())
sns.scatterplot(data=df, x='lng', y='lat', hue='Ozone AQI Value', palette=colormap)
cbar = plt.gca().figure.colorbar(sm, ax=plt.gca(),ticks=[25,75,125,175,225])
cbar.ax.set_yticklabels(['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().get_legend().remove()

plt.get_current_fig_manager().set_window_title('Ozone AQI with Seaborn')
plt.show()