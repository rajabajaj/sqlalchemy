import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/startdate"
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all passengers
    results = session.query(func.distinct(Measurement.station)).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """  * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
  * Return the JSON representation of your dictionary."""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.tobs).all()

    # Convert list of tuples into normal list
    all_percp = list(np.ravel(results))
    
        # Create a dictionary from the row data and append to a list of all_passengers
    all_percps = []
    percps_dict = {}
    for row in results:
        percps_dict = {}
        percps_dict[row.date] = row.tobs
        all_percps.append(percps_dict)

    return jsonify(all_percps)




@app.route('/api/v1.0/startdate')

def temps():

 
    start_date = "2016-08-23"
    results  = results = session.query(func.min(Measurement.tobs),
                                       func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    


    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
