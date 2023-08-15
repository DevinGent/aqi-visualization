import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import random
import numpy as np
from matplotlib.colors import LinearSegmentedColormap 

# We test how to create a custom color bar and color map.

###################################################################
# First we create a dataframe consisting of (x,y) pairs, where each point has a value attached (which will eventually
# determine the color of the point.)
df = pd.DataFrame({'x': [i for i in range(10)]*2,
                   'y': [random.randint(0,9) for i in range(20)],
                   'value': ([0]*4)+([100]*4)+([200]*4)+([300]*4)+([400]*4)})

df.info()
print(df)
# The following will create an object that scales all numbers from value.min() to value.max() to numbers in the interval [0,1].
# i.e. it rescales/transforms the interval [df['value'].min(), df['value'].max()] into the interval [0,1]
norm = plt.Normalize(df['value'].min(), df['value'].max())
print(norm)
# Note that the normalize object doesn't print to anything interesting.  But if we feed it a particular value lying in the
# original interval it gives us the corresponding number in the interval [0,1] like so:
print(norm(1.5))

# We now create a colormap: a list of colors corresponding to values in [0,1].  
# By a LinearSegmentedColormap we mean that specific colors are chosen for specific values in [0,1] and then the remaining
# values are assigned colors by linearly bleeding from one color to the next.  For instance, if 'red' is assigned to .25 and
# 'blue' to .75, we can expect .5 to be about purple (between red and blue).
#  'custom' is a name for the colormap (we could have chosen anything)
# The list that follows contains pairs (value,color) where value is a number in [0,1] (note that in each instance we use
# norm to ensure the number is in the correct interval) and color is its corresponding color.  
# N denotes how many different colors are created (so if N=4 EVERY value in [0,1] would have to be one of the four colors listed)
colormap = LinearSegmentedColormap.from_list('custom', [(norm(0), 'green'), (norm(150), 'yellow'), (norm(250),'red'), (norm(400), 'blue')], N=400)
# NOTE: The list must start with (0,color) and end with (1,color).  In our case 0 IS df['value'].min() (so norm(0)=0)
# and 400 IS df['value'].max() (so norm(400)=1)

# We now test plotting a scatterplot using these colors.
plt.figure(figsize=(8,4))
# In the following x= and y= decide what values represent the x coordinates.  c= Decides what values represent the color for each 
# point in the plot.  cmap= decides what color map is being used
plt.scatter(x=df.x, y=df.y, c=df.value, cmap=colormap)
# The following creates a colorbar based on the colormap we chose.
plt.colorbar()
plt.show()

# Now we do the same with seaborn.  Note that we have to use hue rather than c in this case, and palette instead of cmap
plt.figure(figsize=(8,4))
sns.scatterplot(data=df, x='x', y='y', hue='value', palette=colormap)
plt.show()

# We are curious how the colors scale to different values.  We will create multiple lines (intervals)

line=np.linspace(0,400)
line2=np.linspace(0,200)
line3=np.linspace(300,400)
line4=np.linspace(300,400)
# Testing how a single line prints
plt.figure(figsize=(8,4))
sns.scatterplot(x=line, y=line)
plt.show()

plt.subplot(2,2,1)
sns.scatterplot(x=line, y=line, hue=line, palette=colormap)
plt.subplot(2,2,2)
sns.scatterplot(x=line2, y=line2, hue=line2, palette=colormap)
plt.subplot(2,2,3)
sns.scatterplot(x=line3, y=line3, hue=line3, palette=colormap)
plt.subplot(2,2,4)
sns.scatterplot(x=[0,125,150], y=[0,125,150], hue=[0,125,150], palette=colormap)

plt.show()

colormap2 = LinearSegmentedColormap.from_list('custom2', [(norm(0), 'green'),(1,'red')], N=3)

plt.subplot(2,2,1)
sns.scatterplot(x=[0,20,100,250],y=[0,20,100,250],hue=[0,20,100,250], palette=colormap2)

plt.subplot(2,2,2)
sns.scatterplot(x=[0,250],y=[0,250],hue=[0,250], palette=colormap2)
plt.subplot(2,2,3)
sns.scatterplot(x=[0,20,100,105,250],y=[0,20,100,105,250],hue=[0,20,100,105,250], palette=colormap2)
plt.subplot(2,2,4)
sns.scatterplot(x=[0,125,150], y=[0,125,150], hue=[0,125,150], palette=colormap2)

plt.show()