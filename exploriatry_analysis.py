import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import datetime as dt
import matplotlib.dates as mdates

# importing csv files

df_gen1 = pd.read_csv("Plant_1_Generation_Data.csv")
df_gen1.head()
df_gen1.isnull()


df_sen1 = pd.read_csv("Plant_1_Weather_Sensor_Data.csv")
df_sen1.head()
df_sen1.isnull()

# droping columns which are not in use
#sinnce this data is of Plant 1 only hence there is no use of PLant ID
df_gen1.drop("PLANT_ID",1,inplace = True)
df_sen1.drop("PLANT_ID",1,inplace = True)


#converting date time into sutiable formate
df_gen1["DATE_TIME"]  = pd.to_datetime(df_gen1["DATE_TIME"],format = '%d-%m-%Y %H:%M')
df_sen1["DATE_TIME"]  = pd.to_datetime(df_sen1["DATE_TIME"],format = '%Y-%m-%d %H:%M:%S')


#getting stats of data
df_gen1.describe()
df_sen1.describe()


#total number of inverters
inv_id_list = df_gen1["SOURCE_KEY"].unique()
print(len(inv_id_list))
print(inv_id_list)

#maximum value of AC current and DC current generated 
df_gen1[["AC_POWER","DC_POWER"]].idxmax(axis=0)



#plotting heat map to understand relation between numerical values
plt.figure(figsize=(10,5))
c = df_sen1.corr()
sb.heatmap(c,cmap="coolwarm",annot = True)
c
plt.savefig("relation.png",dpi = 300)


#Finding least efficent working invertor
dc_gen = df_gen1.copy()
dc_gen["TIME"] = dc_gen["DATE_TIME"].dt.time
dc_gen = dc_gen.groupby(["TIME","SOURCE_KEY"])["DC_POWER"].mean().unstack()


cmap = sb.color_palette("Spectral",n_colors = 12)
fig,ax=plt.subplots(ncols=2,nrows=1,dpi=100,figsize=(16,9))
dc_gen.iloc[:,0:11].plot(ax=ax[0],color=cmap)
dc_gen.iloc[:,11:22].plot(ax=ax[1],color = cmap)
ax[0].set_title("First 11 source")
ax[0].set_ylabel("Dc power(KW)")
ax[1].set_title("Last 11 Source")
plt.show()
plt.savefig("efficiency of inverter.png",dpi = 75)


# daily yield on genarting side
df_gen1["TIME"] = df_gen1["DATE_TIME"].dt.time
fig,ax = plt.subplots(ncols = 2,nrows = 1,figsize=(16,9))
df_gen1.plot(x="DATE_TIME",y="DAILY_YIELD",color = "y",ax=ax[0])
df_gen1.plot(x="TIME",y="DC_POWER",style = "^",ax=ax[1])
df_gen1.plot(x="TIME",y="AC_POWER",style= "^" ,ax=ax[1])





temp_gen1 = df_gen1.copy()
temp_gen1["TIME"] = temp_gen1["DATE_TIME"].dt.time
temp_gen1["DAY"] = temp_gen1["DATE_TIME"].dt.time


temp_sen1 = df_sen1.copy()
temp_sen1["TIME"] = temp_sen1["DATE_TIME"].dt.time
temp_sen1["DAY"] = temp_sen1["DATE_TIME"].dt.time

cols =temp_gen1.groupby(["TIME","DAY"])["DC_POWER"].mean().unstack()


ax = cols.plot(sharex = True,subplots = True,layout=(17,2),figsize = (20,30))

i = 0
for a in range(len(ax)):
    for b in range(len(ax[a])):
        ax[a,b].set_title(cols.columns[i],size=15)
        ax[a,b].legend(["DC_POWER","DAILY_YIELD"])
        i = i+1
plt.tight_layout()
plt.show()



