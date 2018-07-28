# 1. import Flask
from flask import Flask, jsonify

#import sqlalchemy stuff
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

#import date stuff
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
# http://localhost:5000/api/v1.0
@app.route("/api/v1.0")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# http://localhost:5000/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    today = dt.date.today()
    twelve_months_ago = dt.date.today() - dt.timedelta(days=365)

    results = (session.query(Measurements.date, Measurements.precipitation)
            .filter(Measurements.date > twelve_months_ago)
            .filter(Measurements.date < today)
            .all()
            )
    
    all_prec = []
    for result in results:
        prec_dict = {}
        prec_dict["date"] = result.date
        prec_dict["precipitation"] = result.precipitation
        all_prec.append(prec_dict)
        
    return jsonify(all_prec)

# http://localhost:5000/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    results = (session
                .query(Measurements.station)
                .group_by(Measurements.station)
                )

    # Convert list of tuples into normal list
    all_stations = [row[0] for row in results]

    return jsonify(all_stations)

# http://localhost:5000/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    today = dt.date.today()
    twelve_months_ago = dt.date.today() - dt.timedelta(days=365)

    results = (session.query(Measurements.tobs)
            .filter(Measurements.date > twelve_months_ago)
            .filter(Measurements.date < today)
            .all()
            )
    
    #flattens the list so that we're not passing a list of 1 item lists...so it just returns a list of items.
    all_tobs = [row[0] for row in results]

    return jsonify(all_tobs)

# http://localhost:5000/api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def using_start(start):
    #convert start string to datetime object
    try:
        start_date = dt.datetime.strptime(start,"%Y-%m-%d")
        #chage date object back to date string in proper format
        start_date = f"{start_date:%Y-%m-%d}"
    except Exception as e:
        return jsonify({"error": f"Date with {start} threw error {e}."}), 404
    
    query_tobs = (session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs))
            .filter(Measurements.date >= start_date)
            .all()
            )
    
    prec_dict = {}
    prec_dict["TSTART"] = start_date
    prec_dict["TAVG"] = query_tobs[0][2]
    prec_dict["TMAX"] = query_tobs[0][1]
    prec_dict["TMIN"] = query_tobs[0][0]

    return jsonify(prec_dict)

# http://localhost:5000/api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def using_start_end(start,end):
    #convert start string to datetime object
    try:
        start_date = dt.datetime.strptime(start,"%Y-%m-%d")
        end_date = dt.datetime.strptime(end,"%Y-%m-%d")
        #chage date object back to date string in proper format
        start_date = f"{start_date:%Y-%m-%d}"
        end_date = f"{end_date:%Y-%m-%d}"
    except Exception as e:
        return jsonify({"error": f"Date with {start} or {end} threw error {e}."}), 404
    
    query_tobs = (session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs))
            .filter(Measurements.date >= start_date)
            .filter(Measurements.date <= end_date)
            .all()
            )
    
    prec_dict = {}
    prec_dict["TSTART"] = start_date
    prec_dict["TEND"] = end_date
    prec_dict["TAVG"] = query_tobs[0][2]
    prec_dict["TMAX"] = query_tobs[0][1]
    prec_dict["TMIN"] = query_tobs[0][0]

    return jsonify(prec_dict)

if __name__ == "__main__":
    app.run(debug=True)