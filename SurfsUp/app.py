# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
import os


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
    """List api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/bydate/&lt;start&gt;<br>"
        f"/api/v1.0/bydate/&lt;start&gt;/&lt;end&gt;<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    #query
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    session.close()

    #dicitonary
    all_prcp = []
    for date, prcp in data:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #query the stations
    stations_data = session.query(Station.station, Station.name).all()
    session.close()
    all_stations = []
    for station, name in stations_data:
        stations_dict = {}
        stations_dict[station] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Most active station in the last year
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    mostactivestation = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc())[0][0]
    print(mostactivestation)
    mostactivedata = session.query(Measurement.date,Measurement.tobs).\
            filter(Measurement.station==mostactivestation).filter(Measurement.date >= query_date).all()
    print(mostactivedata)
    all_tobs = []
    for date, tobs in mostactivedata:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    session.close()
    return jsonify(all_tobs)

@app.route("/api/v1.0/bydate/<string:start>")
def bystartdate(start):
    # For a specified start, Calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs).label("min_temp"),
        func.avg(Measurement.tobs).label("avg_temp"),func.max(Measurement.tobs).label("max_temp")
    ).filter(Measurement.date >= start).all()
    
    session.close()
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    if results:
        min_temp, avg_temp, max_temp = results[0]
        return jsonify({
            "start_date": start,
            "min_temperature": min_temp,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        })
    
@app.route("/api/v1.0/bydate/<string:start>/<string:end>")
def bydate_start_end(start, end):
    # Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    session = Session(engine)
    
    results = session.query(
        func.min(Measurement.tobs).label("min_temp"),
        func.avg(Measurement.tobs).label("avg_temp"),
        func.max(Measurement.tobs).label("max_temp")
    ).filter(
        Measurement.date >= start,
        Measurement.date <= end
    ).all()
    
    session.close()
    
    if results:
        min_temp, avg_temp, max_temp = results[0]
        return jsonify({
            "start_date": start,
            "end_date": end,
            "min_temperature": min_temp,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        })
    

if __name__ == "__main__":
    app.run(debug=True)