%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, inspect
from sqlalchemy import func
from sqlalchemy import distinct
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create inspect to get the table names & columns from engine 
inspector = inspect(engine)

# Get the columns for Measure Class

column_measure = inspector.get_columns('measurement')
for columns in column_measure:
    print(columns['name'],columns['type'])

#Get the columns for Station Class

column_station = inspector.get_columns('station')
for columns in column_station:
    print(columns['name'],columns['type'])



# Calculate the last data point for date
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
last_date[0]

# Calculate the date 1 year ago from the last data point in the database

year_ago= dt.date(2017,8,23) - dt.timedelta(days=365)
print("Year Ago from last date:" ,year_ago)
print("Last Date :", last_date[0])



# Perform a query to retrieve the date and precipitation scores

dates_prcp = session.query(Measurement.date,Measurement.prcp).all()


pdf = pd.DataFrame(dates_prcp,columns = ["Dates","Precipitation"])

# Save the query results as a Pandas DataFrame and set the index to the date column

pdf.set_index("Dates", inplace=True)


# Sort the dataframe by date

pdf.sort_index(ascending=False, inplace=True)
pdf = pdf.dropna(how='any')
pdf.reset_index(drop = True,inplace=True)
pdf.head()


# Design a query to retrieve the last 12 months of precipitation data and plot the results

yearly = pdf.iloc[0:365, 0:1]
yearly = yearly.dropna(how ="any")
x = range(len(yearly))

#Use Pandas Plotting with Matplotlib to plot the data(Run this cell twice to enlarge the fig size as its rcparams)


plt.bar(x, yearly["Precipitation"],4, color ="skyblue")
plt.rcParams["figure.figsize"] = [16,13]
plt.legend(yearly,fontsize=25)
plt.xlabel('Date', fontsize=16)
plt.savefig('Trip_Avg with_error_bars.png')
plt.show()

# Use Pandas to calcualte the summary statistics for the precipitation data
pdf.describe()


# Design a query to show how many stations are available in this dataset?
session.query(func.count(Station.id)).all()




# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.

active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
                  group_by(Measurement.station).\
                  order_by(func.count(Measurement.station).desc()).all()

active_stations



# Get the most active station from list of most active station(s) 

most_active_station = active_stations[0][0]

most_active_station



# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
filter(Measurement.station == most_active_station).all()



def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        12 months of temperature observations
    """
    
    return session.query(Measurement.tobs).\
        filter (Measurement.station == most_active_station).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


#Call the function in a variable

trip_temps = (calc_temps('2016-08-23', '2017-08-23'))

trip_temps


# Create a dataframe/series object 
trip_temps_df = pd.DataFrame(trip_temps)
trip_temps_df.head()


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
trip_temps_df.hist(bins=12,xlabelsize=20,ylabelsize=20)
plt.xlabel("Temprature observations",fontsize=30)
plt.ylabel("Frequency",fontsize=30)
plt.title("Temp observations for most active station",fontsize = 30)
plt.legend(trip_temps_df, fontsize =30)
plt.savefig('Trip_Avg with_error_bars.png')
plt.show()



# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#Call the function in a variable

trip_temps = (calc_temps('2016-08-23', '2017-08-23'))

# Slice the list and assisgn the variables for plotting

t_min = trip_temps[0][0]
t_avg = trip_temps[0][1]
t_max = trip_temps[0][2]
trip_temps


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

peak_to_peak = t_max - t_min


plt.bar(1, t_avg, yerr = peak_to_peak,align='center',color = "coral",alpha=0.5, ecolor='black')
plt.ylabel('Average Temperature (F)',fontsize=20)
plt.title('Trip Avg Temperature',fontsize=20)

# Save the figure and show

plt.savefig('Trip_Avg with_error_bars.png')
plt.show()





# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

sel = [Measurement.station,Station.name,func.avg(Measurement.prcp),Station.latitude,Station.longitude,Station.elevation]

rainfall_per_weather = session.query(*sel).\
filter(Measurement.station == Station.station).\
filter (Measurement.date >= '2015-08-23').filter(Measurement.date <= '2016-08-23').\
group_by(Station.name).\
order_by(func.avg(Measurement.prcp).desc()).all()

rainfall_per_weather

