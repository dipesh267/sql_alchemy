

```python
import os
import pandas as pd

# Imports the method used for connecting to DBs
from sqlalchemy import create_engine, inspect

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
from sqlalchemy import func
```


```python
import matplotlib
from matplotlib import style
import matplotlib.pyplot as plt
style.use('fivethirtyeight')
```


```python
import datetime as dt
import numpy as np
```


```python
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()

```


```python
Base.prepare(engine, reflect=True)
```


```python
Base.classes.keys()
```




    ['measurements', 'stations']




```python
# Using the inspector to print the column names within the table and its types
inspector = inspect(engine)

print("table names")
print(inspector.get_table_names())
columns = inspector.get_columns('measurements')

print("Table measurements")
for column in columns:
    print(column["name"], column["type"])

print("____________________")
print("Table stations")
columns = inspector.get_columns('stations')
for column in columns:
    print(column["name"], column["type"])
```

    table names
    ['measurements', 'stations']
    Table measurements
    index INTEGER
    station VARCHAR(255)
    date VARCHAR(255)
    precipitation FLOAT
    tobs INTEGER
    ____________________
    Table stations
    index INTEGER
    station VARCHAR(255)
    name VARCHAR(255)
    latitude FLOAT
    longitude FLOAT
    elevation FLOAT



```python
# Assign the measurements class to a variable called `Demographics`
Measurements = Base.classes.measurements
Stations = Base.classes.stations
```


```python
# Create a session
session = Session(engine)
```


```python
rows = (session
        .query(Stations.station)
        .limit(5)
        .all())
for row in rows:
    print(row)
```

    ('USC00519397',)
    ('USC00513117',)
    ('USC00514830',)
    ('USC00517948',)
    ('USC00518838',)



```python
results = (session.query(Measurements.date, Measurements.precipitation)
            .filter(Measurements.date > "2010-01-1")
            .filter(Measurements.date < "2010-12-31")
            .limit(5)
            .all()
            )

results
```




    [('2010-01-10', 0.0),
     ('2010-01-11', 0.01),
     ('2010-01-12', 0.0),
     ('2010-01-14', 0.0),
     ('2010-01-15', 0.0)]



## Precipitation Analysis


```python
today = dt.date.today()
twelve_months_ago = dt.date.today() - dt.timedelta(days=365)
print(today)
print(twelve_months_ago)

```

    2018-07-28
    2017-07-28



```python
results = (session.query(Measurements.date, Measurements.precipitation)
            .filter(Measurements.date > twelve_months_ago)
            .filter(Measurements.date < today)
            .order_by(Measurements.date)
            .all()
           )
```


```python
df = pd.DataFrame(results,columns=['Dates','Precipitations'])
#df.set_index('Dates',inplace=True)
#df.index = pd.to_datetime(df.index)
df.Dates = pd.to_datetime(df.Dates)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Dates</th>
      <th>Precipitations</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-29</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-29</td>
      <td>0.06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-29</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-29</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-29</td>
      <td>0.23</td>
    </tr>
  </tbody>
</table>
</div>




```python
#plt.style.use('seaborn')
plt.figure(figsize=(12,7))
plt.plot(df["Dates"], df["Precipitations"], label='Precipitation')

plt.xlabel('Dates')
plt.ylabel('Precipitation')
plt.title("Precipitation in a 12 month period")
plt.legend()
plt.show()
```


![png](output_15_0.png)


## Summary Staticstics


```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitations</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>96.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.058750</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.117198</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.060000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>0.560000</td>
    </tr>
  </tbody>
</table>
</div>



## Station Analysis

### Total Stations 


```python
station_count = (session
                .query(Measurements.station)
                .group_by(Measurements.station)
                .count()
                )
print(station_count)
```

    9


### Most Active Station


```python
active_stations = (session
                 .query(Measurements.station, func.count(Measurements.station))
                 .group_by(Measurements.station)
                 .order_by(func.count(Measurements.station).desc())
                 .all())

print("Highest Number of observations: " + str(active_stations[0]))
print("\b")

print("Active Stations in Descending Order:")
for station in active_stations:
    print(station)
```

    Highest Number of observations: ('USC00519281', 2772)
    
    Active Stations in Descending Order:
    ('USC00519281', 2772)
    ('USC00513117', 2696)
    ('USC00519397', 2685)
    ('USC00519523', 2572)
    ('USC00516128', 2483)
    ('USC00514830', 1937)
    ('USC00511918', 1932)
    ('USC00517948', 683)
    ('USC00518838', 342)


### 12 Months of Temperature Observation Data


```python
query_tobs = (session.query(Measurements.date, Measurements.station, Measurements.tobs)
            .filter(Measurements.date > twelve_months_ago)
            .filter(Measurements.date < today)
            .order_by(Measurements.tobs.desc())
            .all()
            )

print(query_tobs[0])
```

    ('2017-07-30', 'USC00519523', 84)



```python
tobs_df = pd.DataFrame(query_tobs,columns=['Date','Stations','Tobs'])
tobs_df.Date = pd.to_datetime(tobs_df.Date)
tobs_df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Stations</th>
      <th>Tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-30</td>
      <td>USC00519523</td>
      <td>84</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-08-13</td>
      <td>USC00519523</td>
      <td>84</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-29</td>
      <td>USC00519523</td>
      <td>83</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-08-02</td>
      <td>USC00519523</td>
      <td>83</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-08-06</td>
      <td>USC00519523</td>
      <td>83</td>
    </tr>
  </tbody>
</table>
</div>




```python
num_bins = 12
plt.style.use('seaborn')
plt.figure(figsize=(12,7))
plt.hist(tobs_df["Tobs"], num_bins, color = 'blue', edgecolor = 'black')

plt.xlabel('Tobs')
plt.ylabel('Frequency')
plt.title("12 Month Temperature Observation")
plt.legend()
plt.show()
```

    No handles with labels found to put in legend.



![png](output_26_1.png)


## Temperature Analysis


```python
def checkDate(date):
    try:
        date = dt.datetime.strptime(date,"%Y-%m-%d")
        return date
    except Exception as e:
        print(e)
        print("The Entry is not a valid date!!!!")
        print("Try again !")
        getDates()

```


```python
def getDates():
    start_date = input("Enter the Start Date: YYYY-MM-DD ")
    start_date = checkDate(start_date)
    end_date = input("Enter the End Date: YYYY-MM-DD ")
    end_date = checkDate(end_date)
    
    return{"start_date":start_date,"end_date":end_date}
```


```python
def calc_temps(begin, end):
    query_tobs = (session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs))
            .filter(Measurements.date > begin)
            .filter(Measurements.date < end)
            .all()
            )
    
    print("Mininim for the date range is: " + str(query_tobs[0][0]))
    print("Maximum for the date range is: " + str(query_tobs[0][1]))
    print("Average for the date range is: " + str(query_tobs[0][2]))
    
    plot_bar(query_tobs[0][2], query_tobs[0][1], query_tobs[0][0])
    
```


```python
def getTempDesc():
    dates = getDates()
    begin_date = dates["start_date"]
    begin_date = f"{begin_date:%Y-%m-%d}"
    
    end_date = dates["end_date"]
    end_date = f"{end_date:%Y-%m-%d}"
    
    print("\b")
    print("The Entered Year Range Data:\b")
    print("\b")
    print("Start date is :" + begin_date)
    print("End date is :" + end_date)
    print("\b")
    print("\b")
    calc_temps(begin_date, end_date)
    print("\b")
    
    #get year range for 1 year before provided date
    print("The Prior Year Data:\b")
    prior_start_date = dates["start_date"] - dt.timedelta(days=365)
    prior_start_date = f"{prior_start_date:%Y-%m-%d}"
    
    prior_end_date = dates["start_date"]
    prior_end_date = f"{prior_end_date:%Y-%m-%d}"
    
    print("\b")
    print("Start date for Prior year is :" + prior_start_date)
    print("End date for Prior year is:" + prior_end_date)
    print("\b")
    
    calc_temps(prior_start_date, prior_end_date)
```


```python
def plot_bar(avg, maximum, minimum):
    x = (1)
    y = avg
    err = maximum - minimum

    fig, ax = plt.subplots()

    index = np.arange(1)
    bar_width = 0.2

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(x, y, bar_width,
                    alpha=opacity, color='b',
                    yerr=err, error_kw=error_config,
                    label='Average')

    ax.set_xlabel('Range')
    ax.set_ylabel('Average Temperature')
    ax.set_title('Average Temperature for Year')
    ax.set_xticks(index + bar_width / 2)
    ax.legend()
    fig.tight_layout()
    plt.show()
```

#### Temperature Report For Entered Date and Year Prior to that


```python
getTempDesc()

```

    Enter the Start Date: YYYY-MM-DD 2012-12-23
    Enter the End Date: YYYY-MM-DD 2013-12-23
    
    The Entered Year Range Data
    
    Start date is :2012-12-23
    End date is :2013-12-23
    
    
    Mininim for the date range is: 53
    Maximum for the date range is: 86
    Average for the date range is: 72.51462225832657



![png](output_34_1.png)


    
    The Prior Year Data:
    
    Start date for Prior year is :2011-12-24
    End date for Prior year is:2012-12-23
    
    Mininim for the date range is: 56
    Maximum for the date range is: 86
    Average for the date range is: 72.25385865150284



![png](output_34_3.png)

